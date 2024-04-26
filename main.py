import json
from datetime import timedelta, datetime
from io import BytesIO

from PIL import Image
from aiogram.types import InputFile
import requests
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from api_manager import getAllChannels, getParseItem

from keys import TOKEN
from parser import parse
import asyncio
from aiogram import Bot, Dispatcher
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()

message_id = 0
saitUrl = "http://127.0.0.1:8000"


async def clear_jobs():
    scheduler.remove_all_jobs()


async def sendMessage(chat_id, message, image):
    global message_id
    message_obj = await bot.send_photo(chat_id=chat_id, caption=message, photo=image)
    message_id = message_obj.message_id



async def forwardMessage(sourceChatId, targetChatId):
    global message_id
    await bot.forward_message(chat_id=targetChatId, from_chat_id=sourceChatId, message_id=message_id)


async def generate_posts_schedule(channel, post_time, post_time_delta, post_quantity, post_quantity_delta):
    name_channel: str = channel["name"]
    name_channel_id: str = channel["name_id"]

    crosslink_1_id: str = channel["crosslink_1_id"]
    crosslink_2_id: str = channel["crosslink_2_id"]
    crosslink_3_id: str = channel["crosslink_3_id"]
    crosslink: bool = channel["crosslink"]
    crosslink_time = channel["crosslink_time"]
    crosslink_delta = channel["crosslink_delta"]

    list_links_tg_parsing = channel["list_links_tg_parsing"]
    list_links_tg_parsing = json.loads(list_links_tg_parsing)
    # list_links_site_parsing: dict = channel["list_links_site_parsing"]

    # Отправка на django db
    await parse(list_links_tg_parsing, name_channel)

    # Получение из django db
    parse_result = getParseItem(name_channel)

    total_posts = post_quantity + post_quantity_delta
    initial_post_time = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    current_time = initial_post_time
    for i in range(total_posts):
        post_time_for_current_post = current_time + timedelta(minutes=post_time)
        current_time = post_time_for_current_post
        post_time_for_current_post += timedelta(minutes=i * post_time_delta)
        print(f"post_time_for_current_post: {post_time_for_current_post}")

        post_content_for_current_post: dict = parse_result[i % len(parse_result)]

        caption = f"{post_content_for_current_post['title']} {post_content_for_current_post['description']}"
        image = post_content_for_current_post['image_url']
        print(f"{saitUrl}{image}")
       # await sendMessage(name_channel_id, caption, f"{saitUrl}{image}")
        await sendMessage(name_channel_id, caption, f"https://cdn.litemarkets.com/cache/uploads/blog_post/blog_posts/BTC_Price_Analysis/Bitcoin-Price-Prediction.jpg?q=75&w=1000&s=6c20e77623d5230b4c2fdd5d461b9feb")
        # scheduler.add_job(sendMessage, 'date', run_date=post_time_for_current_post,
        #                   args=[name_channel_id, caption, image])

        if crosslink:
            crosslink_time_for_current_post = current_time + timedelta(hours=crosslink_time)
            current_time = crosslink_time_for_current_post
            crosslink_time_for_current_post += timedelta(hours=i * crosslink_delta)
            print(f"crosslink_time_for_current_post: {crosslink_time_for_current_post}")
            if crosslink_1_id:
                # scheduler.add_job(forwardMessage, 'date', run_date=crosslink_time_for_current_post,
                #                   args=[name_channel_id, crosslink_1_id, message_id])
                await forwardMessage(name_channel_id, crosslink_1_id)
            elif crosslink_2_id:
                scheduler.add_job(forwardMessage, 'date', run_date=crosslink_time_for_current_post,
                                  args=[name_channel_id, crosslink_2_id, message_id])
            elif crosslink_3_id:
                scheduler.add_job(forwardMessage, 'date', run_date=crosslink_time_for_current_post,
                                  args=[name_channel_id, crosslink_3_id, message_id])


async def generate_posts():
    all_channels = getAllChannels()
    for channel in all_channels:
        if channel["autopost"]:
            post_time = channel["post_time"]
            post_time_delta = channel["post_time_delta"]
            post_quantity = channel["post_quantity"]
            post_quantity_delta = channel["post_quantity_delta"]
            await generate_posts_schedule(channel, post_time, post_time_delta, post_quantity, post_quantity_delta)
        else:
            continue


async def mainFunc():
    scheduler.add_job(clear_jobs, 'cron', hour=12, minute=0, second=0, timezone='UTC')
    #scheduler.add_job(generate_posts, 'cron', hour=12, minute=0, second=0, timezone='UTC')
    await generate_posts()
    await dp.start_polling(bot)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(mainFunc())
    loop.run_forever()
