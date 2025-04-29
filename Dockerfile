FROM python:3.11
WORKDIR /app
COPY /grzybnet .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
