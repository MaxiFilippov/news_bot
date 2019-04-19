import logging
import asyncio

from datetime import datetime

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from set_advirt import *
from helpers import *
from getnews import sort_req
from helpers_buttons import *
from helpers_variables import *
from config import *
from cache import *
from db import *
from time_settings import *
from change_current_settings import *
from change_all_settings import *
from aiogram.contrib.middlewares.i18n import I18nMiddleware
from translations import *
# Configure logging
logging.basicConfig(level=logging.INFO)


# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN, proxy=PROXY , parse_mode="HTML")
dp = Dispatcher(bot)


# States init
dp = Dispatcher(bot, storage=MemoryStorage())


# For setting language from main menu
@dp.callback_query_handler(state=['Language'])
async def set_lang(callback_query: types.CallbackQuery):
    global main_lang
    state = dp.current_state(user=callback_query.from_user.id)
    language[str(callback_query.from_user.id)] = callback_query.data
    await state.reset_state(with_data=False)
    await callback_query.answer()
    await bot.send_message(callback_query.from_user.id, specify_cat_trans[bot_language[str(callback_query.from_user.id)]], reply_markup=get_default_buttons(str(callback_query.from_user.id)))

# For settings language though a command
@dp.message_handler(commands=['language'])
async def handle_lang(message: types.Message):
    await bot.send_message(message.chat.id, 'Please select <b>language</b>\n\nПожалуйста, укажите <b>язык</b>', reply_markup=language_icb)
    state = dp.current_state(user=message.chat.id)
    await state.set_data({'username': str(message.chat.id)})
    await state.set_state('main_language')

# Help
@dp.message_handler(commands=['help'])
async def process_start_command(message: types.Message):
    await bot.send_message(message.chat.id, help_trans[bot_language[str(message.chat.id)]])
    state = dp.current_state(user=message.chat.id)
    await state.set_data({'username': str(message.chat.id)})

# Start
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    #await bot.send_message(message.chat.id, 'Welcome to Newsbot, if you want to immediately get the latest news, then click on one of the proposed categories.\n\nДобро пожаловать в <b>Новостного Бота</b>, если вы хотите немедленно получить самые последние новости, то нажмите на одну из предложенных категорий.\nЕсли вы хотите получать новости в определенное время, задаваемое вами - нажмите <b>Настройка По Времени</b>', reply_markup=start_markup)
    await bot.send_message(message.chat.id, 'Welcome to <b>Newsbot</b>! Please select <b>language</b>\nДобро пожаловать в <b>Новостного Бота</b>! Пожалуйста укажите <b>язык</b>', reply_markup=language_icb)
    state = dp.current_state(user=message.chat.id)
    await state.set_data({'username': str(message.chat.id)})
    await state.set_state('main_language')
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, send_username, message.chat.id)

# For settings language in bot
@dp.callback_query_handler(state=['main_language'])
async def set_main_lang(callback_query: types.CallbackQuery):
    state = dp.current_state(user=callback_query.from_user.id)
    bot_language[str(callback_query.from_user.id)] = callback_query.data
    await bot.send_message(callback_query.from_user.id, 'Works!', reply_markup=get_default_buttons(str(callback_query.from_user.id)))
    await callback_query.answer()
    await state.reset_state(with_data=False)
    

# async def count_active():
#     users = return_list_of_users()
#     count = 0
#     for i in range(len(users)):
#         try:
#             await bot.get_chat(int(users[i]))  
#             count = count + 1
#             print(count) 
#         except:
#             pass
#     return count 

# For getting amount of users
@dp.message_handler(commands=['eval'])
async def evaluate(message: types.Message):
    loop = asyncio.get_event_loop()
    users = []
    users = await loop.run_in_executor(None, return_list_of_users)
    await bot.send_message(message.chat.id, users_in_bot[bot_language[str(message.chat.id)]].format(len(users)))


# For setting local time
@dp.message_handler(state=['set_local'])
async def change_settings_in_time_icb(message: types.Message):
    print("Set_local")
    ts = time_settings()
    await ts.set_local_time(message, dp)
    

