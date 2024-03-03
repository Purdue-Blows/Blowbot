from typing import List
from discord.ext import commands
from utils.constants import SERVERS, PURDUE_BLOWS_PLAYLIST_URL, bot


@bot.slash_command(
    name="get_playlist",
    description="Returns a link to the Purdue Blows playlist",
    guild_ids=SERVERS,
)
async def get_playlist(ctx: commands.Context) -> None:
    await ctx.respond(PURDUE_BLOWS_PLAYLIST_URL, ephemeral=True)
