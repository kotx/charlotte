from discord.ext import commands
import discord
import ujson
import asyncio

class Guilds:
    def __init__(self, bot):
        self.bot = bot

    async def update_guild_count(self, shard_id):
        await self.bot.change_presence(activity=discord.Activity(name=f'$help | {len(self.bot.guilds)} guilds', type=discord.ActivityType.listening))
        await self.bot.session.request('POST', f'https://botlist.space/api/bots/{self.bot.user.id}', data=ujson.dumps(payload, ensure_ascii=True),
        headers={'Content-Type': 'application/json', 'Authorization': self.bot.config.botlist})
        dPayload = {'guildCount': sum(1 for g in self.bot.guilds), 'shardCount': len(self.bot.shards), 'shardId': shard_id}
        await self.bot.session.request('POST', f'https://discord.bots.gg/api/v1/bots/{self.bot.user.id}/stats', data=ujson.dumps(payload, ensure_ascii=True),
        headers={'Content-Type': 'application/json', 'Authorization': self.bot.config.dbots})
        await asyncio.sleep(1)

    async def on_ready(self):
        await self.update_guild_count(0)
   
    async def on_guild_join(self, guild):
        await self.update_guild_count(guild.shard_id)
    
    async def on_guild_remove(self, guild):
        await self.update_guild_count(guild.shard_id)

def setup(bot):
    bot.add_cog(Guilds(bot))
