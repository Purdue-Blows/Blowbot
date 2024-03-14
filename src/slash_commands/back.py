import traceback
from models.songs import Song
from models.model_fields import PlaybackFields
from models.playlist import Playlist
from models.playback import Playback
from utils.constants import SERVERS, CurrentlyPlaying, Session, bot
from utils.messages import COULD_NOT_FIND_ERROR, GENERIC_ERROR, NO_GUILD_ERROR

from models.queue import Queue
from services.discord_service import play_song
from discord.ext import commands


BACK_NO_PREVIOUS_SONG_MESSAGE = "Could not go back to the previous song because there IS no previous song in the queue"
BACK_SUCCESS_MESSAGE = "Playing the previous song again at {ctx.author.name}'s request"


@bot.slash_command(
    name="back",
    description="Relisten to the previous song (if it exists)",
    guild_ids=SERVERS,
)
async def back(ctx) -> None:
    if ctx.guild is None:
        raise Exception(NO_GUILD_ERROR)
    with Session() as session:
        # update queue_num and current_song accordingly and the session
        try:
            currently_playing = await Playback.get_currently_playing(
                session, ctx.guild.id
            )
            if currently_playing == CurrentlyPlaying.PLAYLIST:
                current_playlist_name = await Playback.get_current_playlist(
                    session, ctx.guild.id
                )
                current_playlist_index = await Playback.get_current_playlist_index(
                    session, ctx.guild.id
                )
                song = await Playlist.get_previous_song(
                    session,
                    ctx.guild.id,
                    current_playlist_name,
                    current_playlist_index,
                )
                if song:
                    if song.audio:  # type: ignore
                        await play_song(bot, song.audio)  # type: ignore
                        await ctx.send(BACK_SUCCESS_MESSAGE)
                        return
            elif currently_playing == CurrentlyPlaying.QUEUE:
                song = await Queue.get_previous_song(
                    session,
                    guild_id=ctx.guild.id,
                )
                if song:
                    if song.audio:  # type: ignore
                        await play_song(bot, song.audio)  # type: ignore
                        await ctx.send(BACK_SUCCESS_MESSAGE)
                        return
            else:
                await ctx.respond(COULD_NOT_FIND_ERROR.format("song"), ephemeral=True)
                return
        except Exception as e:
            await ctx.respond(GENERIC_ERROR.format("back"), ephemeral=True)
            traceback.print_exc()
            return
