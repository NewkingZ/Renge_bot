# This library is intended to manage the data access of the tasks tables in the database
from sqlalchemy import create_engine, desc, asc
from sqlalchemy.orm import Session as Session_alc
from sqlalchemy import select, update, insert
from .task_models import Task, TaskSetting
from .sql_db_manager import db_query, db_commit

# The following commands will be needed

# Task settings
# - Search by server ID
# - Add / modify setting based on server ID


# Tasks
# - Create task
# - Fetch tasks based on current_user
# - Fetch tasks based on server
# - Fetch tasks based on author
# - Fetch tasks based on completed status
# - Fetch tasks based on interval
# - Delete task based on ID (only if same server)
# - Complete task

def create_task(server_id, task_name, repeat_interval, author_id):
	# Entry fields cannot be None
	if any([server_id is None, task_name is None, repeat_interval is None, author_id is None]):
		return

	statement = insert(Task).values(
		id_server=server_id,
		task_name=task_name,
		interval_days=repeat_interval,
		id_author=author_id,
		id_last_user=0,
		completed=False,
		id_current_user=0
	)

	return db_commit(statement)


def get_tasks(server_id, author_id=None, last_user_id=None, current_user=None, completed=None):
	# Following fields cannot be None
	if any([server_id is None]):
		return None

	statement = select(Task).where(id_server=server_id)

	if author_id is not None:
		statement = statement.where(id_author=author_id)
	if last_user_id is not None:
		statement = statement.where(id_last_user=last_user_id)
	if current_user is not None:
		statement = statement.where(id_current_user=current_user)
	if completed is not None:
		statement = statement.where(completed=completed)

	return db_query(statement)

