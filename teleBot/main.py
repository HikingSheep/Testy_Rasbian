#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import string
import duckduckgo
import pymongo

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from spotify import get_playlist, get_track
from imdb import IMDb
from weatherapi import GetWeather
myclient = pymongo.MongoClient("mongodb+srv://berlyozzy:****@cluster0-wnddk.mongodb.net/test?retryWrites=true&w=majority")

mydb = myclient["mydatabase"]
mycol = mydb["users"]
mycol2 = mydb["codes"]


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
ia = IMDb()

class saddness:
    vol = "50"
    temp = "/home/pi/Testy_Rasbian/teleBot"
    playlist_int = '1-15'

os.system('pulseaudio --start && amixer -D pulse sset Master 50% && aplay ' + saddness.temp + '/media/.bot_media/start.wav')


def start(update, context):
    os.system('aplay '+ saddness.temp + '/media/.bot_media/function.wav')
    update.message.reply_text('Hi, Meatbag!')

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help! \n \n'
+'/yt + URL/keywords - play a song from youtube \n'
+'/yt_last - play last song \n'
+'/yt_playlist + URL - download and play a playlist from youtube \n'
+'/yt_last_playlist - fetch last played playlist from local storage \n'
+'/yt_local + URL/keywords - play a song from youtube and add it to local playlist \n'
+'/yt_playlist_int_cur - range of tracks, that are being downloaded from YT playlist (defauld 1-15 = first 15 tracks) \n'
+'/yt_playlist_int_set + RANGE - change the range of tracks to RANGE (e.g. 1-5 = first 5 tracks), that are being downloaded from YT playlist (defauld 1-15 = first 15 tracks) \n \n'
+'/local - play local playlist \n'
+'/local_view - view local playlist tracks \n'
+'/local_edit + track name - remove a track from playlist \n'
+'/local_purge - delete local playlist contents \n \n'
+'/sp + keywords - find a track on spotify \n'
+'/sp_playlist + keywords - find a playlist on spotify \n \n'
+'/play + URL - play audio from website/link \n'
+'/play_video + URL - play video from website/link \n'
+'/pasue - pause audio playback \n'
+'/cont - continue audio playback \n'
+'/stop - stop audio playback \n \n'
+'/cur_volume - get current volume\n'
+'/volume + INT (e.g. 50 = 50%) - change volume to INT \n \n'
+'/q + query - search for something online \n'
+'/imdb + movie - search for movie on IMDb \n'
+'/git - request git repository link \n'
+'/cmd + command - allows to perform a terminal command on the local machine (!DANGEROUS!) \n \n'
+'/ls - list available file system directories \n'
+'/ls + available folder name - list files in the specified folder \n'
+'/dw + /location/file name - download specified file \n'
+'/file_rename + /location/file name(space)new name - rename specified file \n'
+'/file_delete + /location/file name - delete local file \n \n'
+'**/play function was tested only on youtube, vk, vimeo \n'
+'Since Spotfiy has a lot of restrictions, it allows playback only through certified applications and Web Player \n \n'
+'***Drop images, video or documents in chat to upload them to the host machine \n \n'
+'****File system includes folders that are not visible through ```/ls``` command, however, if the folder name is known, it can be opened (currently available hidden folders: .bot_media, .playlist, .local_playlist, .track). Therefore, these files can be downloaded manually ^_^ \n')


####Youtube

def youtube_play(update, context):
    user_id = update.message.from_user.id
    access_list = ("0","1")

    for x in mycol.find():
        if x.get("id") == str(user_id):
            level = x.get("access_level")
            if level not in access_list:
                return update.message.reply_text("Denied")
        else:
            return update.message.reply_text("Denied")

    os.system('aplay '+ saddness.temp + '/media/.bot_media/function.wav && sudo rm ' + saddness.temp + '/media/.track/*')
    song_name = open(saddness.temp + '/temp/name.txt', 'r') 
    os.system('pkill mpv')
    URL = update.message.text.strip("/yt")[1:]
    if ".com" in URL or ".be" in URL:
      os.system('$(youtube-dl -f bestaudio -o - ytsearch:"' + URL + '" | mpv --no-video - >/dev/null 2>&1 &)'
+' && youtube-dl -o "' + saddness.temp + '/media/.track/%(title)s" -f bestaudio ytsearch:"' + URL
+'" && youtube-dl --get-title ytsearch:"' + URL + '" > ' + saddness.temp + '/temp/name.txt' 
+' && youtube-dl --get-id ytsearch:"' + URL + '" >> ' + saddness.temp + '/temp/name.txt')
      update.message.reply_text('Playing... ~(˘▾˘~) \n')
    else:
      os.system('$(youtube-dl -f bestaudio -o - ytsearch:"' + URL + '" | mpv --no-video - >/dev/null 2>&1 &)'
+' && youtube-dl -o "' + saddness.temp + '/media/.track/%(title)s" -f bestaudio ytsearch:"' + URL
+'" && youtube-dl --get-title ytsearch:"' + URL + '" > ' + saddness.temp + '/temp/name.txt' 
+' && youtube-dl --get-id ytsearch:"' + URL + '" >> ' + saddness.temp + '/temp/name.txt')
      update.message.reply_text('Playing... ~(˘▾˘~) \n' + song_name.readline() + '\n' + 'https://youtu.be/' + song_name.readline())

    song_name.close()

#if "http" -> no display for get-title and get-id
#if "keyword" -> go full function
    
def youtube_play_last_track(update, context):
    user_id = update.message.from_user.id
    access_list = ("0","1")

    for x in mycol.find():
        if x.get("id") == str(user_id):
            level = x.get("access_level")
            if level not in access_list:
                return update.message.reply_text("Denied")
        else:
            return update.message.reply_text("Denied")

    os.system('aplay '+ saddness.temp + '/media/.bot_media/function.wav')
    song_name = open(saddness.temp + '/temp/name.txt', 'r') 
    update.message.reply_text('Playing... ~(˘▾˘~)\n' + song_name.readline() + '\n' + 'https://youtu.be/' + song_name.readline())
    os.system('$(mpv --playlist ' + saddness.temp + '/media/.track/ >/dev/null 2>&1 &)')
    song_name.close()
    
