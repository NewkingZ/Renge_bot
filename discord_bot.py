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
    # print message architecture to see what tf is there.
    print("Message author: " + message.author.name)
    print("Message author guild: " + message.author.guild.name)
    print("Message content: " + message.content)
    print("Message channel: " + message.channel.name)
    if message.content == str(PREFIX) + "Hi":
        print("Fack you")

# Finally, run the bot
client.run(TOKEN)
