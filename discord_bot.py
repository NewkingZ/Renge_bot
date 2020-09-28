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

status = cycle(['Nyanpasu!', 'Killin it'])


# Event triggered when the bot has completed setup and is now ready to perform tasks
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Nyanpasu!'))
    print(f'{client.user} has connected to Discord!')
    for guild in client.guilds:
        print("Guild name is: " + guild.name + " with an id of: " + str(guild.id))
    change_status.start()


# Event triggered when members join a discord server (guild)
@client.event
async def on_member_join(member):
    print("Member has joined, nothing enabled currently")
    # await member.createdm()
    # await member.dm_channel.send("Word is on the street that you like to go by 'last place larry'")

# ##################### Client Commands ##################################
@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')


@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f'cogs.{filename[:-3]}')

# Finally, run the bot
client.run(TOKEN)
