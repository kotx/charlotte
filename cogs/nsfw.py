import discord
import aiohttp
import random
import json
from discord.ext import commands


class NSFW:
    """"NSFW commands.
    Most commands are "borrowed" from Godavaru (https://github.com/Godavaru/Godavaru), with little/no modification."""
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.is_nsfw()
    async def lewdneko(self, ctx):
        '''Gets a random lewd neko o.o'''
        e = discord.Embed(color=0x43b2c2)
        resp = await self.bot.session.get(url='https://nekos.life/api/lewd/neko')
        resp = await resp.json()
        e.set_image(url=resp['neko'])
        e.set_footer(text='Powered by nekos.life')
        await ctx.send(embed=e)

    @commands.command(aliases=["r34"])
    async def rule34(self, ctx, tag: str):
        """Search for an image on rule34!
        Note: To use this command, the channel must be NSFW."""
        if ctx.channel.is_nsfw():
            try:
                url = 'https://rule34.xxx/index.php?page=dapi&s=post&q=index&json=1&tags=' + tag
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as resp:
                        js = json.loads(await resp.text())
                non_loli = list(filter(lambda x: 'loli' not in x['tags'] and 'shota' not in x['tags'], js))
                if len(non_loli) == 0:
                    return await ctx.send(":warning: All results included loli/shota content; this search is invalid.")
                response = non_loli[random.randint(0, len(non_loli) - 1)]
                img = f"https://img.rule34.xxx/images/{response['directory']}/{response['image']}"
                tags = response['tags'].split(' ')
                em = discord.Embed(description=f'`{", ".join(tags)}`', colour=0xff0000)
                em.set_image(url=img)
                em.set_author(name='Found Image! Click me if it doesn\'t load!', url=img)
                await ctx.send(embed=em)
            except json.JSONDecodeError:
                await ctx.send(":x: No image found. Sorry :/")
        else:
            await ctx.send(":x: This is not an NSFW channel.")

    @commands.command()
    async def yandere(self, ctx, tag: str, rating: str = None):
        """Search for an image on yande.re!
        Note: To use this command, the channel must be NSFW."""
        rating = rating.lower() if rating else None
        if ctx.channel.is_nsfw():
            url = 'https://yande.re/post.json?tags=rating:' + (
                rating if rating in ['safe', 'questionable', 'explicit'] else 'safe') + '%20' + tag
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    js = await resp.json()
            if len(js) > 0:
                non_loli = list(filter(
                    lambda x: 'loli' not in x['tags'] and 'shota' not in x['tags'] and 'deletethistag' not in x['tags'],
                    js))
                if len(non_loli) == 0:
                    return await ctx.send(":warning: All results included loli/shota content; this search is invalid.")
                response = non_loli[random.randint(0, len(non_loli) - 1)]
                img = response['file_url']
                tags = response['tags'].split(' ')
                em = discord.Embed(
                    description=f'**Rating:** {(rating if rating in ["safe", "questionable", "explicit"] else "safe")}\n`{", ".join(tags)}`',
                    colour=0xff0000)
                em.set_image(url=img)
                em.set_author(name='Found Image! Click me if it doesn\'t load!', url=img)
                await ctx.send(embed=em)
            else:
                await ctx.send(":x: No image found. Sorry :/")
        elif rating == "safe" and not ctx.channel.is_nsfw():
            await ctx.send(
                ":warning: Sorry! I know that this image is marked as `safe`, but yande.re sometimes returns lewd images in the safe rating. Please use an NSFW channel.")
        else:
            await ctx.send(":x: This is not an NSFW channel.")


def setup(bot):
    bot.add_cog(NSFW(bot))
