import discord
from discord.ext import commands
import aiohttp

class Minecraft:
    """ A minecraft cog for you! >~< """
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def hivemc(self, ctx):
        """ HiveMC Group """
        if ctx.invoked_subcommand is None:
            await ctx.send(f"B-baka! V-view `{ctx.prefix}help hivemc`!")

    @hivemc.command()
    async def player(self, ctx, player: str = None):
        if player is None:
            await ctx.send("B-baka! You need to s-specify a player!")
        else:
            url = self.bot.session.get(f'https://api.hivemc.com/v1/player/{player}')
            player = await url.json()
            owo = f'```ini\n[ Player {player.username} ]\n\nUUID: {player.UUID}\nRank: {player.rankname}\nTokens: {player.tokens}\nCredits: {player.credits}```'
            e = discord.Embed(description=owo)
            await ctx.send(embed=e)

def setup(bot):
    bot.add_cog(Minecraft(bot))
