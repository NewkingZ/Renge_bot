import discord
from discord.ext import commands
import modules.sqlalchemy.task_commands as sql_tasks
import modules.sqlalchemy.task_models as task_models

TASK_FIELD_DURATION = "Duration"
TASK_FIELD_NAME = "Name"
TASK_FIELD_DEADLINE = "Deadline"
TASK_FIELD_GROUP = "Group"
TASK_FIELD_INTERVAL = "Interval"


class Tasks(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.client.loop.create_task(self.ready())

	async def ready(self):
		await self.client.wait_until_ready()

		# Check to make sure all guilds are in the database:
		existing_guilds = sql_tasks.server_id_list()
		for guild in self.client.guilds:
			if guild.id not in existing_guilds:
				print(f"Missing server {guild.name} in database. Adding it...")
				sql_tasks.put_new_server(server_id=guild.id,
										 server_name=guild.name,
										 announcement_channel=guild.system_channel.id)

		print('Tasks Cog is ready')

	@commands.Cog.listener()
	async def on_guild_join(self, guild):
		print('Adding new guild to database')
		sql_tasks.put_new_server(server_id=guild.id,
								 server_name=guild.name,
								 announcement_channel=guild.system_channel.id)

	@commands.command()
	async def my_tasks(self, ctx: discord.ext.commands.Context):
		# Replace contents here with the ability to return that user's tasks FOR THIS SERVER
		tasks = sql_tasks.get_tasks(server_id=ctx.author.guild.id, current_user=ctx.author.id)
		if len(tasks) == 0:
			await ctx.send("Looks like you don't have any tasks assigned to you."
						   " You're going to have to assign them to yourself")
		else:
			message = f"You have {len(tasks)} tasks available;"
			for task in tasks:
				message = f"{message}\n{task.task_name}: which is due by X days from now"

	@commands.command()
	async def task_role(self, ctx: discord.ext.commands.Context, *, role):
		role = role.strip('><&@')
		for server_role in ctx.guild.roles:
			if str(server_role.id) == role:
				sql_tasks.update_server_role(ctx.guild.id, role)
				await ctx.send("Updated server task role")
				return

		await ctx.send("Invalid task role")

	@commands.command()
	async def task_create(self, ctx: discord.ext.commands.Context, *, task_name):
		inserted = sql_tasks.put_task(ctx.guild.id, task_name, 7, ctx.author.id, 0)
		message = f"Created a task for the server with the following settings:\n"\
			  f"	Task name: {task_name}\n"\
			  f"	Task ID: {inserted.inserted_primary_key[0]}\n"\
			  f"	Author: {ctx.author.name}\n"\
			  f"	Repeat cycle: 7 days\n"\
			  f"	Task length: 0 Hours\n"\
			  f"	Assigned to: Author\n\n"\
			  f"Settings can be changed with `task_edit`"

		await ctx.send(f"{message}")

	@commands.command()
	async def task_edit(self, ctx: discord.ext.commands.Context, task_id, field, *, value):
		# Fields that should be able to be changed: Task name, duration, repeat interval, assigned group, and deadline

		# User must enter field type and it's new value:
		if any([task_id is None, field is None, value is None]):
			await ctx.send(f"Missing information. Please specify task Id, field type, and value\n"
						   f"Possible fields include {TASK_FIELD_NAME}, {TASK_FIELD_GROUP}, {TASK_FIELD_INTERVAL},"
						   f" {TASK_FIELD_DEADLINE}, {TASK_FIELD_DURATION}\n"
						   f"E.g.: task_edit 1 name\n")

		# Validate that task_id is an integer
		try:
			task_id = int(task_id)
			if task_id < 0:
				await ctx.send("First value must be a number representing the task ID")
				return
		except ValueError:
			await ctx.send("First value must be a number representing the task ID")
			return

		# Validate that the type is a valid option
		if field.lower() not in [TASK_FIELD_NAME.lower(), TASK_FIELD_GROUP.lower(), TASK_FIELD_INTERVAL.lower(),
								 TASK_FIELD_DEADLINE.lower(), TASK_FIELD_DURATION.lower()]:
			await ctx.send(f"Second value must be a field type. Options include: {TASK_FIELD_NAME}, {TASK_FIELD_GROUP},"
						   f" {TASK_FIELD_INTERVAL}, {TASK_FIELD_DEADLINE}, {TASK_FIELD_DURATION}\n")
			return

		# Confirm that the value fits the type

		print(value)

		# Once the data has been validated, push to database
		# Ensure task is associated with the server

		await ctx.send("Still needs to be implemented")

	@task_edit.error
	async def on_application_command_error(self, ctx: discord.ext.commands.Context, error: discord.DiscordException):
		if isinstance(error, commands.CommandInvokeError):
			await ctx.send(f"Unfortunately 3 parameters are needed. Format request like this:\n"
						   f"task_edit [Task_ID] [Type] [New Value]\n"
						   f"task_edit 1 Name Rake the leaves")
			return
		elif isinstance(error, discord.ext.commands.MissingRequiredArgument):
			await ctx.send(f"Unfortunately 3 parameters are needed. Format request like this:\n"
						   f"task_edit [Task_ID] [Type] [New Value]\n"
						   f"task_edit 1 Name Rake the leaves")
			return
		else:
			raise error

	@commands.command()
	async def task_settings(self, ctx: discord.ext.commands.Context):
		server = sql_tasks.get_servers(ctx.guild.id)[0]
		server: task_models.Server

		task_role = ""
		announcement_channel = ""

		for channel in ctx.guild.channels:
			if channel.id == server.announcement_channel:
				announcement_channel = channel.name
				continue

		for role in ctx.guild.roles:
			if role.id == server.task_role:
				task_role = role.name
				continue

		await ctx.send(f"{server.server_name} settings:\n"
					   f"	Task Role: {task_role}\n"
					   f"	Announcement channel: {announcement_channel}\n"
					   f"	Announcement time: {int(server.announcement_time/60)}:{server.announcement_time%60:02}\n")

	@commands.command()
	async def task_list(self, ctx: discord.ext.commands.Context):
		# List all tasks associated with the server
		tasks = sql_tasks.get_tasks(server_id=ctx.author.guild.id)

		if tasks is None:
			await ctx.send("There was an error retrieving tasks for this server")
			return
		elif len(tasks) == 0:
			await ctx.send("There are currently no tasks configured for this server")
			return

		message = "The server has the following tasks:\n"
		for item in tasks:
			item: task_models.Task
			message = message + f"	{item.id} {item.task_name}\n"

		await ctx.send(message)

	@commands.command()
	async def task_remove(self, ctx: discord.ext.commands.Context, *, task_id):
		if task_id is None:
			await ctx.send("Please specify the ID of the task to remove")
			return

		try:
			int(task_id)
		except ValueError:
			await ctx.send("Task ID must be a number")
			return

		# Confirm the task is one accessible to the server:
		matches = sql_tasks.get_tasks(ctx.guild.id, task_id=task_id)
		if len(matches) == 0:
			await ctx.send("No task with the corresponding ID was found for the server")
			return

		sql_tasks.remove_task(task_id)
		await ctx.send(f"Removed task {task_id} ({matches[0].task_name})")

	# TODO complete task, assign task to me

	async def cog_command_error(self, ctx: discord.ext.commands.Context, error: discord.DiscordException):
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send('Please pass in required arguments')
		elif isinstance(error, commands.CommandNotFound):
			await ctx.send('Invalid command')
		elif isinstance(error, commands.MissingPermissions):
			await ctx.send('Missing permissions')
		else:
			print("Unhandled error")
			print("Message: " + ctx.message.content)
			print("Author: " + ctx.message.author.name)
			print(f"Traceback: {error}")


async def setup(client):
	await client.add_cog(Tasks(client))
