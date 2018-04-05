# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import textwrap

class Lounge:
    """Management for Charlotte's guild."""

    def __init__(self, bot):
        self.bot = bot

    async def on_guild_join(self, guild):
        desc = textwrap.dedent(f'''
        ```ini
        [ {guild.name} ]
        ID: {guild.id}
        Large: {guild.large}
        Member Count: {guild.member_count}
        Icon URL: {guild.icon_url}
        Owner ID: {guild.owner.id}
        ```
        ''')
        e = discord.Embed(title='Joined Guild', description=desc)
        log = self.bot.get_channel(431447344894967808)
        await log.send(embed=e)


    async def on_guild_remove(self, guild):
        desc = textwrap.dedent(f'''
        ```ini
        [ {guild.name} ]
        ID: {guild.id}
        Large: {guild.large}
        Member Count: {guild.member_count}
        Icon URL: {guild.icon_url}
        Owner ID: {guild.owner.id}
        ```
        ''')
        e = discord.Embed(title='Left Guild', description=desc)
        log = self.bot.get_channel(431447344894967808)
        await log.send(embed=e)

def setup(bot):
    bot.add_cog(Lounge(bot))
