import asyncio
from db import * 

class Adv:
    count_of_shows = 0
    max_shows = 0
    text = ''
    session = 'inactive'
    users = []
    language = ''
    def __init__(self):
        pass

    # For incremeting count_of_shows
    @classmethod
    def inc_count(self):
        print("Incrementing")
        self.count_of_shows += 1
    
    @classmethod
    def compare_language(self, lang):
        if self.language == lang:
            return True
        return False    

    @classmethod
    async def reset_count(self):
        print('Reseting')
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, reset_session, self.count_of_shows)
        self.count_of_shows = 0
        self.session = 'inactive'
        self.users.clear()

    @classmethod
    def insert_user(self, username):
        self.users.append(username)

    @classmethod
    def return_count(self):
        return self.count_of_shows

    @classmethod
    def return_max_shows(self):
        print(self.max_shows)
        return self.max_shows

    @classmethod 
    def check_user(self, username):
        print("Checking user")
        if username in self.users:
            return False
        return True

    @classmethod
    def return_text(self):
        return self.text

    @classmethod
    def return_session(self):
        return self.session

    @classmethod
    async def check_new_session(self, loop):
        while True:
            adv = get_adv()
            if adv['session'] == 'active':
                print("Session is active")
                self.max_shows = int(adv['max_shows'])
                self.text = adv['text']
                self.session = 'active'
                self.language = adv['language']
            await asyncio.sleep(7200, loop=loop)



#Adv.check_new_session()