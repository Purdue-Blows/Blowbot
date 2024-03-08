# TODO
- [] Finish implementing service helper functions
- [] Finish implementing main.py
- [] Finish adding and verifying static typing
- [] Test run, deploy on Wednesday


- [x] Install py-cord and use py-cord instead of discord
- [x] Copy and paste server id into constants.py; update imports
- [] Use spotipy to extract metadata
- [] Set up yt-dlp
- [] Integrate yt-dlp and the database
- [] Playlist related commands
  - [] Admin-specific functionality
- [] Badges & Roles (handled via discord; database doesn't contain ALL the info)

## HELPFUL
db.playlist.deleteMany({});
db.songs.deleteMany({});
db.playlist.find({}, { song_id: 1, played: 1, user_id: 1 })