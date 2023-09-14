# Flask Code Base

### Requirements
- **Python 3.8**

### Tech stack:
- Database: postgres
- Handle api: flask_restx
- Authenticate: flask_jwt_extend

### Installation:

### Create environment:
```
cd project_name

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt
```
### If you don't have db yet, please follow this instruction:
```
sudo -i -u postgres psql

CREATE DATABASE flask_code_base;

CREATE USER fudo WITH PASSWORD 'admin123';

GRANT ALL PRIVILEGES ON DATABASE flask_code_base TO fudo;
```

### Setting up environment
- Create .env file in the root folder.
- Copy the content from .env.example file to .env file.
- Change config db info in .env file

### Run migrate:
```
flask db upgrade
```
### Run:
```
flask run
```
### Go to `127.0.0.1:5000`

### Pre-commit:
- Run this command and fix all the warning before committing code to the repo
```
pre-commit run --all-files
```
-  Or run
```
pre-commit install
```