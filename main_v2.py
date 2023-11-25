import asyncio
import base64
import logging
import time
from io import BytesIO

import requests
from aiogram import Bot, F
from aiogram import Dispatcher
from aiogram import types
from aiogram.enums import ContentType
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
TOKEN = bot.token

login = os.getenv('LOGIN')
password = os.getenv('PASSWORD')
upload_file = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                           "..", "testMidjourney/photos/"))

download_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            "..", "testMidjourney/generated_photos/"))

SEND_PHOTO = f'https://api.telegram.org/bot{TOKEN}/sendPhoto'
DOWNLOAD_PHOTO = f'https://api.telegram.org/bot{TOKEN}/getfile?file_id='


def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


async def image_to_text(photo_url):
    response = await client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What’s in this image?"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": photo_url,
                        },
                    },
                ],
            }
        ],
        max_tokens=300,
    )
    return response.choices[0].message.content


async def text_to_image(prompt):
    response = await client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1792x1024",
        quality="standard",
        n=1,
    )
    return response.data[0].url


def send_image(base64_image):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Describe everything on picture like you are "
                                "trying to generate an interior out of your prompt, "
                                "avoid making collage, do the whole interior"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }
    return requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)


@dp.message()
async def get_message(message: types.Message):
    await bot.send_message(message.chat.id, "Генерация изображения...")
    match message.content_type:
        case ContentType.TEXT:
            print("text generating")
            txt2img = await text_to_image(message.text)
            print(txt2img)
            await message.reply_photo(photo=txt2img)
        case ContentType.PHOTO:
            print("image generating")
            photo_id = message.photo[-1].file_id
            file = await bot.get_file(photo_id)
            file_path = file.file_path
            destination = f"photos/{photo_id}.png"
            await bot.download_file(file_path, destination)
            base64_image = encode_image(destination)
            response = send_image(base64_image)
            if response.status_code == 200:
                result = response.json()

                img2txt = result['choices'][0]['message']['content']
                print(img2txt)
                txt2img = await text_to_image(img2txt)
                await message.reply_photo(photo=txt2img)
        case _:
            await message.reply("Не распознано...")


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
