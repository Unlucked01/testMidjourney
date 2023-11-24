import asyncio
import logging

from aiogram import Bot, F
from aiogram import Dispatcher
from aiogram import types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from openai import AsyncOpenAI, APIError
from aiogram import Router

import os
import dotenv

import commands

dotenv.load_dotenv()

client = AsyncOpenAI()
bot = Bot(token=os.getenv('BOT_TOKEN'))
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
dp = Dispatcher()


menu_markup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=commands.generate), KeyboardButton(text=commands.redact)],
        [KeyboardButton(text=commands.menu_command)],
    ],
    resize_keyboard=True
)


@dp.message(Command(commands.start_command))
async def welcome_command(message: types.Message):
    await message.answer(commands.start_message)
    await menu_command(message)


@dp.message(Command(commands.menu_command))
@dp.message(F.text == commands.back_button)
async def menu_command(message: types.Message):
    await message.answer(commands.menu_message, reply_markup=menu_markup)


@dp.message(Command(commands.menu_command))
@dp.message(F.text == commands.generate)
async def generate(message: types.Message):
    await message.answer(commands.generate, reply_markup=menu_markup)


@dp.message(Command(commands.menu_command))
@dp.message(F.text == commands.redact)
async def generate(message: types.Message):
    await message.answer(commands.redact, reply_markup=menu_markup)


async def get_image(prompt):
    response = await client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    return response.data[0].url


@dp.message(Command(commands.generate))
async def get_message(message: types.Message):
    await bot.send_message(
        chat_id=message.chat.id,
        text="Генерация изображения...",
    )
    if message.text:
        try:
            out = await get_image(message.text)
            await message.reply_photo(
                photo=out,
            )
        except APIError as e:
            print(e.message)
            await message.reply("Не удалось сгенерировать картинку")
    else:
        await message.reply("Не удалось обработать запрос")


@dp.message(Command(commands.generate))
async def redact_image(message: types.Message):
    await message.answer("handle redact command")


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