def youtube_play_local(update, context):
    user_id = update.message.from_user.id
    access_list = ("0","1")
    for x in mycol.find():
        if x.get("id") == str(user_id):
            level = x.get("access_level")
            if level not in access_list:
                return update.message.reply_text("Denied")
        else:
            return update.message.reply_text("Denied")

    os.system('aplay '+ saddness.temp + '/media/.bot_media/function.wav')
    song_name = open(saddness.temp + '/temp/name.txt', 'r') 
    os.system('pkill mpv')
    URL = update.message.text.strip("/yt_local")[1:]
    if ".com" in URL or ".be" in URL:
      os.system('$(youtube-dl -f bestaudio -o - ytsearch:"' + URL + '" | mpv --no-video - >/dev/null 2>&1 &)'
+' && youtube-dl -o "' + saddness.temp + '/media/.local_playlist/%(title)s" -f bestaudio ytsearch:"' + URL
+'" && youtube-dl --get-title ytsearch:"' + URL + '" > ' + saddness.temp + '/temp/name.txt' 
+' && youtube-dl --get-id ytsearch:"' + URL + '" >> ' + saddness.temp + '/temp/name.txt')
      update.message.reply_text('Playing... ~(˘▾˘~) \n')
    else:
      os.system('$(youtube-dl -f bestaudio -o - ytsearch:"' + URL + '" | mpv --no-video - >/dev/null 2>&1 &)'
+' && youtube-dl -o "' + saddness.temp + '/media/.local_playlist/%(title)s" -f bestaudio ytsearch:"' + URL
+'" && youtube-dl --get-title ytsearch:"' + URL + '" > ' + saddness.temp + '/temp/name.txt' 
+' && youtube-dl --get-id ytsearch:"' + URL + '" >> ' + saddness.temp + '/temp/name.txt')
      update.message.reply_text('Playing... ~(˘▾˘~) \n' + song_name.readline() + '\n' + 'https://youtu.be/' + song_name.readline())

    song_name.close()
    
def youtube_local(update, context):
    user_id = update.message.from_user.id
    access_list = ("0","1")
    
    for x in mycol.find():
        if x.get("id") == str(user_id):
            level = x.get("access_level")
            if level not in access_list:
                return update.message.reply_text("Denied")
        else:
            return update.message.reply_text("Denied")

    os.system('aplay '+ saddness.temp + '/media/.bot_media/function.wav && pkill mpv')
    song_name = open(saddness.temp + '/temp/name.txt', 'r') 
    update.message.reply_text('Starting local playlist... ~(˘▾˘~)\n')
    os.system('cd '+ saddness.temp + '/media/.local_playlist && ls > ' + saddness.temp + '/temp/local_list.txt')
    file_list = open(saddness.temp + '/temp/local_list.txt', 'r')
    update.message.reply_text(file_list.read())
    os.system('$(mpv --playlist ' + saddness.temp + '/media/.local_playlist/ >/dev/null 2>&1 &)')
    file_list.close()
    song_name.close()

def youtube_local_purge(update, context):
    user_id = update.message.from_user.id
    access_list = ("0","1")

    for x in mycol.find():
        if x.get("id") == str(user_id):
            level = x.get("access_level")
            if level not in access_list:
                return update.message.reply_text("Denied")
        else:
            return update.message.reply_text("Denied")

    os.system('pkill mpv')
    os.system('aplay '+ saddness.temp + '/media/.bot_media/function.wav && sudo rm ' + saddness.temp + '/media/.local_playlist/* && sudo rm ' + saddness.temp + '/media/.track/* && sudo rm ' + saddness.temp + '/media/.playlist/* && sudo rm ' + saddness.temp + '/temp/*')
    update.message.reply_text('Removed all local playlist media \n ༼ つ ಥ_ಥ ༽つ ')

def local_playlist_view(update, context):
    user_id = update.message.from_user.id
    access_list = ("0","1")

    for x in mycol.find():
        if x.get("id") == str(user_id):
            level = x.get("access_level")
            if level not in access_list:
                return update.message.reply_text("Denied")
        else:
            return update.message.reply_text("Denied")

    os.system('aplay '+ saddness.temp + '/media/.bot_media/function.wav')
    os.system('cd '+ saddness.temp + '/media/.local_playlist && ls > ' + saddness.temp + '/temp/local_list.txt')
    file_list = open(saddness.temp + '/temp/local_list.txt', 'r')
    update.message.reply_text(file_list.read())
    file_list.close()
    
def local_playlist_edit(update, context):
    user_id = update.message.from_user.id
    access_list = ("0","1")

    for x in mycol.find():
        if x.get("id") == str(user_id):
            level = x.get("access_level")
            if level not in access_list:
                return update.message.reply_text("Denied")
        else:
            return update.message.reply_text("Denied")

    os.system('pkill mpv')
    keyword = update.message.text.strip("/local_edit")[1:]
    os.system('sudo rm ' + saddness.temp + '/media/.local_playlist/"' + keyword + '" ')
    update.message.reply_text('File: \n' + keyword + '\n was removed (;´༎ຶД༎ຶ`)\n')
    os.system('cd '+ saddness.temp + '/media/.local_playlist && ls > ' + saddness.temp + '/temp/local_list.txt')
    file_list = open(saddness.temp + '/temp/local_list.txt', 'r')
    update.message.reply_text(file_list.read())
    file_list.close()
    


def youtube_play_playlist(update, context):
    user_id = update.message.from_user.id
    access_list = ("0","1")

    for x in mycol.find():
        if x.get("id") == str(user_id):
            level = x.get("access_level")
            if level not in access_list:
                return update.message.reply_text("Denied")
        else:
            return update.message.reply_text("Denied")

    os.system('aplay '+ saddness.temp + '/media/.bot_media/function.wav && rm ' + saddness.temp + '/media/.playlist/*')
    song_name = open(saddness.temp + '/temp/playlist.txt', 'r') 
    os.system('pkill mpv')
    URL = update.message.text.strip("/yt_playlist")[1:]
    update.message.reply_text('Fetching playlist data...')
    os.system('youtube-dl --skip-unavailable-fragments --yes-playlist --playlist-items ' + saddness.playlist_int + ' -o "' + saddness.temp + '/media/.playlist/%(title)s" -f bestaudio ' + URL)
    os.system('cd ' + saddness.temp + '/media/.playlist && ls > ' + saddness.temp + '/temp/playlist.txt')
    update.message.reply_text('Playing... (~˘▾˘)~ \n')
    update.message.reply_text(song_name.read())
    song_name.close()
    os.system('$(mpv --no-video --playlist ' + saddness.temp + '/media/.playlist/ >/dev/null 2>&1 &)')

def youtube_play_last(update, context):
    user_id = update.message.from_user.id
    access_list = ("0","1")

    for x in mycol.find():
        if x.get("id") == str(user_id):
            level = x.get("access_level")
            if level not in access_list:
                return update.message.reply_text("Denied")
        else:
            return update.message.reply_text("Denied")

    os.system('aplay '+ saddness.temp + '/media/.bot_media/function.wav && pkill mpv')  
    song_name = open(saddness.temp + '/temp/playlist.txt', 'r') 
    update.message.reply_text('Fetching playlist data... \n \n' + song_name.read())
    song_name.close()
    update.message.reply_text('Playing... (~˘▾˘)~\n')
    os.system('$(mpv --playlist ' + saddness.temp + '/media/.playlist/ >/dev/null 2>&1 &)')
    
