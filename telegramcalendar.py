import datetime
from telebot import types
import calendar


def create_calendar(year, month):
    now = datetime.datetime.now()
    markup = types.InlineKeyboardMarkup()
    row = []
    calendar_name = calendar.month_name[month]
    row.append(types.InlineKeyboardButton(calendar_name + " " + str(year), callback_data="ignore"))
    markup.row(*row)
    week_days = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
    row = []
    for day in week_days:
        row.append(types.InlineKeyboardButton(day, callback_data="ignore"))
    markup.row(*row)

    my_calendar = calendar.monthcalendar(year, month)
    for week in my_calendar:
        row = []
        for day in week:
            if day == 0:
                row.append(types.InlineKeyboardButton(" ", callback_data="ignore"))
            elif str(now.day) == str(day) and str(now.month) == str(month) and str(now.year) == str(year):
                row.append(types.InlineKeyboardButton("[" + str(day) + "]", callback_data="calendar-day-" + str(day)))
            else:
                row.append(types.InlineKeyboardButton(str(day), callback_data="calendar-day-" + str(day)))
        markup.row(*row)
    # Last row - Buttons
    row = [types.InlineKeyboardButton("<", callback_data="previous-month"),
           types.InlineKeyboardButton(" ", callback_data="ignore"),
           types.InlineKeyboardButton(">", callback_data="next-month")]
    markup.row(*row)
    return markup
