import eventlet
eventlet.monkey_patch()
from flask import Flask, render_template, url_for, request, jsonify, redirect, session, abort, Response
from flask_cors import CORS
import uuid
from datetime import date
import json
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
import logging
import random
from pymongo import MongoClient
from bson import ObjectId  
import time
import emoji
from dotenv import load_dotenv
import os
from authlib.integrations.flask_client import OAuth



load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET', 'fallback-secret')
app.config['TEMPLATES_AUTO_RELOAD'] = True


app.config['MQTT_BROKER_URL'] = os.getenv('MQTT_BROKER_URL', 'broker.hivemq.com')
app.config['MQTT_BROKER_PORT'] = int(os.getenv('MQTT_BROKER_PORT', 1883))
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False

CORS(app)
client = MongoClient("mongodb://db:27017/") 
db = client.mydatabase  
users_collection = db.users  
discussions_collection = db.discussions 



KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM")
KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID")
KEYCLOAK_CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET")

KEYCLOAK_PUBLIC_URL = os.getenv("KEYCLOAK_PUBLIC_URL",)    
KEYCLOAK_INTERNAL_URL = os.getenv("KEYCLOAK_INTERNAL_URL") 


oauth = OAuth(app)
keycloak = oauth.register(
    name='keycloak',
    client_id=KEYCLOAK_CLIENT_ID,
    client_secret=KEYCLOAK_CLIENT_SECRET,
    authorize_url=f"{KEYCLOAK_PUBLIC_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/auth",
    access_token_url=f"{KEYCLOAK_INTERNAL_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token",
    userinfo_endpoint=f"{KEYCLOAK_INTERNAL_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/userinfo",
    jwks_uri=f"{KEYCLOAK_INTERNAL_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/certs",
    client_kwargs={'scope': 'openid profile email'},
)



log_filename = "test.log"
logging.basicConfig(
    level=logging.INFO,  
    format="%(asctime)s - %(levelname)s - %(message)s",  # Format logów
    handlers=[
        logging.FileHandler(log_filename),  # Zapis do pliku
        logging.StreamHandler()  # Wyświetlanie w konsoli
    ]
)
logger = logging.getLogger(__name__)

topic = '/flask/mqtt'

def makeKey(alphabet):
   alphabet = list(alphabet)
   random.shuffle(alphabet)
   return ''.join(alphabet)

def encrypt(plaintext, key, alphabet):
    keyMap = dict(zip(alphabet, key))
    return ''.join(keyMap.get(c.lower(), c) for c in plaintext)

def decrypt(cipher, key, alphabet):
    keyMap = dict(zip(key, alphabet))
    return ''.join(keyMap.get(c.lower(), c) for c in cipher)

alphabet = 'abcdefghijklmnopqrstuvwxyz.,!@#$%^&*()123456789 '
key = makeKey(alphabet)

mqtt_client = Mqtt(app)
socketio = SocketIO(app, async_mode='eventlet')

app.secret_key = 'secret'

@socketio.on('publish')
def handle_publish(json_str):
    logger.info(f"Received publish event: {json_str}")
    data = json.loads(json_str)
    mqtt_client.publish(data['topic'], data['message'])

@socketio.on('subscribe')
def handle_subscribe(json_str):
    logger.info(f"Received subscribe event: {json_str}")
    data = json.loads(json_str)
    mqtt_client.subscribe(data['topic'])

@socketio.on('unsubscribe_all')
def handle_unsubscribe_all():
    logger.info("Received unsubscribe_all event")
    mqtt_client.unsubscribe_all()

@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
    logger.info(f"MQTT message received on topic {message.topic}: {message.payload.decode()}")
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    socketio.emit('mqtt_message', data=data)


@app.route("/", methods=['GET'])
def home():
    logger.info("Rendering home page")
    discussions = list(discussions_collection.find())
    count_of_discussions = discussions_collection.count_documents({})
    return render_template('home.html', countOfDiscussions=count_of_discussions, dataBaseDiscussions=discussions)




@app.route("/search", methods=['GET'])
def search():
    query = request.args.get('q')
    logger.info(f"Search query received: {query}")
    discussionsNames = []
    discussions = list(discussions_collection.find())
    for i in discussions:
        if str(query).upper() in str(i).upper():
            discussionsNames.append(i)

    logger.info(f"Found {len(discussionsNames)} discussions matching the query")
    return render_template('search.html', names=discussionsNames, dataBaseDiscussions=discussions, countOfDiscussions=len(discussionsNames))


@app.route("/controlpoint", methods=['GET'])
def control_point():
    if session and session['role'] == 'admin':
        logger.info("Rendering control_point page")
        return render_template('control_point.html')
    else:
        return abort(404)
    



from uuid import uuid4

