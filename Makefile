default: setup_db install run

setup_db: 
	sudo -u postgres psql -f setup_db.sql
	alembic upgrade head 

install:
	pip install -r requirements.txt

run:
	python app.py

cli:
	pgcli postgresql+psycopg2://aiopg_user:password@127.0.0.1:5432/aiopg_db
