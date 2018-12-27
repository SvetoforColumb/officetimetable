from telebot import types


def getRemoveMarkup():
        return types.ReplyKeyboardRemove()


def getMainMarkup():
        markup_main = types.ReplyKeyboardMarkup(True)
        markup_main.row('Make a note')
        markup_main.row('View notes')
        markup_main.row('Set a remind time')
        return markup_main


def getYesNoMarkup():
        yes_no_markup = types.InlineKeyboardMarkup(row_width=2)
        yes_no_markup_row = [
                types.InlineKeyboardButton('No', callback_data="add_remind_no"),
                types.InlineKeyboardButton('Yes', callback_data="add_remind_yes")]
        yes_no_markup.row(*yes_no_markup_row)
        return yes_no_markup


def getNoteMarkup():
        note_markup = types.InlineKeyboardMarkup(row_width=2)
        note_markup_row = [
                types.InlineKeyboardButton('<', callback_data="next"),
                types.InlineKeyboardButton('Delete', callback_data=""),
                types.InlineKeyboardButton('>', callback_data="add_remind_yes")]
        note_markup.row(*note_markup_row)
        return note_markup
