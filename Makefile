install:
	poetry install

dev:
	poetry run flask --app converter:app run


PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) converter:app

lint:
	poetry run flake8