# For gettings buttons
@dp.message_handler(commands=['getupdates'])
async def process_start_command(message: types.Message):
    await bot.send_message(message.chat.id, specify_cat_trans[bot_language[str(message.chat.id)]], reply_markup=get_default_buttons(str(message.chat.id)))


# For changing settings by time icb
@dp.callback_query_handler(state=['change_state'])
async def change_settings_in_time_icb(callback_query: types.CallbackQuery):
    ch_all = change_all_settings()
    await ch_all.change_all_icb(callback_query, dp)
    

# For changing current settings icb
@dp.callback_query_handler(state=['change_current_settings'])
async def change_settings_in_time_icb(callback_query: types.CallbackQuery):
    chk = change_current_settings()
    await chk.change_current(callback_query, dp)

# For changing current settings messages   
@dp.message_handler(state=['change_current_settings'])
async def change_current_setting(message: types.Message):
    chk = change_current_settings()
    await chk.handle_changes(message, dp)


# For handling all and one deleting
@dp.message_handler(state=['change_state'])
async def change_settings_in_time_text(message: types.Message):
    ch_all = change_all_settings()
    await ch_all.change_all_handler(message, dp)
    

# For quiting from state 'setting_category'
@dp.message_handler(state=['setting_category', 'language_in_time'])
async def quit_from_cat(message: types.Message):
    ts = time_settings()
    await ts.quit_from_settings(message, dp)


# For setting language from settings by time
@dp.callback_query_handler(state=['language_in_time'])
async def set_lang_in_time(callback_query: types.CallbackQuery):
    ts = time_settings()
    await ts.set_language(callback_query, dp)


# For setting category in settings by time
@dp.callback_query_handler(state=['setting_category'])
async def set_time_in_time(callback_query: types.CallbackQuery):
    ts = time_settings()
    await ts.set_category(callback_query, dp)


# For setting time from settings by time
@dp.message_handler(state=['setting_time'])
async def set_category_in_time(message: types.Message):
    ts = time_settings()
    await ts.set_time(message, dp)


