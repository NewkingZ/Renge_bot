# Required resource: https://www.ffmpeg.org/
# Also need youtube.dl
import discord
import youtube_dl
from discord.ext import commands

players = {}


class Music(commands.Cog):
    def __init(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Music module is ready')

    @commands.command()
    async def leave(self, ctx):
        server = ctx.message.server
        voice_client = self.client.voice_client_in(server)
        await voice_client.disconnect()

    @commands.command()
    async def join(self, ctx):
        channel = ctx.message.author.voice.voice_channel
        await self.client.join_voice_channel(channel)

    @commands.command()
    async def play(self, ctx, url):
        server = ctx.message.server
        voice_client = self.client.voice_client_in(server)
        player = await voice_client.create_ytdl_player(url)
        players[server.id] = player
        player.start()


def setup(client):
    client.add_cog(Music(client))


