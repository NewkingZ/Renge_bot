# Renge bot python

# Import block for getting libraries
import os
import discord
from discord.ext import commands, tasks
import logging
from dotenv import load_dotenv
from itertools import cycle

# Get the environment variables like the keys
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('DISCORD_PREFIX')

# Set up work environment
logging.basicConfig(level=logging.INFO)
client = commands.Bot(command_prefix=PREFIX)
# client.remove_command('help')

status = cycle(['Nyanpasu!', 'Killin it'])


async def ready():
    await client.wait_until_ready()
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Nyanpasu!'))
    print(f'{client.user} has connected to Discord!')
    for guild in client.guilds:
        print("Guild name is: " + guild.name + " with an id of: " + str(guild.id))
    # change_status.start()


# Event triggered when members join a discord server (guild)
@client.event
async def on_member_join(member):
    print("Member has joined, nothing enabled currently")
    # await member.createdm()
    # await member.dm_channel.send("Word is on the street that you like to go by 'last place larry'")


@client.command()
async def Nyanpasu(ctx):
    await ctx.send("Nyanpasu!", file=discord.File("./resources/pictures/morning.png"))


# @client.event
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.MissingRequiredArgument):
#         await ctx.send('Please pass in required arguments')
#     elif isinstance(error, commands.CommandNotFound):
#         await ctx.send('Invalid command')
#     elif isinstance(error, commands.MissingPermissions):
#         await ctx.send('Missing permissions')
#     else:
#         print("Unhandled error")
#         print("Message: " + ctx.message.content)
#         print("Author: " + ctx.message.author.name)

# ##################### Client Commands ##################################
@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')


# @tasks.loop(seconds=10)
# async def change_status():
#     await client.change_presence(activity=discord.Game(next(status)))


# Load cogs and then start the client
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f'cogs.{filename[:-3]}')

client.loop.create_task(ready())

client.run(TOKEN)
