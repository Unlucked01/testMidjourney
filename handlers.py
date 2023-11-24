from aiogram import F, Router, flags
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

import commands
import menu
from misc import text
import utils
from states import Gen

router = Router()


@router.message(Command(text.start_activity))
async def command_start(msg: Message):
    await msg.answer(text.start_message,
                     reply_markup=ReplyKeyboardMarkup(
                         keyboard=[
                             [
                                 KeyboardButton(text="Сгенерировать картинку!"),
                                 KeyboardButton(text="Редактировать картинку!")
                             ]
                         ],
                         resize_keyboard=True,
                     ))


@router.message()

@router.message(F.text == "Меню")
@router.message(F.text == "Выйти в меню")
async def menu(msg: Message):
    await msg.answer(text.menu_message, reply_markup=menu.menu)


