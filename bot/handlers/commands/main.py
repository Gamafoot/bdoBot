from bot.tools.keyboards import *
from aiogram import types
from bot.tools import database
from bot.tools.keyboards import menus


async def start(msg: types.Message):
    database.add_user(msg.from_user.id)
    await msg.answer('Добро пожаловать в бота!', reply_markup=menus.update())