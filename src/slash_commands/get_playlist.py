import traceback
from typing import List
from discord.ext import commands
from models.playback import Playback
from utils.constants import PURDUE_BLOWS_PLAYLISTS, SERVERS, Session, bot
from utils.messages import GENERIC_ERROR, NO_GUILD_ERROR


@bot.slash_command(
    name="get_playlist",
    description="Returns links to Purdue Blows playlists",
    guild_ids=SERVERS,
)
async def get_playlist(ctx) -> None:
    print("THIS COMMAND CALLS")
    print(ctx.guild)
    if ctx.guild is None:
        raise Exception(NO_GUILD_ERROR)
    with Session() as session:
        # Returns the url of all the purdue blows playlists
        # As well as specifies the currently selected playlist
        try:
            currently_playing = await Playback.get_currently_playing(
                session, ctx.guild.id
            )
            message = ""
            for playlist in PURDUE_BLOWS_PLAYLISTS.items():
                message += playlist[0].name + ": " + playlist[1]
                if currently_playing:
                    # I would need to get the current song, find the playlist instance with that song,
                    # and then check from there
                    # How do I get the current song?
                    message += " - Currently Playing :notes:"
                message += "\n"
            message = message[:-1]  # Remove extra \n
            await ctx.respond(message, ephemeral=True)
        except Exception as e:
            await ctx.respond(GENERIC_ERROR.format("get_playlist"), ephemeral=True)
            traceback.print_exc()
