import asyncio
import logging

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import types
from openai import AsyncOpenAI

import os
import dotenv


dotenv.load_dotenv()

client = AsyncOpenAI()
bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()


async def get_image(prompt):
    response = await client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    return response.data[0].url


@dp.message()
async def get_message(message: types.Message):
    await bot.send_message(
        chat_id=message.chat.id,
        text="Генерация изображения...",
    )
    if message.text:
        out = await get_image(message.text)
        if out:
            await message.reply_photo(
                photo=out,
            )
        else:
            await message.reply("Не удалось сгенерировать картинку")
    else:
        await message.reply("Не удалось обработать запрос")


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
