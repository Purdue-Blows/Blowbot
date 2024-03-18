# Refresh credentials for connecting the bot to the YT channel; admin only, requires access to the YT channel account
import webbrowser
from utils.constants import SERVERS, bot, yt, yt_oauth_authorize_url
from utils.messages import GENERIC_ERROR, NO_GUILD_ERROR

NO_CREDENTIALS_WARNING = """If you want to update bot credentials, use this command again but pass the redirect_url and code as parameters"""
INVALID_PARAMETERS = "Could not create a refresh token with those values"
REFRESH_ERROR = "Could not refresh the access token"


@bot.slash_command(
    name="connect_to_yt",
    description="Refreshes or creates credentials for blowbot to connect to yt",
    guild_ids=SERVERS,
)
async def connect_to_yt(
    ctx, authorization_response: str | None, code: str | None
) -> None:
    if ctx.guild is None:
        raise Exception(NO_GUILD_ERROR)
    if not yt.refresh_token:
        if authorization_response == None or code == None:
            webbrowser.open(yt_oauth_authorize_url[0])
            await ctx.respond(NO_CREDENTIALS_WARNING, ephemeral=True)
            return
        try:
            yt.generate_access_token(
                authorization_response=authorization_response, code=code
            )
            if yt.access_token == None or yt.refresh_token == None:
                await ctx.respond(INVALID_PARAMETERS, ephemeral=True)
                return
        except Exception as e:
            print(str(e))
            await ctx.respond(GENERIC_ERROR.format("connect_to_yt"), ephemeral=True)
            return
    else:
        # If the refresh token exists, generate a new access token
        try:
            yt.refresh_access_token(refresh_token=yt.refresh_token)
            if yt.access_token == None:
                await ctx.respond(REFRESH_ERROR, ephemeral=True)
                return
        except Exception as e:
            print(str(e))
            await ctx.respond(GENERIC_ERROR.format("connect_to_yt"), ephemeral=True)
            return
