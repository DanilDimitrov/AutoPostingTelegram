import json
from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta, datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.types import URLInputFile
from api_manager import getAllChannels, getParseItem

from keys import TOKEN
from parser import parse, get_last_message_id
import asyncio
from aiogram import Bot, Dispatcher
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()
executor = ThreadPoolExecutor()

saitUrl = "http://138.201.33.30:999"
#saitUrl = "http://127.0.0.1:8000"


async def clear_jobs():
    scheduler.remove_all_jobs()


async def sendMessage(chat_id, message, image):
    image = URLInputFile(
        image, filename="image.png"
    )
    print(message)
    await bot.send_photo(chat_id=chat_id, caption=message, photo=image)


async def forwardMessage(sourceChatId, targetChatId):
    message_id = await get_last_message_id(sourceChatId)
    await bot.forward_message(chat_id=targetChatId, from_chat_id=sourceChatId, message_id=message_id)


async def generate_posts_schedule(channel, post_time, post_time_delta, post_quantity, post_quantity_delta):
    try:
        name_channel: str = channel["name"]
        name_channel_id: str = channel["name_id"]
        language: str = channel["language"]

        crosslink_1_id: str = channel["crosslink_1_id"]
        crosslink_2_id: str = channel["crosslink_2_id"]
        crosslink_3_id: str = channel["crosslink_3_id"]
        crosslink: bool = channel["crosslink"]
        crosslink_time = channel["crosslink_time"]
        crosslink_delta = channel["crosslink_delta"]

        list_links_tg_parsing = channel["list_links_tg_parsing"]
        list_links_tg_parsing = json.loads(list_links_tg_parsing)

        list_links_site_parsing = []
        if channel["list_links_site_parsing"]:
            cleaned_string = channel["list_links_site_parsing"].strip('[]\r\n')
            list_links_site_parsing = [link.strip() for link in cleaned_string.split(',')]
            print(list_links_site_parsing)

        # Отправка на django db
        await parse(list_links_tg_parsing, name_channel, language, list_links_site_parsing)

        # Получение из django db
        parse_result_no_unique = sorted(getParseItem(name_channel), key=lambda x: x["date"], reverse=True)

        # это для выбора уникальных постов
        unique_descriptions = set()
        parse_result = []

        for item in parse_result_no_unique:
            description = item['description']
            if description not in unique_descriptions:
                parse_result.append(item)
                unique_descriptions.add(description)
            else:
                pass

        print(len(parse_result))

        total_posts = post_quantity + post_quantity_delta
        current_date = datetime.utcnow().date()
        initial_post_time = datetime.combine(current_date, datetime.min.time())

        for i in range(total_posts):
            post_time_for_current_post = initial_post_time + (i * timedelta(minutes=post_time_delta)) + timedelta(
                minutes=post_time)
            print(f"post_time_for_current_post: {post_time_for_current_post.strftime('%Y-%m-%d %H:%M:%S')}")

            post_content_for_current_post: dict = parse_result[i % len(parse_result)]
            caption = f"{post_content_for_current_post['title']} {post_content_for_current_post['description']}"
            image = post_content_for_current_post['image_url']
            print(f"{saitUrl}{image}")

            scheduler.add_job(sendMessage, 'date', run_date=post_time_for_current_post,
                              args=[name_channel_id, caption,
                                    f"{saitUrl}{image}"
                                    ], max_instances=1)
            crosslinkTg(crosslink, post_time_for_current_post,
                        crosslink_time, crosslink_1_id, name_channel_id,
                        crosslink_2_id, crosslink_3_id)
    except Exception as ex:
        print(f"error: {ex}")


def crosslinkTg(crosslink, post_time_for_current_post,
                crosslink_time, crosslink_1_id, name_channel_id,
                crosslink_2_id, crosslink_3_id):
    if crosslink:
        crosslink_time_for_current_post = post_time_for_current_post + timedelta(hours=crosslink_time)
        print(f"crosslink_time_for_current_post: {crosslink_time_for_current_post.strftime('%Y-%m-%d %H:%M:%S')}")
        if crosslink_1_id:
            scheduler.add_job(forwardMessage, 'date', run_date=crosslink_time_for_current_post,
                              args=[name_channel_id, crosslink_1_id], max_instances=1)
            # await forwardMessage(name_channel_id, crosslink_1_id)
        elif crosslink_2_id:
            scheduler.add_job(forwardMessage, 'date', run_date=crosslink_time_for_current_post,
                              args=[name_channel_id, crosslink_2_id], max_instances=1)
        elif crosslink_3_id:
            scheduler.add_job(forwardMessage, 'date', run_date=crosslink_time_for_current_post,
                              args=[name_channel_id, crosslink_3_id], max_instances=1)


async def generate_posts():
    all_channels = getAllChannels()
    for channel in all_channels:
        print(channel)
        if channel["autopost"]:
            post_time = channel["post_time"]
            post_time_delta = channel["post_time_delta"]
            post_quantity = channel["post_quantity"]
            post_quantity_delta = channel["post_quantity_delta"]
            await generate_posts_schedule(channel, post_time, post_time_delta, post_quantity, post_quantity_delta)
        else:
            continue


async def mainFunc():
    #await generate_posts()
    scheduler.add_job(generate_posts, 'cron', hour=10, minute=40, second=0, timezone='Europe/Kyiv')
    scheduler.start()
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        loop.create_task(mainFunc())
        loop.run_forever()
    except:
        scheduler.shutdown()
        loop.run_until_complete(bot.close())

