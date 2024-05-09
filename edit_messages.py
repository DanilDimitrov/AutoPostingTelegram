import asyncio
import logging

from aiogram import Bot, types
from deep_translator import GoogleTranslator

from keys import API_ID, API_HASH, containsAD, find_word_in_text
from pyrogram import Client
from api_manager import get_all_posts

bot = Bot(token="6506417602:AAEoALt6bdbgC_rsTjxUNSGh5VGxP8nIVKo")
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
messages_id = []
parse_result = []

saitUrl = "http://138.201.33.30:999"
#saitUrl = "http://127.0.0.1:8000"


def translateText(target_language_for_google, text):
    translated_text = GoogleTranslator(source='auto', target=target_language_for_google).translate(text)
    return translated_text


def get_posts():
    parse_result_no_unique = get_all_posts()
    unique_descriptions = set()
    for item in parse_result_no_unique:
        description = item['description']
        if (description not in unique_descriptions) and len(description) < 500:
            parse_result.append(item)
            unique_descriptions.add(description)
        else:
            continue


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
    image = types.URLInputFile(
        url, filename="image.png"
    )
    captionTrans = translateText("ru", caption)
    photo = types.InputMediaPhoto(media=image, caption=captionTrans, filename="image.png")
    await bot.edit_message_media(chat_id=-1001925019718, message_id=post_id, media=photo)


async def mainFunc():
    get_posts()
    await get_chat_history(-1001925019718)
    print(len(parse_result))

    for post_id, post in zip(messages_id, parse_result):
        try:
            caption = (post['title'] + post['description'])
            photo_url = f"{saitUrl}{post['image_url']}"
            print(photo_url)
            await edit_posts(photo_url, caption, post_id)
        except Exception as ex:
            print(ex)
            continue


if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        loop.create_task(mainFunc())
        loop.run_forever()
    except KeyboardInterrupt:
        loop.run_until_complete(bot.close())
