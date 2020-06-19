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
        update.message.reply_sticker('CAACAgIAAxkBAAIJ9l7qpUCvzZVRWaWd1y0VMvVOJLV_AAIwAQACpkRICxFy70LZy4AdGgQ')
        update.message.reply_html(str(weatherData[0]) + ", " + str(weatherData[1]) + "\n\n"
        + "<b>Temperature</b>: " + str(weatherData[2]) + " C" + "\n"
        + "<b>Feels like</b>: " + str(weatherData[3]) + " C" + "\n"
        + "<b>Humidity</b>: " + str(weatherData[4]) + " %" + "\n"
        + "<b>Wind</b>: " + str(weatherData[5]) + " m/s" + "\n"
        + "<b>Sunrise</b>: " + str(weatherData[6])[11:] + "\n"
        + "<b>Sunset</b>: " + str(weatherData[7])[11:] + "\n\n"
        + str(weatherData[8]).capitalize()) 

    

    

####Random

def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)
    print(update.message)

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
