# Follow https://www.youtube.com/watch?v=pKkrCHnun0M&ab_channel=Lucas
import json
from discord.ext import commands


class Levels(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.client.loop.create_task(self.ready())

    async def ready(self):
        await self.client.wait_until_ready()
        print('Level system module is ready')
        # Needs to be implemented


async def setup(client):
    await client.add_cog(Levels(client))

