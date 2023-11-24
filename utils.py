from typing import Tuple, Any

import openai
import logging

import os
import dotenv
from openai import AsyncOpenAI

dotenv.load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
client = AsyncOpenAI()


async def generate_text(prompt) -> tuple[Any, Any]:
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content'], response['usage']['total_tokens']
    except Exception as e:
        logging.error(e)


async def generate_image(prompt, n=1, size="1024x1024") -> list[str]:
    try:
        response = await openai.Image.acreate(
            prompt=prompt,
            n=n,
            size=size
        )
        urls = []
        for i in response['data']:
            urls.append(i['url'])
    except Exception as e:
        logging.error(e)
        return []
    else:
        return urls


async def get_image(prompt):
    try:
        response = await client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        return response.data[0].url
    except Exception as e:
        logging.error(e)
    return None