@app.route('/login')
def login():
    nonce = str(uuid4())  
    session['nonce'] = nonce  
    redirect_uri = url_for('authorize', _external=True)
    return keycloak.authorize_redirect(redirect_uri, nonce=nonce) 




@app.route('/authorize')
def authorize():
    token = keycloak.authorize_access_token()  
    userinfo = keycloak.parse_id_token(token, nonce=session.get('nonce'))
    

    session['user'] = {
        'username': userinfo['preferred_username'],
        'email': userinfo['email'],
        'roles': userinfo.get('realm_access', {}).get('roles', [])
    }

    return redirect('/')



@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')






@app.route("/discussion", methods=['GET'])
def create_discussion_get():
    logger.info("Rendering discussion creation form")
    return render_template('discussion_form.html', user=session)

@app.route("/discussion/<id>", methods=['GET'])
def get_discussion(id):
    logger.info(f"Fetching discussion with ID: {id}")
    discussion = discussions_collection.find_one({"_id": ObjectId(id)})
    
    if discussion:
        logger.info(f"Discussion found: {discussion['name']}")
        return render_template('discussion.html', id=str(discussion['_id']), title=discussion['name'], 
                               dataBaseDiscussions=discussion, author=discussion['author'])
    
    logger.warning(f"Discussion with ID {id} not found")
    return abort(404)

@app.route("/discussion/<id>", methods=['PUT'])
def update_discussion(id):
    data = request.get_json()
    content = data.get('newTitle')
    logger.info(f"Updating discussion with ID: {id}, new title: {content}")
    
    discussion = discussions_collection.find_one({"_id": ObjectId(id)})
    if discussion:
        discussions_collection.update_one({"_id": ObjectId(id)}, {"$set": {"name": content}})
        logger.info(f"Discussion {id} updated successfully")
        return '', 201
    
    logger.warning(f"Failed to update discussion: ID {id} not found")
    return abort(404)

@app.route("/discussion/<id>", methods=['DELETE'])
def remove_discussion(id):
    logger.info(f"Attempting to delete discussion with ID: {id}")
    
    discussion = discussions_collection.find_one({"_id": ObjectId(id)})
    if discussion:
        discussions_collection.delete_one({"_id": ObjectId(id)})
        logger.info(f"Discussion {id} deleted successfully")
        return '', 204
    
    logger.warning(f"Failed to delete discussion: ID {id} not found")
    return abort(404)


@app.route("/discussion/comment/<id>", methods=['DELETE'])
def remove_comment(id):
    logger.info(f"Attempting to delete comment with ID: {id}")
    data = request.get_json()
    discussion = discussions_collection.find_one({"_id": ObjectId(data['discussionId'])})
    if discussion:
        discussions_collection.update_one(
            {"_id": ObjectId(data['discussionId'])},  
            {"$pull": {"comments": {"id": id}}}  
        )
        mqtt_client.publish(f"comments/{id}", 'removed')
        socketio.emit('remove_comment', {'discussion_id': str(ObjectId(data['discussionId'])), 'comment':  {'id': id}})
        logger.info(f"Comment {id} deleted successfully")
        return '', 204
    
    logger.warning(f"Failed to delete comment: ID {id} not found")
    return abort(404)

@app.route("/discussion/<id>", methods=['POST'])
def create_comment_for_discussion(id):
    title = request.form['title']
    logger.info(f"Adding comment to discussion ID: {id}, title: {title}")

    discussion = discussions_collection.find_one({"_id": ObjectId(id)})
    if discussion:
        new_comment = {
            'id': str(uuid.uuid4()),
            'title': title,
            'author': session['user']['username'],
            'date': date.today().isoformat()
        }
        
        discussions_collection.update_one({"_id": ObjectId(id)}, {"$push": {"comments": new_comment}})
        mqtt_client.publish(f"comments/{id}", json.dumps(new_comment))
        socketio.emit('new_comment', {'discussion_id': id, 'comment': new_comment})
        
        logger.info(f"Comment added successfully to discussion ID: {id}")
        return '', 200
    
    logger.warning(f"Failed to add comment: discussion ID {id} not found")
    return abort(404)

@app.route("/users", methods=['GET'])
def users():
    if session and session['user']['role'] == 'admin':
        logger.info("Rendering users list")
        users = list(users_collection.find())
        for user in users:
            user['_id'] = str(user['_id'])
        return jsonify({"users": users})
    else:
        return abort(404)



@app.route("/discussion", methods=['POST'])
def create_discussion():
    name = request.form['name']
    logger.info(f"Creating new discussion: {name}")
    
    discussion = {
        'name': name,
        'author': session['user']['username'],
        'comments': [],
        'date': date.today().isoformat()
    }
    
    result = discussions_collection.insert_one(discussion)
    logger.info(f"Discussion {name} created successfully with ID: {result.inserted_id}")
    return redirect(url_for('home'))





if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)


