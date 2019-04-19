import sys
import asyncio

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from helpers import *
from getnews import sort_req
from helpers_buttons import *
from helpers_variables import *
from config import *
from cache import *
from db import *
from translations import *
bot = Bot(token=API_TOKEN, proxy=PROXY,  parse_mode="HTML")

class change_current_settings:
    def __init__(self):
        pass


    #  For callback query
    async def change_current(self, callback_query, dp):
        state = dp.current_state(user=callback_query.from_user.id)
        all_settings = {}
        _user_settings = {
            str(callback_query.from_user.id): {'category': [],
            'time_to_receive': [],
            'language': [],
            'difference': ''}
        }
        all_settings[str(callback_query.from_user.id)] = await state.get_data(callback_query.from_user.id)
        if callback_query.data == 'delete':
            await callback_query.answer()
            await bot.send_message(callback_query.from_user.id, change_current_trans[bot_language[str(callback_query.from_user.id)]] + show_settings_for_changing_with_user_settings(all_settings[str(callback_query.from_user.id)]), reply_markup=get_save_icb(str(callback_query.from_user.id)))
        if callback_query.data == 'save':
            await state.reset_state()
            await callback_query.answer()
            await bot.send_message(callback_query.from_user.id, settings_saved[bot_language[str(callback_query.from_user.id)]], reply_markup=get_default_buttons(str(callback_query.from_user.id)))
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, setoff_settings, callback_query, _user_settings, all_settings)
    
    
    # For messages
    async def handle_changes(self, message, dp):
        state = dp.current_state(user=message.chat.id)
        all_settings = {}
        all_settings[str(message.chat.id)] = await state.get_data(message.chat.id)
        if message.text == 'Все' or message.text == 'All':
            await state.reset_state()
            await bot.send_message(message.chat.id, settings_deleted[bot_language[str(message.chat.id)]], reply_markup=get_default_buttons(str(message.chat.id)))
        elif message.text.isdigit():
            try:
                del all_settings[str(message.chat.id)]['category'][int(message.text)-1] 
                del all_settings[str(message.chat.id)]['time_to_receive'][int(message.text)-1] 
                await state.update_data({'category': all_settings[str(message.chat.id)]['category'], 'time_to_receive': all_settings[str(message.chat.id)]['time_to_receive']})
                print(show_settings_for_changing_with_user_settings(all_settings[str(message.chat.id)]))
                if show_settings_for_changing_with_user_settings(all_settings[str(message.chat.id)]) != '':
                    await bot.send_message(message.chat.id, change_current_trans[bot_language[str(callback_query.from_user.id)]] + show_settings_for_changing_with_user_settings(all_settings[str(message.chat.id)]), reply_markup=get_save_icb(str(message.chat.id)))
                else:
                    await bot.send_message(message.chat.id, settings_deleted[bot_language[str(message.chat.id)]], reply_markup=get_default_buttons(str(message.chat.id)))
                    await state.reset_state()
            except:
                await bot.send_message(message.chat.id, invalid_value[bot_language[str(message.chat.id)]])            
        else:
            await bot.send_message(message.chat.id, invalid_value[bot_language[str(message.chat.id)]])


def setoff_settings(callback_query, _user_settings, all_settings):
    if 'category' in set_settings(str(callback_query.from_user.id)):
        _user_settings[str(callback_query.from_user.id)] = set_settings(str(callback_query.from_user.id))
        print(user_settings)    
    _user_settings[str(callback_query.from_user.id)]['category'].append(
        all_settings[str(callback_query.from_user.id)]['category'])
    _user_settings[str(callback_query.from_user.id)]['time_to_receive'].append(
        all_settings[str(callback_query.from_user.id)]['time_to_receive'])
    _user_settings[str(callback_query.from_user.id)]['language'].append(all_settings[str(callback_query.from_user.id)]['language'])
    _user_settings[str(callback_query.from_user.id)]['difference'] = all_settings[str(callback_query.from_user.id)]['difference']
    send_settings(_user_settings[str(callback_query.from_user.id)], str(callback_query.from_user.id))