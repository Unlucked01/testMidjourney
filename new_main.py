import asyncio
import logging

from aiogram import Bot, F
from aiogram import Dispatcher
from aiogram import types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.chat_action import ChatActionMiddleware
from aiogram.utils.keyboard import InlineKeyboardBuilder
from openai import AsyncOpenAI, APIError
from aiogram import Router

import os
import dotenv

import commands
from handlers import router

dotenv.load_dotenv()

client = AsyncOpenAI()
bot = Bot(token=os.getenv('BOT_TOKEN'))
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
dp = Dispatcher()
dp.include_router(router)
dp.message.middleware(ChatActionMiddleware())


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
