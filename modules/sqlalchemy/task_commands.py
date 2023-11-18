# This library is intended to manage the data access of the tasks tables in the database
from sqlalchemy import create_engine, desc, asc
from sqlalchemy.orm import Session as Session_alc
from sqlalchemy import select, update, insert, delete
from .task_models import Task, Server, User
from .sql_db_manager import db_query, db_commit
import datetime as dt

TASK_GROUP_AUTHOR = "Author"
TASK_GROUP_ROLE = "Role"

# The following commands will be needed

# Servers
# - Create server
# - Change announcement channel
# - Change announcement time

# Tasks
# - Create task
# - Fetch tasks based on current_user
# - Fetch tasks based on server
# - Fetch tasks based on author
# - Fetch tasks based on completed status
# - Fetch tasks based on interval
# - Delete task based on ID (only if same server)
# - Complete task

# ##############################################################################################################
# ##################               Task Functions                  #############################################
# ##############################################################################################################


def put_task(server_id, task_name, repeat_interval, author_id, duration):
	# Entry fields cannot be None
	if any([server_id is None, task_name is None, repeat_interval is None, author_id is None, duration is None]):
		print("Error in values to create task")
		return None

	# Check if user exists
	if not exists_user(author_id):
		put_user(author_id)

	print("Inserting task")
	statement = insert(Task).values(
		id_server=server_id,
		task_name=task_name,
		interval_days=repeat_interval,
		id_author=author_id,
		id_last_user=0,
		id_current_user=0,
		completed=False,
		duration=duration,
		deadline=0,
		valid_users=TASK_GROUP_AUTHOR
	)

	return db_commit(statement)


def get_tasks(server_id, task_id=None, author_id=None, last_user_id=None, current_user=None, completed=None):
	# Following fields cannot be None
	if any([server_id is None]):
		return None

	statement = select(Task).where(Task.id_server == server_id)

	if author_id is not None:
		statement = statement.where(Task.id_author == author_id)
	if last_user_id is not None:
		statement = statement.where(Task.id_last_user == last_user_id)
	if current_user is not None:
		statement = statement.where(Task.id_current_user == current_user)
	if completed is not None:
		statement = statement.where(Task.completed == completed)
	if task_id is not None:
		statement = statement.where(Task.id == task_id)

	return db_query(statement)


def remove_task(task_id):
	statement = delete(Task).where(Task.id == task_id)
	return db_commit(statement)

# ##############################################################################################################
# ##################             Server Functions                  #############################################
# ##############################################################################################################


def get_servers(server_id):
	statement = select(Server).where(Server.id_server == server_id)
	return db_query(statement)


def put_new_server(server_id, server_name, announcement_channel):
	if any in [server_id is None, server_name is None, announcement_channel is None]:
		return

	statement = insert(Server).values(id_server=server_id,
									  server_name=server_name,
									  announcement_channel=announcement_channel,
									  announcement_time=420)
	return db_commit(statement)


def update_server_role(server_id, role):
	if any in [server_id is None, role is None]:
		return

	statement = update(Server).where(Server.id_server == server_id).values(task_role=role)

	return db_commit(statement)


def server_id_list():
	statement = select(Server.id_server)
	return db_query(statement)


# ##############################################################################################################
# ##################               User Functions                  #############################################
# ##############################################################################################################
def exists_user(user_id):
	statement = select(User).where(User.id_user == user_id)
	return len(db_query(statement)) > 0


def put_user(user_id):
	statement = insert(User).values(id_user=user_id)
	return db_commit(statement)
