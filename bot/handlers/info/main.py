from bot.tools.keyboards import *
from aiogram import types
from bot.tools import utils
import random


phrases = [
    'Пошел нахуй чепушила',
    'Тебе сказано было ждать ебанат',
    'Терпи',
    '"Ожидайте, идёт загрузка данных с сайта" <- ты блять читал это?!'
    'Терпи сука',
    'Хули ты долбишься, щас бан выдам',
]

async def get_info(msg: types.Message):
    tg = msg.from_user.id
    if not utils.userReq.check(tg):
        utils.userReq.add(tg)
        await msg.answer('Ожидайте, идёт загрузка данных с сайта')
        data = await utils.get_info_about_next_boss()
        await msg.answer_photo(photo=data['place'], caption=f"Следующий босс: {data['boss']}\nЧерез {data['time']}", reply_markup=menus.update())
        utils.userReq.remove(tg)
    else:
        await msg.answer(random.choice(phrases))