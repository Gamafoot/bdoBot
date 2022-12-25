from requests_html import AsyncHTMLSession
from bot import bot
from bot.tools.keyboards import menus
import json
import asyncio

def register_user(telegram_id:str):
    db_data = open('db.txt', 'r').read()
    if telegram_id not in db_data.split(','):
        db_data += str(telegram_id)+','
        with open('db.txt', 'w') as file:
            file.write(db_data)
            

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


async def send_auto_info():
    while True:
        await asyncio.sleep(5)
        db_data = open('db.txt', 'r').read()
        for tg_id in db_data.split(','):
            data = await get_info_about_next_boss()
            await bot.send_photo(chat_id=tg_id, photo=data['place'], caption=f"Следующий босс: {data['boss']}\nБудет через {data['time']}", reply_markup=menus.update())
    
    
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