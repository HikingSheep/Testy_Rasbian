#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import string
import duckduckgo
import imdb

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from spotify import get_playlist, get_track


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
ia = imdb.IMDb()

class saddness:
    vol = "50"
    temp = "/home/pi/Testy_Rasbian/teleBot"
    #temp = "/home/hopu/Desktop/Testy_Rasbian/teleBot"
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
+'/dw + /location/file name - download specified file \n \n'
+'**/play function was tested only on youtube, vk, vimeo \n'
+'Since Spotfiy has a lot of restrictions, it allows playback only through certified applications and Web Player \n \n'
+'***Drop images, video or documents in chat to upload them to the host machine \n \n'
+'****File system includes folders that are not visible through ```/ls``` command, however, if the folder name is knonw, it can be opened (currently available hidden folders: .bot_media, .playlist, .local_playlist, .track). Therefore, these files can be downloaded manually ^_^ \n')


####Youtube

def youtube_play(update, context):
    os.system('aplay '+ saddness.temp + '/media/.bot_media/function.wav && sudo rm ' + saddness.temp + '/media/.track/*.webm')
    song_name = open(saddness.temp + '/temp/name.txt', 'r') 
    os.system('pkill mpv')
    URL = update.message.text.strip("/yt").encode('utf-8')
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
    os.system('aplay '+ saddness.temp + '/media/.bot_media/function.wav')
    song_name = open(saddness.temp + '/temp/name.txt', 'r') 
    update.message.reply_text('Playing... ~(˘▾˘~)\n' + song_name.readline() + '\n' + 'https://youtu.be/' + song_name.readline())
    os.system('$(mpv --playlist ' + saddness.temp + '/media/.track/ >/dev/null 2>&1 &)')
    song_name.close()
    
    
    
def youtube_play_local(update, context):
    os.system('aplay '+ saddness.temp + '/media/.bot_media/function.wav')
    song_name = open(saddness.temp + '/temp/name.txt', 'r') 
    os.system('pkill mpv')
    URL = update.message.text.strip("/yt_local ").encode('utf-8')
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
    os.system('pkill mpv')
    os.system('aplay '+ saddness.temp + '/media/.bot_media/function.wav && sudo rm ' + saddness.temp + '/media/.local_playlist/* && sudo rm ' + saddness.temp + '/media/.track/*')
    update.message.reply_text('Removed all local playlist media \n ༼ つ ಥ_ಥ ༽つ ')

def local_playlist_view(update, context):
    os.system('aplay '+ saddness.temp + '/media/.bot_media/function.wav')
    os.system('cd '+ saddness.temp + '/media/.local_playlist && ls > ' + saddness.temp + '/temp/local_list.txt')
    file_list = open(saddness.temp + '/temp/local_list.txt', 'r')
    update.message.reply_text(file_list.read())
    file_list.close()
    
def local_playlist_edit(update, context):
    os.system('pkill mpv')
    keyword = update.message.text.strip("/local_edit ").encode('utf-8')
    os.system('sudo rm ' + saddness.temp + '/media/.local_playlist/"' + keyword + '" ')
    update.message.reply_text('File: \n' + keyword + '\n was removed (;´༎ຶД༎ຶ`)\n')
    os.system('cd '+ saddness.temp + '/media/.local_playlist && ls > ' + saddness.temp + '/temp/local_list.txt')
    file_list = open(saddness.temp + '/temp/local_list.txt', 'r')
    update.message.reply_text(file_list.read())
    file_list.close()
    


def youtube_play_playlist(update, context):
    os.system('aplay '+ saddness.temp + '/media/.bot_media/function.wav && rm ' + saddness.temp + '/media/.playlist/*')
    song_name = open(saddness.temp + '/temp/playlist.txt', 'r') 
    os.system('pkill mpv')
    URL = update.message.text.strip("/yt_playlist").replace(" ","").encode('utf-8')
    update.message.reply_text('Fetching playlist data...')
    os.system('youtube-dl --skip-unavailable-fragments --yes-playlist --playlist-items ' + saddness.playlist_int + ' -o "' + saddness.temp + '/media/.playlist/%(title)s" -f bestaudio ' + URL)
    os.system('cd ' + saddness.temp + '/media/.playlist && ls > ' + saddness.temp + '/temp/playlist.txt')
    update.message.reply_text('Playing... (~˘▾˘)~ \n')
    update.message.reply_text(song_name.read())
    song_name.close()
    os.system('$(mpv --no-video --playlist ' + saddness.temp + '/media/.playlist/ >/dev/null 2>&1 &)')

def youtube_play_last(update, context):
    os.system('aplay '+ saddness.temp + '/media/.bot_media/function.wav && pkill mpv')  
    song_name = open(saddness.temp + '/temp/playlist.txt', 'r') 
    update.message.reply_text('Fetching playlist data... \n \n' + song_name.read())
    song_name.close()
    update.message.reply_text('Playing... (~˘▾˘)~\n')
    os.system('$(mpv --playlist ' + saddness.temp + '/media/.playlist/ >/dev/null 2>&1 &)')
    
def youtube_playlist_int_cur(update, context):
    update.message.reply_text(saddness.playlist_int)

