import asyncio
import requests
from config import TOKEN
from bot.tools.utils import get_info_about_next_boss


async def send_auto_info():
    while True:
        await asyncio.sleep(600)
        db_data = open('db.txt', 'r').read()
        arr_db_data = db_data.split(',')
        if len(arr_db_data) > 0:
            for tg_id in arr_db_data:
                game_data = await get_info_about_next_boss(update=False)
                if game_data:
                    await send_message(tg_id, game_data)
            
            
async def send_message(tg_id, game_data):
    data = {"chat_id": tg_id, "caption": f"Следующий босс: {game_data['boss']}\nБудет через {game_data['time']}"}
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    requests.post(url, data=data, files={"photo": game_data['place']})
        
        
async def main():
   await asyncio.gather(send_auto_info())

asyncio.run(main())