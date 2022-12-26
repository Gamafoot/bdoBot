import asyncio
import requests
from config import TOKEN
from bot.tools.utils import get_info_about_next_boss


class LastBoss:
    name = ''


async def send_auto_info(last_boss:LastBoss):
    while True:
        await asyncio.sleep(600)
        db_data = open('db.txt', 'r').read()
        if len(db_data.strip()) > 0:
            for tg_id in db_data.split(','):
                game_data = await get_info_about_next_boss(update=False)
                if game_data:
                    if game_data['boss'].lower() != last_boss.name:
                        last_boss.name = game_data['boss'].lower()
                        await send_message(tg_id, game_data)
            
            
async def send_message(tg_id, game_data):
    data = {"chat_id": tg_id, "caption": f"Следующий босс: {game_data['boss']}\nБудет через {game_data['time']}"}
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    requests.post(url, data=data, files={"photo": game_data['place']})
    

async def main():
    await asyncio.gather(send_auto_info(LastBoss))
    
asyncio.run(main())