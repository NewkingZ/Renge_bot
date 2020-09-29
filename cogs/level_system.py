# Follow https://www.youtube.com/watch?v=pKkrCHnun0M&ab_channel=Lucas
import json
from discord.ext import commands


class Levels(commands.Cog):
    def __init(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Level system module is ready')
        # Needs to be implemented


def setup(client):
    client.add_cog(Levels(client))

