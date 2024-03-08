from sre_constants import SUCCESS
import discord_service
from models.queue import Queue
from discord_service import pause, play_song
from src.models.playback import Playback
from src.models.playlist import Playlist
from utils.constants import DB_CLIENT, SERVERS, CurrentlyPlaying, bot
from discord.ext import commands


# Define constants for response messages
NO_NEXT_SONG_MESSAGE = (
    "Could not skip to the next song because there IS no next song in the queue"
)
PLAYING_PREVIOUS_SONG_MESSAGE = (
    "Playing the previous song again at {ctx.author.name}'s request"
)
GENERIC_ERROR = "Sorry, an error occurred while trying to skip the song"
NO_GUILD_MESSAGE = "You must be in a guild to use blowbot"
SUCCESS_MESSAGE = "Song skipped successfully"


@bot.command(
    name="skip",
    description="Skip the current song",
    guild_ids=SERVERS,
)
async def skip(ctx: commands.Context):
    if ctx.guild is None:
        raise Exception(NO_GUILD_MESSAGE)
    db = DB_CLIENT[str(ctx.guild.id)]
    try:
        # Pause the current song
        await discord_service.pause(bot)
        # Determine whether the queue or playlist is playing
        currently_playing: CurrentlyPlaying = await Playback.get_currently_playing(db)
        if currently_playing == CurrentlyPlaying.QUEUE:
            # If the queue is playing, skip to the next song
            song = await Queue.get_next_song(db)
            if song:
                if song.audio:
                    await discord_service.play_song(bot, song.audio)
                    await ctx.send(SUCCESS_MESSAGE, ephemeral=True)
                    return
        elif currently_playing == CurrentlyPlaying.PLAYLIST:
            # If the playlist is playing, skip to the next song
            song = await Playlist.get_next_song(db)
            if song:
                if song.audio:
                    await discord_service.play_song(bot, song.audio)
                    await ctx.send(SUCCESS_MESSAGE, ephemeral=True)
                    return
        else:
            await ctx.send(GENERIC_ERROR, ephemeral=True)
    except Exception as e:
        await ctx.send(GENERIC_ERROR, ephemeral=True)
