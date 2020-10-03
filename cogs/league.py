# Module for League of legends related functionality

import os
import requests
from discord.ext import commands
from dotenv import load_dotenv
import json

LEAGUE_HEADER = "https://na1.api.riotgames.com/lol/"

LEAGUE_COMMANDS = {"get_summoner": "summoner/v4/summoners/by-name/",
                   "get_most_played": "champion-mastery/v4/champion-masteries/by-summoner/"}

# Maximum # of commands for bot is 20 requests / second, 100 / 2 minutes
load_dotenv()
LEAGUE_KEY = os.getenv('RIOT_KEY')

CHAMPIONS = None


class League(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.client.loop.create_task(self.ready())

    async def ready(self):
        await self.client.wait_until_ready()
        print('League module is ready')

    @commands.command()
    async def summoner(self, ctx, *, user):
        _url = LEAGUE_HEADER + LEAGUE_COMMANDS["get_summoner_by_name"] + user
        headers = {
            "Origin": "https://developer.riotgames.com",
            "X-Riot-Token": LEAGUE_KEY
        }
        response = requests.get(_url, headers=headers)
        if response.status_code != 200:
            await ctx.send(f'Unsuccessful request. Code: {response.status_code}')
        else:
            # await ctx.send("Successfully retrieved information on user: " + user)
            content = json.loads(response.content.decode())
            await ctx.send(f'{user} is level {content["summonerLevel"]}. Encrypted ID: {content["id"]}')

    @commands.command()
    async def mostPlayed(self, ctx, *, user):
        _url = LEAGUE_HEADER + LEAGUE_COMMANDS["get_summoner"] + user
        headers = {
            "Origin": "https://developer.riotgames.com",
            "X-Riot-Token": LEAGUE_KEY
        }
        response = requests.get(_url, headers=headers)
        if response.status_code != 200:
            await ctx.send(f'Unsuccessful request referencing summoner ID. Code: {response.status_code}')
            return

        content = json.loads(response.content.decode())
        _url = LEAGUE_HEADER + LEAGUE_COMMANDS["get_most_played"] + content["id"]
        response = requests.get(_url, headers=headers)

        if response.status_code != 200:
            await ctx.send(f'Unsuccessful request getting mastery list. Code: {response.status_code}')
            return

        content = json.loads(response.content.decode())
        results = f'Summoner {user}\'s most played are:\n'

        for i in range(5):
            results = results + f'\t{CHAMPIONS[str(content[i]["championId"])]} with {content[i]["championPoints"]}\n'
        await ctx.send(results)


def setup(client):
    client.add_cog(League(client))
    global CHAMPIONS
    with open('resources/champion.json') as f:
        CHAMPIONS = json.load(f)

