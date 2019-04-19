import sys

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
bot = Bot(token=API_TOKEN, proxy=PROXY, parse_mode="HTML")


class time_settings:
    def __init__(self):
        pass


    # For setting time only 
    async def set_time(self, message, dp):
        state = dp.current_state(user=message.chat.id)
        all_settings = {}
        all_settings[str(message.chat.id)] = await state.get_data(message.chat.id)
        try:
            print(message.text[2:], message.text)
            if (message.text[1:] == 'Закончить' or message.text[1:] == 'Finish') and (len(all_settings[str(message.chat.id)]['category']) > len(all_settings[str(message.chat.id)]['time_to_receive'])):
                await bot.send_message(message.chat.id, incomplete_setting[bot_language[str(message.chat.id)]])        
            elif message.text[1:] == 'Закончить' or message.text[1:] == 'Finish':
                await bot.send_message(message.chat.id, del_of_save[bot_language[str(message.chat.id)]], reply_markup=get_delete_icb(str(message.chat.id)))
                await state.reset_state(with_data=False)
                await state.set_state('change_state')
            elif message.text[2:] == 'Выйти' or message.text[2:] == 'Exit':
                await state.reset_state()
                await bot.send_message(message.chat.id, specify_cat_trans[bot_language[str(message.chat.id)]], reply_markup=get_default_buttons(str(message.chat.id)))    
            else:
                if is_time_format(message.text):
                    time_settings = {
                        str(message.chat.id): []
                    }
                    all_settings = {}
                    all_settings[str(message.chat.id)] = await state.get_data(message.chat.id)
                    print(all_settings)
                    try:
                        time_settings[str(message.chat.id)] = all_settings[str(
                            message.chat.id)]['time_to_receive']
                    except:
                        print('Key error')
                    time_settings[str(message.chat.id)].append(set_time(set_time_with_difference(
                        message.text, all_settings[str(message.chat.id)]['difference'])))
                    print('Setting category')
                    await state.update_data({'time_to_receive': time_settings[str(message.chat.id)]})
                    print(all_settings)
                    await state.reset_state(with_data=False)
                    await bot.send_message(message.chat.id, set_cat_or_finish[bot_language[str(message.chat.id)]], reply_markup=get_category_icb(str(message.chat.id)))
                    await state.set_state('setting_category')
                else:
                    await bot.send_message(message.chat.id, correct_format[bot_language[str(message.chat.id)]])
        except:
            await bot.send_message(message.chat.id, incomplete_setting[bot_language[str(message.chat.id)]])


    # For setting category only without unexpected situtions
    async def set_category(self, callback_query, dp):
        all_settings = {}
        state = dp.current_state(user=callback_query.from_user.id)
        time_settings = {
            str(callback_query.from_user.id): []
        }
        all_settings[str(callback_query.from_user.id)] = await state.get_data(callback_query.from_user.id)
        print('ALL settings inside setting category',all_settings)
        try:
            time_settings[str(callback_query.from_user.id)] = all_settings[str(
                callback_query.from_user.id)]['category']
        except:
            print('Key error')
        time_settings[str(callback_query.from_user.id)].append(callback_query.data)
        print('Setting category')
        await state.update_data({'category': time_settings[str(callback_query.from_user.id)]})
        await state.reset_state(with_data=False)
        await callback_query.answer()
        await bot.send_message(callback_query.from_user.id, hh_mm[bot_language[str(callback_query.from_user.id)]])
        await state.set_state('setting_time')

    # For setting difference(or local time)
    async def set_local_time(self, message, dp):
        msg = message.text[:2]
        print("Setting local time")
        state = dp.current_state(user=message.chat.id)
        if message.text[2:] == 'Выйти' or message.text[2:] == 'Exit':
            await state.reset_state()
            await bot.send_message(message.chat.id, specify_cat_trans[bot_language[str(message.chat.id)]], reply_markup=get_default_buttons(str(message.chat.id)))
        elif message.text[1:] == 'Закончить' or message.text[1:] == 'Finish':
            await bot.send_message(message.chat.id, inc_sett[bot_language[str(message.chat.id)]])        
        elif is_time_format(message.text):
            await state.update_data({'difference': get_difference(message.text)})
            await bot.send_message(message.chat.id, country_given[bot_language[str(message.chat.id)]], reply_markup=get_country_icb(str(message.from_user.id)))
            await state.set_state('language_in_time')
        else: 
            await bot.send_message(message.chat.id, correct_format[bot_language[str(message.chat.id)]])
        
        
    # For quiting from settings
    async def quit_from_settings(self, message, dp):
        state = dp.current_state(user=message.chat.id)
        all_settings = {}
        all_settings[str(message.chat.id)] = await state.get_data(message.chat.id)
        try:
            if (message.text[1:] == 'Закончить' or message.text[1:] == 'Finish') and ((all_settings[str(message.chat.id)]['time_to_receive'] == [] or all_settings[str(message.chat.id)]['category'] == []) or (len(all_settings[str(message.chat.id)]['category']) > len(all_settings[str(message.chat.id)]['time_to_receive']))) :
                await bot.send_message(message.chat.id, inc_sett[bot_language[str(message.chat.id)]])
            elif message.text[1:] == 'Закончить' or message.text[1:] == 'Finish':
                await bot.send_message(message.chat.id, d_or_save[bot_language[str(message.chat.id)]] + show_settings_for_changing_with_user_settings(all_settings[str(message.chat.id)]), reply_markup=get_delete_icb(str(message.chat.id)))
                await state.reset_state(with_data=False)
                await state.set_state('change_current_settings')
        except:
            e = sys.exc_info()
            print(e, 'Settings', all_settings[str(message.chat.id)])
            await bot.send_message(message.chat.id, inc_sett[bot_language[str(message.chat.id)]])
        if message.text[2:] == 'Выйти' or message.text[2:] == 'Exit':
            await state.reset_state()
            await bot.send_message(message.chat.id, specify_cat_trans[bot_language[str(message.chat.id)]], reply_markup=get_default_buttons(str(message.chat.id)))


    async def set_language(self, callback_query, dp):
        state = dp.current_state(user=callback_query.from_user.id)
        await state.update_data({'language': callback_query.data})
        await state.reset_state(with_data=False)
        await callback_query.answer()
        await bot.send_message(callback_query.from_user.id, spec_cat[bot_language[str(callback_query.from_user.id)]], reply_markup=get_category_icb(str(callback_query.from_user.id)))
        await state.set_state('setting_category')