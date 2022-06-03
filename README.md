# This project is to practice flask api

### we use flask_restx to handle api and flask_jwt to handle authenticate

### first of all, you need to run this command to create environment for this project

`cd project_name`

`python3 -m venv venv`

`source venv/bin/activate`

`pip install -r requirements.txt`

### then, run this command to migrate database

`flask db init`

`flask db migrate -m "Initial migration."`

`flask db upgrade`

### now, you are good to go
### other information i've comment in the code
### try to read it to know how to use this api project