def youtube_playlist_int_cur(update, context):
    user_id = update.message.from_user.id
    access_list = ("0","1")

    for x in mycol.find():
        if x.get("id") == str(user_id):
            level = x.get("access_level")
            if level not in access_list:
                return update.message.reply_text("Denied")
        else:
            return update.message.reply_text("Denied")

    update.message.reply_text(saddness.playlist_int)

def youtube_playlist_int_set(update, context):
    user_id = update.message.from_user.id
    access_list = ("0","1")

    for x in mycol.find():
        if x.get("id") == str(user_id):
            level = x.get("access_level")
            if level not in access_list:
                return update.message.reply_text("Denied")
        else:
            return update.message.reply_text("Denied")

    update.message.reply_text('Changing to... \n' + update.message.text.strip("/yt_playlist_int_set ").replace(" ",""))
    saddness.playlist_int = update.message.text.strip("/yt_playlist_int_set ").replace(" ","")

####Spotify

def spotify_playlist(update, context):
    user_id = update.message.from_user.id

    for x in mycol.find():
        if x.get("id") == str(user_id):
            print("has_access, spotify playlist")
        else:
            return update.message.reply_text("Denied")

    keyword = update.message.text.strip("/sp_playlist")[1:]
    update.message.reply_text('Enjoy your playlist! \n' + get_playlist(str(keyword)))

def spotify_track(update, context):
    user_id = update.message.from_user.id

    for x in mycol.find():
        if x.get("id") == str(user_id):
            print("has_access, spotify track")
        else:
            return update.message.reply_text("Denied")

    keyword = update.message.text.strip("/sp")[1:]
    update.message.reply_text('Enjoy your track! \n' + get_track(keyword))

####Play other


def play_audio(update, context):
    user_id = update.message.from_user.id
    access_list = ("0","1")

    for x in mycol.find():
        if x.get("id") == str(user_id):
            level = x.get("access_level")
            if level not in access_list:
                return update.message.reply_text("Denied")
        else:
            return update.message.reply_text("Denied")

    os.system('aplay '+ saddness.temp + '/media/.bot_media/function.wav')
    os.system('pkill mpv')
    update.message.reply_text('Playing... (~˘▾˘)~\n')
    URL = update.message.text.strip("/play")
    os.system('$(mpv --no-video ' + URL + ' >/dev/null 2>&1 &)')

def play_video(update, context):
    user_id = update.message.from_user.id
    access_list = ("0","1")

    for x in mycol.find():
        if x.get("id") == str(user_id):
            level = x.get("access_level")
            if level not in access_list:
                return update.message.reply_text("Denied")
        else:
            return update.message.reply_text("Denied")

    os.system('aplay '+ saddness.temp + '/media/.bot_media/function.wav')
    os.system('pkill mpv')
    update.message.reply_text('Playing... (~˘▾˘)~\n')
    URL = update.message.text.strip("/play_video")
    os.system('mpv ' + URL)


####Playback options 

def pause_playback(update, context):
    user_id = update.message.from_user.id
    access_list = ("0","1")

    for x in mycol.find():
        if x.get("id") == str(user_id):
            level = x.get("access_level")
            if level not in access_list:
                return update.message.reply_text("Denied")
        else:
            return update.message.reply_text("Denied")

    os.system('aplay '+ saddness.temp + '/media/.bot_media/function.wav')
    update.message.reply_text('Pause...')
    os.system('pkill mpv -STOP')

def continue_playback(update, context):
    user_id = update.message.from_user.id
    access_list = ("0","1")

    for x in mycol.find():
        if x.get("id") == str(user_id):
            level = x.get("access_level")
            if level not in access_list:
                return update.message.reply_text("Denied")
        else:
            return update.message.reply_text("Denied")

    os.system('aplay '+ saddness.temp + '/media/.bot_media/function.wav')
    update.message.reply_text('Continuing...')
    os.system('pkill mpv -CONT')

def stop_playback(update, context):
    user_id = update.message.from_user.id
    access_list = ("0","1")
    
    for x in mycol.find():
        if x.get("id") == str(user_id):
            level = x.get("access_level")
            if level not in access_list:
                return update.message.reply_text("Denied")
        else:
            return update.message.reply_text("Denied")

    os.system('aplay '+ saddness.temp + '/media/.bot_media/function.wav')
    update.message.reply_text('Stopping...')
    os.system('pkill mpv')

####Volume

def volume(update, context):
    user_id = update.message.from_user.id
    access_list = ("0","1")

    for x in mycol.find():
        if x.get("id") == str(user_id):
            level = x.get("access_level")
            if level not in access_list:
                return update.message.reply_text("Denied")
        else:
            return update.message.reply_text("Denied")

    os.system('aplay '+ saddness.temp + '/media/.bot_media/function.wav')
    update.message.reply_text('Changing to... \n' + update.message.text.strip("/volume")[1:] + '%')
    saddness.vol = update.message.text.strip("/volume ").replace(" ","").replace("%","")
    os.system('amixer -D pulse sset Master ' + saddness.vol + '%')

def volume_cur(update, context):
    user_id = update.message.from_user.id
    access_list = ("0","1")

    for x in mycol.find():
        if x.get("id") == str(user_id):
            level = x.get("access_level")
            if level not in access_list:
                return update.message.reply_text("Denied")
        else:
            return update.message.reply_text("Denied")

    update.message.reply_text(saddness.vol + '%')

####DuckDuckGo

def search(update, context):
    user_id = update.message.from_user.id

    for x in mycol.find():
        if x.get("id") == str(user_id):
            print("has_access, showing media")
        else:
            return update.message.reply_text("Denied")   

    query = update.message.text.strip("/q")[1:]
    update.message.reply_text(duckduckgo.get_zci(query))
    print (duckduckgo.get_zci(query))

####IMDb

def search_movie(update, context):
    user_id = update.message.from_user.id

    for x in mycol.find():
        if x.get("id") == str(user_id):
            print("has_access, showing media")
        else:
            return update.message.reply_text("Denied")

    keyword = update.message.text.strip("/imdb")[1:]
    movies = ia.search_movie(keyword)
    url = ia.get_imdbURL(movies[0])
    update.message.reply_text(str(movies[0]['title']) + '\n https://www.imdb.com/title/tt' + str(movies[0].movieID))

####Weather

