from bot.tools.keyboards import *
from aiogram import types
from bot.tools import utils
import random


phrases = [
    'Пошел нахуй чепушила',
    'Сказано было ждать, ебанат',
    'Терпи',
    'Сука в России живешь',
    'Терпи сука',
    'Хули ты долбишься',
    'Успокойся нахуй',
    'По лбу себе постучи',
    'Утырок неотесанный',
]

async def get_info(msg: types.Message):
    tg = msg.from_user.id
    if not utils.userReq.check(tg):
        utils.userReq.add(tg)
        
        data = utils.get_next_boss()
        text = f"Следующий босс: {data['boss']}\nЧерез {data['time']}"
        
        try:
            if len(data['file_paths']) > 1:
                media = types.MediaGroup()
                for index, path in enumerate(data['file_paths']):
                    caption = text
                    if index == 1:
                        caption = None
                    media.attach_photo(types.InputFile(path), caption=caption)
                await msg.answer_media_group(media=media)
            else:
                await msg.answer_photo(photo=types.InputFile(data['file_paths'][0]), caption=text)
        except:
            await msg.answer(text=text+'\nКакой-то мудак, зажопил фото босса)')
        
        utils.userReq.remove(tg)
    else:
        await msg.answer(text=random.choice(phrases))