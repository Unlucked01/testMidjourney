import asyncio
import logging
import time
from io import BytesIO

import requests
from aiogram import Bot, F
from aiogram import Dispatcher
from aiogram import types
from aiogram.filters import Command
from openai import AsyncOpenAI, APIError
from aiogram import Router
from PIL import Image

import os
import dotenv
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

dotenv.load_dotenv()

client = AsyncOpenAI()
bot = Bot(token=os.getenv('BOT_TOKEN'))
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
dp = Dispatcher()

login = os.getenv('LOGIN')
password = os.getenv('PASSWORD')
upload_file = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                           "..", "testMidjourney/photos/test-1.jpeg"))

download_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                           "..", "testMidjourney/photos/"))


def generate_image_from_site():
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    chrome_options = Options()
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"download.default_directory={download_dir}")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(f'https://www.stylar.ai/')
    time.sleep(2)
    driver.find_element(By.CLASS_NAME, 'login-1').click()
    time.sleep(3)
    driver.find_element(By.NAME, 'username').send_keys(login)
    driver.find_element(By.NAME, 'password').send_keys(password)
    time.sleep(3)
    driver.find_element(By.CLASS_NAME, 'continue').click()
    time.sleep(3)
    driver.find_element(By.CLASS_NAME, 'new-project').click()
    time.sleep(3)
    # driver.find_element(By.CLASS_NAME, 'c-scale-size')
    # driver.find_element(By.TAG_NAME, 'button').click()
    # buttons = driver.find_element(By.CLASS_NAME, 'dialog-content')
    # button_elements = buttons.find_elements(By.TAG_NAME, 'button') # apply aspect ratio
    # button_elements.pop()
    # button_elements.pop().click()
    # time.sleep(3)
    # return
    file_input = driver.find_element(By.CLASS_NAME, "file")
    file_input.send_keys(upload_file)
    time.sleep(3)
    driver.find_element(By.CLASS_NAME, 'img2img').click()
    time.sleep(3)
    driver.find_element(By.CLASS_NAME, 'hide-style').click()
    group_elements = driver.find_element(By.CLASS_NAME, 'styles')
    li_elements = group_elements.find_elements(By.TAG_NAME, 'li')
    li_elements.pop().click()
    time.sleep(3)
    driver.find_element(By.CLASS_NAME, 'generative').click()
    time.sleep(40)
    driver.find_element(By.CLASS_NAME, 'image-cover').click()
    time.sleep(2)
    driver.find_element(By.CLASS_NAME, 'result-on-canvas').click()
    time.sleep(7)
    export = driver.find_element(By.CLASS_NAME, 'c-export')
    export.find_element(By.CLASS_NAME, 'export').click()
    time.sleep(3)
    export_dialog = driver.find_element(By.CLASS_NAME, 'c-export-dialog')
    download_footer = export_dialog.find_element(By.CLASS_NAME, 'export-dialog-footer')
    download_footer.find_element(By.CLASS_NAME, 'small').click()
    time.sleep(3)
    driver.close()
    return


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
    generate_image_from_site()
    # logging.basicConfig(level=logging.INFO)
    # await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
