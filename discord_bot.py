# Renge bot python

# Import block for getting libraries
import os
import random
import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import modules.toolkit as toolkit

# Get the environment variables like the keys
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('DISCORD_PREFIX')

# Set up work environment
logging.basicConfig(level=logging.INFO)
client = commands.Bot(command_prefix=PREFIX)


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
    # await member.dm_channel.send("Word is on the street that you like to go by 'last place larry'")

# Base command
@client.command()
async def ping(ctx):
    await ctx.send(f'pong! {round(client.latency * 1000)} ms')


@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = ["It is certain",
                 "It is decidedly so",
                 "Without a doubt",
                 "Yes, definitely",
                 "You may rely on it",
                 "As I see it, yes",
                 "Most Likely",
                 "Outlook Good",
                 "Yes",
                 "Signs point to yes",
                 "Reply hazy, try again",
                 "Ask again later",
                 "Better not tell you now",
                 "Cannot predict now",
                 "Concentrate and ask again",
                 "Don't count on it",
                 "My reply is no",
                 "My sources say no",
                 "Outlook not so good",
                 "Very Doubtful"]
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')


# Finally, run the bot
client.run(TOKEN)
