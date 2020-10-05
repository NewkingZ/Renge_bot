from discord.ext import commands
import subprocess
import asyncio

# Things that are needed:
# Path to starting the server
# Bash file to start the script

DST_STATUS = False


async def startDST():
    proc = await asyncio.create_subprocess_shell('tasklist',
                                                 stdout=asyncio.subprocess.PIPE,
                                                 stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    print(f'[command exited with {proc.returncode}]')
    if stdout:
        print(f'[stdout]\n{stdout.decode()}')
    if stderr:
        print(f'[stderr]\n{stderr.decode()}')


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
        await ctx.send("Still needs to be implemented")
        await startDST()

    @commands.command()
    async def dstStop(self, ctx):
        # Stop the server
        await ctx.send("Still needs to be implemented")

def setup(client):
    client.add_cog(DST(client))

