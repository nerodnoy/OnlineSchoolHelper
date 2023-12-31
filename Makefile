install:
	poetry install

dev:
	poetry run flask --app osh:app run


PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) osh:app

lint:
	poetry run flake8