def weather(update, context):
    user_id = update.message.from_user.id

    for x in mycol.find():
        if x.get("id") == str(user_id):
            print("has_access, showing weather")
        else:
            return update.message.reply_text("Denied")

    keyword = update.message.text.strip("/w")[1:]
    weatherData = GetWeather(keyword)

    if weatherData == "City Not Found":
        update.message.reply_text("City Not Found")
    else:
        update.message.caption_html(
            '<img style="display:block" src="data:image/svg+xml;base64,PHN2ZyBoZWlnaHQ9IjUxMiIgdmlld0JveD0iMCAwIDEyOCAxMjgiIHdpZHRoPSI1MTIiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGc+PGNpcmNsZSBjeD0iNjQiIGN5PSI2My45OTciIGZpbGw9IiNmZWRiNDEiIHI9IjM5LjI0NyIvPjxnIGZpbGw9IiNmZWE4MzIiPjxwYXRoIGQ9Im05NS4yNDcgNjUuNzQ3YTEuNzQ5IDEuNzQ5IDAgMCAxIC0xLjc0Ny0xLjc0NyAyOS41MyAyOS41MyAwIDAgMCAtMjkuNS0yOS41IDEuNzUgMS43NSAwIDAgMSAwLTMuNSAzMy4wMzUgMzMuMDM1IDAgMCAxIDMzIDMzIDEuNzQ5IDEuNzQ5IDAgMCAxIC0xLjc1MyAxLjc0N3oiLz48Zz48cGF0aCBkPSJtNjQgMTYuNzVhNDcuMjUyIDQ3LjI1MiAwIDAgMSA4LjUuNzgxYy4wMzgtLjU0NS4wNjMtMS4xLjA2My0xLjY1OC0uMDAxLTcuODAxLTguNTYzLTE0LjEyNi04LjU2My0xNC4xMjZzLTguNTYzIDYuMzI1LTguNTYzIDE0LjEyNmMwIC41NjIuMDI2IDEuMTEzLjA2NCAxLjY1OGE0Ny4yNDMgNDcuMjQzIDAgMCAxIDguNDk5LS43ODF6Ii8+PHBhdGggZD0ibTY0IDExMS4yNDRhNDcuMzQzIDQ3LjM0MyAwIDAgMCA4LjUtLjc4Yy4wMzguNTQ0LjA2MyAxLjA5NS4wNjMgMS42NTcgMCA3LjgtOC41NjIgMTQuMTI2LTguNTYyIDE0LjEyNnMtOC41NjMtNi4zMjQtOC41NjMtMTQuMTI2YzAtLjU2Mi4wMjYtMS4xMTMuMDY0LTEuNjU3YTQ3LjMzNSA0Ny4zMzUgMCAwIDAgOC40OTguNzh6Ii8+PHBhdGggZD0ibTk3LjQwOSAzMC41ODhhNDcuMzQ5IDQ3LjM0OSAwIDAgMSA1LjQ1NyA2LjU2MmMuNDEzLS4zNTguODItLjczIDEuMjE3LTEuMTI3IDUuNTE3LTUuNTE3IDMuOTM0LTE2LjA0MyAzLjkzNC0xNi4wNDNzLTEwLjUyNi0xLjU4LTE2LjA0MyAzLjkzNGMtLjQuNC0uNzY5LjgtMS4xMjcgMS4yMTdhNDcuMzQ5IDQ3LjM0OSAwIDAgMSA2LjU2MiA1LjQ1N3oiLz48cGF0aCBkPSJtMzAuNTkxIDk3LjQwNmE0Ny4yMzIgNDcuMjMyIDAgMCAwIDYuNTYyIDUuNDU3Yy0uMzU4LjQxMy0uNzMuODItMS4xMjcgMS4yMTctNS41MTcgNS41MTctMTYuMDQzIDMuOTM0LTE2LjA0MyAzLjkzNHMtMS41ODMtMTAuNTI2IDMuOTM0LTE2LjA0M2MuNC0uNC44LS43NjkgMS4yMTctMS4xMjdhNDcuMjkxIDQ3LjI5MSAwIDAgMCA1LjQ1NyA2LjU2MnoiLz48cGF0aCBkPSJtMTExLjI0NyA2NGE0Ny4zMzUgNDcuMzM1IDAgMCAxIC0uNzggOC41Yy41NDQuMDM4IDEuMDk1LjA2NCAxLjY1Ny4wNjQgNy44IDAgMTQuMTI2LTguNTYzIDE0LjEyNi04LjU2M3MtNi4zMjUtOC41NjItMTQuMTI2LTguNTYyYy0uNTYyIDAtMS4xMTMuMDI1LTEuNjU3LjA2M2E0Ny4zNDMgNDcuMzQzIDAgMCAxIC43OCA4LjQ5OHoiLz48cGF0aCBkPSJtMTYuNzUzIDY0YTQ3LjMzNSA0Ny4zMzUgMCAwIDAgLjc4IDguNWMtLjU0NC4wMzgtMS4xLjA2NC0xLjY1Ny4wNjQtNy44MDEtLjAwNC0xNC4xMjYtOC41NjQtMTQuMTI2LTguNTY0czYuMzI1LTguNTYyIDE0LjEyNi04LjU2MmMuNTYyIDAgMS4xMTMuMDI1IDEuNjU3LjA2M2E0Ny4zNDMgNDcuMzQzIDAgMCAwIC0uNzggOC40OTl6Ii8+PHBhdGggZD0ibTk3LjQwOSA5Ny40MDZhNDcuMzQ5IDQ3LjM0OSAwIDAgMSAtNi41NjIgNS40NTdjLjM1OC40MTMuNzMuODIgMS4xMjcgMS4yMTcgNS41MTcgNS41MTcgMTYuMDQzIDMuOTM0IDE2LjA0MyAzLjkzNHMxLjU4My0xMC41MjYtMy45MzQtMTYuMDQzYy0uNC0uNC0uOC0uNzY5LTEuMjE3LTEuMTI3YTQ3LjI5MSA0Ny4yOTEgMCAwIDEgLTUuNDU3IDYuNTYyeiIvPjxwYXRoIGQ9Im0zMC41OTEgMzAuNTg4YTQ3LjM0OSA0Ny4zNDkgMCAwIDAgLTUuNDU3IDYuNTYyYy0uNDEzLS4zNTgtLjgyLS43My0xLjIxNy0xLjEyNy01LjUxNy01LjUxNy0zLjkzNC0xNi4wNDMtMy45MzQtMTYuMDQzczEwLjUyNi0xLjU4IDE2LjA0MyAzLjkzNGMuNC40Ljc2OS44IDEuMTI3IDEuMjE3YTQ3LjI5MSA0Ny4yOTEgMCAwIDAgLTYuNTYyIDUuNDU3eiIvPjwvZz48L2c+PC9nPjwvc3ZnPg=="/>'
            + "\n" + str(weatherData[1]) + " C" + 
            '<img style="display:block" src="data:image/svg+xml;base64,PHN2ZyBpZD0iTGF5ZXJfMSIgZW5hYmxlLWJhY2tncm91bmQ9Im5ldyAwIDAgNTExLjk5OCA1MTEuOTk4IiBoZWlnaHQ9IjUxMiIgdmlld0JveD0iMCAwIDUxMS45OTggNTExLjk5OCIgd2lkdGg9IjUxMiIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48Zz48Zz48cGF0aCBkPSJtMzk5LjI5NyAzNDguNjQxYy01My41OTggMC05Ny4yMDMtNDMuNjA0LTk3LjIwMy05Ny4yMDIgMC0zMC40OTIgMjQuMTY5LTc2LjQwNyAzOC41NzctMTAxLjA2MyA5LjU0Ni0xNi4zMzggMTkuNzUxLTMxLjc4NCAyOC43MzUtNDMuNDk1IDEzLjI0NC0xNy4yNjQgMjEuMDY1LTIzLjM4MyAyOS44OTEtMjMuMzgzczE2LjY0NyA2LjExOSAyOS44OTEgMjMuMzgzYzguOTgzIDExLjcxMSAxOS4xODggMjcuMTU3IDI4LjczNSA0My40OTUgMTQuNDA3IDI0LjY1NSAzOC41NzcgNzAuNTcgMzguNTc3IDEwMS4wNjMtLjAwMSA1My41OTctNDMuNjA2IDk3LjIwMi05Ny4yMDMgOTcuMjAyeiIgZmlsbD0iIzUyNWNkZCIvPjwvZz48Zz48cGF0aCBkPSJtMTk4Ljk5OSA1MTEuOTk4Yy0xMDEuMTgyIDAtMTgzLjUtODIuMzE3LTE4My41LTE4My41IDAtNjAuOTg3IDUzLjc5NS0xNTkuNjMzIDc2LjkyNC0xOTkuMjE0IDE5LjI0Ny0zMi45MzggMzkuNzczLTY0LjAxOCA1Ny43OTktODcuNTE3IDI5LjU2NS0zOC41MzkgNDAuNjgtNDEuNzY3IDQ4Ljc3Ny00MS43NjdzMTkuMjEyIDMuMjI4IDQ4Ljc3NiA0MS43NjhjMTguMDI2IDIzLjQ5OSAzOC41NTMgNTQuNTc5IDU3LjggODcuNTE3IDIzLjEyOCAzOS41ODEgNzYuOTI0IDEzOC4yMjcgNzYuOTI0IDE5OS4yMTQgMCAxMDEuMTgyLTgyLjMxOCAxODMuNDk5LTE4My41IDE4My40OTl6IiBmaWxsPSIjN2RkNWY0Ii8+PC9nPjxwYXRoIGQ9Im0zMDUuNTc1IDEyOS4yODRjLTE5LjI0Ny0zMi45MzgtMzkuNzczLTY0LjAxOC01Ny44LTg3LjUxNy0yOS41NjQtMzguNTM5LTQwLjY3OS00MS43NjctNDguNzc2LTQxLjc2N3Y1MTEuOTk4YzEwMS4xODIgMCAxODMuNS04Mi4zMTcgMTgzLjUtMTgzLjUgMC02MC45ODctNTMuNzk1LTE1OS42MzMtNzYuOTI0LTE5OS4yMTR6IiBmaWxsPSIjNDc5M2ZmIi8+PGc+PHBhdGggZD0ibTE2NS4zMDIgNDAxLjg0MmMtMi41NDUgMC01LjEyNC0uNjQ4LTcuNDg2LTIuMDEzLTcuMTc0LTQuMTQyLTkuNjMyLTEzLjMxNS01LjQ5LTIwLjQ5bDY3LjM2Ni0xMTYuNjgyYzQuMTQyLTcuMTc0IDEzLjMxNS05LjYzNSAyMC40OS01LjQ5IDcuMTc0IDQuMTQyIDkuNjMyIDEzLjMxNSA1LjQ5IDIwLjQ5bC02Ny4zNjYgMTE2LjY4MmMtMi43NzggNC44MTEtNy44MiA3LjUwMy0xMy4wMDQgNy41MDN6IiBmaWxsPSIjZmZmNGY0Ii8+PC9nPjxnPjxwYXRoIGNsaXAtcnVsZT0iZXZlbm9kZCIgZD0ibTE0Ni41IDMwMS45OTljOC4yNjIgMCAxNS02LjczOSAxNS0xNSAwLTguMjYyLTYuNzM4LTE1LTE1LTE1cy0xNSA2LjczOC0xNSAxNWMtLjAwMSA4LjI2MSA2LjczOCAxNSAxNSAxNXoiIGZpbGw9IiNmZmY0ZjQiIGZpbGwtcnVsZT0iZXZlbm9kZCIvPjwvZz48Zz48cGF0aCBjbGlwLXJ1bGU9ImV2ZW5vZGQiIGQ9Im0yNDYuNSAzODYuOTk4YzguMjYyIDAgMTUtNi43MzggMTUtMTVzLTYuNzM4LTE1LTE1LTE1LTE1IDYuNzM4LTE1IDE1Yy0uMDAxIDguMjYyIDYuNzM4IDE1IDE1IDE1eiIgZmlsbD0iI2Y2ZWZlYSIgZmlsbC1ydWxlPSJldmVub2RkIi8+PC9nPjxwYXRoIGQ9Im0yNDAuMTgyIDI1Ny4xNjdjLTcuMTc1LTQuMTQ1LTE2LjM0OC0xLjY4NC0yMC40OSA1LjQ5bC0yMC42OTMgMzUuODQxdjYwbDQ2LjY3My04MC44NDFjNC4xNDItNy4xNzUgMS42ODQtMTYuMzQ4LTUuNDktMjAuNDl6IiBmaWxsPSIjZjZlZmVhIi8+PC9nPjwvc3ZnPg=="/>'
            "\n" + str(weatherData[0]) + " %" +
            '<img style="display:block" src="data:image/svg+xml;base64,PHN2ZyBpZD0iTGF5ZXJfMSIgZW5hYmxlLWJhY2tncm91bmQ9Im5ldyAwIDAgNTEyIDUxMiIgaGVpZ2h0PSI1MTIiIHZpZXdCb3g9IjAgMCA1MTIgNTEyIiB3aWR0aD0iNTEyIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxnPjxwYXRoIGQ9Im0xOTEuNzMzIDQxMi40aC0xNzYuNzMzYy04LjI4NCAwLTE1LTYuNzE2LTE1LTE1czYuNzE2LTE1IDE1LTE1aDE3Ni43MzNjOC4yODQgMCAxNSA2LjcxNiAxNSAxNXMtNi43MTUgMTUtMTUgMTV6IiBmaWxsPSIjOWJmMGZmIi8+PHBhdGggZD0ibTc5LjI2NyAxMjkuNmgtNjQuMjY3Yy04LjI4NCAwLTE1LTYuNzE2LTE1LTE1czYuNzE2LTE1IDE1LTE1aDY0LjI2N2M4LjI4NCAwIDE1IDYuNzE2IDE1IDE1cy02LjcxNiAxNS0xNSAxNXoiIGZpbGw9IiM5YmYwZmYiLz48cGF0aCBkPSJtNDUzLjYwMSAxMjIuNDcyYy0zMy4wNjUtLjQ2My02MC4xMTIgMjYuMy02MC4xMTIgNTkuMjYxIDAgMTQuMjQ4IDExLjU0IDIwLjU3IDE3Ljk2MyAyMS43NSAxNC4wMjIgMi41NzUgMjYuMjkxLTguMTY5IDI2LjMwNC0yMS43MjguMDA2LTYuNTQyIDQuMTIyLTEyLjQ2MyAxMC4zOTEtMTQuMzM1IDEwLjI1LTMuMDYgMTkuNjA5IDQuNTM0IDE5LjYwOSAxNC4zMTMgMCAyOC43NDctMjMuMzg3IDUyLjEzMy01Mi4xMzMgNTIuMTMzaC00MDAuNjIzYy04LjI4NCAwLTE1IDYuNzE2LTE1IDE1djE0LjI2N2MwIDguMjg0IDYuNzE2IDE1IDE1IDE1aDQwMC42MjJjNTEuNjExIDAgOTQuNTEzLTQwLjcxNSA5Ni4zMzktOTIuOTM0IDEuMTczLTMzLjUyLTI0LjgyMy02Mi4yNTctNTguMzYtNjIuNzI3eiIgZmlsbD0iIzE3YmNmZSIvPjxwYXRoIGQ9Im0yODUuNjU2IDMwOC4xMzNoLTI3MC42NTZjLTguMjg0IDAtMTUgNi43MTYtMTUgMTV2MTQuMjY3YzAgOC4yODQgNi43MTYgMTUgMTUgMTVoMjcwLjY1NmMyOC40OTkgMCA1MS43MjkgMjIuOTg1IDUyLjEyOCA1MS4zOTEuMTE2IDguMjMxLTYuNDIyIDE1LjU1NS0xNC42NTIgMTUuNzM5LTguNDQxLjE4OS0xNS4zNDMtNi41OTgtMTUuMzQzLTE0Ljk5NiAwLTEyLjIwNS05LjkyOS0yMi4xMzMtMjIuMTMzLTIyLjEzMy0xMi4wNzYgMC0yMi4xMzMgOS43MTEtMjIuMTMzIDIyLjEzMyAwIDMyLjk2MSAyNy4wNDcgNTkuNzI0IDYwLjExMiA1OS4yNjEgMzMuNTM3LS40NyA1OS41MzMtMjkuMjA3IDU4LjM2MS02Mi43MjctMS44MjQtNTIuMTE4LTQ0LjYxMi05Mi45MzUtOTYuMzQtOTIuOTM1eiIgZmlsbD0iIzJkZTFmZCIvPjxwYXRoIGQ9Im0xNTUuNjg5IDIwMy44NjdoLTE0MC42ODZjLTguMjg0IDAtMTUtNi43MTYtMTUtMTV2LTE0LjI2N2MwLTguMjg0IDYuNzE2LTE1IDE1LTE1aDE0MC42ODVjMjguNDk5IDAgNTEuNzI5LTIyLjk4NSA1Mi4xMjgtNTEuMzkxLjExNi04LjIzMS02LjQyMi0xNS41NTUtMTQuNjUyLTE1LjczOS04LjQ0MS0uMTg5LTE1LjM0MyA2LjU5OC0xNS4zNDMgMTQuOTk2IDAgMTIuMjA1LTkuOTI5IDIyLjEzMy0yMi4xMzMgMjIuMTMzLTEyLjA3NiAwLTIyLjEzMy05LjcxMS0yMi4xMzMtMjIuMTMzIDAtMzIuOTYxIDI3LjA0Ny01OS43MjQgNjAuMTEyLTU5LjI2MSAzMy41MzcuNDcgNTkuNTMzIDI5LjIwNyA1OC4zNjEgNjIuNzI3LTEuODIzIDUyLjExOC00NC42MTEgOTIuOTM1LTk2LjMzOSA5Mi45MzV6IiBmaWxsPSIjMmRlMWZkIi8+PHBhdGggZD0ibTUxMS45NjIgMTg1LjE5OWMxLjE3Mi0zMy41Mi0yNC44MjQtNjIuMjU4LTU4LjM2MS02Mi43MjctMzMuMDY1LS40NjMtNjAuMTEyIDI2LjMtNjAuMTEyIDU5LjI2MSAwIDE0LjI0OCAxMS41NCAyMC41NyAxNy45NjMgMjEuNzUgMTQuMDIyIDIuNTc1IDI2LjI5MS04LjE2OSAyNi4zMDQtMjEuNzI4LjAwNi02LjU0MiA0LjEyMi0xMi40NjMgMTAuMzkxLTE0LjMzNSAxMC4yNS0zLjA2IDE5LjYwOSA0LjUzNCAxOS42MDkgMTQuMzEzIDAgMjguNzQ3LTIzLjM4NyA1Mi4xMzMtNTIuMTMzIDUyLjEzM2gtMTYzLjU5NXY0NC4yNjdoMTYzLjU5NGM1MS42MTIgMCA5NC41MTMtNDAuNzE1IDk2LjM0LTkyLjkzNHoiIGZpbGw9IiMwMDk2ZmYiLz48cGF0aCBkPSJtMzM3Ljc4NCA0MDMuNzkxYy4xMTYgOC4yMzEtNi40MjIgMTUuNTU1LTE0LjY1MiAxNS43MzktOC40NDEuMTg5LTE1LjM0My02LjU5OC0xNS4zNDMtMTQuOTk2IDAtMTIuMjA1LTkuOTI5LTIyLjEzMy0yMi4xMzMtMjIuMTMzLTEyLjA3NiAwLTIyLjEzMyA5LjcxMS0yMi4xMzMgMjIuMTMzIDAgMzIuOTYxIDI3LjA0NyA1OS43MjQgNjAuMTEyIDU5LjI2MSAzMy41MzctLjQ3IDU5LjUzMy0yOS4yMDcgNTguMzYxLTYyLjcyNy0xLjgyMy01Mi4xMTctNDQuNjExLTkyLjkzNC05Ni4zMzktOTIuOTM0aC0zMy42Mjd2NDQuMjY2aDMzLjYyN2MyOC40OTcgMCA1MS43MjggMjIuOTg1IDUyLjEyNyA1MS4zOTF6IiBmaWxsPSIjMTdiY2ZlIi8+PC9nPjwvc3ZnPg=="/>'
            "\n" + str(weatherData[3]) + " m/s" +
            "\n\n" + str(weatherData[2]))

    

    

