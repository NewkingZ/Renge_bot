# Renge bot python

# Import block for getting libraries
import os
import discord
import logging
from dotenv import load_dotenv

# Get the environment variables like the keys
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('DISCORD_PREFIX')

# Set up work environment
logging.basicConfig(level=logging.INFO)
client = discord.Client()

# Event triggered when the bot has completed setup and is now ready to perform tasks
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    for guild in client.guilds:
        print("Guild name is: " + guild.name + " with an id of: " + str(guild.id))

# Event triggered when members join a discord server (guild)
@client.event
async def on_member_join(member):
    await member.createdm()
    await member.dm_channel.send("Word is on the street that you like to go by 'last place larry'")

# Event triggered when a message is sent to a discord server that the bot is in
@client.event
async def on_message(message):
    # Check to see if the user for the command is the same as the bot (Not responding to a response)
    if message.author == client.user:
        return

    # Check to see if the prefix is valid at the beginning of the message
    if message.content[0] != PREFIX or message.content == "~":
        return

    # Get the command that was passed to the bot
    command = message.content[1:].split(" ")[0].lower()

    # At this point the command is in lower case, just needs to be handled accordingly
    print(command)

# Finally, run the bot
client.run(TOKEN)
