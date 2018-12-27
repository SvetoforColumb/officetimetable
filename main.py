import datetime
import os
import time
from multiprocessing import Process

import telebot

from flask import Flask, request

import config
import markups

import telegramcalendar
import dbworker

current_shown_dates = {}
bot = telebot.TeleBot(config.token)
server = Flask(__name__)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hi! it's your timekeep bot!\nUse this bot to manage your reminds ",
                     reply_markup=markups.getMainMarkup())
    name = message.chat.first_name
    if message.chat.last_name != "None":
        name = name + " " + message.chat.last_name
    username = ' '
    if message.chat.username != "None":
        username = message.chat.username
    dbworker.addUser(message.chat.id, name, username)


@bot.message_handler(func=lambda message: "Make a note" in message.text)
def make(message):
    bot.send_message(message.chat.id, "Enter a text of note", reply_markup=markups.getRemoveMarkup())
    dbworker.setState(message.chat.id, config.States.ENTER_TEXT.value)


@bot.message_handler(func=lambda message: str(dbworker.getState(message.chat.id)[0]) == config.States.ENTER_TEXT.value)
def text(message):
    dbworker.addNote(message.chat.id, message.text)
    bot.send_message(message.chat.id, "Text added")
    bot.send_message(message.chat.id, "Would you like to set up remind?", reply_markup=markups.getYesNoMarkup())
    dbworker.setState(message.chat.id, config.States.TEXT_ADDED.value)


@bot.callback_query_handler(func=lambda call: call.data == "add_remind_no")
def callback(call):
    bot.send_message(call.message.chat.id, "Note added", reply_markup=markups.getMainMarkup())


@bot.callback_query_handler(func=lambda call: call.data == "add_remind_yes")
def callback(call):
    now = datetime.datetime.now()
    chat_id = call.message.chat.id
    date = (now.year, now.month)
    current_shown_dates[chat_id] = date
    markup_calendar = telegramcalendar.create_calendar(now.year, now.month)
    bot.send_message(call.message.chat.id, "What date?", reply_markup=markup_calendar)


@bot.callback_query_handler(func=lambda call: call.data == 'next-month')
def next_month(call):
    chat_id = call.message.chat.id
    saved_date = current_shown_dates.get(chat_id)
    if saved_date is not None:
        year, month = saved_date
        month += 1
        if month > 12:
            month = 1
            year += 1
        date = (year, month)
        current_shown_dates[chat_id] = date
        markup = telegramcalendar.create_calendar(year, month)
        bot.edit_message_text("Choose date", call.from_user.id, call.message.message_id, reply_markup=markup)
        bot.answer_callback_query(call.id, text="")
    else:
        bot.send_message(call.message.chat.id, "2")
        pass


@bot.callback_query_handler(func=lambda call: call.data == 'previous-month')
def previous_month(call):
    chat_id = call.message.chat.id
    saved_date = current_shown_dates.get(chat_id)
    if saved_date is not None:
        year, month = saved_date
        month -= 1
        if month < 1:
            month = 12
            year -= 1
        date = (year, month)
        current_shown_dates[chat_id] = date
        markup = telegramcalendar.create_calendar(year, month)
        bot.edit_message_text("Choose date", call.from_user.id, call.message.message_id, reply_markup=markup)
        bot.answer_callback_query(call.id, text="")
    else:
        bot.send_message(call.message.chat.id, "3")
        pass


@bot.callback_query_handler(func=lambda call: call.data[0:13] == 'calendar-day-')
def get_day(call):
    chat_id = call.message.chat.id
    saved_date = current_shown_dates.get(chat_id)
    if saved_date is not None:
        day = call.data[13:]
        date = datetime.datetime(int(saved_date[0]), int(saved_date[1]), int(day), 0, 0, 0)
        bot.answer_callback_query(call.id, text="")
        normal_date = str(date)[0: -8]
        now = datetime.datetime.now()
        if int(normal_date[0] + normal_date[1] + normal_date[2] + normal_date[3]) <= int(now.year) and int(
                normal_date[5] + normal_date[6]) <= int(now.month) and int(normal_date[8] + normal_date[9]) < int(
                now.day):
            bot.send_message(call.message.chat.id, "This is past", reply_markup=markups.getRemoveMarkup())
            return
        dbworker.setDate(call.message.chat.id, normal_date.strip())
        bot.send_message(call.message.chat.id, "Enter time in format XX:XX", reply_markup=markups.getRemoveMarkup())
        dbworker.setState(call.message.chat.id, config.States.ENTERING_TIME.value)


def isTimeFormat(a):
    try:
        time.strptime(a, '%H:%M')
        return True
    except ValueError:
        return False


@bot.message_handler(
    func=lambda message: str(dbworker.getState(message.chat.id)[0]) == config.States.ENTERING_TIME.value)
def text(message):
    if isTimeFormat(message.text):
        dbworker.setTime(message.chat.id, message.text)
        bot.send_message(message.chat.id, "Reminder added!", reply_markup=markups.getMainMarkup())
        dbworker.setState(message.chat.id, config.States.START.value)
    else:
        bot.send_message(message.chat.id, "Incorrect date")


@bot.message_handler(func=lambda message: "View notes" in message.text)
def view(message):
    last_note_id = dbworker.getLastNotesId(message.chat.id)
    print("last_note_id " + str(last_note_id))
    if last_note_id == '-':
        bot.send_message(message.chat.id, "You don't have notes")
    else:
        note = dbworker.getNotesById(last_note_id)
        bot.send_message(message.chat.id, note, reply_markup=markups.getNoteMarkup(message.chat.id))


@bot.callback_query_handler(func=lambda call: call.data[0:10] == 'next_note-')
def nextNode(call):
    r_node_id = call.data[10:]
    print('next ' + str(r_node_id))
    note = dbworker.getNotesById(r_node_id)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=note)
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=markups.getNoteMarkup(call.message.chat.id, r_node_id))


@bot.callback_query_handler(func=lambda call: call.data[0:10] == 'prev_note-')
def nextNode(call):
    r_node_id = call.data[10:]
    print('prev ' + str(r_node_id))
    note = dbworker.getNotesById(r_node_id)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=note)
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  reply_markup=markups.getNoteMarkup(call.message.chat.id, r_node_id))


@bot.callback_query_handler(func=lambda call: call.data[0:11] == 'delete_note-')
def nextNode(call):
    r_node_id = call.data[11:]
    dbworker.deleteNote(r_node_id)
    bot.send_message(call.message.chat.id, 'Note deleted')


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
