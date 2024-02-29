async def is_bot_playing():
    # Retrieve the current playback state from Spotify
    current_playback = spotify.current_playback()

    # Check if the playback state exists and if the bot is currently playing
    if current_playback is not None and current_playback["is_playing"]:
        return True
    else:
        return False


async def clear_queue():
    pass
