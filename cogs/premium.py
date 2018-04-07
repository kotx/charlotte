# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import os
from PIL import Image, ImageDraw, ImageFont
import textwrap

class Premium:
    """Upvote-locked commands uwu"""

    def __init__(self, bot):
        self.bot = bot

    class UserIsNotPremium(commands.CheckFailure):
        pass

    def is_premium():
        async def predicate(ctx):
            if True: # ctx.author.id in self.bot.upvoters:
                return True
            raise UserIsNotPremium(f'{ctx.author} is not premium')
        return commands.check(predicate)

    @is_premium()
    @commands.command()
    async def masterrace(self, ctx, *, args):
        masterrace = args.split(' | ')[0]
        peasants = args.split(' | ')[1]

        img = Image.open(f"peasants.png")
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("fonts/arial.ttf", 30)

        draw.text((100, 220), '\n'.join(textwrap.wrap(peasants, 13)), (0, 0, 0), font)
        draw.text((300, 90), '\n'.join(textwrap.wrap(masterrace, 13)), (0, 0, 0), font)

        img.save(f'cache/peasants/{ctx.author.id}.png')
        await ctx.send(file=discord.File(fp=f'cache/peasants/{ctx.author.id}.png'))
        os.remove(f'cache/peasants/{ctx.author.id}.png')

def setup(bot):
    bot.add_cog(Premium(bot))