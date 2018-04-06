# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import weeb
import os.path
import random

class Fun:
    """W-want to have some f-fun with me?"""

    def __init__(self, bot):
        self.bot = bot
        self.weeb = sh_client = weeb.Client(token=bot.config.weebsh, user_agent="Weeb.py/1.1.0")

    @commands.command()
    async def pat(self, ctx, user: discord.User=None):
        '''Pat someone.'''
        img = await self.weeb.get_image(imgtype='pat')
        if user:
            if user.id == ctx.author.id:
                e = discord.Embed(description=f'{ctx.author.name} was feeling lonely so I gave them a pat!')
            elif user.id == self.bot.user.id:
                e = discord.Embed(description=f'B-Baka!')
                e.set_image(url='https://data.whicdn.com/images/65768241/large.gif')
                return await ctx.send(embed=e)
            else:
                e = discord.Embed(description=f'{ctx.author.name} patted {user.name}')
        else:
            e = discord.Embed()
        e.set_image(url=img[0])
        await ctx.send(embed=e)

    @commands.command()
    async def bite(self, ctx, user: discord.User=None):
        '''Bite someone.'''
        img = await self.weeb.get_image(imgtype='bite')
        if user:
            if user.id == ctx.author.id:
                e = discord.Embed(description=f'{ctx.author.name} bit themselves \o/')
            elif user.id == self.bot.user.id:
                e = discord.Embed(description=f'N-nooo!')
            else:
                e = discord.Embed(description=f'{ctx.author.name} bit {user.name}')
        else:
            e = discord.Embed()
        e.set_image(url=img[0])
        await ctx.send(embed=e)

    @commands.command()
    async def waifuinsult(self, ctx, user:discord.User=None):
        '''Insults somebody's waifu.'''
        if user is None:
            user = ctx.author
        async with ctx.typing(): 
            if not os.path.isfile(f'cache/waifuinsult/{user.id}.webp'):
                with open(f'cache/waifuinsult/{user.id}.webp', 'wb') as f:
                    f.write(await self.weeb.generate_waifu_insult(avatar=user.avatar_url))

            with open(f'cache/waifuinsult/{user.id}.webp', 'rb') as f:
                await ctx.send(file=discord.File(fp=f))

    @commands.command()
    async def ship(self, ctx, user:discord.User, user2:discord.User):
        '''Ships two users.'''
        async with ctx.typing(): 
            if not os.path.isfile(f'cache/ship/{user.id}-{user2.id}.webp'):
                with open(f'cache/ship/{user.id}-{user2.id}.webp', 'wb') as f:
                    f.write(await self.weeb.generate_love_ship(target_one=user.avatar_url, target_two=user2.avatar_url))

            with open(f'cache/ship/{user.id}-{user2.id}.webp', 'rb') as f:
                await ctx.send(file=discord.File(fp=f))

    @commands.command(aliases=['roll', 'dice'])
    async def rtd(self, ctx):
        '''Rolls a die.'''
        await ctx.send(f'I-I have to choose? I\'m not sure... I pick... **{random.randint(1, 6)}**')

    @commands.command(aliases=['choose'])
    async def pick(self, ctx, *, choices):
        '''Picks a random choice. Choices must be separated by ' | '.'''
        choice = random.choice(choices.split(' | ')) 
        await ctx.send(f'Mmm... I pick... **{choice}**')


def setup(bot):
    bot.add_cog(Fun(bot))
