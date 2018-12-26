from telebot import types

markup_remove = types.ReplyKeyboardRemove()

markup_main = types.ReplyKeyboardMarkup(True)
markup_main.row('Make a note')
markup_main.row('View notes')
markup_main.row('Set a remind time')

yes_no_markup = types.InlineKeyboardMarkup(row_width=2)
yes_no_markup_row = [
        types.InlineKeyboardButton('No', callback_data="add_remind_no"),
        types.InlineKeyboardButton('Yes', callback_data="add_remind_yes")]
yes_no_markup.row(*yes_no_markup_row)
