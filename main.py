import telebot
import os
import config
from flask import Flask, request
import logging

print("172.17.32.42")

bot = telebot.TeleBot(config.token)

# Здесь пишем наши хэндлеры


@bot.message_handler(commands=['start'])
def handle_start_help(message):
    # dbworker.addUser(message.chat.id)
    # now = datetime.datetime.now()
    bot.send_message(message.chat.id, "Hi! This is your time keeper bsot!")


# Проверим, есть ли переменная окружения Хероку (как ее добавить смотрите ниже)
if "HEROKU" in list(os.environ.keys()):
    logger = telebot.logger
    telebot.logger.setLevel(logging.INFO)

    server = Flask(__name__)
    @server.route("/bot", methods=['POST'])
    def getMessage():
        bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
        return "!", 200
    @server.route("/")
    def webhook():
        bot.remove_webhook()
        bot.set_webhook(url="https://officetimetable.herokuapp.com/")
    server.run(host="0.0.0.0", port=os.environ.get('PORT', 80))
else:
    bot.remove_webhook()
    bot.polling(none_stop=True)
