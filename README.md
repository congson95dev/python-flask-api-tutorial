# This project is to practice flask api 

### We use flask_restx to handle api and flask_jwt_extend to handle authenticate 

### For db, we use postgres

### First of all, you need to run this command to create environment for this project

`cd project_name`

`python3 -m venv venv`

`source venv/bin/activate`

`pip install -r requirements.txt`

### If you don't have db yet, please follow this instruction:

`sudo -i -u postgres psql`

`CREATE DATABASE flask_api_tutorial_2;`

`CREATE USER fudo8 WITH PASSWORD 'admin123';`

`GRANT ALL PRIVILEGES ON DATABASE flask_api_tutorial_2 TO fudo8;`

### Then you need to config db info in .env file
### After that, run this command to migrate database

`flask db upgrade`

### Now, you are good to go
### Other information i've comment in the code
### Try to read it to know how to use this api project