# First handling settings by time
@dp.message_handler(state=['setting_by_time'])
async def handle_settings_by_time(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    all_settings = {}
    print("Settings by time", message.text[1:], message.text)
    if message.text[1:] == 'Добавить Новые' or message.text[1:] == 'Add New':
        await bot.send_message(message.chat.id, add_new_trans[bot_language[str(message.chat.id)]])
        await bot.send_message(message.chat.id, local_time_trans[bot_language[str(message.chat.id)]])
        await state.set_state("set_local")
    if message.text[1:] == 'Закончить' or message.text[1:] == 'Finish':
        await bot.send_message(message.chat.id, finish_in_add_new[bot_language[str(message.chat.id)]])
    if message.text[2:] == 'Выйти' or message.text[2:] == 'Exit':
        await bot.send_message(message.chat.id, specify_cat_trans[bot_language[str(message.chat.id)]], reply_markup=get_default_buttons(str(message.chat.id)))
        await state.reset_state(with_data=False)
    if message.text[2:] == 'Изменить' or message.text[2:] == 'Change':
        print('Gettings news for changing')
        try:
            loop = asyncio.get_event_loop()
            news = {}
            news = await loop.run_in_executor(None, set_settings, str(message.chat.id))
            if news != {}:
                await bot.send_message(message.chat.id, change_trans[bot_language[str(message.chat.id)]])
                await bot.send_message(message.chat.id, show_settings_for_changing(news), reply_markup=get_save_icb(str(message.chat.id)))
                await state.set_data(news)
                await state.reset_state(with_data=False)
                await state.set_state('change_state')
            else:
                await bot.send_message(message.chat.id, empty_settings[bot_language[str(message.chat.id)]])    
        except:
            print(sys.exc_info()[-1].tb_lineno)
            await bot.send_message(message.chat.id, empty_settings[bot_language[str(message.chat.id)]])

# For hadling More News
@dp.callback_query_handler(state='*')
async def handle_all_cb(callback_query: types.CallbackQuery):
    print("Inside cbq handler")
    if callback_query.data in list_of_cats:
        print("Gettins sub")
        try:
            await bot.send_message(callback_query.from_user.id, get_sub_cached(language[str(callback_query.from_user.id)], callback_query.data), disable_web_page_preview=True)
        except:
            await bot.send_message(callback_query.from_user.id, no_more_news[bot_language[str(callback_query.from_user.id)]])
        


# for hadling all messages
@dp.message_handler(state='*')
async def handle_all_messages(message: types.Message):
    global main_lang
    msg = message.text[2:]
    session = Adv.return_session()   
    if Adv.return_count() >= Adv.return_max_shows() and session == 'active':
        session = 'inactive'
        await Adv.reset_count()
    if str(message.chat.id) in bot_language:
        if msg == ' Шоу-Бизнес':
            msg = message.text[3:]
        state = dp.current_state(user=message.from_user.id) 
        print(message.date.strftime("%H:%M"))
        if msg in list_of_cats or msg in list_of_cats_eng:
            if str(message.from_user.id) in language:
                try:
                    if session == 'active' and Adv.check_user(message.chat.id) and (Adv.compare_language(bot_language[str(message.chat.id)][:2]) or Adv.compare_language(language[str(message.from_user.id)])):
                        await bot.send_message(message.chat.id, f"{Adv.return_text()}\n{getCached(language[str(message.from_user.id)], list_of_categories[msg])}", disable_web_page_preview=True)
                        Adv.inc_count()
                        Adv.insert_user(message.chat.id)
                    else:
                        await bot.send_message(message.chat.id, "getCached(language[str(message.from_user.id)], list_of_categories[msg])", disable_web_page_preview=True, reply_markup=get_more(list_of_categories[msg], str(message.from_user.id)))
                except:
                    print(sys.exc_info()[-1].tb_lineno," " , sys.exc_info())
                    await bot.send_message(message.chat.id, went_wrong_trans[bot_language[str(message.chat.id)]])
            else:
                await bot.send_message(message.chat.id, get_updates_trans[bot_language[str(message.chat.id)]])        
        print(msg)
        if msg == 'Указать Страну' or msg == 'Specify Country':    
            print('WTF????', msg)
            await bot.send_message(message.chat.id, get_country_trans[bot_language[str(message.chat.id)]], reply_markup=get_country_icb(str(message.from_user.id)))
            state = dp.current_state(user=message.from_user.id)
            await state.set_state('Language')
        if msg == 'Настройки По Времени' or msg == 'Time Settings':
            await state.update_data({'username': str(message.from_user.id)})
            await bot.send_message(message.chat.id, setting_by_time_trans[bot_language[str(message.chat.id)]], reply_markup=get_time_buttons(str(message.from_user.id)))
            await state.set_state('setting_by_time')
    else: 
        
        await bot.send_message(message.chat.id, 'Please select <b>language</b>\n\nПожалуйста, укажите <b>язык</b>', reply_markup=language_icb)
        state = dp.current_state(user=message.chat.id)
        await state.set_state('main_language')


       

async def send_by_time(loop):
    while True:
        time = datetime.utcnow().strftime("%H:%M")
        print(time)
        users = {}
        loop = asyncio.get_event_loop()
        users = await loop.run_in_executor(None, get_by_time, time)
        print(users['category'] )
        if users['usernames'] != []:
            for i in range(len(users['usernames'])): 
                print(users['language'][i], users['category'][i])   
                try:     
                    await bot.send_message(users['usernames'][i], getCached(users['language'][i], users['category'][i]), disable_web_page_preview=True)
                    
                    if i % 29 == 0:
                        await asyncio.sleep(0.03, loop=loop)
                except:
                    print("Error")        
                  
        else:
            print('Error')
        await asyncio.sleep(60, loop=loop)

loop = asyncio.get_event_loop()
loop.create_task(cache(loop))
loop.create_task(send_by_time(loop))
loop.create_task(send_lang(bot_language, loop))
loop.create_task(Adv.check_new_session(loop))
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
