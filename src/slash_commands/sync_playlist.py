from typing import List
from discord import VoiceClient
from discord.ext import commands
from utils.constants import DB_CLIENT, SERVERS, bot

# from utils.state import CURRENT_SONG
from models.songs import Song

CURRENT_SONG_MESSAGE = "Blowbot is not currently playing anything"
NO_GUILD_MESSAGE = "You must be in a guild to use blowbot"


@bot.command(
    name="sync_playlist",
    description="Syncs the playlist with the YT playlist if you are an admin, REMOVES RANDOMIZATION",
    guild_ids=SERVERS,
)
async def sync_playlist_command(ctx: commands.Context) -> None:
    if ctx.guild is None:
        raise Exception(NO_GUILD_MESSAGE)
    db = DB_CLIENT[str(ctx.guild.id)]
    # Retrieve the bots current song
    voice_client = ctx.voice_client
    if isinstance(voice_client, VoiceClient):
        if voice_client and voice_client.is_playing():
            await ctx.send(Song.format_song(voice_client.source), ephemeral=True)
        else:
            await ctx.send(CURRENT_SONG_MESSAGE, ephemeral=True)
        return
