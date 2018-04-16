import traceback
import sys
from discord.ext import commands
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


class CommandErrorHandler:
    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        ctx   : Context
        error : Exception"""

        await ctx.send(f'B-baka! You broke something! `{error}`')

        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return
        
        ignored = (commands.CommandNotFound, commands.UserInputError)
        
        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)
        
        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            return

def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
