from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def update():
    update_btn = KeyboardButton('🔁 Обновить')
    return ReplyKeyboardMarkup(resize_keyboard=True).add(update_btn)