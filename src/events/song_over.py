import random
from models.playlist import Playlist
from models.queue import Queue
from services.discord_service import play_song
from models.playback import Playback
from utils.messages import COULD_NOT_FIND_ERROR
from utils.constants import Session, bot
from discord.ext import commands

END_OF_PLAYLIST = ":confetti_ball: The entire playlist has been listened to! It will now repeat! :confetti_ball:"


# Custom on_track_end event
@bot.listen()
async def on_track_end(member, before, after):
    print("on_track_end")
    if member.bot and before.channel and not after.channel:
        # Bot has stopped playing audio
        await on_song_over(member.guild)


async def on_song_over(guild) -> None:
    print("on_song_over")
    with Session() as session:
        try:
            playback = await Playback.retrieve_one(session, guild.id)
            if playback is None:
                raise Exception(COULD_NOT_FIND_ERROR.format("playback instance"))
            queue = await Queue.retrieve_one(session, guild.id)
            playlist = await Playlist.retrieve_one(
                session,
                id=playback.current_playlist_index,  # type: ignore
                playlist_name=playback.current_playlist,  # type: ignore
            )
            if playlist is None:
                raise Exception(
                    COULD_NOT_FIND_ERROR.format(
                        f"playlist at index {playback.current_playlist_index}"
                    )
                )
            # Update the values
            playlist.played = True  # type: ignore
            playback.current_playlist_index += 1  # type: ignore
            session.commit()
            # Retrieve new playlist instance
            song = await Playlist.get_next_song(session, playlist.guild_id)
            if song is None:
                await guild.text_channels[0].send(END_OF_PLAYLIST)
                # Reset the playlist, but don't play a new song
                await Playlist.reset_playlist(session, playlist_name=playback.current_playlist)  # type: ignore
                return
            if song.audio is not None:
                # Play new song
                await play_song(bot, song.audio)  # type: ignore
            else:
                raise Exception(COULD_NOT_FIND_ERROR.format("song"))
        except Exception as e:
            session.rollback()
            raise e
