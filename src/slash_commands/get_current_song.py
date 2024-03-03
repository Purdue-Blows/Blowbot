from typing import List
from discord.ext import commands
from utils.constants import SERVERS, bot
from utils.state import CURRENT_SONG
from models.songs import Song


@bot.slash_command(
    name="get_current_song",
    description="Get the song that Blowbot is currently playing",
    guild_ids=SERVERS,
)
async def get_current_song(ctx: commands.Context) -> None:
    if CURRENT_SONG is not None:
        await ctx.respond(Song.format_song(CURRENT_SONG.song), ephemeral=True)
    else:
        await ctx.respond("Blowbot is not currently playing anything", ephemeral=True)
    return
