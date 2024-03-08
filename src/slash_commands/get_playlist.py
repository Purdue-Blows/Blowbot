from typing import List
from discord.ext import commands
from utils.constants import PURDUE_BLOWS_PLAYLISTS, SERVERS, bot


@bot.command(
    name="get_playlist",
    description="Returns links to Purdue Blows playlists",
    guild_ids=SERVERS,
)
async def get_playlist(ctx: commands.Context) -> None:
    # Returns the url of all the purdue blows playlists
    # As well as specifies the currently selected playlist
    message = ""
    for playlist in PURDUE_BLOWS_PLAYLISTS.items():
        message += playlist[0] + ": " + playlist[1]
        if currently_playing:  # How to check the currently playing playlist?
            # I would need to get the current song, find the playlist instance with that song,
            # and then check from there
            # How do I get the current song?
            message += " - Currently Playing"
        message += "\n"
    message[0:-1]  # Remove extra \n
    await ctx.send(message, ephemeral=True)
