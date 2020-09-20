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

# ##################### Client Commands ##################################

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


@client.command()
async def clear(ctx, amount=5):
    # TODO: check to see if user has permissions to remove messages
    await ctx.channel.purge(limit=amount)


@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    try:
        await member.kick(reason=reason)
    except discord.ext.commands.errors.BadArgument:
        ctx.send("User not found")


@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    try:
        await member.ban(reason=reason)
        await ctx.send(f'Banned {user.mention}')
    except discord.ext.commands.errors.BadArgument:
        ctx.send("User not found")


@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return


# Finally, run the bot
client.run(TOKEN)
