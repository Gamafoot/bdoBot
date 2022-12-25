from aiogram import Dispatcher
from .main import *
from aiogram.dispatcher.filters import Text


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(get_info, Text(equals='🔁 Обновить'))