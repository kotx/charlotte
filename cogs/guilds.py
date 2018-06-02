from discord.ext import commands
import discord
import ujson
import asyncio

class Guilds:
    def __init__(self, bot):
        self.bot = bot

    async def update_guild_count(self):
        await self.bot.change_presence(activity=discord.Activity(name=f'$help | {len(self.bot.guilds)} guilds', type=discord.ActivityType.listening))
        payload = {'server_count': sum(1 for g in self.bot.guilds)}
        await self.bot.session.request('POST', f'https://discordbots.org/api/bots/{self.bot.user.id}/stats', data=ujson.dumps(payload, ensure_ascii=True),
        headers={'Content-Type': 'application/json', 'Authorization': self.bot.config.dbl})
        await self.bot.session.request('POST', f'https://botlist.space/api/bots/{self.bot.user.id}', data=ujson.dumps(payload, ensure_ascii=True),
        headers={'Content-Type': 'application/json', 'Authorization': self.bot.config.botlist})
        await self.bot.session.request('POST', f'https://bots.discord.pw/api/bots/{self.bot.user.id}/stats', data=ujson.dumps(payload, ensure_ascii=True),
        headers={'Content-Type': 'application/json', 'Authorization': self.bot.config.dbots})
        await asyncio.sleep(1)

    async def on_ready(self):
        await self.update_guild_count()
   
    async def on_guild_join(self, guild):
        await self.update_guild_count()
    
    async def on_guild_remove(self, guild):
        await self.update_guild_count()

def setup(bot):
    bot.add_cog(Guilds(bot))
