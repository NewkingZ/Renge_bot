import discord
from discord.ext import commands


class Toolkit(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print('Toolkit Cog is ready')

    # Commands
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'pong! {round(self.client.latency * 1000)} ms')

    @commands.command()
    async def clear(self, ctx, amount: int):
        # TODO: check to see if user has permissions to remove messages
        await ctx.channel.purge(limit=amount)

    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        try:
            await member.kick(reason=reason)
            await ctx.send(f'Kicked {member.display_name}')
        except discord.ext.commands.errors.BadArgument:
            ctx.send("User not found")

    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        try:
            await member.ban(reason=reason)
            await ctx.send(f'Banned {member.display_name}')
        except discord.ext.commands.errors.BadArgument:
            ctx.send("User not found")

    @commands.command()
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.mention}')
                return

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Error with the clear command")


def setup(client):
    client.add_cog(Toolkit(client))

