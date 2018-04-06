#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import config
import aiohttp

class Bot(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix=commands.when_mentioned_or('$'), **kwargs)
        self.config = config
        self.session = aiohttp.ClientSession(loop=self.loop)
        for cog in config.cogs:
            try:
                self.load_extension(cog)
            except Exception as e:
                print('Could not load extension {0} due to {1.__class__.__name__}: {1}'.format(cog, e))

    async def on_ready(self):
        print('Logged on as {0} (ID: {0.id})'.format(self.user))
        await self.change_presence(activity=discord.Game(name=f'$help | {len(bot.guilds)} guilds'))

    async def on_message(self, message):
        if not message.author.bot:
            await bot.process_commands(message)

bot = Bot()

# write general commands here

bot.run(config.token)
