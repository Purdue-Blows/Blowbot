import traceback
from typing import Any
from discord.ext import commands
from models.playback import Playback
from models.playlist import Playlist
from utils.constants import SERVERS, Session, bot
from services import discord_service
from utils.messages import GENERIC_ERROR, NO_GUILD_ERROR


PAUSE_MESSAGE = "Blowbot was paused by {ctx.author.name}"


@bot.slash_command(
    name="pause",
    description="Pause Blowbot",
    guild_ids=SERVERS,
)
async def pause(ctx) -> Any:
    if ctx.guild is None:
        raise Exception(NO_GUILD_ERROR)
    with Session() as session:
        try:
            # pause the current song
            await discord_service.pause(bot)
            # return a success message as confirmation
            await ctx.send(PAUSE_MESSAGE.format(ctx=ctx))
            return
        except Exception:
            await ctx.respond(GENERIC_ERROR.format("pause"), ephemeral=True)
            traceback.print_exc()
            return
