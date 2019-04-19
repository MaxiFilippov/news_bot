from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot, Dispatcher, executor, types    
from helpers_variables import *
import time
from datetime import datetime
from translations import *

def show_settings_for_changing(settings):
    print("Settings ",settings)
    msg =  time_cat_country[bot_language[settings['username']]]
    if settings['category'] == []:
        return ''
    for x in range(len(settings['time_to_receive'])):
        for y in range(len(settings['time_to_receive'][x])):
            print(dict_of_cats_en[settings['category'][x][y]])
            if bot_language[str(settings['username'])] == 'rus':
                msg = msg + '   ' + str(x+1) + '.' + str(y+1) + '     ' + set_with_difference(settings['time_to_receive'][x][y], settings['difference']) + '    ' + dict_of_cats_en[settings['category'][x][y]] + '    ' + country[settings['language'][x]] + '\n'
            else:
                msg = msg + '   ' + str(x+1) + '.' + str(y+1) + '     ' + set_with_difference(settings['time_to_receive'][x][y], settings['difference']) + '    ' + settings['category'][x][y].capitalize() + '    ' + country_en[settings['language'][x]] + '\n'
            print(msg)
    return msg


def show_settings_for_changing_with_user_settings(user_settings):
    print('User settings ',user_settings)
    if user_settings['category'] == []:
        return ''
    msg =  time_cat[bot_language[user_settings['username']]]
    for x in range(len(user_settings['time_to_receive'])):
        if bot_language[str(user_settings['username'])] == 'rus':
            msg = msg + '     ' + str(x+1) +'       ' + set_time(set_with_difference(user_settings['time_to_receive'][x], user_settings['difference'])) + '   ' + dict_of_cats_en[user_settings['category'][x]] + '\n'
        else:
            msg = msg + '     ' + str(x+1) +'       ' + set_time(set_with_difference(user_settings['time_to_receive'][x], user_settings['difference'])) + '   ' + user_settings['category'][x].capitalize() + '\n'
    return msg


def split_to_numbers(msg):
    arr = msg.split('.')
    return arr


# For validating time in time settings
def is_time_format(input):
    try:
        time.strptime(input, '%H:%M')
        return True
    except ValueError:
       return False

def set_time(time):
    times = time.split(':')
    if int(times[0]) > 10 and int(times[1]) > 10 or times[0] == '00' and times[1] == '00':
        print('Returning time')
        return time
    else:
        print(times[1] > '0' and times[1] < '10')
        if (times[0] == '0' or (int(times[0]) > 0 and int(times[0]) < 10)) and len(times[0]) < 2:
            times[0] = '0' + times[0]
        if (times[1] == '0' or (int(times[1]) > 0 and int(times[1]) < 10)) and len(times[1]) < 2:
            times[1] = '0' + times[1]
    return times[0] + ':' + times[1]       


def set_time_with_difference(time, difference):
    print("Setting with difference")
    times = time.split(':')
    return str(int(times[0]) - int(difference)) + ':' + times[1]


def get_difference(local_time):
    local = local_time.split(':')
    difference = int(local[0]) - int(datetime.utcnow().strftime("%H:%M").split(':')[0])
    return difference

def set_with_difference(time, difference):
    times = time.split(':')
    return str(int(times[0]) + difference) + ':' + times[1]