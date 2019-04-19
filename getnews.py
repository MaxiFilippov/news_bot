import aiohttp
from aiogram.utils.markdown import text, bold, italic, code, pre
from config import change_key

# Sending request to google news
async def send_req(session, cat, main_lang):  
    print(main_lang)
    async with session.get(f"https://newsapi.org/v2/top-headlines?country={main_lang}&category={cat}&apiKey={change_key()}") as response:
        return await response.json()     
    
# Sorting received news and returning message  
def check_news(articles):
    if articles['title'] != None and articles['description'] != None and articles['url'] != None and 'Ð' not in articles['description'] and "<p>" not in articles['description'] and "&nbsp" not in articles['description'] and "&ndash" not in articles['description'] and "<img>" not in articles['description']:
        return True        
    else:
        return False     
async def sort_req(cat, main_lang):
    print("Inside req", cat)
    try:
        async with aiohttp.ClientSession() as session:
            response = await send_req(session, cat, main_lang)
        print(response)    
        articles = response['articles']
        message = ""
        sub_message = ""
        rng = 0
        if len(articles) <= 10:
            rng = len(articles)
        else:
            rng = 10    
        print(len(articles))
        for i in range(rng):  
            if check_news(articles[i]) and articles[i]['description'] == '':
                print('Inserting with no description')
                message = message + f"<a href=\"{articles[i]['url']}\">{articles[i]['title']}</a>  \n\n"
            elif check_news(articles[i]):
                message = message + f"<a href=\"{articles[i]['url']}\">{articles[i]['title']}</a> \n{articles[i]['description']} \n\n" 
        if len(articles) > 10:
            print("Setting more news")
            for i in range(10, len(articles)):  
                if check_news(articles[i]) and articles[i]['description'] == '':
                    print('Inserting with no description')
                    sub_message = sub_message + f"<a href=\"{articles[i]['url']}\">{articles[i]['title']}</a>  \n\n"
                elif check_news(articles[i]):
                    sub_message = sub_message + f"<a href=\"{articles[i]['url']}\">{articles[i]['title']}</a> \n{articles[i]['description']} \n\n"         
        return [message, sub_message]
    except:
        print("Server-Side error")    
        