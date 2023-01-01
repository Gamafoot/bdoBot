from requests_html import AsyncHTMLSession
import asyncio
import requests
from config import TOKEN
            

async def get_info_about_next_boss(update=True) -> dict:
    session = AsyncHTMLSession()
    res = await session.get('https://bdocodex.com/ru/bosstimer/')
    await res.html.arender(timeout=30)
    time = res.html.find('#timer', first=True).text
    name = res.html.find('.inlinediv', first=True).find('div', first=True).text
    
    if int(time.split(':')[0]) < 1 or update:
        time = calculate_time(time)
        with open(f'bot/media/{name.lower()}.png', 'rb') as file:
            data = {
                'boss': name,
                'time': time,
                'place': file.read()
            }
        return data
    return None
    
def calculate_time(time:str):
    time_arr = time.split(':')
    hours = time_arr[0]
    minuts = time_arr[1]
    seconds = time_arr[2]
    res_time = ''
    if int(hours) == 0:
        if int(minuts) == 0:
            res_time += f'{int(seconds)} секунд'
        else:
            res_time += f'{int(minuts)} минут'
    else:
        if int(minuts) == 0:
            res_time += f'{int(hours)} час'
        else:
            res_time += f'{int(hours)} час {int(minuts)} минут'
    return res_time

class UserRequest:
    def __init__(self):
        self.users_was_request = []
        
    def add(self, telegram_id:str):
        self.users_was_request.append(telegram_id)
        
    def remove(self, telegram_id:str):
        self.users_was_request.remove(telegram_id)
    
    def check(self, telegram_id:str):
        return telegram_id in self.users_was_request
    
userReq = UserRequest()