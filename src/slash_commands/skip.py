import traceback
from models.queue import Queue
from services.discord_service import pause, play_song
from models.playback import Playback
from models.playlist import Playlist
from utils.constants import SERVERS, CurrentlyPlaying, Session, bot
from discord.ext import commands
from utils.messages import GENERIC_ERROR, NO_GUILD_ERROR


# Define constants for response messages
NO_NEXT_SONG_MESSAGE = (
    "Could not skip to the next song because there IS no next song in the queue"
)
PLAYING_PREVIOUS_SONG_MESSAGE = "Playing the previous song again at {}'s request"
SUCCESS_MESSAGE = "{name} skipped to next song in {currently_playing}"


@bot.slash_command(
    name="skip",
    description="Skip the current song",
    guild_ids=SERVERS,
)
async def skip(ctx):
    if ctx.guild is None:
        raise Exception(NO_GUILD_ERROR)
    with Session() as session:
        try:
            # Pause the current song
            await pause(bot)
            # Determine whether the queue or playlist is playing
            currently_playing: CurrentlyPlaying = await Playback.get_currently_playing(
                session, ctx.guild.id
            )
            if currently_playing == CurrentlyPlaying.QUEUE:
                # If the queue is playing, skip to the next song
                song = await Queue.get_next_song(session, ctx.guild.id)
                if song:
                    if song.audio:  # type: ignore
                        await discord_service.play_song(bot, song.audio)  # type: ignore
                        await ctx.send(
                            SUCCESS_MESSAGE.format(
                                name=ctx.author.name, currently_playing="queue"
                            )
                        )
                        return
            elif currently_playing == CurrentlyPlaying.PLAYLIST:
                # If the playlist is playing, skip to the next song
                song = await Playlist.get_next_song(session, ctx.guild.id)
                if song:
                    if song.audio:  # type: ignore
                        await discord_service.play_song(bot, song.audio)  # type: ignore
                        await ctx.send(
                            SUCCESS_MESSAGE.format(
                                name=ctx.author.name, currently_playing="playlist"
                            )
                        )
                        return
            else:
                await ctx.respond(GENERIC_ERROR.format("skip"), ephemeral=True)
        except Exception as e:
            await ctx.respond(GENERIC_ERROR.format("skip"), ephemeral=True)
            traceback.print_exc()
