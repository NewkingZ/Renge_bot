import discord
from discord.ext import commands
import modules.sqlalchemy.task_commands as sql_tasks


class Tasks(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.client.loop.create_task(self.ready())

	async def ready(self):
		await self.client.wait_until_ready()

		# Check to make sure all guilds are in the database:
		existing_guilds = sql_tasks.get_servers()
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
		print(f"Got the following task command: {ctx.author}")
		# Replace contents here with the ability to return that user's tasks FOR THIS SERVER
		# Maybe allow option to list all by adding flag

		# To get the relevant data, use the following:
		# user id: ctx.author.id
		# server id: ctx.author.guild.id
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
				await ctx.send("Updated role to assign tasks")
				return

		await ctx.send("Invalid task role")


async def setup(client):
	await client.add_cog(Tasks(client))
