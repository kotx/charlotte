import asyncio
import io
import traceback
import sys
import textwrap
from contextlib import redirect_stdout
from discord.ext import commands
import discord
from cogs.utils import paste
import textwrap

async def run_cmd(cmd: str) -> str:
    """Runs a subprocess and returns the output."""
    process = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    results = await process.communicate()
    return "".join(x.decode("utf-8") for x in results)


class Base:
    """Basic stuff."""

    def __init__(self, bot):
        self.bot = bot
        self._last_result = None

    # Stats

    @commands.command(aliases=['latency', 'pong'])
    async def ping(self, ctx):
        '''W-what are you looking at! P-pong!'''
        await ctx.send(f'w-what do you want from me? p-pong! ({round(self.bot.latency*1000)}ms)')

    @commands.command()
    async def botinfo(self, ctx):
        '''Y-you wanna learn about me? uwu'''
        total_members = sum(1 for x in self.bot.get_all_members())
        total_online = len({m.id for m in self.bot.get_all_members() if m.status is not discord.Status.offline})
        total_unique = len(self.bot.users)
        total_bots = len([m.id for m in self.bot.get_all_members() if m.bot])
        total_servers = len(self.bot.guilds)
        total_shards = self.bot.shard_count
        shard_num = ctx.guild.shard_id
        python_version = sys.version.split()[0]
        library_version = discord.__version__
        codeblock = f'```ini\n' + f'[ Bot Info ]\n' + \
                f'Total Users: {total_members}\n' + \
                f'Total Online Users: {total_online}\n' + \
                f'Total Unique Users: {total_unique}\n' + \
                f'Total Bots: {total_bots}\n' + \
                f'Total Guilds: {total_servers}\n' + \
                f'Total Shards: {total_shards}\n' + \
                f'Shard: {shard_num}/{total_shards}\n' + \
                f'Python Version: {python_version}\n' + \
                f'Library: discord.py {library_version}\n' + \
                f'```'
        e = discord.Embed(description=codeblock)
        await ctx.send(embed=e)

    @commands.command()
    async def shardinfo(self, ctx):
        '''Information about my shards baka'''
        codeblock = '```ini\n' + \
                '\n'.join([f'{shard}. online' for shard in self.bot.shards]) + \
                '```'
        e = discord.Embed(description=codeblock)

    # Owner Stuff

    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')
    
    @commands.command(hidden=True, aliases=['exec'])
    @commands.is_owner()
    async def shell(self, ctx, *, command: str):
        """Run stuff"""
        with ctx.typing():
            command = self.cleanup_code(command)
            result = await run_cmd(command)
            if len(result) >= 1500:
                pa = await paste.haste(ctx.bot.session, result)
                await ctx.send(f'`{command}`: Too long for Discord! {pa}')
            else:
                await ctx.send(f"`{command}`: ```{result}```\n")

    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    async def cog_load(self, ctx, *, module):
        """Loads a module."""
        try:
            self.bot.load_extension(module)
        except Exception as e:
            await ctx.send(f'B-baka! You broke something!```py\n{traceback.format_exc()}\n```')
        else:
            await ctx.send(f'I-I have loaded {module}! desu~')

    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    async def cog_unload(self, ctx, *, module):
        """Unloads a module."""
        try:
            self.bot.unload_extension(module)
        except Exception as e:
            await ctx.send(f'B-baka! You broke something!```py\n{traceback.format_exc()}\n```')
        else:
            await ctx.send(f'I-I have unloaded {module}! desu~')

    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def cog_reload(self, ctx, *, module):
        """Reloads a module."""
        try:
            self.bot.unload_extension(module)
            self.bot.load_extension(module)
        except Exception as e:
            await ctx.send(f'B-baka! You broke something!```py\n{traceback.format_exc()}\n```')
        else:
            await ctx.send(f'I-I have reloaded {module}! desu~')
    
    @commands.command(pass_context=True, hidden=True, name='eval')
    @commands.is_owner()
    async def _eval(self, ctx, *, body: str):
        """Evaluates a code"""

        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    if len(value) >= 1500:
                        pa = await paste.haste(ctx.bot.session, result)
                        return await ctx.send(f'Too long for Discord! {pa}')
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                if len(str(value)+str(ret)) >= 1501:
                    pa = await paste.haste(ctx.bot.session, f'{value}{ret}')
                    return await ctx.send(f'Too long for Discord! {pa}')
                await ctx.send(f'```py\n{value}{ret}\n```')

def setup(bot):
    bot.add_cog(Base(bot))
