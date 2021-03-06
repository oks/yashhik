from telegram.ext import Updater, MessageHandler, Filters
from pytube import YouTube

import logging
logging.getLogger().setLevel(logging.DEBUG)

from yandex import sendToScreen
import config


last_url = ""

def getVideoUrl(url):

    global last_url

    if url == last_url:  # Second attempt - trying another player
        yt = YouTube(url).streams.first()
        last_url = url
        return yt.url

    last_url = url

    if "www.youtube" in url:
        url = url.split("&")[0]  # Removing arguments

    if "https://youtu.be" in url:
        url = "https://www.youtube.com/watch?v=" + url.split("/")[-1]

    # Page parsing and getting video_url here
    return url


def extractUrl(message):
    return message.text  # TODO: getting url by entities info


def message_recieved(bot, update):

    user_id = update.message.chat_id
    # TODO: get yandex configs based on user_id

    print(update.message)

    url = extractUrl(update.message)
    video_url = getVideoUrl(url)
    result = sendToScreen(video_url)

    print(result)

    bot.send_message(chat_id=update.message.chat_id, text=result + video_url)


updater = Updater(token=config.telegram_bot_token, request_kwargs=config.proxy)

message_handler = MessageHandler(Filters.all, message_recieved)
updater.dispatcher.add_handler(message_handler)

print("Start polling...")

updater.start_polling()