####Random

def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def git(update, context):
    """Returns projects git repository"""
    update.message.reply_text("https://github.com/HikingSheep/Testy_Rasbian")
    
def OS(update, context):
    user_id = update.message.from_user.id
    level = ''

    for x in mycol.find():
        if x.get("id") == str(user_id):
            level = x.get("access_level")
            if level != "0":
                return update.message.reply_text("Denied")
        else:
            return update.message.reply_text("Denied")

    command = update.message.text.strip("/cmd")[1:]
    os.system(command)

####File System

def show_media(update, context):
    user_id = update.message.from_user.id

    for x in mycol.find():
        if x.get("id") == str(user_id):
            print("has_access, showing media")
        else:
            return update.message.reply_text("Denied")

    keyword = update.message.text.strip("/ls ")
    os.system('cd '+ saddness.temp + '/media/' + keyword + ' && ls > ' + saddness.temp + '/temp/list.txt')
    file_list = open(saddness.temp + '/temp/list.txt', 'r')
    update.message.reply_text(file_list.read())
    file_list.close()

def download_media(update, context):
    user_id = update.message.from_user.id

    for x in mycol.find():
        if x.get("id") == str(user_id):
            print("has_access, allow download")
        else:
            return update.message.reply_text("Denied")

    URL = update.message.text.strip("/dw").replace(" ","")
    update.message.bot.send_document(chat_id = update.message.chat_id, filename=URL, document=open(saddness.temp + '/media' + URL, 'rb'))
    update.message.reply_text('Downloading from storage... ' + URL)

