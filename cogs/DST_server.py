# Don't starve together library for server handling

import os
import signal
import asyncio
import subprocess
from dotenv import load_dotenv
from discord.ext import commands

# Things that are needed:
# Path to starting the server
# Bash file to start the script

load_dotenv()
DST_SERVER_DIR = os.getenv("DST_SERVER_EXE")
DST_SERVER = None


class DST(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.client.loop.create_task(self.ready())

    async def ready(self):
        await self.client.wait_until_ready()
        print("DST Cog is ready")

    @commands.command()
    async def dstStart(self, ctx):
        # Start the server
        global DST_SERVER

        if DST_SERVER is not None:
            await ctx.send("Renge's Backyard is already running")
            return

        f = open("./logs/DST.txt", "w+")
        current_path = os.getcwd()
        os.chdir("/".join(DST_SERVER_DIR.split("/")[:-1]))
        DST_SERVER = subprocess.Popen([DST_SERVER_DIR.split("/")[-1], "-conf_dir", "myDSTserver"], stdout=f)
        os.chdir(current_path)
        await ctx.send("Server has started, it might take a couple of minutes for you to see it.\n"
                       "Look for my backyard!")

    @commands.command()
    async def dstStop(self, ctx):
        # Stop the server
        global DST_SERVER
        if DST_SERVER is not None:
            DST_SERVER.kill()
            await ctx.send("Server has been killed")
            DST_SERVER = None
        else:
            await ctx.send("Server isn't running currently")

    @commands.command()
    async def dstPW(self, ctx):
        await ctx.send("Password for the server: " + os.getenv("DST_SERVER_PASSWORD"))

    @commands.command()
    async def dstStatus(self, ctx):
        if DST_SERVER is None:
            await ctx.send("Server is down, use dstStart to get it going!")
        else:
            await ctx.send("Server is running right now!")


def setup(client):
    client.add_cog(DST(client))
