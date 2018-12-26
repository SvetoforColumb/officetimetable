import os

from flask import Flask, request

import config
import markups
import telebot
from telebot import TeleBot
import dbworker

bot = telebot.TeleBot(config.token)
server = Flask(__name__)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hi! it's your timekeep bot!\n use this bot to manage your reminds",
                     reply_markup=markups.markup_main)
    print(str(message))
    #dbworker.addUser()


@bot.message_handler(func=lambda message: "Make a note" in message.text)
def handle(message):
    bot.send_message(message.chat.id, "OK")




@server.route('/' + config.token, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://officetimetable.herokuapp.com/' + config.token)
    return "!", 200


server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