def voice(update, context):
    user_id = update.message.from_user.id
    access_list = ("0","1")

    for x in mycol.find():
        if x.get("id") == str(user_id):
            level = x.get("access_level")
            if level not in access_list:
                return update.message.reply_text("Denied")
        else:
            return update.message.reply_text("Denied")

    FileID = update.message.voice.file_id[20:]
    print (FileID)
    newFile = update.message.voice.get_file()
    newFile.download(saddness.temp + '/media/audio/' + FileID + '.mp3')
    update.message.reply_text('Hmmm... Uploaded ┬┴┬┴┤(･_├┬┴┬┴')

def photo(update, context):
    user_id = update.message.from_user.id
    access_list = ("0","1")

    for x in mycol.find():
        if x.get("id") == str(user_id):
            level = x.get("access_level")
            if level not in access_list:
                return update.message.reply_text("Denied")
        else:
            return update.message.reply_text("Denied")


    FileID = update.message.photo[-1].file_id[:20]
    print (FileID)
    newFile = update.message.photo[-1].get_file()
    newFile.download(saddness.temp + '/media/image/' + FileID + '.jpg')
    update.message.reply_text('Hmmm... Uploaded ┬┴┬┴┤(･_├┬┴┬┴')

def video(update, context):
    user_id = update.message.from_user.id
    access_list = ("0","1")

    for x in mycol.find():
        if x.get("id") == str(user_id):
            level = x.get("access_level")
            if level not in access_list:
                return update.message.reply_text("Denied")
        else:
            return update.message.reply_text("Denied")


    FileID = update.message.video.file_id[20:]
    print (FileID)
    newFile = update.message.video.get_file()
    newFile.download(saddness.temp + '/media/video/' + FileID + '.mp4')
    update.message.reply_text('Hmmm... Uploaded ┬┴┬┴┤(･_├┬┴┬┴')

