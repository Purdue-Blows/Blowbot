from utils.constants import SERVERS
from bot import bot


@bot.slash_command(
    name="get_current_song",
    description="Get the song that Blowbot is currently playing",
    guild_ids=SERVERS,
)
async def get_current_song(ctx):
    return
