# Required resource: https://www.ffmpeg.org/
# Also need youtube.dl
import discord
import youtube_dl
from discord.ext import commands

players = {}


class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.client.loop.create_task(self.ready())

    async def ready(self):
        await self.client.wait_until_ready()
        print('Music module is ready')

    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()

    @commands.command()
    async def join(self, ctx: commands.Context):
        destination = ctx.author.voice.channel

        if ctx.voice_client is not None:
            await ctx.voice_client.voice.move_to(destination)
            return
        ctx.voice_client.voice = await destination.connect()

    @commands.command(aliases=['play'])
    async def _play(self, ctx: commands.Context):
        vc = ctx.voice_client
        vc.play(discord.FFmpegPCMAudio('Play_this_daily.m4a'), after=lambda e: print('done', e))

    @commands.command(aliases=['brag'])
    async def _megan(self, ctx: commands.Context):
        vc = ctx.voice_client
        vc.play(discord.FFmpegPCMAudio('Play_this_daily.m4a'), after=lambda e: print('done', e))


def setup(client):
    client.add_cog(Music(client))