def youtube_playlist_int_set(update, context):
    update.message.reply_text('Changing to... \n' + update.message.text.strip("/yt_playlist_int_set ").replace(" ",""))
    saddness.playlist_int = update.message.text.strip("/yt_playlist_int_set ").replace(" ","")

####Spotify

def spotify_playlist(update, context):
    keyword = update.message.text.strip("/sp_playlist ").encode('utf-8')
    update.message.reply_text('Enjoy your playlist! \n' + get_playlist(str(keyword)))

def spotify_track(update, context):
    keyword = update.message.text.strip("/sp ").encode('utf-8')
    update.message.reply_text('Enjoy your track! \n' + get_track(keyword))

####Play other


def play_audio(update, context):
    os.system('aplay '+ saddness.temp + '/media/.bot_media/function.wav')
    os.system('pkill mpv')
    update.message.reply_text('Playing... (~˘▾˘)~\n')
    URL = update.message.text.strip("/play").encode('utf-8')
    os.system('$(mpv --no-video ' + URL + ' >/dev/null 2>&1 &)')

def play_video(update, context):
    os.system('aplay '+ saddness.temp + '/media/.bot_media/function.wav')
    os.system('pkill mpv')
    update.message.reply_text('Playing... (~˘▾˘)~\n')
    URL = update.message.text.strip("/play_video").encode('utf-8')
    os.system('mpv ' + URL)


####Playback options 

def pause_playback(update, context):
    os.system('aplay '+ saddness.temp + '/media/.bot_media/function.wav')
    update.message.reply_text('Pause...')
    os.system('pkill mpv -STOP')

def continue_playback(update, context):
    os.system('aplay '+ saddness.temp + '/media/.bot_media/function.wav')
    update.message.reply_text('Continuing...')
    os.system('pkill mpv -CONT')

def stop_playback(update, context):
    os.system('aplay '+ saddness.temp + '/media/.bot_media/function.wav')
    update.message.reply_text('Stopping...')
    os.system('pkill mpv')

####Volume

def volume(update, context):
    os.system('aplay '+ saddness.temp + '/media/.bot_media/function.wav')
    update.message.reply_text('Changing to... \n' + update.message.text.strip("/volume ").replace(" ","") + '%')
    saddness.vol = update.message.text.strip("/volume ").replace(" ","").replace("%","")
    os.system('amixer -D pulse sset Master ' + saddness.vol + '%')

def volume_cur(update, context):
    update.message.reply_text(saddness.vol + '%')

####DuckDuckGo

def search(update, context):
    query = update.message.text.strip("/q ").encode('utf-8')
    update.message.reply_text(duckduckgo.get_zci(query))
    print (duckduckgo.get_zci(query))

####IMDb

def search_movie(update, context):
    keyword = update.message.text.strip("/imdb ").encode('utf-8')
    movies = ia.search_movie(keyword)
    url = ia.get_imdbURL(movies[0])
    update.message.reply_text(str(movies[0]['title']) + '\n https://www.imdb.com/title/tt' + str(movies[0].movieID))

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
    command = update.message.text.strip("/cmd").encode('utf-8')
    os.system(command)

####File System

def show_media(update, context):
    keyword = update.message.text.strip("/ls ")
    os.system('cd '+ saddness.temp + '/media/' + keyword + ' && ls > ' + saddness.temp + '/temp/list.txt')
    file_list = open(saddness.temp + '/temp/list.txt', 'r')
    update.message.reply_text(file_list.read())
    file_list.close()

def download_media(update, context):
    URL = update.message.text.strip("/dw").replace(" ","").encode('utf-8')
    update.message.bot.send_document(chat_id = update.message.chat_id, filename=URL, document=open(saddness.temp + '/media' + URL, 'rb'))
    update.message.reply_text('Downloading from storage... ' + URL)

def voice(update, context):
    FileID = update.message.voice.file_id[20:]
    print (FileID)
    newFile = update.message.voice.get_file()
    newFile.download(saddness.temp + "/media/audio/" + FileID + '.mp3')
    update.message.reply_text('Hmmm... Uploaded ┬┴┬┴┤(･_├┬┴┬┴')

def photo(update, context):
    FileID = update.message.photo[-1].file_id[40:]
    print (FileID)
    newFile = update.message.photo[-1].get_file()
    newFile.download(saddness.temp + "/media/image/" + FileID + '.jpg')
    update.message.reply_text('Hmmm... Uploaded ┬┴┬┴┤(･_├┬┴┬┴')

def video(update, context):
    FileID = update.message.video.file_id[20:]
    print (FileID)
    newFile = update.message.video.get_file()
    newFile.download(saddness.temp + "/media/video/" + FileID + '.mp4')
    update.message.reply_text('Hmmm... Uploaded ┬┴┬┴┤(･_├┬┴┬┴')

def document(update, context):
    FileID = update.message.document.file_id[20:]
    print (FileID)
    newFile = update.message.document.get_file()
    newFile.download(saddness.temp + "/media/document/" + FileID)
    update.message.reply_text('Hmmm... Uploaded ┬┴┬┴┤(･_├┬┴┬┴')

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

    # Random

    dp.add_handler(CommandHandler("q", search))
    dp.add_handler(CommandHandler("imdb", search_movie))
    dp.add_handler(CommandHandler("git", git))
    dp.add_handler(CommandHandler("cmd", OS))
    
    

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
