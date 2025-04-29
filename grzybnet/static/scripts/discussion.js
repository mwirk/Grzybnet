
function removeDiscussion(id) {
    $.ajax({
        url: `/discussion/${id}`,
        type: 'DELETE',
        success: () => {
            window.location.href = '/'; 
        },
        error: () => {
            alert('Błąd podczas usuwania dyskusji');
        }
    });
}

function removeComment(discussionId, commentId) {
    console.log(commentId);
    console.log(discussionId);
    
    
    $.ajax({
        url: `/discussion/comment/${commentId}`,
        type: 'DELETE',
        contentType: 'application/json', 
        data: JSON.stringify({ 'discussionId': discussionId }), 
        success: () => {
            window.location.href = `/discussion/${discussionId}`; 
        },
        error: () => {
            alert('Błąd podczas usuwania komentarza');
        }
    });
}


function changeTitle(id) {
    const title = document.querySelector('#newTitle').value
    if (title == ''){
        alert('Pole do zmiany nazwy nie może być puste')
    }
    else{
    $.ajax({
        url: `/discussion/${id}`,
        contentType: 'application/json',
        type: 'PUT',
        data: JSON.stringify({'newTitle': title}),
        success: () => {
            window.location.href = `/discussion/${id}`;  
        },
        error: () => {
            alert('Błąd podczas zmiany tytułu dyskusji');
        }
    });
}
}



document.addEventListener('DOMContentLoaded', () => {
  const socket = io();

  const discussionId = window.location.pathname.substring(window.location.pathname.lastIndexOf('/') + 1);
  

  socket.on('new_comment', (data) => {
      if (data.discussion_id === discussionId) {
          addCommentToPage(data.comment);
      }
  });
  socket.on('remove_comment', (data) => {

    removeComment(data.comment);

});

  function addCommentToPage(comment) {

      const commentsContainer = document.getElementById('comments');
      const commentDiv = document.createElement('div');
      commentDiv.id = comment.id;
      commentDiv.style = "margin-top: 0.5em; width:50%; margin:1em auto auto auto; padding-bottom: 1em; border: 1px solid black";
      commentDiv.innerHTML = `
          <p id=${comment.id}>${comment.date} Użytkownik ${comment.author} napisał:</p>
          <p>${comment.title}</p>
      `;
      commentsContainer.appendChild(commentDiv);
  }


  function removeComment(comment) {
    const commentsContainer = document.getElementById('comments');
    const commentToRemove = document.getElementById(comment.id)
    commentsContainer.removeChild(commentToRemove)
    
}

  const createCommentForm = document.getElementById('createCommentForm');
  createCommentForm.addEventListener('submit', (event) => {
      event.preventDefault();

      const commentInput = document.getElementById('commentTitle');
      const commentText = commentInput.value;

      
      fetch(createCommentForm.action, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: new URLSearchParams({ title: commentText }),
      }).then(response => {
          if (response.ok) {
              commentInput.value = ''; // Wyczyść pole po dodaniu komentarza
          } else {
              alert('Błąd podczas dodawania komentarza.');
          }
      });
  });
});


// Funkcja do przełączania widoczności menu emoji
document.getElementById('toggleEmojiButton').addEventListener('click', function() {
    const emojiMenu = document.getElementById('emojiMenu');
    if (emojiMenu.style.display === 'none') {
        emojiMenu.style.display = 'block'; // Pokaż menu
        this.textContent = 'Ukryj emoji'; // Zmień tekst przycisku
    } else {
        emojiMenu.style.display = 'none'; // Ukryj menu
        this.textContent = 'Pokaż emoji'; // Zmień tekst przycisku
    }
});

// Funkcja do dodawania emoji do tytułu komentarza
function addEmoji(emoji) {
    const commentTitleInput = document.getElementById('commentTitle');
    commentTitleInput.value += emoji; // Dodaj emoji do pola tytułu komentarza
}
