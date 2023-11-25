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
TOKEN = bot.token

login = os.getenv('LOGIN')
password = os.getenv('PASSWORD')
upload_file = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                           "..", "testMidjourney/photos/"))

download_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            "..", "testMidjourney/generated_photos/"))

SEND_PHOTO = f'https://api.telegram.org/bot{TOKEN}/sendPhoto'
DOWNLOAD_PHOTO = f'https://api.telegram.org/bot{TOKEN}/getfile?file_id='


def generate_image_from_site(photo_id):
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    chrome_options = Options()
    prefs = {"download.default_directory": f"{download_dir}"}
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(f'https://www.stylar.ai/')
    time.sleep(2)
    driver.find_element(By.CLASS_NAME, 'login-1').click()
    time.sleep(2)
    driver.find_element(By.NAME, 'username').send_keys(login)
    driver.find_element(By.NAME, 'password').send_keys(password)
    time.sleep(2)
    driver.find_element(By.CLASS_NAME, 'continue').click()
    time.sleep(2)
    driver.find_element(By.CLASS_NAME, 'new-project').click()
    time.sleep(2)
    project_properties = driver.find_element(By.CLASS_NAME, 'c-scale-size')
    project_properties.find_element(By.TAG_NAME, 'button').click()
    properties = project_properties.find_element(By.CLASS_NAME, 'dialog-content')
    li_elements = properties.find_elements(By.TAG_NAME, 'li')
    for elem in li_elements:
        if elem.text == "Project name":
            proj_name = elem.find_element(By.CLASS_NAME, 'project-name')
            proj_name.send_keys("_" + photo_id[:51])

    buttons = properties.find_elements(By.CLASS_NAME, 'stances')
    for b in buttons:
        ratio = b.find_element(By.CLASS_NAME, 'ratio')
        if ratio.text == "16:9":
            b.click()
    time.sleep(2)
    properties.find_element(By.CLASS_NAME, 'done').click()
    time.sleep(2)
    file_input = driver.find_element(By.CLASS_NAME, "file")
    file_input.send_keys(upload_file + "/" + photo_id + ".png")
    time.sleep(2)
    driver.find_element(By.CLASS_NAME, 'img2img').click()
    time.sleep(2)
    driver.find_element(By.CLASS_NAME, 'hide-style').click()
    group_elements = driver.find_element(By.CLASS_NAME, 'styles')
    li_elements = group_elements.find_elements(By.TAG_NAME, 'li')
    li_elements.pop().click()
    time.sleep(2)
    driver.find_element(By.CLASS_NAME, 'generative').click()
    time.sleep(35)
    driver.find_element(By.CLASS_NAME, 'image-cover').click()
    time.sleep(2)
    driver.find_element(By.CLASS_NAME, 'result-on-canvas').click()
    time.sleep(4)
    export = driver.find_element(By.CLASS_NAME, 'c-export')
    export.find_element(By.CLASS_NAME, 'export').click()
    time.sleep(2)
    export_dialog = driver.find_element(By.CLASS_NAME, 'c-export-dialog')
    download_footer = export_dialog.find_element(By.CLASS_NAME, 'export-dialog-footer')
    download_footer.find_element(By.CLASS_NAME, 'small').click()
    time.sleep(2)
    driver.close()
    return


@dp.message()
async def get_message(message: types.Message):
    photo_id = message.photo[-1].file_id
    file = await bot.get_file(photo_id)
    file_path = file.file_path
    destination = f"photos/{photo_id}.png"
    await bot.download_file(file_path, destination)
    generate_image_from_site(photo_id)
    image = Image.open(f'generated_photos/Untitled_{photo_id[:51]}.png')
    with BytesIO() as output:
        image.save(output, format='PNG')
        output.seek(0)
        requests.post(SEND_PHOTO, data={'chat_id': message.chat.id}, files={'photo': output.read()})


async def main():
    # generate_image_from_site("photos/test-1.jpeg")
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
