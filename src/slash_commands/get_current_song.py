from typing import List
from discord.ext import commands
from utils.constants import SERVERS, bot
from utils.state import CURRENT_SONG
from models.songs import Song

CURRENT_SONG_MESSAGE = "Blowbot is not currently playing anything"


@bot.slash_command(
    name="get_current_song",
    description="Get the song that Blowbot is currently playing",
    guild_ids=SERVERS,
)
async def get_current_song(ctx: commands.Context) -> None:
    if CURRENT_SONG is not None:
        await ctx.respond(Song.format_song(CURRENT_SONG.song), ephemeral=True)
    else:
        await ctx.respond(CURRENT_SONG_MESSAGE, ephemeral=True)
    return
