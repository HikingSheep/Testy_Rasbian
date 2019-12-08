# Testy

A telegram bot, running on Raspberry Pi (Rasbian Burst).



Available commands:

/help - request a list of commands 

#Youtube

/yt + URL/keywords - play a song from youtube
/yt_playlist + URL [under_dev] - play a playlist from youtube

#Spotify

/sp + keywords [under_dev] - find a track on spotify
/sp_playlist + keywords - find a playlist on spotify

#Playback

/play + URL - play audio from any website/link
/pasue - pause audio playback
/cont - continue audio playback
/stop - stop audio playback

#Volume

/volume + INT (e.g. 50 = 50%) - change volume to INT
/cur_volume - get current volume

#DuckDuckGo

/q + query - search for something online

#File System

/ls - list available file system directories
/ls + available folder name - list files in the specified folder
/dw + /location(folder name)/file name - download specified file


######

**/play function was tested only on youtube, vk, vimeo
Since Spotfiy has a lot of restrictions, it allows playback only through certified applications and Web Player

***Drop images, video or documents in chat to upload them to the host machine. Can be viewed through /ls command after they are uploaded
