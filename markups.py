from telebot import types

markup_remove = types.ReplyKeyboardRemove()

markup_main = types.ReplyKeyboardMarkup()
markup_main.row('Make a note')
markup_main.row('View notes')
markup_main.row('Set a remind time')

