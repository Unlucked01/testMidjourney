from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

import handlers
from main import dp
from aiogram import types, F
from misc import text
from aiogram.fsm.context import FSMContext


builder = InlineKeyboardBuilder()

menu_markup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=text.profile_button), KeyboardButton(text=text.activity_button)],
        [KeyboardButton(text=text.shop_button), KeyboardButton(text=text.orders_button)]
    ],
    resize_keyboard=True
)


@dp.message(Command(text.start_command))
async def welcome_command(message: types.Message):
    await message.answer(text.start_message)
    await menu_command(message)


@dp.message(Command(text.menu_command))
@dp.message(F.text == text.back_button)
async def menu_command(message: types.Message):
    await message.answer(text.menu_message, reply_markup=menu_markup)


@dp.message(Command(text.menu_command))
@dp.message(F.text == text.activity_button)
async def activity(message: types.Message):
    await handlers.command_start(message, Form.initial)
