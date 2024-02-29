# async def from_url(cls, url, *, loop=None, stream=False):
#     youtube_dl.utils.bug_reports_message = lambda: ""
#     ydl_opts = {
#         "format": "bestaudio/best",
#         "restrictfilenames": True,
#         "noplaylist": True,
#         "nocheckcertificate": True,
#         "ignoreerrors": False,
#         "logtostderr": False,
#         "quiet": True,
#         "no_warnings": True,
#         "default_search": "auto",
#         "source_address": "0.0.0.0",
#     }
#     ffmpeg_options = {
#         "options": "-vn",
#         "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
#     }
#     ytdl = youtube_dl.YoutubeDL(ydl_opts)
#     loop = loop or asyncio.get_event_loop()
#     data = await loop.run_in_executor(
#         None, lambda: ytdl.sanitize_info(ytdl.extract_info(url, download=not stream))
#     )
#     if "entries" in data:
#         # take first item from a youtube playlist
#         data = data["entries"][0]

#     filename = data["url"] if stream else ytdl.prepare_filename(data)
#     return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
