# -*- coding: utf-8 -*-
from __future__ import print_function

import datetime
import os
import re

import logging
import cherrypy
import telebot

from multiprocessing import Process

import config
import dbworker
from telegramcalendar import create_calendar

logging.basicConfig(filename="/home/user/scripts/main.log", level=logging.ERROR)

current_shown_dates = {}
WEBHOOK_HOST = config.host_ip
WEBHOOK_PORT = 443  # 443, 80, 88, 8443
WEBHOOK_LISTEN = '0.0.0.0'

WEBHOOK_SSL_CERT = config.ssl_cert  # Путь к сертификату
WEBHOOK_SSL_PRIV = config.ssl_priv  # Путь к приватному ключу

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % config.token

digits_pattern = re.compile(r"^[0-9]+ [0-9]+$", re.MULTILINE)

bot = telebot.TeleBot(config.token)

markup_main = telebot.types.ReplyKeyboardMarkup()
markup_main.row('Записаться на автомойку')
markup_main.row('Отменить запись')
markup_main.row('Акции')
markup_main.row('Оставить отзыв')
markup_remove = telebot.types.ReplyKeyboardRemove()



def f(s):
    total = 0
    for ch in s:
        if ch.isdigit():
            total += 1
    return total


class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                'content-type' in cherrypy.request.headers and \
                cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            # Эта функция обеспечивает проверку входящего сообщения
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)


@bot.message_handler(commands=['start'])
def handle_start_help(message):
    dbworker.addUser(message.chat.id)
    now = datetime.datetime.now()
    bot.send_message(message.chat.id,
                     "Hi! This time keep bot!"
                     "", reply_markup=markup_main)


@bot.message_handler(commands=['help'])
def handle_start_help(message):
    dbworker.addUser(message.chat.id)
    markup_commands = telebot.types.ReplyKeyboardMarkup()
    markup_commands.row('/start')
    markup_commands.row('/reset')
    markup_commands.row('/help')
    bot.send_message(message.chat.id, "Доступные команды: \n'start' – начало диалога с ботом'\n'reset' – сброс "
                                      "данных\n'help' – список доступных команд", reply_markup=markup_commands)




bot.remove_webhook()

bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))

# Указываем настройки сервера CherryPy
cherrypy.config.update({
    'server.socket_host': WEBHOOK_LISTEN,
    'server.socket_port': WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': WEBHOOK_SSL_CERT,
    'server.ssl_private_key': WEBHOOK_SSL_PRIV
})

cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})
