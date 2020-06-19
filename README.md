# Testy

A telegram bot, running on Raspberry Pi (Raspbian Pi OS).
[http://www.theatticproject.co.uk](http://www.theatticproject.co.uk)



## Available commands:

```/help``` - request a list of commands 

```/hi``` - say "Hi!" to the bot

```/git``` - request a git repository link

```/cmd + command``` - allows to perform a terminal command on the host machine (!DANGEROUS!) ```(admin only)```

### Youtube

```/yt + URL/keywords``` - play a song from youtube

```/yt_last``` - play last song

```/yt_playlist + URL``` - download and play a playlist from youtube

```/yt_last_playlist``` - fetch last played playlist from local storage

```/yt_local + URL/keywords``` - play a song from youtube and add it to local playlist

```/yt_playlist_int_cur``` - range of tracks, that are being downloaded from YT playlist (defauld 1-15 = first 15 tracks)

```/yt_playlist_int_set + RANGE``` - change the range of tracks to RANGE (e.g. 1-5 = first 5 tracks), that are being downloaded from YT playlist (defauld 1-15 = first 15 tracks)

### Local playlist 

```/local``` - play local playlist

```/local_view``` - view local playlist tracks

```/local_edit + track name``` - remove a track from playlist

```/local_purge``` - delete local playlist contents

### Spotify

```/sp + keywords``` - find a track on spotify

```/sp_playlist + keywords``` - find a playlist on spotify

### Playback

```/play + URL``` - play audio from website/link

```/play_video + URL``` - play video from website/link

```/pasue``` - pause audio playback

```/cont``` - continue audio playback

```/stop``` - stop audio playback

>_```/play``` function was tested only on youtube, vk, vimeo._

>_Since Spotfiy has a lot of restrictions, it allows playback only through certified applications and Web Player_

### Volume

```/volume + INT (e.g. 50 = 50%)``` - change volume to INT

```/cur_volume``` - get current volume

### DuckDuckGo

```/q + query``` - search for something online

### IMDb

```/imdb + movie name``` - search for movie on IMDb

### Weather

```/w + city name``` - show current weather and additional relevant information 

### File System

```/ls``` - list available file system directories

```/ls + available folder name``` - list files in the specified folder

```/dw + /location(folder name)/file name``` - download specified file

```/file_rename + /location/file name(space)new name``` - rename specified file

```/file_delete + /location/file name``` - delete local file

>_File system includes folders that are not visible through ```/ls``` command, however, if the folder name is known, it can be opened (currently available hidden folders: .bot_media, .playlist, .local_playlist, .track). Therefore, these files can be downloaded manually ^_^_

>_Drop images, video or documents in chat to upload them to the host machine. Can be viewed through ```/ls``` command after they are uploaded_

### Authentication

```/admin_help``` - list of admin/authentication commands

```/getID``` - get your telegram ID

```/auth``` - check if registered

```/req + code``` - request access

```/req_code``` - get a code for your access level to share with unregistered user 

```/del_user + id``` - delete user from DB ```(admin only)```

```/update_user + id/access level + old value + new value``` - update users id or access level ```(admin only)```

```/update_code + old value + new value``` - change a specified code ```(admin only)```

```/view_users``` - list all users ```(admin only)```

```/view_codes``` - list all codes ```(admin only)```

>_Every registered user has an id and an access level {id : access level}. Access level is used to determain if the user has enough privelegies to use specific functions._

>_If the user is not registered, they are unable to interact with a bot, with an exception of a few simple commands (help, echo, git). Unregistered users can also request access (register), if they received a code of any access level from registered user._

>_There is a total of 3 different codes/access levels: 0 - admin, 1 - normal user, 2 - is for external users, who don't need access to host machine (e.g. they can use spotify api, but not youtube (play music on the device) {tbr later}). Admin can change access levels for users. Every user can request a code for new users, but they will receive a code only for their own access level._

## Requirements:

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [youtube-dl (latest)](http://ytdl-org.github.io/youtube-dl/download.html)
- [spotipy](https://github.com/plamere/spotipy)
- [DuckDuckGo2](https://pypi.org/project/DuckDuckGo-Python3-Library/)
- [IMDbpy](https://github.com/alberanid/imdbpy)
- [Weather](https://openweathermap.org/api)
- [Strava](https://developers.strava.com/docs/reference/) - to be added
- pymongo + dnspython
- mpv
- pulseaudio
