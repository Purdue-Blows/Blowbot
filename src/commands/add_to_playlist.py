from utils.constants import SERVERS
from bot import bot


@bot.slash_command(
    name="add_to_playlist",
    description="Adds a link to the Purdue Blows playlist",
    guild_ids=SERVERS,
)
async def add_to_playlist(ctx, arg):
    return
