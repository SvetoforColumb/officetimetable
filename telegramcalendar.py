import datetime

from telebot import types
import calendar


def create_calendar(year, month):
    now = datetime.datetime.now()

    markup = types.InlineKeyboardMarkup()
    # First row - Month and Year
    row = []
    calendar_name = calendar.month_name[month]
    if calendar_name == "January":
        calendar_name = "Январь"
    elif calendar_name == "February":
        calendar_name = "Февраль"
    elif calendar_name == "March":
        calendar_name = "Март"
    elif calendar_name == "April":
        calendar_name = "Апрель"
    elif calendar_name == "May":
        calendar_name = "Май"
    elif calendar_name == "June":
        calendar_name = "Июнь"
    elif calendar_name == "July":
        calendar_name = "Июль"
    elif calendar_name == "August":
        calendar_name = "Август"
    elif calendar_name == "September":
        calendar_name = "Сентябрь"
    elif calendar_name == "October":
        calendar_name = "Октябрь"
    elif calendar_name == "November":
        calendar_name = "Ноябрь"
    elif calendar_name == "December":
        calendar_name = "Декабрь"
    row.append(types.InlineKeyboardButton(calendar_name + " " + str(year), callback_data="ignore"))
    markup.row(*row)
    # Second row - Week Days
    week_days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
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
