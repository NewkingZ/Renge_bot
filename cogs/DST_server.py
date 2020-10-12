# Don't starve together library for server handling

import os
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
        DST_SERVER = subprocess.Popen([DST_SERVER_DIR.split("/")[-1], "-conf_dir", "myDSTserver"],
                                      stdout=f, stdin=subprocess.PIPE)
        os.chdir(current_path)
        await ctx.send("Server has started, it might take a couple of minutes for you to see it.\n"
                       "Look for my backyard!")

    @commands.command()
    async def dstStop(self, ctx):
        # Stop the server
        global DST_SERVER
        if DST_SERVER is not None:
            DST_SERVER.stdin.write(bytearray('c_shutdown()\n', "utf-8"))
            DST_SERVER.stdin.flush()
            await ctx.send("Server has been killed")
            DST_SERVER = None
        else:
            await ctx.send("Server isn't running currently")

    @commands.command()
    async def dstPW(self, ctx):
        if DST_SERVER is None:
            await ctx.send("There is no password for a server that isn't running")
        else:
            await ctx.send("Password for the server: " + os.getenv("DST_SERVER_PASSWORD"))

    @commands.command()
    async def dstStatus(self, ctx):
        if DST_SERVER is None:
            await ctx.send("Server is down, use dstStart to get it going!")
        else:
            await ctx.send("Server is running right now!")

    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def dstReset(self, ctx: commands.context, *, reason):
        if DST_SERVER is None:
            await ctx.send("Server is currently down. It must be running before passing the command")
        else:
            print("DST Server was restarted by: " + ctx.author.name)
            print("Reason was: " + reason)
            DST_SERVER.stdin.write(bytearray('c_regenerateworld()\n', "utf-8"))
            DST_SERVER.stdin.flush()
            await ctx.send("Restarting the server")

    @dstReset.error
    async def dstReset_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please give a reason to restart the server when using the command")

    @commands.command()
    async def dstSave(self, ctx):
        if DST_SERVER is None:
            await ctx.send("Server is currently down. It's gotta be running for it to be saved")
        else:
            DST_SERVER.stdin.write(bytearray('c_save()\n', "utf-8"))
            DST_SERVER.stdin.flush()
            await ctx.send("Saved the server state (auto-save is done at the end of every night)")
            

def setup(client):
    client.add_cog(DST(client))
