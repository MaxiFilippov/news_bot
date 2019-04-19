# User buttons
# Start Buttons init
from db import get_lang
list_of_cats = [
    "Главные",
    "Политика",
    "Спорт",
    "Бизнес",
    "Наука",
    "Медицина",
    "Шоу-Бизнес",
    "Технологии"
]

list_of_cats_eng = [
    "General",
    "Politics",
    "Sport",
    "Business",
    "Science",
    "Health",
    "Entertainment",
    "Technology"
]

dict_of_cats_num = {
    "Главные": "0",
    "Политика": "1",
    "Спорт": "2",
    "Бизнес": "3",
    "Наука": "4",
    "Медицина": "5",
    "Шоу-Бизнес": "6",
    "Технологии": "7"
}

dict_of_cats_num_en = {
    "general": "0",
    "politics": "1",
    "sport": "2",
    "business": "3",
    "science": "4",
    "health": "5",
    "entertainment": "6",
    "technology": "7"
}


dict_of_cats_en = {
    "general": "Главные",
    "politics": "Политика",
    "sport": "Спорт",
    "business": "Бизнес",
    "science": "Наука",
    "health": "Медицина",
    "entertainment": "Шоу-Бизнес",
    "technology": "Технологии"
}

list_of_categories = {
    "General": "Главные",
    "Politics": "Политика",
    "Sport": "Спорт",
    "Business": "Бизнес",
    "Science": "Наука",
    "Health": "Медицина",
    "Entertainment": "Шоу-Бизнес",
    "Technology": "Технологии",
    "Главные": "Главные",
    "Политика": "Политика",
    "Спорт": "Спорт",
    "Бизнес": "Бизнес",
    "Наука": "Наука",
    "Медицина": "Медицина",
    "Шоу-Бизнес": "Шоу-Бизнес",
    "Технологии": "Технологии"
}

list_of_cats_en = [
    "general",
    "politics",
    "sport",
    "business",
    "science",
    "health",
    "entertainment",
    "technology"
]

languages = [
    'ru', 'ua', 'us', 'ca'
]
languages_numbers = {
    'ru': '1',
    'ua': '2',
    'us': '3',
    'ca': '4'
}
country = {
    "ru": "Россия",
    "ua": "Украина",
    "us": "США",
    "ca": "Канада"
}

country_en = {
    "ru": "Russia",
    "ua": "Ukrauine",
    "us": "USA",
    "ca": "Canada"
}

language = {

}
settings = {

}
# It is needed for adding array in 'settings'
user_settings = {

}

by_time_settings = {

}
bot_language  = get_lang()
global main_lang
main_lang = 'ru'
flag = 'none'


# Tranalastions
# Buttons
kb_buttons = {
    'eng': [
        "General",
        "Politics",
        "Sport",
        "Business",
        "Science",
        "Health",
        "Entertainment",
        "Technology",
        "Specify Country",
        "Time Settings"
    ],
    'rus': [
        "Главные",
        "Политика",
        "Спорт",
        "Бизнес",
        "Наука",
        "Медицина",
        "Шоу-Бизнес",
        "Технологии",
        "Указать Страну",
        "Настройки По Времени"
    ]
}
# Time Settigs Buttons
time_buttons = {
    'eng': [
        "Add New",
        "Change",
        "Finish",
        "Exit"
    ],
    'rus': [
        "Добавить Новые",
        "Изменить",
        "Закончить",
        "Выйти"
    ]
}
# Country ICB
country_icb = {
    'eng': [
        "Country: Russia. Language: Russian",
        "Country: Ukrain. Language: Ukranian",
        "Country: USA. Language: English",
        "Country: Canada. Language: English"
    ],
    'rus': [
        "Страна: Россия. Язык: Русский",
        "Страна: Украина. Язык: Украинский",
        "Страна: США. Язык: Английский",
        "Страна: Канада. Язык: Английский"
    ]
}

# Delete ICB
delete_icb = {
    'eng': [
        "Save",
        "Delete"
    ],
    'rus': [
        "Сохранить",
        "Удалить"
    ]
}