from typing import Any
from discord.ext import commands
from src.models.playlist import Playlist
from utils.constants import DB_CLIENT, SERVERS, bot
from services import discord_service


SUCCESS_MESSAGE = "Blowbot was resumed by {ctx.author.name}"
NO_GUILD_MESSAGE = "You must be in a guild to use blowbot"
RESUME_ERROR_MESSAGE = "An error occurred while trying to resume the current song"
GENERIC_ERROR = "There was an error trying to play"


@bot.command(
    name="play",
    description="Attempt to resume blowbot playback",
    guild_ids=SERVERS,
)
async def play(ctx: commands.Context) -> Any:
    if ctx.guild is None:
        raise Exception(NO_GUILD_MESSAGE)
    db = DB_CLIENT[str(ctx.guild.id)]
    # play the current song
    try:
        song = await Playlist.get_current_song(db)
        if song:
            if song.audio:
                await discord_service.play_song(bot, song.audio)
                # return a success message as confirmation
                await ctx.send(SUCCESS_MESSAGE, ephemeral=True)
                return
        await ctx.send(RESUME_ERROR_MESSAGE, ephemeral=True)
    except Exception as e:
        await ctx.send(GENERIC_ERROR, ephemeral=True)
        print(f"An error occurred: {str(e)}")
