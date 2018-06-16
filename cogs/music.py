import logging
import math
import re

import discord
import lavalink
from discord.ext import commands

time_rx = re.compile('[0-9]+')


class Music:
    def __init__(self, bot):
        self.bot = bot

        if not hasattr(bot, 'lavalink'):
            lavalink.Client(bot=bot, host=self.bot.config.lavalink['host'], ws_port=8080, password=self.bot.config.lavalink['password'], loop=self.bot.loop, log_level=logging.INFO)
            self.bot.lavalink.register_hook(self.track_hook)

    async def track_hook(self, event):
        if isinstance(event, lavalink.Events.TrackStartEvent):
            c = event.player.fetch('channel')
            if c:
                c = self.bot.get_channel(c)
                if c:
                    embed = discord.Embed(colour=c.guild.me.top_role.colour, title='Now Playing', description=event.track.title)
                    embed.set_thumbnail(url=event.track.thumbnail)
                    await c.send(embed=embed)
        elif isinstance(event, lavalink.Events.QueueEndEvent):
            c = event.player.fetch('channel')
            if c:
                c = self.bot.get_channel(c)
                if c:
                    await c.send('Reached end of queue! M-maybe add more songs?')

    @commands.command(aliases=['p'])
    async def play(self, ctx, *, query):
        '''Play a song, what did you expect, baka'''
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.is_connected:
            if not ctx.author.voice or not ctx.author.voice.channel:
                return await ctx.send('Join a voice channel, baka!')

            permissions = ctx.author.voice.channel.permissions_for(ctx.me)

            if not permissions.connect or not permissions.speak:
                return await ctx.send('Baka! I\'m missing permissions for connecting or speaking in voice channels!')

            player.store('channel', ctx.channel.id)
            await player.connect(ctx.author.voice.channel.id)
        else:
            if not ctx.author.voice or not ctx.author.voice.channel or player.connected_channel.id != ctx.author.voice.channel.id:
                return await ctx.send('Join my voice channel, baka!!')

        query = query.strip('<>')

        if not query.startswith('http'):
            query = f'ytsearch:{query}'

        tracks = await self.bot.lavalink.get_tracks(query)

        if not tracks:
            return await ctx.send('Nothing found uwu')

        embed = discord.Embed(colour=ctx.guild.me.top_role.colour)

        if 'list' in query and 'ytsearch:' not in query:
            for track in tracks:
                player.add(requester=ctx.author.id, track=track)

            embed.title = "Playlist Enqueued!"
            embed.description = f"Imported {len(tracks)} tracks from the playlist c:"
            await ctx.send(embed=embed)
        else:
            embed.title = "Track Enqueued"
            embed.description = f'[{tracks[0]["info"]["title"]}]({tracks[0]["info"]["uri"]})'
            await ctx.send(embed=embed)
            player.add(requester=ctx.author.id, track=tracks[0])

        if not player.is_playing:
            await player.play()

    @commands.command()
    async def seek(self, ctx, time):
        '''Seek to a part of the song :>'''
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send('Not playing.')

        pos = '+'
        if time.startswith('-'):
            pos = '-'

        seconds = time_rx.search(time)

        if not seconds:
            return await ctx.send('Baka, how long do you want me to skip?')

        seconds = int(seconds.group()) * 1000

        if pos == '-':
            seconds = seconds * -1

        track_time = player.position + seconds

        await player.seek(track_time)

        await ctx.send(f'Moved track to **{lavalink.Utils.format_time(track_time)}**!')

    @commands.command(aliases=['forceskip', 'fs'])
    async def skip(self, ctx):
        '''Skips a song'''
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send('I\'m not playing >~<')

        await ctx.send('I-I skipped it for you, I\'m sorry if I messed up...')
        await player.skip()

    @commands.command()
    async def stop(self, ctx):
        '''S-stops the music'''
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send('Not playing.')

        player.queue.clear()
        await player.stop()
        await ctx.send('⏹ | S-stopped.')

    @commands.command(aliases=['np', 'n'])
    async def now(self, ctx):
        '''Displays currently playing song~'''
        player = self.bot.lavalink.players.get(ctx.guild.id)
        song = 'Nothing'

        if player.current:
            pos = lavalink.Utils.format_time(player.position)
            if player.current.stream:
                dur = 'LIVE'
            else:
                dur = lavalink.Utils.format_time(player.current.duration)
            song = f'**[{player.current.title}]({player.current.uri})**\n({pos}/{dur})'

        embed = discord.Embed(colour=ctx.guild.me.top_role.colour, title='Now Playing', description=song)
        await ctx.send(embed=embed)

    @commands.command(aliases=['q'])
    async def queue(self, ctx, page: int=1):
        '''Shows the queue!'''
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.queue:
            return await ctx.send('N-no! There\'s no queue! D-do you want me to explode?')

        items_per_page = 10
        pages = math.ceil(len(player.queue) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue_list = ''

        for i, track in enumerate(player.queue[start:end], start=start):
            queue_list += f'`{i + 1}.` [**{track.title}**]({track.uri})\n'

        embed = discord.Embed(colour=ctx.guild.me.top_role.colour,
                              description=f'**{len(player.queue)} tracks**\n\n{queue_list}')
        embed.set_footer(text=f'Viewing page {page}/{pages}')
        await ctx.send(embed=embed)

    @commands.command(aliases=['resume'])
    async def pause(self, ctx):
        '''Pause the song if you're annoyed of me :<'''
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send('Not playing.')

        if player.paused:
            await player.set_pause(False)
            await ctx.send('⏯ | Resumed! c:')
        else:
            await player.set_pause(True)
            await ctx.send('⏯ | P-paused!')

    @commands.command(aliases=['vol'])
    async def volume(self, ctx, volume: int=None):
        '''Changes player volume, duh'''
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not volume:
            return await ctx.send(f'T-the current volume is {player.volume}%, you should know that already >~<')

        await player.set_volume(volume)
        await ctx.send(f'I-I set the volume to {player.volume}%')

    @commands.command()
    async def shuffle(self, ctx):
        '''Shuffles the queue, in case you like surprises...'''
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send('Nothing playing.')

        player.shuffle = not player.shuffle

        await ctx.send('🔀 | N-now ' + ('shuffling' if player.shuffle else 'unshuffling')) + ' the queue'

    @commands.command(aliases=['loopqueue'])
    async def loop(self, ctx):
        '''Loops the queue, baka'''
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send('Nothing playing.')

        player.repeat = not player.repeat

        await ctx.send('🔁 | ' + ('Looping' if player.repeat else 'Not looping') + ' the queue! :>')

    @commands.command()
    async def remove(self, ctx, index: int):
        '''Removes a track from the queue!'''
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.queue:
            return await ctx.send('Nothing queued.')

        if index > len(player.queue) or index < 1:
            return await ctx.send('Index can\'t be less than 1 and greater than queue size, baka')

        index = index - 1
        removed = player.queue.pop(index)

        await ctx.send('Removed **' + removed.title + '** from the queue... W-what now?')

    @commands.command()
    async def find(self, ctx, *, query):
        '''Searches for a song by name'''
        if not query.startswith('ytsearch:') and not query.startswith('scsearch:'):
            query = 'ytsearch:' + query

        tracks = await self.bot.lavalink.get_tracks(query)

        if not tracks:
            return await ctx.send('Nothing found uwu')

        tracks = tracks[:10]  # First 10 results

        o = ''
        for i, t in enumerate(tracks, start=1):
            o += f'`{i}.` [{t["info"]["title"]}]({t["info"]["uri"]})\n'

        embed = discord.Embed(colour=ctx.guild.me.top_role.colour,
                              description=o)

        await ctx.send(embed=embed)

    @commands.command(aliases=['dc'])
    async def disconnect(self, ctx):
        '''L-leaves the voice channel'''
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.is_connected:
            return await ctx.send('Not connected, you baka~')

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            return await ctx.send('Y-you\'re not in my voice channel! J-join it first ;-;')

        await player.disconnect()
        await ctx.send('*⃣ | Disconnected... What did I do this time?')


def setup(bot):
    bot.add_cog(Music(bot))
