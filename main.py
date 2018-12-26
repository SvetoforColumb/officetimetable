import datetime
import os
from multiprocessing import Process
from time import sleep

from flask import Flask, request

import config
import markups

import telebot
import telegramcalendar
import dbworker

current_shown_dates = {}
bot = telebot.TeleBot(config.token)
server = Flask(__name__)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hi! it's your timekeep bot!\n use this bot to manage your reminds ",
                     reply_markup=markups.markup_main)
    bot.send_message(message.chat.id, str(message))
    name = message.chat.first_name
    if message.chat.last_name != "None":
        name = name + message.chat.last_name
    username = ' '
    if message.chat.username != "None":
        username = message.chat.username
    dbworker.addUser(message.chat.id, name, username)


@bot.message_handler(func=lambda message: "Make a note" in message.text)
def make(message):
    bot.send_message(message.chat.id, "Enter a text of note")
    dbworker.setState(message.chat.id, config.States.ENTER_TEXT.value)


@bot.message_handler(func=lambda message: str(dbworker.getState(message.chat.id)[0]) == config.States.ENTER_TEXT.value)
def text(message):
    dbworker.addNote(message.chat.id, message.text)
    bot.send_message(message.chat.id, "Text added")
    bot.send_message(message.chat.id, "Would you like to set up remind?", reply_markup=markups.yes_no_markup)
    dbworker.setState(message.chat.id, config.States.TEXT_ADDED.value)


@bot.callback_query_handler(func=lambda call: call.data == "add_remind_yes")
def callback(call):
    now = datetime.datetime.now()
    chat_id = call.message.chat.id
    date = (now.year, now.month)
    current_shown_dates[chat_id] = date
    markup_calendar = telegramcalendar.create_calendar(now.year, now.month)
    bot.send_message(call.message.chat.id, "What date?", reply_markup=markup_calendar)


@bot.message_handler(func=lambda message: "View notes" in message.text)
def view(message):
    bot.send_message(message.chat.id, "SEE")


class Reminder:
    def __call__(self, *args, **kwargs):
        while True:
            now = datetime.datetime.now()
            # n_time = str(now.time())[0] + str(now.time())[1]
            # a_time = str(int(n_time) + 1)
            # r_day = str(now.month)
            # if now.month == 1:
            #     r_month = "01"
            # elif now.month == 2:
            #     r_month = "02"
            # elif now.month == 2:
            #     r_month = "02"
            # elif now.month == 3:
            #     r_month = "03"
            # elif now.month == 4:
            #     r_month = "04"
            # elif now.month == 5:
            #     r_month = "05"
            # elif now.month == 6:
            #     r_month = "06"
            # elif now.month == 7:
            #     r_month = "07"
            # elif now.month == 8:
            #     r_month = "08"
            # elif now.month == 9:
            #     r_month = "09"
            # elif now.month == 10:
            #     r_month = "10"
            # elif now.month == 11:
            #     r_month = "11"
            # elif now.month == 12:
            #     r_month = "12"
            # if now.day == 1:
            #     r_day = "01"
            # elif now.day == 2:
            #     r_day = "02"
            # elif now.day == 2:
            #     r_day = "02"
            # elif now.day == 3:
            #     r_day = "03"
            # elif now.day == 4:
            #     r_day = "04"
            # elif now.day == 5:
            #     r_day = "05"
            # elif now.day == 6:
            #     r_day = "06"
            # elif now.day == 7:
            #     r_day = "07"
            # elif now.day == 8:
            #     r_day = "08"
            # elif now.day == 9:
            #     r_day = "09"
            # elif now.day == 10:
            #     r_day = "10"
            # elif now.day == 11:
            #     r_day = "11"
            # elif now.day == 12:
            #     r_day = "12"
            # elif now.day == 13:
            #     r_day = "13"
            # elif now.day == 14:
            #     r_day = "14"
            # elif now.day == 15:
            #     r_day = "15"
            # elif now.day == 16:
            #     r_day = "16"
            # elif now.day == 17:
            #     r_day = "17"
            # elif now.day == 18:
            #     r_day = "18"
            # elif now.day == 19:
            #     r_day = "19"
            # elif now.day == 20:
            #     r_day = "20"
            # elif now.day == 21:
            #     r_day = "21"
            # elif now.day == 22:
            #     r_day = "22"
            # elif now.day == 23:
            #     r_day = "23"
            # elif now.day == 24:
            #     r_day = "24"
            # elif now.day == 25:
            #     r_day = "25"
            # elif now.day == 26:
            #     r_day = "26"
            # elif now.day == 27:
            #     r_day = "27"
            # elif now.day == 28:
            #     r_day = "28"
            # elif now.day == 29:
            #     r_day = "29"
            # elif now.day == 30:
            #     r_day = "30"
            # elif now.day == 31:
            #     r_day = "31"
            # else:
            #     r_day = "0"
            # # bot.send_message(89503357, str(now.year) + '-' + r_month + '-' + r_day + a_time)
            # id1 = dbworker.remindUser(str(now.year) + '-' + r_month + '-' + r_day, a_time)
            # # bot.send_message(89503357, str(now.year) + '-' + r_month + '-' + r_day + " " + a_time + " " + id1 + ' 0' + dbworker.getTelNumber(89503357))
            # c_time = str(now.time())[0] + str(now.time())[1] + ":" + str(now.time())[3] + str(now.time())[4]
            #
            # if id1 != "0" and str(int(dbworker.getTime(id1)) - 1) + ":01" == c_time:
            #     bot.send_message(89503357, id1 + ' ' + c_time + " " + str(int(dbworker.getTime(id1)) - 1) + " " + str(
            #         str(int(dbworker.getTime(id1)) - 1) + ":00" == c_time))
            #     bot.send_message(id1, "Напоминаем, что вы записаны на мойку в " + dbworker.getTime(id1) + ":00")
            # sleep(60)


gettingMsg = Reminder()
p2 = Process(target=gettingMsg)
p2.start()


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
