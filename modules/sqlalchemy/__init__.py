from .sql_db_manager import connect_db
import os
from dotenv import load_dotenv

# Get the environment variables like the keys
load_dotenv()
DB_USER = os.getenv('DATABASE_USER')
DB_PW = os.getenv('DATABASE_PW')
DB_SERVER = os.getenv('DATABASE_SERVER')
DB_DATABASE = os.getenv('DATABASE_DB')
DB_PORT = os.getenv('DATABASE_PORT')

credentials = {"Username": DB_USER,
			   "Password": DB_PW,
			   "Server": DB_SERVER,
			   "Database": DB_DATABASE,
			   "Port": DB_PORT}

print('Connecting to db')
sql_db_manager.connect_db(credentials)
