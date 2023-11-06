from sqlalchemy import create_engine, desc, asc
from sqlalchemy.orm import Session as Session_alc
from sqlalchemy import select, update, insert
from sqlalchemy.exc import OperationalError, IntegrityError

# Global variables
db_engine = None


# Need a function to first connect to the database (a close connection would be good too)
def connect_db(credentials):
	global db_engine
	if db_engine is not None:
		return

	db_string = f"postgresql+psycopg2://{credentials['Username']}:{credentials['Password']}@{credentials['Server']}" \
				f":{credentials['Port']}/{credentials['Database']}"
	db_engine = create_engine(db_string)

	try:
		conn = db_engine.connect()
		conn.close()
		return True
	except OperationalError:
		return False


# General query functions, requires active connection, and statement command
def db_query(stmt):
	if db_engine is None:
		return None
	ret_data = []
	with Session_alc(db_engine) as session:
		for value in session.scalars(stmt):
			ret_data.append(value)
	return ret_data


def db_commit(stmt):
	try:
		if db_engine is None:
			return None
		with Session_alc(db_engine) as session:
			result = session.execute(stmt)
			session.commit()
		return result
	# Error occurred (content probably already exists)
	except IntegrityError:
		return None
