from bot.tools.keyboards import *
from aiogram import types
from bot.tools import utils
from bot.tools.keyboards import menus

use_nitifications = False

async def start(msg: types.Message):
    utils.register_user(msg.from_user.id)
    await msg.answer('Ожидайте, идёт загрузка данных с сайта')
    data = await utils.get_info_about_next_boss()
    await msg.answer_photo(photo=data['place'], caption=f"Следующий босс: {data['boss']}\nЧерез {data['time']}", reply_markup=menus.update())