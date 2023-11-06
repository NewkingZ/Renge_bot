import discord
from discord.ext import commands
import modules.sqlalchemy.task_commands as sql_tasks


class Tasks(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.client.loop.create_task(self.ready())

	async def ready(self):
		await self.client.wait_until_ready()
		print('Tasks Cog is ready')

	@commands.command()
	async def my_tasks(self, ctx, *, user):
		print(f"Got the following: {user}, {ctx}")


def setup(client):
	client.add_cog(Tasks(client))
