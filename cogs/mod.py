# -*- coding: utf-8 -*-

from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import discord

class Moderation:
    """Moderation related commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def userinfo(self, ctx, user: discord.User=None):
        '''Gets info about a user.'''
        async with ctx.typing():
            if user is None:
                user = ctx.author
            e = discord.Embed(color=0x43b2c2)
            username = f'{user.name}#{user.discriminator}'
            join_date = user.created_at
            e.set_image(url=user.avatar_url)
            e.add_field(name='Name', value=username)
            e.add_field(name='Account Created', value=join_date)
            if ctx.guild:
                join_guild_date = ctx.guild.get_member(user.id)
                e.add_field(name='Joined Guild', value=join_guild_date, inline=False)
            e.add_field(name='ID', value=user.id, inline=False)
            e.add_field(name='Bot Account', value=user.bot)
            e.add_field(name='Animated Avatar', value=user.is_avatar_animated())
            await ctx.send(embed=e)

    @commands.guild_only()
    @commands.command()
    async def guildinfo(self, ctx):
        '''Gets info about the current guild.'''
        async with ctx.typing():
            e = discord.Embed(color=0x43b2c2)
            info = {}
            info['Creation Date'] = ctx.guild.created_at
            info['Guild ID'] = ctx.guild.id
            info['Roles'] = '\n'+''.join(f'\n{role.name}' for role in ctx.guild.roles) + '\n'
            info['Emojis'] = len(ctx.guild.emojis)
            info['Voice Region'] = ctx.guild.region
            icon = ctx.guild.icon
            info['Owner ID'] = ctx.guild.owner_id
            info['Owner'] = f'{ctx.guild.owner.name}#{ctx.guild.owner.discriminator}'
            info['2FA'] = 'On' if ctx.guild.mfa_level else 'Off'
            info['Verification Level'] = ctx.guild.verification_level.name
            info['Explicit Content'] = ctx.guild.explicit_content_filter.name
            info['Features'] = '\n'.join(f'`{feature}`' for feature in ctx.guild.features)
            info['Text Channels'] = len(ctx.guild.text_channels)
            info['Voice Channels'] = len(ctx.guild.voice_channels)
            info['Member Count'] = ctx.guild.member_count
            info['Large'] = ctx.guild.large
            

            afk_timeout = ctx.guild.afk_timeout
            if ctx.guild.afk_channel:
                afk_channel = ctx.guild.afk_channel.name
           
            fmtinfo = []
            for attr in info:
                fmtinfo.append(f'{attr}: {info[attr]}')
            
            e.description = f'```ini\n[ {ctx.guild.name} ]\n' + '\n'.join(fmtinfo) + '```'
            await ctx.send(embed=e)

    @commands.command(aliases=['prune'])
    async def purge(self, ctx, limit: int=None):
        '''Purge messages from the current channel~'''
        if limit is None:
            await ctx.channel.purge()
        else:
            await ctx.channel.purge(limit=limit)

    def is_me(self, m):
        return m.author == self.bot.user

    @commands.command()
    async def clean(self, ctx, limit: int=None):
        '''Cleans my messages~'''
        if limit is None:
            deleted = await ctx.channel.purge(check=self.is_me)
        else:
            deleted = await ctx.channel.purge(check=self.is_me, limit=limit)
        await ctx.send(f'Deleted {len(deleted)} messages(s)')

    @commands.guild_only()
    @commands.group()
    async def hoisters(self, ctx):
        '''Get information about hoisters.'''
        if ctx.invoked_subcommand is None:
            await ctx.send(f'Use `{ctx.prefix}help hoisters` for more info')

    @commands.guild_only()
    @hoisters.command(name='list')
    async def hoisters_list(self, ctx):
        '''Lists all the hoisters in the current guild.'''
        async with ctx.typing():
            try:
                e = discord.Embed(color=0x43b2c2)
                memberlist = sorted([str(member.display_name) for member in ctx.guild.members])[:10]
                e.add_field(name='Hoisters', value='```md\n- '+'\n- '.join(memberlist)+'```', inline=False)
                e.set_footer(text=f'To reset nicks for all hoisters do {self.bot.config.prefixes[0]}hoisters set [nick]')
            except Exception as err:
                e = discord.Embed(color=0x43b2c2)
                e.add_field(name='Why am I seeing this?', value='An error occured', inline=False)
                e.add_field(name='Traceback', value=f'```py\n{err}```')
            
            await ctx.send(embed=e)

    @commands.guild_only()
    @commands.has_permissions(manage_nicknames=True)
    @hoisters.command(name='set')
    async def hoisters_set(self, ctx, *, nick=None):
        '''Sets all the hoister's names in the current guild to [nick].
        Will reset all nicks by default.'''
        async with ctx.typing():
            try:
                e = discord.Embed(color=0x43b2c2)
                memberlist = sorted([str(member.display_name) for member in ctx.guild.members])[:10]
                memberlistid = sorted([str(member.id) for member in ctx.guild.members])[:10]
                for memberid in memberlistid:

                    try:
                        message = []
                        member=ctx.guild.get_member(int(memberid))
                        await member.edit(nick=nick, reason=f'Hoister removal by {ctx.author.name}#{ctx.author.discriminator}')
                        message.append(['Success', member.name])
                    except discord.errors.Forbidden:
                        message.append(['Privilege is too low...', member.display_name])
                    except Exception as err:
                        message.append([f'Failed: `{err}`', member.display_name])

                    for m in message:
                        e.add_field(name=m[1], value=m[0], inline=False)

            except TypeError as err:
                e = discord.Embed(color=0x43b2c2)
                e.add_field(name='Why am I seeing this?', value='An error occured', inline=False)
                e.add_field(name='Traceback', value=f'```py\n{err}```')
            
            await ctx.send(embed=e)

def setup(bot):
    bot.add_cog(Moderation(bot))

