# Module for League of legends related functionality

import os
import requests
from discord.ext import commands
from dotenv import load_dotenv
import json

LEAGUE_HEADER = "https://na1.api.riotgames.com/lol/"

LEAGUE_COMMANDS = {"get_summoner": "summoner/v4/summoners/by-name/",
                   "get_most_played": "champion-mastery/v4/champion-masteries/by-summoner/",
                   "get_rank": "league/v4/entries/by-summoner/",
                   "get_active_game": "spectator/v4/active-games/by-summoner/"}

LEAGUE_RANK_TYPES = {"RANKED_FLEX_SR" : "Ranked Flex",
                     "RANKED_SOLO_5x5" : "Ranked Solo",}

LEAGUE_RANKS = { "IRON" : "Iron",
                 "BRONZE": "Bronze",
                 "SILVER" : "Silver",
                 "GOLD" : "Gold",
                 "PLATINUM" : "Platinum",
                 "DIAMOND" : "Diamond",
                 "MASTER" : "Master",
                 "GRANDMASTER" : "Grandmaster",
                 "CHALLENGER" : "Challenger",
}

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
        _url = LEAGUE_HEADER + LEAGUE_COMMANDS["get_summoner"] + user
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
            results = results + f'\t{CHAMPIONS[str(content[i]["championId"])]} ' \
                                f'with {content[i]["championPoints"]:,} pts. level {content[i]["championLevel"]}\n'
        await ctx.send(results)

    @commands.command()
    async def getRank(self, ctx, *, user):
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
        _url = LEAGUE_HEADER + LEAGUE_COMMANDS["get_rank"] + content["id"]
        response = requests.get(_url, headers=headers)

        if response.status_code != 200:
            await ctx.send(f'Unsuccessful request getting summoner ranks. Code: {response.status_code}')
            return

        content = json.loads(response.content.decode())
        results = f'Summoner {user}\'s ranks are:\n'
        for rank in content:
            results = results + f'\t{LEAGUE_RANK_TYPES[rank["queueType"]]}: {LEAGUE_RANKS[rank["tier"]]}' \
                                f' {rank["rank"]} with {rank["leaguePoints"]} pts.' \
                                f'\t\t\tW/L = {rank["wins"]}/{rank["losses"]}\n'
            if "miniSeries" in rank:
                results = results + f'\t\t\tMini-series: {rank["miniSeries"]["wins"]}-{rank["miniSeries"]["losses"]}\n'
        await ctx.send(results)

    @commands.command()
    async def activeGame(self, ctx, *, user):
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
        _url = LEAGUE_HEADER + LEAGUE_COMMANDS["get_active_game"] + content["id"]
        response = requests.get(_url, headers=headers)

        if response.status_code != 200:
            print(_url)
            print(headers)
            await ctx.send(f'Unsuccessful request getting active game. Code: {response.status_code}')
            return

        # General informations
        content = json.loads(response.content.decode())
        results = f'Summoner {user}\'s game information:\n' \
                  f'Game type: {content["gameMode"]}\n' \
                  f'Duration: {(content["gameLength"] + 180)%60} minutes, seconds\n' \
                  f'Banned Champions: '

        # Banned Champions
        if "bannedChampions" in content:
            for champion in content["bannedChampions"]:
                results = results + CHAMPIONS[str(champion["championId"])] + ", "

            results = results[:-2]

        results = results + "\n\nTeam Blue\n"

        # Add participant information
        # Team blue
        for participant in content["participants"][len(content["participants"])//2:]:
            results = results + f'[{participant["summonerName"]}]   {CHAMPIONS[str(participant["championId"])]}\n'

        results = results + "\nTeam Red\n"

        # Add participant information
        # Team red
        for participant in content["participants"][:len(content["participants"])//2]:
            results = results + f'participant: {participant["summonerName"]}\n'

        await ctx.send(results)


def setup(client):
    client.add_cog(League(client))
    global CHAMPIONS
    with open('resources/champion.json') as f:
        CHAMPIONS = json.load(f)

