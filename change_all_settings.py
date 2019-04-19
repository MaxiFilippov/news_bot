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

class change_all_settings:
    def __init__(self):
        pass

    # For handling text messages
    async def change_all_handler(self, message, dp):
        state = dp.current_state(user=message.chat.id)
        all_settings = {}
        all_settings[str(message.chat.id)] = await state.get_data(message.chat.id)
        if message.text[2:] == 'Выйти' or message.text[2:] == 'Exit':
            await state.reset_state()
            await bot.send_message(message.chat.id, specify_cat_trans[str(message.chat.id)], reply_markup=get_default_buttons(str(message.chat.id)))
        elif message.text == 'Все' or message.text == 'All':
            all_settings[str(message.chat.id)].clear()
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, del_settings, str(message.chat.id))
            await state.reset_state()
            await bot.send_message(message.chat.id, settings_deleted[bot_language[str(message.chat.id)]], reply_markup=get_default_buttons(str(message.chat.id)))
        else:
            try:
                if split_to_numbers(message.text)[0].isdigit():
                    global_arr = int(split_to_numbers(message.text)[0])-1
                    local_arr = int(split_to_numbers(message.text)[1])-1
                    print('Deleting settings',
                            all_settings[str(message.chat.id)])
                    del all_settings[str(message.chat.id)]['time_to_receive'][global_arr][local_arr]
                    del all_settings[str(message.chat.id)]['category'][global_arr][local_arr]
                    print(len(all_settings[str(message.chat.id)]['time_to_receive'][global_arr]), ' ', len(all_settings[str(message.chat.id)]['language'][global_arr]))
                    print('Language', all_settings[str(message.chat.id)]['language'][global_arr])
                    print("Len is ",len(all_settings[str(message.chat.id)]['time_to_receive'][global_arr]))
                    if len(all_settings[str(message.chat.id)]['time_to_receive'][global_arr]) == 0:
                        print('Deleting language', all_settings[str(message.chat.id)]['language'][global_arr])
                        del all_settings[str(message.chat.id)]['category'][global_arr]
                        del all_settings[str(message.chat.id)]['time_to_receive'][global_arr]
                        del all_settings[str(message.chat.id)]['language'][global_arr]
                        print("Deleting language has ended")
                    await state.update_data({'category': all_settings[str(message.chat.id)]['category'], 'time_to_receive': all_settings[str(message.chat.id)]['time_to_receive'], 'language': all_settings[str(message.chat.id)]['language']})
                    if all_settings[str(message.chat.id)]['time_to_receive'] != []:
                        print("Trying to show settings again")
                        if show_settings_for_changing(all_settings[str(message.chat.id)]) != '':
                            print("Showing settings again")
                            await bot.send_message(message.chat.id, show_settings_for_changing(all_settings[str(message.chat.id)]), reply_markup=get_save_icb(str(message.chat.id)))
                        else:
                            await bot.send_message(message.chat.id, settings_deleted[bot_language[str(message.chat.id)]], reply_markup=get_default_buttons(str(message.chat.id)))
                            loop = asyncio.get_running_loop()
                            await loop.run_in_executor(None, del_settings, str(message.chat.id))
                            await state.reset_state()
                    else:   
                        await bot.send_message(message.chat.id, settings_deleted[bot_language[str(message.chat.id)]], reply_markup=get_default_buttons(str(message.chat.id)))
                        loop = asyncio.get_running_loop()
                        await loop.run_in_executor(None, del_settings, str(message.chat.id))
                        await state.reset_state()        
                else:
                    await bot.send_message(message.chat.id, delete_or_save_all_trans[bot_language[str(message.chat.id)]])
            except:
                e = sys.exc_info()
                print(e)
                await bot.send_message(message.chat.id, invalid_value[bot_language[str(message.chat.id)]])    
    
    # For handling icb
    async def change_all_icb(self, callback_query, dp):
        state = dp.current_state(user=callback_query.from_user.id)
        all_settings = {}
        all_settings[str(callback_query.from_user.id)] = await state.get_data(callback_query.from_user.id)
        print('Inside change_state cbq handler ', all_settings)
        if callback_query.data == 'save':
            await state.reset_state()
            await callback_query.answer()
            await bot.send_message(callback_query.from_user.id, settings_saved[bot_language[str(message.chat.id)]], reply_markup=get_default_buttons(str(callback_query.from_user.id)))
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, send_settings, all_settings[str(callback_query.from_user.id)], str(callback_query.from_user.id))
                        