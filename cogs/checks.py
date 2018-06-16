import traceback
import sys
from discord.ext import commands
import textwrap
import discord

"""
If you are not using this inside a cog, add the event decorator e.g:
@bot.event
async def on_command_error(ctx, error)

For examples of cogs see:
Rewrite:
https://gist.github.com/EvieePy/d78c061a4798ae81be9825468fe146be
Async:
https://gist.github.com/leovoel/46cd89ed6a8f41fd09c5

This example uses @rewrite version of the lib. For the async version of the lib, simply swap the places of ctx, and error.
e.g: on_command_error(self, error, ctx)

For a list of exceptions:
http://discordpy.readthedocs.io/en/rewrite/ext/commands/api.html#errors
"""


class CommandHandler:
    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        ctx   : Context
        error : Exception"""
        
        ignored = (commands.CommandNotFound, commands.UserInputError)
        
        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return
        
        
        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)
        
        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            return


        await ctx.send(f'B-baka! You broke something! `{error}`. If you think this is a mistake, feel free to report it at our support server( https://discord.gg/R3HCMRU )')

        error_channel = self.bot.get_channel(435276965361090560)
        err = ''.join(traceback.format_exception(type(error), error, error.__traceback__))
        e = discord.Embed(color=discord.Color.red(), title='Command Errored', description=f'```ini\n[ {ctx.command.qualified_name} ]\n{err}```')
        await error_channel.send(embed=e)

    async def on_command(self, ctx):
        command_log = self.bot.get_channel(435287819385307137)
        e = discord.Embed(color=0x43b2c2, title='Command Invoked')
        e.description = textwrap.dedent(f'```ini\n[ {ctx.command.qualified_name} ]\nGuild ID: {ctx.guild.id}\nChannel ID: {ctx.channel.id}\nInvoker: {ctx.author.id}\nInvoker Name: {ctx.author.name}#{ctx.author.discriminator}\nMessage ID: {ctx.message.id}\nMessage content: {ctx.message.content}```')
        await command_log.send(embed=e)

def setup(bot):
    bot.add_cog(CommandHandler(bot))
