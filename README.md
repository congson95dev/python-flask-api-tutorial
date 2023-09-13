# This project is to practice flask api 

### We use flask_restx to handle api and flask_jwt_extend to handle authenticate 

### For db, we use postgres

### Install steps:

### First of all, you need to run this command to create environment for this project
```
cd project_name

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt
```
### If you don't have db yet, please follow this instruction:
```
sudo -i -u postgres psql

CREATE DATABASE flask_api_tutorial_2;

CREATE USER fudo8 WITH PASSWORD 'admin123';

GRANT ALL PRIVILEGES ON DATABASE flask_api_tutorial_2 TO fudo8;
```
### Then you need to config db info in .env file
### After that, run this command to migrate database
```
flask db upgrade
```
### Run:
```
flask run
```
### Go to `127.0.0.1:5000`

### Now, you are good to go
### Other information i've comment in the code
### Try to read it to know how to use this api project

# Knowledge i've used in this project:

### 1. flask_restx for handle api

### 2. flask_jwt_extend for authenticate

### note: for authenticate, this project have login, logout, refresh token, revoke both refresh token and access token in one logout action, check token revoked, get current user info, check valid aud
### Please check in this file: 
```
src/apis/auth/routes.py
```
### 3. migration to add sample data
### Please check in this file:
```
migrations/versions/2c35179aa1da_create_sample_data_for_users_and_books.py
```
### 4. flask_accepts for set request schema, response schema

### 5. set a general format for every api
### Please check in this file:
```
src/apis/book/routes.py

src/schemas/Book/BookSchema.py
```

### 6. custom exception response
### Please check in this file:
```
src/common/response.py
```
### 7. general validate check exists by id
### Please check in this file:
```
src/common/validate.py
```
### 8. @hybrid_property

### 9. @validates_schema

# Knowledge i still need to learning about:
### ARRAY in db
### schema job, employee, master data on screen
### flask_accept accept/response
### cron
### authenticate
### send email
### upload/download
### import/export (read file/write file)
### command
### read DB view
### return 2 difference schema in 1 api
### unit test
### firebase notification
### azure storage
### POC
### subcribe