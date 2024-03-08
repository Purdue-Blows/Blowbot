# Blowbot
The official Purdue Blows Discord Bot! 
- Built by Purdue Jazz for Purdue Jazz!
- Utilizes: 
  - Pycord API: https://docs.pycord.dev/en/stable/ext/commands/api.html#discord.ext.commands.Bot
  - Spotipy API: https://spotipy.readthedocs.io/en/2.22.1/
  - Yt-dlp API: https://github.com/yt-dlp/yt-dlp/blob/c54ddfba0f7d68034339426223d75373c5fc86df/yt_dlp/YoutubeDL.py#L457
## Commands
To view a list of commands, run "/help"

## Running
> NOTE: the following commands a for a Linux environment. On other environments, the commands may differ slightly
To set up your environment, run the following command sequence:
```python -m venv venv```
```source venv/bin/activate```
To run the bot, run the following command:
```python src/main.py```
Note that you will need access to the .env file in order to run Blowbot
Also note that the database is locally hosted. If you want to create test data yourself though, you can install mongod on your system from and run the following commands:
```mongod```
```mongosh``` // In a different terminal
To run the tests, run the following command:
```python -m unittest```