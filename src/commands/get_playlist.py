from utils.constants import SERVERS
from bot import bot


@bot.slash_command(
    name="get_playlist",
    description="Returns a link to the Purdue Blows playlist",
    guild_ids=SERVERS,
)
async def get_playlist(ctx):
    return
