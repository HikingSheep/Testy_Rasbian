#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import string
import duckduckgo

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from spotify import get_playlist, get_track

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

class saddness:
    vol = "50"
    temp = "/home/pi/Testy_Rasbian/teleBot"
    playlist_int = '1-15'


os.system('pulseaudio --start && amixer -D pulse sset Master 50% && aplay ' + saddness.temp + '/media/.bot_media/start.wav && aplay ' + saddness.temp + '/start.wav')


def start(update, context):
    os.system('aplay '+ saddness.temp + '/function.wav && aplay ' + saddness.temp + '/media/.bot_media/function.wav')
    print(update.message.reply_text('Hi, Meatbag!'))

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help! \n'
+'/yt + URL/keywords - play a song from youtube \n'
+'/yt_playlist + URL - play a playlist from youtube \n'
+'/stop - stop audio playback \n'
+'/pasue - pause audio playback \n'
+'/cont - continue audio playback \n'
+'/volume + INT (e.g. 50 = 50%) - change volume to INT \n'
+'/cur_volume - get current volume\n'
+'/play + URL - play audio from any website/link \n'
+'/sp + keywords - find a track on spotify \n'
+'/sp_playlist + keywords - find a playlist on spotify \n \n'
+'/ls - list available file system directories \n'
+'/ls + available folder name - list files in the specified folder \n'
+'/dw + /location/file name - download specified file \n \n'
+'/git - request git repository link \n \n'
+'**/play function was tested only on youtube, vk, vimeo \n'
+'Since Spotfiy has a lot of restrictions, it allows playback only through certified applications and Web Player \n \n'
+'***Drop images, video or documents in chat to upload them to the host machine \n')


####Youtube

def youtube_play(update, context):
    song_name = open(saddness.temp + '/temp/name.txt', 'r') 
    os.system('pkill mpv')
    URL = update.message.text.strip("/yt ").replace(" ","").encode('utf-8')
    os.system('$(youtube-dl -f worst -o - ytsearch:' + URL + '| mpv --no-video - >/dev/null 2>&1 &)'
+' && youtube-dl --get-title ytsearch:' + URL + ' > ' + saddness.temp + '/temp/name.txt' 
+' && youtube-dl --get-id ytsearch:' + URL + ' >> ' + saddness.temp + '/temp/name.txt')
    update.message.reply_text('Playing... \n' + song_name.readline() + '\n' + 'https://youtu.be/' + song_name.readline())
    song_name.close()

def youtube_play_playlist(update, context):
    song_name = open(saddness.temp + '/temp/name.txt', 'r') 
    os.system('pkill mpv && rm ' + saddness.temp + '/media/.playlist/*.webm')
    URL = update.message.text.strip("/yt_playlist ").replace(" ","").encode('utf-8')
    os.system('youtube-dl --get-title '+ URL +' > ' + saddness.temp + '/temp/name.txt')
    update.message.reply_text('Playing playlist... \n' + song_name.read())
    song_name.close()
    update.message.reply_text('Downloading... Please wait')
    os.system('$(youtube-dl --skip-unavailable-fragments --yes-playlist --playlist-items ' + saddness.playlist_int + ' -o "' + saddness.temp + '/media/.playlist/%(title)s-%(id)s.%(ext)s" -f bestaudio' + URL+ ' >/dev/null 2>&1 &)')
    update.message.reply_text('Playing...')
    os.system('$(mpv --playlist ' + URL + 'media/.playlist/ >/dev/null 2>&1 &)')

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


def play_other(update, context):
    os.system('pkill mpv')
    update.message.reply_text('Playing... \n' + update.message.text.strip("/play "))
    URL = update.message.text.strip("/play").replace(" ","").encode('utf-8')
    os.system('$(mpv --no-video ' + URL + ' >/dev/null 2>&1 &)')


####Playback options 

def pause_playback(update, context):
    update.message.reply_text('Pause...')
    os.system('pkill mpv -STOP')

def continue_playback(update, context):
    update.message.reply_text('Continuing...')
    os.system('pkill mpv -CONT')

def stop_playback(update, context):
    update.message.reply_text('Stopping...')
    os.system('pkill mpv')

####Volume

def volume(update, context):
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

    ###TODO

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
    update.message.reply_text('Hmmm... Uploaded -_-')

def photo(update, context):
    FileID = update.message.photo[-1].file_id[40:]
    print (FileID)
    newFile = update.message.photo[-1].get_file()
    newFile.download(saddness.temp + "/media/image/" + FileID + '.jpg')
    update.message.reply_text('Hmmm... Uploaded -_-')

def video(update, context):
    FileID = update.message.video.file_id[20:]
    print (FileID)
    newFile = update.message.video.get_file()
    newFile.download(saddness.temp + "/media/video/" + FileID + '.mp4')
    update.message.reply_text('Hmmm... Uploaded -_-')

def document(update, context):
    FileID = update.message.document.file_id[20:]
    print (FileID)
    newFile = update.message.document.get_file()
    newFile.download(saddness.temp + "/media/document/" + FileID)
    update.message.reply_text('Hmmm... Uploaded -_-')

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

    dp.add_handler(CommandHandler("yt", youtube_play))
    dp.add_handler(CommandHandler("yt_playlist", youtube_play_playlist))
    dp.add_handler(CommandHandler("yt_playlist_int_cur", youtube_playlist_int_cur))
    dp.add_handler(CommandHandler("yt_playlist_int_set", youtube_playlist_int_set))
    dp.add_handler(CommandHandler("play", play_other))
    dp.add_handler(CommandHandler("volume", volume))
    dp.add_handler(CommandHandler("cur_volume", volume_cur))

    dp.add_handler(CommandHandler("stop", stop_playback))
    dp.add_handler(CommandHandler("pause", pause_playback))
    dp.add_handler(CommandHandler("cont", continue_playback))

    dp.add_handler(CommandHandler("sp_playlist", spotify_playlist)) 
    dp.add_handler(CommandHandler("sp", spotify_track))

    dp.add_handler(CommandHandler("ls", show_media))
    dp.add_handler(CommandHandler("dw", download_media))

    dp.add_handler(CommandHandler("q", search))
    dp.add_handler(CommandHandler("git", git))

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
