# TODO
- [] Rework database to utilize new Enum type
- [] Scaffold desired commands
- [] Organize codebase


- [] Add Purdue Plays challenge and purdue plays submission tables to db/add Purdue Plays challenge and Purdue Plays Submission models
- [] create purdue plays
- [] get purdue plays
- [] upload purdue plays
- [] download purdue plays
- [] Add a potential note about refining/redesigning the creation, update, etc for purdue plays to make it more applicable to other scenarios such as albums; too big of a move for now, so I'll just implement how I think I should implement it
  - One thing I need to consider here is the full-stack process of making a jazz arrangement...
    - Arrangers
    - Performers
    - Editors
  - Roles make this even more powerful because then we can find people to perform; I think I'm going to outline this independently from Purdue Plays for simplicities sake


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