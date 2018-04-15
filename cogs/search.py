# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import random
import wolframalpha
import functools

class Search:
    """Search the web."""

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config
        self.client = wolframalpha.Client(bot.config.wolfram)
        self.invalid_strings = ["Nobody knows.",
                                "It's a mystery.",
                                "I have no idea.",
                                "No clue, sorry!",
                                "I'm afraid I can't let you do that.",
                                "Maybe another time.",
                                "Ask someone else.",
                                "That is anybody's guess.",
                                "Beats me.",
                                "I haven't the faintest idea."]

    @commands.command()
    async def wolfram(self, ctx, *, query):
        """Query Wolfram Alpha."""
        async with ctx.typing():
            def q(query):
                res = self.client.query(query)
                return res
            async def async_q(query):
                thing = functools.partial(q, query)
                return await self.bot.loop.run_in_executor(None, thing)
            res = await async_q(query)
            e = discord.Embed(title="Wolfram|Alpha", description="", color=0x43b2c2)
            def invalid():
                e.add_field(name="Query", value=query, inline=False)
                e.add_field(name="Result", value=random.choice(self.invalid_strings)+"`(Invalid or undefined query)`", inline=False)
            try:
                r = next(res.results).text
                if r == "(undefined)" or r == "(data not available)":
                    invalid()
                else:
                    e.add_field(name="Query", value=query, inline=False)
                    e.add_field(name="Result", value=r, inline=False)
            except:
                invalid()
            await ctx.send(embed=e)

    @commands.command()
    async def quick(self, ctx, *, query: commands.clean_content):
        """Do a quick wolframalpha query, with a short response"""
        async with ctx.typing():
            res = await self.bot.session.get('https://api.wolframalpha.com/v2/result', params={'i': query, 'appid': self.config.wolfram})
            text = await res.text()
            if text == "No short answer available":
                to_send = ""
                to_send += f"{text}. Hint: try doing `{ctx.prefix}wolfram "
                to_send += (query[:35] + '…') if len(query) > 35 else query + '`'

            elif text == "Wolfram|Alpha did not understand your input":
                to_send = "Sorry, I don't understand what you said."
            else:
                to_send = text
        await ctx.send(to_send)

def setup(bot):
    bot.add_cog(Search(bot))
