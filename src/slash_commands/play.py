import traceback
from typing import Any, Optional
import discord
from discord.ext import commands
from models.playlist import Playlist
from models.playback import Playback
from utils.constants import SERVERS, CurrentlyPlaying, PlaylistNames, Session, bot
from services import discord_service
from utils.messages import GENERIC_ERROR, MORE_DATA_ERROR, NO_GUILD_ERROR


SUCCESS_MESSAGE = "Blowbot was resumed by {name}"


@bot.slash_command(
    name="play",
    description="Attempt to start or resume blowbot playback",
    guild_ids=SERVERS,
)
async def play(
    ctx,
    playlist_name: discord.Option(
        str,
        choices=[PlaylistNames.value for PlaylistNames in PlaylistNames],
        description="The name of the playlist",
        required=False,
    ),  # type: ignore
) -> Any:
    if ctx.guild is None:
        raise Exception(NO_GUILD_ERROR)
    with Session() as session:
        # play the current song
        try:
            print("Retrieving song from playlist")
            song = await Playlist.get_current_song(session, ctx.guild.id)
            if song:
                if song.audio:  # type: ignore
                    await discord_service.play_song(bot, song.audio)  # type: ignore
                    # return a success message as confirmation
                    await ctx.respond(
                        SUCCESS_MESSAGE.format(name=ctx.author.name), ephemeral=True
                    )
                    return
            else:
                # Assume starting
                if not playlist_name:
                    await ctx.respond(
                        MORE_DATA_ERROR.format("playlist_name"), ephemeral=True
                    )
                    return
                if playlist_name not in PlaylistNames:
                    await ctx.respond(
                        MORE_DATA_ERROR.format("playlist_name"), ephemeral=True
                    )
                    return
                await Playback.add(
                    session=session,
                    guild_id=ctx.guild.id,
                    current_playlist=playlist_name,
                    currently_playing=CurrentlyPlaying.PLAYLIST,
                )
                await ctx.send(SUCCESS_MESSAGE.format(name=ctx.author.name))
                return
            await ctx.respond(GENERIC_ERROR.format("play"), ephemeral=True)
        except Exception as e:
            try:
                print("Attempting to retrieve playback")
                current_playlist = await Playback.get_current_playlist(
                    session, ctx.guild.id
                )
            except Exception as e:
                print(str(e))
                # If there isn't a current playlist, create a new one
                print("Adding new playback")
                await Playback.add(
                    session=session,
                    guild_id=ctx.guild.id,
                    current_playlist=playlist_name,
                    currently_playing=CurrentlyPlaying.PLAYLIST,
                )
            try:
                print("Retrieving song from playlist 2")
                song = await Playlist.get_current_song(session, ctx.guild.id)
                if song:
                    if song.audio:  # type: ignore
                        await discord_service.play_song(bot, song.audio)  # type: ignore
                        # return a success message as confirmation
                        await ctx.respond(
                            SUCCESS_MESSAGE.format(name=ctx.author.name), ephemeral=True
                        )
                        return
                else:
                    # Assume starting
                    if not playlist_name:
                        await ctx.respond(
                            MORE_DATA_ERROR.format("playlist_name"), ephemeral=True
                        )
                        return
                    if playlist_name not in PlaylistNames:
                        await ctx.respond(
                            MORE_DATA_ERROR.format("playlist_name"), ephemeral=True
                        )
                        return
                    await Playback.add(
                        session=session,
                        guild_id=ctx.guild.id,
                        current_playlist=playlist_name,
                        currently_playing=CurrentlyPlaying.PLAYLIST,
                    )
                    await ctx.send(SUCCESS_MESSAGE.format(name=ctx.author.name))
                    return
                await ctx.respond(GENERIC_ERROR.format("play"), ephemeral=True)
            except Exception as e:
                await ctx.respond(GENERIC_ERROR.format("play"), ephemeral=True)
                traceback.print_exc()
                return
