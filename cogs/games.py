import discord
from discord.ext import commands
import random


def check_is_newking(ctx):
    return ctx.author.id != 222789991036747787


class Games(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print("Games Cog is ready")

    @commands.command(aliases=['8ball'])
    async def _8ball(self, ctx, *, question):
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

    @commands.command()
    @commands.check(check_is_newking)
    async def nyanpasu(self, ctx):
        await ctx.send('Nyanpasu!')


def setup(client):
    client.add_cog(Games(client))
