from aiogram import Dispatcher, Bot, executor
import config


bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

def register_handlers():
    from .handlers import commands, info
    commands.register_handlers(dp)
    info.register_handlers(dp)


def start_bot():    
    register_handlers()
    
    executor.start_polling(dp, skip_updates=True)