def document(update, context):
    user_id = update.message.from_user.id
    access_list = ("0","1")

    for x in mycol.find():
        if x.get("id") == str(user_id):
            level = x.get("access_level")
            if level not in access_list:
                return update.message.reply_text("Denied")
        else:
            return update.message.reply_text("Denied")


    FileID = update.message.document.file_id[20:]
    print (FileID)
    newFile = update.message.document.get_file()
    newFile.download(saddness.temp + '/media/document/' + FileID)
    update.message.reply_text('Hmmm... Uploaded ┬┴┬┴┤(･_├┬┴┬┴')

def local_file_rename(update, context):
    user_id = update.message.from_user.id
    access_list = ("0","1")

    for x in mycol.find():
        if x.get("id") == str(user_id):
            level = x.get("access_level")
            if level not in access_list:
                return update.message.reply_text("Denied")
        else:
            return update.message.reply_text("Denied")


    os.system('aplay '+ saddness.temp + '/media/.bot_media/function.wav')
    URL = update.message.text.strip("/file_rename")[1:].split('/')
    URL2 = URL[1].split()
    URL = URL + URL2
    del URL[1]
    print('mv ' + saddness.temp + '/media/' + URL[0] + "/" + URL[1] + ' ' + saddness.temp + '/media/' + URL[0] + "/" + URL[2])
    os.system('sudo mv ' + saddness.temp + '/media/' + URL[0] + "/" + URL[1] + ' ' + saddness.temp + '/media/' + URL[0] + "/" + URL[2])
    update.message.reply_text('File renamed 🌚')

def local_folder_edit(update, context):
    user_id = update.message.from_user.id
    access_list = ("0","1")

    for x in mycol.find():
        if x.get("id") == str(user_id):
            level = x.get("access_level")
            if level not in access_list:
                return update.message.reply_text("Denied")
        else:
            return update.message.reply_text("Denied")


    os.system('aplay '+ saddness.temp + '/media/.bot_media/function.wav')
    URL = update.message.text.strip("/file_delete")[1:]
    print(saddness.temp + '/media/' + URL)
    os.system('sudo rm ' + saddness.temp + '/media/' + URL)
    update.message.reply_text('File removed \n ༼ つ ಥ_ಥ ༽つ ')

####Authorization

def admin_help(update, context):
    user_id = update.message.from_user.id

    for x in mycol.find():
        if x.get("id") == str(user_id):
            print("has_access, showing media")
        else:
            return update.message.reply_text("Denied")
            
    update.message.reply_text('Help! \n \n'
+'/getID - get your telegram ID \n'
+'/auth - check if registered \n'
+'/req + code - request access \n'
+'/req_code - get a code for your access level to share with unregistered user \n'
+'/del_user + id - delete user from DB \n'
+'/update_user + id/access level + old value + new value - update users id or access level \n'
+'/update_code + old value + new value - change a specified code \n \n'
+'/view_users - list all users \n'
+'/view_codes - list all codes')

def getID(update, context):
    user_id = update.message.from_user.id
    print(update.message.reply_text(user_id))

def auth(update, context):
    user_id = update.message.from_user.id

    for x in mycol.find():
        if x.get("id") == str(user_id):
            print(update.message.reply_text("You are in DB"))
        else:
            return update.message.reply_text("Not yet regitered")

