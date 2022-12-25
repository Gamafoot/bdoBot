from aiogram import Dispatcher
from .main import *

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start', 'help'])