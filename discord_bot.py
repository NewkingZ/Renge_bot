# Renge bot python

import os
import discord
import logging
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('DISCORD_PREFIX')

logging.basicConfig(level=logging.INFO)
client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    for guild in client.guilds:
        print("Guild name is: " + guild.name + " with an id of: " + str(guild.id))


@client.event
async def on_member_join(member):
    await member.createdm()
    await member.dm_channel.send("Word is on the street that you like to go by 'last place larry'")


@client.event
async def on_message(message):
    # print message architecture to see what tf is there.
    print("Message author: " + message.author.name)
    print("Message author guild: " + message.author.guild.name)
    print("Message content: " + message.content)
    print("Message channel: " + message.channel)


client.run(TOKEN)
