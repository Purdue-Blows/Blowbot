from utils.constants import SERVERS
from bot import bot


@bot.slash_command(
    name="jazz_trivia",
    description="Get a jazz trivia question, see your jazz trivia stats",
    guild_ids=SERVERS,
)
async def jazz_trivia(ctx, arg):
    await ctx.respond(
        "Sorry, this command hasn't been implemented yet!", ephemeral=True
    )
