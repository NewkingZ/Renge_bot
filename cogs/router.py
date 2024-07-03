import discord
from discord.ext import commands
from modules import router_lib
from asusrouter import AsusRouter, AsusData
from asusrouter.modules.parental_control import AsusParentalControl
import asyncio
import aiohttp

loop = asyncio.get_event_loop()


class Router(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.client.loop.create_task(self.ready())

		# Connect to the router
		self.session = aiohttp.ClientSession()

		self.router = AsusRouter(
			hostname="192.168.50.1",
			username="Newking",
			password="udc!ie95yrAtzkf",
			use_ssl=True,
			session=self.session,
		)

	async def ready(self):
		await self.client.wait_until_ready()
		await self.router.async_connect()

		print('Router Cog ready')

	@commands.command()
	@commands.is_owner()
	async def router_control(self, ctx, *, mode):
		# Validate that the mode given is either 'on' or 'off
		if str(mode).lower() != 'on' and str(mode).lower() != 'off':
			await ctx.send(f'Mode selected needs to be On or Off')
			return

		res = await self.router.async_set_state(AsusParentalControl.OFF if str(mode).lower() == 'off' else AsusParentalControl.ON)

		# If it didn't work, re-try setting it
		if not res:
			# Try re-logging to server
			await self.router.async_connect()
			res = await self.router.async_set_state(AsusParentalControl.OFF if str(mode).lower() == 'off' else AsusParentalControl.ON)

		await ctx.send(f'Router control {"successfully" if res else "unsuccessfully"} set to {mode}')
		return

	@router_control.error
	async def router_control_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send(f'Command needs an On or Off mode')
		else:
			await ctx.send(f'Sorry, there was an error processing your command')
			print(error)


async def setup(client):
	await client.add_cog(Router(client))