def request_access(update, context):
    user_id = update.message.from_user.id
    code = update.message.text.strip("/req")[1:]
    pass_auth = 'false'
    level = ''

    for x in mycol2.find():
        if x.get("code") == code:
            pass_auth = 'true'
            x = mycol2.find_one(code)
            level = x.get("access_level")
        else:
            return update.message.reply_text("Denied")

    for x in mycol.find():
        if x.get("id") == str(user_id):
            print(update.message.reply_text("You are in DB"))

        elif pass_auth == 'true':
            new_user = { "id": str(user_id), "access_level":level}
            print(update.message.reply_text("You are in DB"))
        
        else:
            return update.message.reply_text("Denied")

def request_code(update, context):
    user_id = update.message.from_user.id
    code = update.message.text.strip("/req_code")[1:]
    level = ''

    for x in mycol.find():
        if x.get("id") == str(user_id):
            level = x.get("access_level")
        else:
            return update.message.reply_text("Denied")

    code_level = mycol2.find_one({"access_level":level})
    update.message.reply_text(code_level.get("code"))

def delete_user(update, context):
    user_id = update.message.from_user.id
    other_id = update.message.text.strip("/del_user")[1:]
    level = ''

    for x in mycol.find():
        if x.get("id") == str(user_id):
            level = x.get("access_level")
            if level != "0":
                return update.message.reply_text("Denied")
        else:
            return update.message.reply_text("Denied")
    
    user = { "id": other_id }
    mycol2.delete_one(user)
    update.message.reply_text("deleted "+other_id)

def view_all(update, context):
    user_id = update.message.from_user.id
    level = ''

    for x in mycol.find():
        if x.get("id") == str(user_id):
            level = x.get("access_level")
            if level != "0":
                return update.message.reply_text("Denied")
        else:
            return update.message.reply_text("Denied")
    
    for x in mycol.find():
        update.message.reply_text(x.get("id") + " : access_level " + x.get("access_level"))

def update_user(update, context):
    user_id = update.message.from_user.id
    other_id = update.message.text.strip("/update_user").split()
    level = ''
    access_list = ['0','1','2']

    for x in mycol.find():
        if x.get("id") == str(user_id):
            level = x.get("access_level")
            if level != "0":
                return update.message.reply_text("Denied")
        else:
            return update.message.reply_text("Denied")
    
    user = { other_id[0] : other_id[1] }
    user_upd = { "$set": { other_id[0] : other_id[2] } }

    if other_id[0] == "id":
        if other_id[2] in access_list:
            mycol.update_one(user, user_upd)
            update.message.reply_text("Updated user ID")
        else:
            return update.message.reply_text("Wrong data")
    elif other_id[0] == "access_level":
        if other_id[2] in access_list:
            mycol.update_one(user, user_upd)
            update.message.reply_text("Updated user's access")
        else:
            return update.message.reply_text("Wrong data")
    else:
        return update.message.reply_text("Wrong data")

def update_code(update, contenxt):
    user_id = update.message.from_user.id
    other_id = update.message.text.strip("/update_code").split()
    level = ''

    for x in mycol.find():
        if x.get("id") == str(user_id):
            level = x.get("access_level")
            if level != "0":
                return update.message.reply_text("Denied")
        else:
            return update.message.reply_text("Denied")
    
    code = { other_id[0] : other_id[1] }
    code_upd = { "$set": { other_id[0] : other_id[2] } }

    if other_id[0] == "code":
        mycol2.update_one(code, code_upd)
        update.message.reply_text("Code updated")
    else:
        return update.message.reply_text("Wrong data")

def view_all_codes(update, context):
    user_id = update.message.from_user.id
    level = ''

    for x in mycol.find():
        if x.get("id") == str(user_id):
            level = x.get("access_level")
            if level != "0":
                return update.message.reply_text("Denied")
        else:
            return update.message.reply_text("Denied")
    
    for x in mycol2.find():
        update.message.reply_text(x.get("code") + " : access_level " + x.get("access_level"))

####

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram

    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("hi", start))

    # Youtube

    dp.add_handler(CommandHandler("yt", youtube_play))
    dp.add_handler(CommandHandler("yt_last", youtube_play_last_track))
    dp.add_handler(CommandHandler("yt_playlist", youtube_play_playlist))
    dp.add_handler(CommandHandler("yt_last_playlist", youtube_play_last))
    dp.add_handler(CommandHandler("yt_playlist_int_cur", youtube_playlist_int_cur))
    dp.add_handler(CommandHandler("yt_playlist_int_set", youtube_playlist_int_set))
    dp.add_handler(CommandHandler("yt_local", youtube_play_local))

    # Spotify

    dp.add_handler(CommandHandler("sp_playlist", spotify_playlist)) 
    dp.add_handler(CommandHandler("sp", spotify_track))

    # Local playlist

    dp.add_handler(CommandHandler("local", youtube_local))
    dp.add_handler(CommandHandler("local_view", local_playlist_view))
    dp.add_handler(CommandHandler("local_edit", local_playlist_edit))
    dp.add_handler(CommandHandler("local_purge", youtube_local_purge))

    # Playback

    dp.add_handler(CommandHandler("play", play_audio))
    dp.add_handler(CommandHandler("play_video", play_video))
    dp.add_handler(CommandHandler("stop", stop_playback))
    dp.add_handler(CommandHandler("pause", pause_playback))
    dp.add_handler(CommandHandler("cont", continue_playback))

    # volume

    dp.add_handler(CommandHandler("volume", volume))
    dp.add_handler(CommandHandler("cur_volume", volume_cur))



    # File System 

    dp.add_handler(CommandHandler("ls", show_media))
    dp.add_handler(CommandHandler("dw", download_media))
    dp.add_handler(CommandHandler("file_delete", local_folder_edit))
    dp.add_handler(CommandHandler("file_rename", local_file_rename))


    # Random

    dp.add_handler(CommandHandler("q", search))
    dp.add_handler(CommandHandler("imdb", search_movie))
    dp.add_handler(CommandHandler("w", weather))
    dp.add_handler(CommandHandler("git", git))
    dp.add_handler(CommandHandler("cmd", OS))
    

    # Authentication

    dp.add_handler(CommandHandler("admin_help", admin_help))
    dp.add_handler(CommandHandler("getID", getID))
    dp.add_handler(CommandHandler("auth", auth))
    dp.add_handler(CommandHandler("req", request_access))
    dp.add_handler(CommandHandler("req_code", request_code))
    dp.add_handler(CommandHandler("del_user", delete_user))
    dp.add_handler(CommandHandler("update_user", update_user))
    dp.add_handler(CommandHandler("update_code", update_code))
    dp.add_handler(CommandHandler("view_users", view_all))
    dp.add_handler(CommandHandler("view_codes", view_all_codes))
    

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(MessageHandler(Filters.photo, photo))
    dp.add_handler(MessageHandler(Filters.voice, voice))
    dp.add_handler(MessageHandler(Filters.video, video))
    dp.add_handler(MessageHandler(Filters.document, document))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
