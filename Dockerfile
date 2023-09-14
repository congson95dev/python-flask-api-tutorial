FROM python:3.8.13-slim-buster

# created if the folder is not exists, if it does exists, then ignore this command
RUN mkdir -p /python-flask-api-tutorial

# copy current directory and main.py to /app/
COPY . /python-flask-api-tutorial/
WORKDIR /python-flask-api-tutorial

RUN pip install -r requirements.txt

EXPOSE 5000
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]