# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import os
from PIL import Image, ImageDraw, ImageFont
import textwrap

class Premium:
    '''Upvote-locked commands uwu'''

    def __init__(self, bot):
        self.bot = bot

    class UserIsNotPremium(commands.CheckFailure):
        pass

    def is_premium():
        async def predicate(ctx):
            i = await ctx.bot.redis.get(ctx.author.id)
            if i:
                return True
            raise UserIsNotPremium(f'{ctx.author} is not premium')
        return commands.check(predicate)

    @is_premium()
    @commands.command()
    async def fbi(self, ctx, *, search: str):
        '''OwO FBI i-is looking for u'''
        img = Image.open(f'images/fbi.jpg')
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('fonts/arial.ttf', 30)

        draw.text((40, 260), search, (0, 0, 0), font)

        img.save(f'cache/fbi/{ctx.author.id}.jpg')
        await ctx.send(file=discord.File(fp=f'cache/fbi/{ctx.author.id}.jpg'))
        os.remove(f'cache/fbi/{ctx.author.id}.jpg')

    @is_premium()
    @commands.command()
    async def thesearch(self, ctx, *, text: str):
        '''Could it be this man?'''
        img = Image.open(f'images/intelligent.png')
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('fonts/arial.ttf', 16)

        draw.text((60, 340), '\n'.join(textwrap.wrap(text, 20)), (0, 0, 0), font)
        
        img.save(f'cache/thesearch/{ctx.author.id}.png')
        await ctx.send(file=discord.File(fp=f'cache/thesearch/{ctx.author.id}.png'))
        os.remove('cache/thesearch/{ctx.author.id}.png')

    @is_premium()
    @commands.command(aliases=['peasants'])
    async def masterrace(self, ctx, *, args):
        '''Declare something as the master race. Separate with ' | '.'''
        masterrace = args.split(' | ')[0]
        peasants = args.split(' | ')[1]

        img = Image.open(f'images/peasants.png')
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('fonts/arial.ttf', 30)

        draw.text((100, 220), '\n'.join(textwrap.wrap(peasants, 13)), (0, 0, 0), font)
        draw.text((350, 90), '\n'.join(textwrap.wrap(masterrace, 10)), (0, 0, 0), font)

        img.save(f'cache/peasants/{ctx.author.id}.png')
        await ctx.send(file=discord.File(fp=f'cache/peasants/{ctx.author.id}.png'))
        os.remove(f'cache/peasants/{ctx.author.id}.png')

def setup(bot):
    bot.add_cog(Premium(bot))
