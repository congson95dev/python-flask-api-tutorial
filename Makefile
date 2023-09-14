install:
	pip install --upgrade pip &&\
	pip install -r requirements.txt
format:
	black .
lint:
	pylint --disable=R,C src/*.py
flake8:
	flake8 --max-line-length=88 \
	--max-complexity=18 \
	--select=B,C,E,F,W,T4,B9 \
	--ignore=E203,E266,W503,F403,F401,E402 \
	--exclude=venv
test:
	# unit test using pytest and pytest-coverage
build:
	docker build -t flask-code-base .
deploy:
	docker run -d -p 0.0.0.0:5000:5000 flask-code-base

all: install format lint flake8 test build deploy