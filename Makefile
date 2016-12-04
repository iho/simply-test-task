setup_db: 
	sudo -u postgres psql -f setup_db.sql

cli:
	pgcli postgresql+psycopg2://aiopg_user:password@127.0.0.1:5432/aiopg_db
