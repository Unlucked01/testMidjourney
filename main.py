import asyncio
import logging

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import types

import os
import replicate
import dotenv

import concurrent.futures

dotenv.load_dotenv()

os.environ["REPLICATE_API_TOKEN"] = os.getenv('REPLICATE_KEY')

bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()


async def get_image(prompt: str, width=768, height=768, negative="None"):
    loop = asyncio.get_event_loop()

    def generate_image():
        return replicate.run(
            "tstramer/midjourney-diffusion:436b051ebd8f68d23e83d22de5e198e0995357afef113768c20f0b6fcef23c8b",
            input={"prompt": "mdjrny-v4 " + prompt, "negative_prompt": negative,
                    "width": width, "height": height}
        )

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(generate_image)
        output = await loop.run_in_executor(None, future.result)
    return output[0]


@dp.message()
async def get_message(message: types.Message):
    await bot.send_message(
        chat_id=message.chat.id,
        text="Генерация изображения...",
    )
    out = await get_image(message.text)
    if out:
        await message.reply_photo(
            photo=out,
        )
    else:
        await message.reply("Не удалось обработать запрос")


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
