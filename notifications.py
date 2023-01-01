import requests
from config import TOKEN
from bot.tools.utils import calculate_time
from bot.tools import database
import time
from requests_html import HTMLSession

wait = 60

loop_end = 3600

def get_info_about_next_boss(update=True) -> dict:
    session = HTMLSession()
    res = session.get('https://bdocodex.com/ru/bosstimer/')
    res.html.render(timeout=20)
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


def send_auto_info():
    time_passed = 0
    last_boss = ''
    while True:
        time.sleep(wait)
        time_passed += wait
        if time_passed >= loop_end:
            time_passed = 0
            users = database.get_users()
            for user_tg in users:
                game_data = get_info_about_next_boss(update=True)
                if game_data:
                    if game_data['boss'].lower() != last_boss:
                        last_boss = game_data['boss'].lower()
                        send_message(user_tg, game_data)
            
            
def send_message(tg_id, game_data):
    data = {"chat_id": tg_id, "caption": f"Следующий босс: {game_data['boss']}\nБудет через {game_data['time']}"}
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    r = requests.post(url, data=data, files={"photo": game_data['place']})
    

def main():
    send_auto_info()
    
main()