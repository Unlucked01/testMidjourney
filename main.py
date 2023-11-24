import asyncio
import logging
from io import BytesIO

from aiogram import Bot, F
from aiogram import Dispatcher
from aiogram import types
from aiogram.filters import Command
from openai import AsyncOpenAI, APIError
from aiogram import Router
from PIL import Image

import os
import dotenv

dotenv.load_dotenv()

client = AsyncOpenAI()
bot = Bot(token=os.getenv('BOT_TOKEN'))
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
dp = Dispatcher()


async def generate_image(prompt):
    response = await client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    return response.data[0].url


async def redact_image(photo, prompt):
    # img = Image.open(photo)
    # width, height = 512, 512
    # image = img.resize((width, height))
    # byte_stream = BytesIO()
    # image.save(byte_stream, format='PNG')
    # byte_array = byte_stream.getvalue()

    response = await client.images.create_variation(
        image=open(photo, 'rb'),
        n=1,
        model="dall-e-2",
        size="1024x1024"
    )

    # return response.data[0].url
    # response = await client.images.edit(
    #     model="dall-e-2",
    #     image=byte_array,
    #     mask=open("photos/mask.png", "rb"),
    #     prompt=prompt,
    #     n=1,
    #     size="512x512"
    # )
    return response.data[0].url


@dp.message()
async def get_message(message: types.Message):
    photo_id = message.photo[0].file_id
    file = await bot.get_file(photo_id)
    file_path = file.file_path
    destination = f"photos/{photo_id}.png"
    await bot.download_file(file_path, destination)
    response = await redact_image(destination, "")
    await message.reply_photo(photo=response)
    # await bot.send_message(
    #     chat_id=message.chat.id,
    #     text="Генерация изображения...",
    # )
    # if message.text:
    #     try:
    #         out = await get_image(message.text)
    #         await message.reply_photo(
    #             photo=out,
    #         )
    #     except APIError as e:
    #         print(e.message)
    #         await message.reply("Не удалось сгенерировать картинку")
    # else:
    #     await message.reply("Не удалось обработать запрос")


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
