FROM python:3.8.13-slim-buster

# created if the folder is not exists, if it does exists, then ignore this command
RUN mkdir -p /flask-code-base

# copy current directory and main.py to /app/
COPY . /flask-code-base/
WORKDIR /flask-code-base

RUN pip install -r requirements.txt

EXPOSE 5000
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]