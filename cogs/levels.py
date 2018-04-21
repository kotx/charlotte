# -*- coding: utf-8 -*-

from discord.ext import commands
import discord

class Levels:
    """The description for Levels goes here."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rep(self, ctx, user: discord.User=None):
        if user is None:
            user = ctx.author
            r = await self.bot.session.get(f'https://api.weeb.sh/reputation/{self.bot.user.id}/{user.id}', headers={'Authorization': self.bot.config.weebsh})
            r = await r.json()
            rep = r['user']['reputation']
            await ctx.send(f'**{ctx.author.name}**, you currently have {rep} reputation~')
        else:
            r = await self.bot.session.post(f'https://api.weeb.sh/reputation/{self.bot.user.id}/{user.id}', headers={'Authorization': self.bot.config.weebsh}, data={'source_user': {ctx.author.id}})
            r = await r.json()
            if  r['code'] == 0:
                rep = r['targetUser']['reputation']
                await ctx.send('Successfully gave {user.name}#{user.discriminator} 1 reputation! They now have `{rep}` reputation!')
            else:
                err = r['message']
                await ctx.send(f'An error occured: `{err}`')

def setup(bot):
    bot.add_cog(Levels(bot))
