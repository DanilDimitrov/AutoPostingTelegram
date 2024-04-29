import asyncio
import datetime
from api_manager import generateText, generateImage, get_themes, parsed_item
from keys import API_ID, API_HASH, validate_photo_and_len, containsAD, find_word_in_text
from pyrogram import Client
from deep_translator import GoogleTranslator


def translateText(target_language_for_google, text):
    translated_text = GoogleTranslator(source='auto', target=target_language_for_google).translate(text)
    return translated_text


async def clone_content(client, source_channel_id: int, themes, source_channel_name: str, channel_go_to: str, language):
    try:
        messages = client.get_chat_history(chat_id=source_channel_id, limit=1)
        async for message in messages:
            if message.caption:
                try:
                    if not containsAD(message.caption.lower()) and validate_photo_and_len(message):
                        data_for_gpt = """rephrase this text in other words, 
                        remove all links and hyperlink, 
                        remove all references to social networks from the text"""
                        data_for_title = "give a theme for this text in 5 words"
                        query_to_GPT = f" {data_for_gpt} {message.caption}"
                        description: str = generateText(query_to_GPT)
                        data_for_theme = (f"Here are all the topics I have: {themes},"
                                          f" Which of these topics does this text relate to? {description}, "
                                          f"((choose only from these topics that I gave you))"
                                          f", give a simple answer where there will only be a topic")

                        title = generateText(f"{data_for_title} {description}")
                        theme = generateText(data_for_theme)
                        theme = find_word_in_text(themes, theme)
                        print(theme)
                        message_date = datetime.datetime.strptime(str(message.date), "%Y-%m-%d %H:%M:%S")
                        milliseconds = message_date.timestamp() * 1000
                        image = generateImage(
                            f"{title} crypto photo, btc, etherium, blockchain, cinematic, nft, crypto, ")

                        if language == "Russian":
                            title = translateText('ru', title)
                            description = translateText('ru', description)
                        else:
                            title = translateText('en', title)
                            description = translateText('en', description)

                        pars = parsed_item(title=title,
                                           description=description,
                                           date=milliseconds,
                                           image=image,
                                           channelParsed=source_channel_name,
                                           channel_go_to=channel_go_to,
                                           prediction_theme=theme)
                        print(pars)

                except:
                    continue

    except Exception as e:
        print(e)


async def get_last_message_id(channel_id) -> int:
    client = Client(name='client', api_id=API_ID, api_hash=API_HASH)
    await client.start()
    try:
        async for message in client.get_chat_history(chat_id=channel_id, limit=1):
            message_id: int = message.id
            return message_id
    finally:
        await client.stop()


async def parse(channels_en_id: dict, channel_go_to, language):
    client = Client(name='client', api_id=API_ID, api_hash=API_HASH)
    await client.start()
    try:
        themes = get_themes()
        for channel_name, channel_id in channels_en_id.items():
            await clone_content(client, channel_id, themes, channel_name, channel_go_to, language)
    finally:
        await client.stop()
