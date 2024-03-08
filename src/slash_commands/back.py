from models.songs import Song
from models.model_fields import PlaybackFields
from models.playlist import Playlist
from src.models.playback import Playback
from utils.constants import DB_CLIENT, SERVERS, CurrentlyPlaying, bot
from models.queue import Queue
from discord_service import play_song
from discord.ext import commands


BACK_NO_PREVIOUS_SONG_MESSAGE = "Could not go back to the previous song because there IS no previous song in the queue"
BACK_SUCCESS_MESSAGE = "Playing the previous song again at {ctx.author.name}'s request"
COULD_NOT_FIND_SONG = "There was an error finding the previous song"
NO_GUILD_MESSAGE = "You must be in a guild to use blowbot"
GENERIC_ERROR = "There was an error trying to go back"


@bot.command(
    name="back",
    description="Relisten to the previous song (if it exists)",
    guild_ids=SERVERS,
)
async def back(ctx: commands.Context) -> None:
    if ctx.guild is None:
        raise Exception(NO_GUILD_MESSAGE)
    db = DB_CLIENT[str(ctx.guild.id)]
    # update queue_num and current_song accordingly and the db
    try:
        currently_playing = await Playback.get_currently_playing(db)
        if currently_playing == CurrentlyPlaying.PLAYLIST:
            song = await Playlist.get_previous_song(db)
            if song:
                if song.audio:
                    await play_song(bot, song.audio)
                    await ctx.send(BACK_SUCCESS_MESSAGE)
                    return
        elif currently_playing == CurrentlyPlaying.QUEUE:
            song = await Queue.get_previous_song(db)
            if song:
                if song.audio:
                    await play_song(bot, song.audio)
                    await ctx.send(BACK_SUCCESS_MESSAGE)
                    return
        else:
            await ctx.send(COULD_NOT_FIND_SONG)
            return
    except Exception as e:
        await ctx.send(GENERIC_ERROR, ephemeral=True)
        return
