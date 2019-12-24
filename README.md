# Testy

A telegram bot, running on Raspberry Pi (Rasbian Burst).



## Available commands:

```/help``` - request a list of commands 

```/hi``` - say "Hi!" to the bot

```/cmd + command``` - allows to perform a terminal command on the local machine (!DANGEROUS!)

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

### File System

```/ls``` - list available file system directories

```/ls + available folder name``` - list files in the specified folder

```/dw + /location(folder name)/file name``` - download specified file

>_File system includes folders that are not visible through ```/ls``` command, however, if the folder name is knonw, it can be opened (currently available hidden folders: .bot_media, .playlist, .local_playlist, .track). Therefore, these files can be downloaded manually ^_^_

>_Drop images, video or documents in chat to upload them to the host machine. Can be viewed through ```/ls``` command after they are uploaded_

## Requirements:

- python-telegram-bot
- youtube-dl (latest)
- spotipy
- DuckDuckGo2
- IMDbpy
- mpv
