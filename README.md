# Blowbot
The official Purdue Blows Discord Bot! 
- Built by Purdue Jazz for Purdue Jazz!
- Utilizes: 
  - Pycord API: https://docs.pycord.dev/en/stable/ext/commands/api.html#discord.ext.commands.Bot
  - Spotipy API: https://spotipy.readthedocs.io/en/2.22.1/
  - Yt-dlp API: https://github.com/yt-dlp/yt-dlp/blob/c54ddfba0f7d68034339426223d75373c5fc86df/yt_dlp/YoutubeDL.py#L457
  - Gemini API: https://ai.google.dev/
  - Youtube API: https://developers.google.com/youtube/v3/docs
 
## Overview
A quick overview of important directories and files in the repository:
```
blowbot/
│
├── src/ -> Directory containing all the code
│   ├── events/ -> Directory containing various bot events
│   ├── models/ -> DB models, CRUD utility methods
│   ├── services/ -> Services and APIs
│   ├── slash_commands/ -> Slash commands
│   ├── utils/ -> Additional utilities
|       └── constants.py -> Loads .env data, initializes database and API services, declares other global constants 
│   └── main.py -> Entry point that imports and registers events, commands, etc; run the bot via `python src/main.py`
│
├── tests/ -> Directory for test cases; mirrors the src/ directory structure
├── blowbot.db -> Postgresql database used for the bot; NOT IN SOURCE CONTROL
├── .env -> File with important env variables; NOT IN SOURCE CONTROL
│
└── requirements.txt -> Dependencies that can be installed via `pip install -r requirements.txt` 
```

## Models
A combination of sqlalchemy (a Python database toolkit; https://www.sqlalchemy.org/) and psycopg (the Python driver for PostgreSQL; https://www.psycopg.org/) is used for the database support. If you want to run the bot standalone, you'll need to install the requirements.txt, as well as PostgreSQL on your system (check out https://www.postgresql.org/download/ for more information). If you want to interface with your local test database, check out the `psql` command: https://www.postgresguide.com/utilities/psql/. Note that blowbot.db is not in source control, so a local version of the database will be created on your local bot instance. The database has tables that follow the models:
- Playback: guild-specific, contains info about the current state of the bots playback
- Playlist: references a song, a particular playlist, and a particular position in that playlist among other things 
- Queue: similar structure to playlist, each guild has a queue that takes precedence over the playlist in playback
- Users: contains user information used in the `/profile` command
- Songs: global to all guilds that use the bot

## Commands
To view a list of commands and their descriptions, run "/help" while the bot is live. For more information, take a look at `src/slash_commands`

## Running
> NOTE: currently, a test key and setup for the bot has yet to be created. Development will be a lot easier once test instances can be deployed locally, but for more progress on this take a look at https://github.com/xanmankey/Blowbot/issues/7#issue-2185212111

> The following commands are for a Linux environment. On other environments, the commands may differ slightly
To set up your environment, run the following command sequence:

```python -m venv venv```

```source venv/bin/activate```

> To run the bot, run the following command:

```python src/main.py```

## Test Cases
Currently not implemented, but an issue for this has been opened up at https://github.com/xanmankey/Blowbot/issues/2#issue-2184388219
