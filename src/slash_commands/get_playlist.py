from typing import List
from discord.ext import commands
from models.playback import Playback
from utils.constants import DB_CLIENT, PURDUE_BLOWS_PLAYLISTS, SERVERS, bot

NO_GUILD_MESSAGE = "You must be in a guild to use blowbot"
GENERIC_ERROR = "There was an error trying to get the playlist"


@bot.command(
    name="get_playlist",
    description="Returns links to Purdue Blows playlists",
    guild_ids=SERVERS,
)
async def get_playlist(ctx: commands.Context) -> None:
    if ctx.guild is None:
        raise Exception(NO_GUILD_MESSAGE)
    db = DB_CLIENT[str(ctx.guild.id)]
    # Returns the url of all the purdue blows playlists
    # As well as specifies the currently selected playlist
    try:
        currently_playing = await Playback.get_currently_playing(db)
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
        await ctx.send(message, ephemeral=True)
    except Exception as e:
        await ctx.send(GENERIC_ERROR, ephemeral=True)
