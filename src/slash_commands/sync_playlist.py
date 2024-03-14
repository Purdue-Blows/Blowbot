import traceback
import discord
from discord.ext import commands
from slash_commands.add_to_playlist import SUCCESS_MESSAGE
from utils.constants import SERVERS, PlaylistNames, Session, bot, ydl

# from utils.state import CURRENT_SONG
from models.songs import Song
from services.youtube_service import sync_playlist
from utils.messages import (
    ADMIN_ONLY_ERROR,
    GENERIC_ERROR,
    NO_GUILD_ERROR,
    NOT_IMPLEMENTED_ERROR,
)


CURRENT_SONG_MESSAGE = "Blowbot is not currently playing anything"
SUCCESS_MESSAGE = "{name} synced the playlist!"


@bot.slash_command(
    name="sync_playlist",
    description="Syncs the playlist with the YT playlist if you are an admin, REMOVES RANDOMIZATION",
    guild_ids=SERVERS,
)
async def sync_playlist_command(
    ctx,
    playlist_name: discord.Option(
        str,
        choices=[PlaylistNames.value for PlaylistNames in PlaylistNames],
        description="The name of the playlist",
    ),  # type: ignore
) -> None:
    if ctx.guild is None:
        raise Exception(NO_GUILD_ERROR)
    with Session() as session:
        try:
            if discord_service.is_admin(ctx.author):  # type: ignore
                if playlist_name in PlaylistNames:
                    await sync_playlist(
                        session,
                        ctx.guild.id,
                        ydl,
                        PlaylistNames.from_string(playlist_name.value),
                    )
                    await ctx.send(SUCCESS_MESSAGE.format(name=ctx.author.name))
            else:
                await ctx.respond(ADMIN_ONLY_ERROR.format("sync_playlist"))
        except Exception as e:
            await ctx.respond(GENERIC_ERROR.format("sync_playlist"))
            traceback.print_exc()
