import requests
from config import TOKEN
from bot.tools import database
import time
import json
import re
from bot.tools.utils import get_next_boss

wait = 10

loop_end = 600


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
                game_data = get_next_boss()
                if game_data['boss'].lower() != last_boss and check_time(game_data['time'], 50):
                    last_boss = game_data['boss'].lower()
                    send_message(user_tg, game_data)
                    
def check_time(current_time, min_time):
    hour = re.search('(\d+) час', current_time)
    if not hour.group(1):
        res = re.search('(\d+) минут', current_time)
        if int(res.group(1)) <= min_time:
            return True
    return False
            
            
def send_message(tg_id, game_data):
    text = f"Следующий босс: {game_data['boss']}\nБудет через {game_data['time']}"
    if len(game_data['file_paths']) > 1:
        bosses_arr = game_data['boss'].split('/')
        data = {
            "chat_id": tg_id,
            "media": json.dumps([
                {"type": "photo", "media": f"attach://{bosses_arr[0].lower()}.png", "caption":text},
                {"type": "photo", "media": f"attach://{bosses_arr[1].lower()}.png"}
            ])
        }

        files = {
            f"{bosses_arr[0].lower()}.png" : open(game_data['file_paths'][0], 'rb'),
            f"{bosses_arr[1].lower()}.png" : open(game_data['file_paths'][1], 'rb')
        }

        requests.post("https://api.telegram.org/bot" + TOKEN + "/sendMediaGroup", data=data, files=files)
    else:
        data = {"chat_id": tg_id, "caption": text}
        url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
        file = open(game_data['file_paths'][0], 'rb')
        requests.post(url, data=data, files={"photo": file})
    

def main():
    send_auto_info()
    
main()