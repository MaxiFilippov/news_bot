from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from helpers_variables import *
from translations import get_more_trans

# Start Buttons Markup


def get_default_buttons(username):

    button1 = KeyboardButton(f"🌎 {kb_buttons[bot_language[username]][0]}")
    button2 = KeyboardButton(f"🏛 {kb_buttons[bot_language[username]][1]}")
    button3 = KeyboardButton(f"🏅 {kb_buttons[bot_language[username]][2]}")
    button4 = KeyboardButton(f"🏙 {kb_buttons[bot_language[username]][3]}")
    button5 = KeyboardButton(f"🚀 {kb_buttons[bot_language[username]][4]}")
    button6 = KeyboardButton(f"💉 {kb_buttons[bot_language[username]][5]}")
    button7 = KeyboardButton(f"⭐️{kb_buttons[bot_language[username]][6]}")
    button8 = KeyboardButton(f"💻 {kb_buttons[bot_language[username]][7]}")
    button9 = KeyboardButton(f"🗺 {kb_buttons[bot_language[username]][8]}")
    button10 = KeyboardButton(f"⌚️{kb_buttons[bot_language[username]][9]}")

    return ReplyKeyboardMarkup(resize_keyboard=True).row(button1, button2, button3).row(button4, button5, button6).row(button7, button8).row(button9, button10)


# Time Settings buttons 
def get_time_buttons(username):

    categorybutton1 = KeyboardButton(f"➕{time_buttons[bot_language[username]][0]}")
    categorybutton2 = KeyboardButton(f"✏️{time_buttons[bot_language[username]][1]}")
    categorybutton3 = KeyboardButton(f"🏁{time_buttons[bot_language[username]][2]}")
    categorybutton4 = KeyboardButton(f"↩️{time_buttons[bot_language[username]][3]}")

    return ReplyKeyboardMarkup(resize_keyboard=True).row(categorybutton1, categorybutton2).row(categorybutton3,categorybutton4)

# Country ICB
def get_country_icb(username):
    ru = InlineKeyboardButton(f'{country_icb[bot_language[username]][0]}🇷🇺', callback_data='ru')
    ua = InlineKeyboardButton(f'{country_icb[bot_language[username]][1]}🇺🇦', callback_data='ua')
    us = InlineKeyboardButton(f'{country_icb[bot_language[username]][2]}🇺🇸', callback_data='us')
    ca = InlineKeyboardButton(f'{country_icb[bot_language[username]][3]}🇨🇦', callback_data='ca')

    return InlineKeyboardMarkup().row(ru).row(ua).row(us).row(ca) #Lang icb

# Category ICb
def get_category_icb(username):
    icb1 = InlineKeyboardButton(f"🌎 {kb_buttons[bot_language[username]][0]}", callback_data='general')
    icb2 = InlineKeyboardButton(f"🏛 {kb_buttons[bot_language[username]][1]}", callback_data='politics')
    icb3 = InlineKeyboardButton(f"🏅 {kb_buttons[bot_language[username]][2]}", callback_data='sport')
    icb4 = InlineKeyboardButton(f"🏙 {kb_buttons[bot_language[username]][3]}", callback_data='business')
    icb5 = InlineKeyboardButton(f"🚀 {kb_buttons[bot_language[username]][4]}", callback_data='science')
    icb6 = InlineKeyboardButton(f"💉 {kb_buttons[bot_language[username]][5]}", callback_data='health')
    icb7 = InlineKeyboardButton(f"⭐️ {kb_buttons[bot_language[username]][6]}", callback_data='entertainment')
    icb8 = InlineKeyboardButton(f"🗺 {kb_buttons[bot_language[username]][7]}", callback_data='technology')

    return InlineKeyboardMarkup().row(icb1, icb2).row(icb3, icb4).row(icb5, icb6).row(icb7, icb8)


# Delete icb
def get_delete_icb(username):
    save_icb = InlineKeyboardButton(f"✅ {delete_icb[bot_language[username]][0]}", callback_data='save')
    del_icb = InlineKeyboardButton(f"❌ {delete_icb[bot_language[username]][1]}", callback_data='delete')

    return InlineKeyboardMarkup().row(save_icb, del_icb)

# Save ICB
def get_save_icb(username):
    return InlineKeyboardMarkup().add(InlineKeyboardButton(f"✅ {delete_icb[bot_language[username]][0]}", callback_data='save'))

# Language icb
rus = InlineKeyboardButton('Русский🇷🇺', callback_data='rus')
eng = InlineKeyboardButton('English🇺🇸', callback_data='eng')

language_icb = InlineKeyboardMarkup().add(eng, rus)

# For Get More news
def get_more(msg, username):
    more = InlineKeyboardButton(get_more_trans[bot_language[username]], callback_data=msg)
    return InlineKeyboardMarkup().add(more)