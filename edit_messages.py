import asyncio
import logging

from aiogram import Bot, types
from keys import API_ID, API_HASH, containsAD, find_word_in_text
from pyrogram import Client
from api_manager import get_all_posts

bot = Bot(token="7156398040:AAHkMiQ4ORAaN3OnXqK0hr45KaTWY1D9QCI")
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
messages_id = []
parse_result = []

saitUrl = "http://138.201.33.30:999"
#saitUrl = "http://127.0.0.1:8000"

def get_posts():
    parse_result_no_unique = get_all_posts()
    unique_descriptions = set()
    for item in parse_result_no_unique:
        description = item['description']
        if description not in unique_descriptions:
            parse_result.append(item)
            unique_descriptions.add(description)
        else:
            pass


async def get_chat_history(channel_id):
    client = Client(name='client', api_id=API_ID, api_hash=API_HASH)
    await client.start()
    try:
        async for message in client.get_chat_history(chat_id=channel_id):
            message_id: int = message.id
            messages_id.append(message_id)
        print(messages_id)
        return messages_id
    finally:
        await client.stop()


async def edit_posts(url, caption, post_id):
    photo = types.InputMediaPhoto(media=url, caption=caption)

    await bot.edit_message_media(chat_id=-1002111756303, message_id=post_id, media=photo)


async def mainFunc():
    get_posts()
    await get_chat_history(-1002111756303)
    print(len(parse_result))

    for post_id, post in zip(messages_id, parse_result):
        try:
            cap = (post['title'] + post['description']).split()
            caption = ' '.join(cap[:100])
            print(f"{saitUrl}{post['image_url']}")

            await edit_posts(f"{saitUrl}{post['image_url']}", caption, post_id)
        except:
            continue


if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        loop.create_task(mainFunc())
        loop.run_forever()
    except KeyboardInterrupt:
        loop.run_until_complete(bot.close())
