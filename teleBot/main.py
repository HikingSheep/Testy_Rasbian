#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from spotify import get_playlist, get_track

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

os.system('pulseaudio --start && amixer -D pulse sset Master 50%')

class saddness:
    vol = "50"
    temp = "/home/pi/Desktop/Testy_Rasbian/teleBot"

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help! \n'
+'/yt + URL/keywords - play a song from youtube \n'
+'/stop - stop audio playback \n'
+'/pasue - pause audio playback \n'
+'/cont - continue audio playback \n'
+'/volume + INT (e.g. 50 = 50%) - change volume to INT \n'
+'/cur_volume - get current volume\n'
+'/play + URL - play audio from any website/link \n'
#+'/sp + keywords - find a track on spotify \n'
+'/sp_playlist + keywords - find a playlist on spotify \n \n'
+'**/play function was tested only on youtube, vk, vimeo \n'
+'Since Spotfiy has a lot of restrictions, it allows playback only through certified applications and Web Player \n \n'
+'***Drop images, video or documents in chat to upload them to the host machine \n')

def youtube_play(update, context):
    song_name = open(saddness.temp + '/temp/name.txt', 'r') 
    os.system('pkill mpv')
    URL = update.message.text.strip("/yt ").replace(" ","").encode('utf-8')
    os.system('$(youtube-dl -o - ytsearch:' + URL + '| mpv --no-video - >/dev/null 2>&1 &)'
+' && youtube-dl --get-title ytsearch:' + URL + ' > ' + saddness.temp + '/temp/name.txt' 
+' && youtube-dl --get-id ytsearch:' + URL + ' >> ' + saddness.temp + '/temp/name.txt')
    update.message.reply_text('Playing... \n' + song_name.readline() + '\n' + 'https://youtu.be/' + song_name.readline())
    song_name.close()

def youtube_play_playlist(update, context):
    song_name = open(saddness.temp + '/temp/name.txt', 'r') 
    os.system('pkill mpv')
    URL = update.message.text.strip("/yt_playlist ").replace(" ","").encode('utf-8')
    os.system('youtube-dl --get-title '+ URL +' > ' + saddness.temp + '/temp/name.txt')
    update.message.reply_text('Playing playlist... \n' + song_name.read())
    song_name.close()
    os.system('youtube-dl --skip-unavailable-fragments --yes-playlist -i -o - '+ URL +' | mpv --no-video - ')


def play_other(update, context):
    os.system('pkill mpv')
    update.message.reply_text('Playing... \n' + update.message.text.strip("/play "))
    URL = update.message.text.strip("/play").replace(" ","").encode('utf-8')
    os.system('$(mpv --no-video ' + URL + ' >/dev/null 2>&1 &)')

def pause_playback(update, context):
    update.message.reply_text('Pause...')
    os.system('pkill mpv -STOP')

def continue_playback(update, context):
    update.message.reply_text('Continuing...')
    os.system('pkill mpv -CONT')

def stop_playback(update, context):
    update.message.reply_text('Stopping...')
    os.system('pkill mpv')

def volume(update, context):
    update.message.reply_text('Changing to... \n' + update.message.text.strip("/volume ").replace(" ","") + '%')
    saddness.vol = update.message.text.strip("/volume ").replace(" ","").replace("%","")
    os.system('amixer -D pulse sset Master ' + saddness.vol + '%')

def volume_cur(update, context):
    update.message.reply_text(saddness.vol + '%')


def voice(update, context):
    FileID = update.message.voice.file_id
    print (FileID)
    newFile = update.message.voice.get_file()
    newFile.download(FileID)
    update.message.reply_text('Hmmm... Uploaded -_-')

def photo(update, context):
    FileID = update.message.photo[-1].file_id
    print (FileID)
    newFile = update.message.photo[-1].get_file()
    newFile.download(saddness.temp + "/media/images/" + FileID)
    update.message.reply_text('Hmmm... Uploaded -_-')

def video(update, context):
    FileID = update.message.video.file_id
    print (FileID)
    newFile = update.message.video.get_file()
    newFile.download(saddness.temp + "/media/video/" + FileID)
    update.message.reply_text('Hmmm... Uploaded -_-')

def document(update, context):
    FileID = update.message.document.file_id
    print (FileID)
    newFile = update.message.document.get_file()
    newFile.download(saddness.temp + "/media/documents/" + FileID)
    update.message.reply_text('Hmmm... Uploaded -_-')

def spotify_playlist(update, context):
    keyword = update.message.text.strip("/sp_playlist ").encode('utf-8')
    update.message.reply_text('Enjoy your playlist! \n' + get_playlist(str(keyword)))

def spotify_track(update, context):
    keyword = update.message.text.strip("/sp ").replace(" ","").encode('utf-8')
    update.message.reply_text('Enjoy your track! \n' + get_track(str(keyword)))
 

def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    dp.add_handler(CommandHandler("yt", youtube_play))
    dp.add_handler(CommandHandler("yt_playlist", youtube_play_playlist))
    dp.add_handler(CommandHandler("play", play_other))
    dp.add_handler(CommandHandler("volume", volume))
    dp.add_handler(CommandHandler("cur_volume", volume_cur))

    dp.add_handler(CommandHandler("stop", stop_playback))
    dp.add_handler(CommandHandler("pause", pause_playback))
    dp.add_handler(CommandHandler("cont", continue_playback))

    dp.add_handler(CommandHandler("sp_playlist", spotify_playlist)) 
#    dp.add_handler(CommandHandler("sp", spotify_track))

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
