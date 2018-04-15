# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import random
import wolframalpha
import functools
from cogs.utils.paginator import EmbedPages

class Search:
    '''Search the web.'''

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config
        self.client = wolframalpha.Client(bot.config.wolfram)
        self.invalid_strings = ['Nobody knows.',
                                'It\'s a mystery.',
                                'I have no idea.',
                                'No clue, sorry!',
                                'I\'m afraid I can\'t let you do that.',
                                'Maybe another time.',
                                'Ask someone else.',
                                'That is anybody\'s guess.',
                                'Beats me.',
                                'I haven\'t the faintest idea.']

    @commands.command()
    async def wolfram(self, ctx, *, query):
        '''Query Wolfram Alpha.'''
        async with ctx.typing():
            def q(query):
                res = self.client.query(query)
                return res
            async def async_q(query):
                thing = functools.partial(q, query)
                return await self.bot.loop.run_in_executor(None, thing)
            res = await async_q(query)
            e = discord.Embed(title='Wolfram|Alpha', description='', color=0x43b2c2)
            def invalid():
                e.add_field(name='Query', value=query, inline=False)
                e.add_field(name='Result', value=random.choice(self.invalid_strings)+'`(Invalid or undefined query)`', inline=False)
            try:
                r = next(res.results).text
                if r == '(undefined)' or r == '(data not available)':
                    invalid()
                else:
                    e.add_field(name='Query', value=query, inline=False)
                    e.add_field(name='Result', value=r, inline=False)
            except:
                invalid()
            await ctx.send(embed=e)

    @commands.command()
    async def quick(self, ctx, *, query: commands.clean_content):
        '''Do a quick wolframalpha query, with a short response'''
        async with ctx.typing():
            res = await self.bot.session.get('https://api.wolframalpha.com/v2/result', params={'i': query, 'appid': self.config.wolfram})
            text = await res.text()
            if text == 'No short answer available':
                to_send = ''
                to_send += f'{text}. Try doing `{ctx.prefix}wolfram '
                to_send += (query[:35] + '…') if len(query) > 35 else query + '`'

            elif text == 'Wolfram|Alpha did not understand your input':
                to_send = 'Sorry, I don\'t understand what you said.'
            else:
                to_send = text
        await ctx.send(to_send)

    @commands.command(aliases=['ddg', 'duck', 'google', 'goog'])
    async def duckduckgo(self, ctx, *, query: str):
        """Search the DuckDuckGo Instant Answer API"""
        await ctx.channel.trigger_typing()
        res = await self.bot.session.get(
                'https://api.duckduckgo.com',
                params={'q': query, 't': 'Charlotte Discord Bot',
                        'format': 'json', 'no_html': '1'})
        resp_json = await res.json(
            content_type='application/x-javascript'
        )
        embeds = {}

        if resp_json['AbstractURL'] != '':
            embeds[f'Abstract: {resp_json["Heading"]}'
                   f' ({resp_json["AbstractSource"]})'] = {
                'image': resp_json['Image'],
                'desc': f'{resp_json.get("AbstractText", "")}\n\n'
                        f'{resp_json["AbstractURL"]}'
            }

        if resp_json['Definition'] != '':
            embeds['Definition'] = {
                'desc': f'{resp_json["Definition"]}\n'
                        f'([{resp_json["DefinitionSource"]}]'
                        f'({resp_json["DefinitionURL"]}))'
            }

        if resp_json['RelatedTopics']:
            desc = []
            for topic in resp_json['RelatedTopics']:
                try:
                    if len('\n'.join(desc)) > 1000:
                        break
                    desc.append(
                        f'[**{topic["Text"]}**]({topic["FirstURL"]})'
                    )
                except KeyError:
                    # some weird subtopic thing I guess
                    continue

            embeds['Related'] = {
                'desc': '\n'.join(desc),
                'image': resp_json['RelatedTopics'][0]['Icon']['URL']
            }

        if resp_json['Results']:
            desc = []
            for result in resp_json['Results']:
                desc.append(
                    f'[**{result["Text"]}**]({result["FirstURL"]})'
                )
            embeds['Top Results'] = {
                'desc': '\n'.join(desc),
                'image': resp_json['Results'][0]['Icon']['URL']
            }

        final_embeds = []

        for embed_title, embed_content in embeds.items():
            final_embeds.append(
                discord.Embed(
                    title=embed_title,
                    description=embed_content['desc'],
                    color=ctx.author.color
                ).set_image(
                    url=embed_content['image']
                ).set_thumbnail(
                    url='https://i.imgur.com/CVogaGL.png'
                )
            )

        if not final_embeds:
            return await ctx.send('No results found.')

        p = EmbedPages(ctx, embeds=final_embeds)
        await p.paginate()

def setup(bot):
    bot.add_cog(Search(bot))
