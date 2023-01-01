import datetime
import pytz
from bot.tools.timetable import timetable

def at(arr:list, index:int):
    res = 0
    if index > len(arr)-1:
        res = index%len(arr)
    else:
        res = index
    return arr[res]

def convert_to_time(time:str):
    #  Не понимаю блять
    
    el = time.split(':')
    return datetime.time(int(el[0]), int(el[1]), 0)
    

def time_calc(t1:datetime.time, t2:datetime.time):
    #  Ебаный рот нахуй
    
    a = datetime.timedelta(hours=t1.hour, minutes=t1.minute, seconds=t1.second)
    b = datetime.timedelta(hours=t2.hour, minutes=t2.minute, seconds=t2.second)
    res = b - a
    if res.days == -1: res += datetime.timedelta(days=1)
    return res


def get_file_paths(boss_name:str):
    bosses = boss_name.split('/')
    paths = []
    for boss in bosses:
        paths.append('bot/media/'+boss.lower()+'.png')
    return paths


def convert_time(time:str):
    # Я хуй знает че тут проиходит
    
    time_arr = time.split(':')
    hours = time_arr[0]
    minuts = time_arr[1]
    seconds = time_arr[2]
    res_time = ''
    
    if int(hours) == 0:
        if int(minuts) == 0:
            res_time += f'{int(seconds)} секунд{conv(int(seconds))}'
        else:
            res_time += f'{int(minuts)} минут{conv(int(minuts))}'
    else:
        if int(minuts) == 0:
            res_time += f'{int(hours)} час'
        else:
            res_time += f'{int(hours)} час {int(minuts)} минут{conv(int(minuts))}'
    return res_time


def conv(n): 
    # -_- ?
    
    es = ['а', 'ы', '']
    n = n % 100
    if n>=11 and n<=19:
        s=es[2] 
    else:
        i = n % 10
        if i == 1:
            s = es[0] 
        elif i in [2,3,4]:
            s = es[1] 
        else:
            s = es[2] 
    return s


def get_next_boss():
    # Ахуеть блять
    
    moscow_time = datetime.datetime.now(pytz.timezone('Europe/Moscow'))
    res_boss = ''
    res_time = 0
    
    data_week = timetable[moscow_time.weekday()]
    for key in data_week.keys():
        time_boss = convert_to_time(key)
        if moscow_time.time() <= time_boss and len(data_week[key]) > 0:
            res_time = time_calc(moscow_time.time(), time_boss)
            for boss in data_week[key]:
                res_boss += boss+'/'
            break
    else:
        data = at(timetable, moscow_time.weekday()+1)
        time_boss = list(data.keys())[0]
        res_time = time_calc(moscow_time.time(), convert_to_time(time_boss))
        data_boss = data[time_boss]
        for boss in data_boss:
            res_boss += boss+'/'
            
    res_time = convert_time(str(res_time))
    res_boss = res_boss[:-1]
    
    res_data = {
        'boss':res_boss,
        'time':res_time,
        'file_paths': get_file_paths(res_boss)
    }
    
    return res_data


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