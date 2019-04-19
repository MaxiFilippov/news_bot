import asyncio
import random
from getnews import sort_req
from helpers_variables import *
from config import change


global final_news

final_news = [
    
]


global sub_final_news

sub_final_news = [
    
]


for_caching = [

]
sub_for_caching = [

]
global changer
changer = True
async def cache(loop):
    global final_news
    # global sub_final_news
    # global changer
    # while True:
    #     changer = not changer
    #     change(changer)
    #     print('Start working', changer)
    #     for_caching.clear()
    #     sub_for_caching.clear()
    #     for j in range(1):
    #         news = []
    #         sub_news = []
    #         for i in range(8): 
    #             response = await sort_req(list_of_cats_en[i], languages[j])
    #             msg = response[0]
    #             news.append(msg)
    #             if len(response) > 0:
    #                 sub_msg = response[1]
    #                 print("Sub msg is ", sub_msg)
    #                 sub_news.append(sub_msg)
    #         for_caching.append(news.copy())
    #         sub_for_caching.append(sub_news.copy())
    #     final_news = []
    #     sub_final_news = []
    #     final_news = for_caching.copy()
    #     sub_final_news = sub_for_caching.copy()
    #     await asyncio.sleep(3600, loop=loop) 
             

def getCached(lang, cat):
    print(lang, ' ', cat)
    if cat in list_of_cats:
        print(final_news[int(languages_numbers[lang])-1][int(dict_of_cats_num[cat])])
        return final_news[int(languages_numbers[lang])-1][int(dict_of_cats_num[cat])]
    elif cat in list_of_cats_en:
        print(final_news[int(languages_numbers[lang])-1][int(dict_of_cats_num_en[cat])])
        return final_news[int(languages_numbers[lang])-1][int(dict_of_cats_num_en[cat])]


def get_sub_cached(lang, cat):
    if cat in list_of_cats:
        return sub_final_news[int(languages_numbers[lang])-1][int(dict_of_cats_num[cat])]
