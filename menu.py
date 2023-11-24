from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

import commands
builder = InlineKeyboardBuilder()

menu_markup = [
        [InlineKeyboardButton(text="Сгенерировать изображения", callback_data=commands.generate),
            InlineKeyboardButton(text="Отредактировать изображение", callback_data=commands.redact)],
        [KeyboardButton(text=commands.menu_command)]
]

menu = InlineKeyboardMarkup(inline_keyboard=menu_markup)
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Выйти в меню")]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]])


async def build_kb(msg):
    for i in range(15):
        builder.button(text=f"Кнопка {i}", callback_data=f"button_{i}")
    builder.adjust(2)
    await msg.answer("Текст сообщения", reply_markup=builder.as_markup())
