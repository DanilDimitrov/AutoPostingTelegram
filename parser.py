import datetime
from api_manager import generateText, generateImage, get_themes, parsed_item
from keys import API_ID, API_HASH, containsAD, find_word_in_text
from pyrogram import Client
from deep_translator import GoogleTranslator
from en_sait_parse import *
from ru_sait_parse import *

data_for_gpt = """rephrase this text in other words,
                        remove all links and hyperlink, 
                        remove all references to social networks from the text"""
data_for_title = "give a theme for this text in 5 words"

available_saits = [cryptoNews, ihodi, cointelegraph, coindesk, bitcoinist, decrypt,
                   forklog, coinspot, coinspot, ttrcoin, altcoinlog]


def translateText(target_language_for_google, text):
    translated_text = GoogleTranslator(source='auto', target=target_language_for_google).translate(text)
    return translated_text


async def go_to_admin(themes, sait, channel_go_to, language, text):
    query_to_GPT = f" {data_for_gpt} {text}"
    desc: str = generateText(query_to_GPT)
    data_for_theme = (f"Here are all the topics I have: {themes},"
                      f" Which of these topics does this text relate to? {desc}, "
                      f"((choose only from these topics that I gave you))"
                      f", give a simple answer where there will only be a topic")

    if len(desc) >= 240:
        description = ' '.join(desc.split()[:240])
        print(len(desc))
    else:
        description = desc

    tit = generateText(f"{data_for_title} {description}")
    if len(tit) >= 12:
        title = ' '.join(tit.split()[:12])
        print(len(title))
    else:
        title = tit
    generateImagePrompt = f"generate prompt for generate beauty crypto image with this text: {title}"
    print(generateImagePrompt)
    generateImagePromptExe = generateText(generateImagePrompt)

    theme = generateText(data_for_theme)
    theme = find_word_in_text(themes, theme)
    print(theme)
    message_date = datetime.datetime.now()
    milliseconds = message_date.timestamp() * 1000
    image = generateImage(
        f"{generateImagePromptExe}, crypto photo, btc, etherium, blockchain, nft, crypto, cyberpunk style, crypto cyber,")

    if language == "ru":
        title = translateText('ru', title)
        description = translateText('ru', description)
    else:
        title = translateText('en', title)
        description = translateText('en', description)


    pars = parsed_item(title=title,
                       description=description,
                       date=milliseconds,
                       image=image,
                       channelParsed=sait,
                       channel_go_to=channel_go_to,
                       prediction_theme=theme)
    print(pars)


async def clone_content(client, source_channel_id: int, themes, source_channel_name: str, channel_go_to: str, language):
    try:
        messages = client.get_chat_history(chat_id=source_channel_id, limit=1)
        async for message in messages:
            if message.caption:
                try:
                    if not containsAD(message.caption.lower()):
                        query_to_GPT = f" {data_for_gpt} {message.caption}"
                        desc: str = generateText(query_to_GPT)
                        data_for_theme = (f"Here are all the topics I have: {themes},"
                                          f" Which of these topics does this text relate to? {desc}, "
                                          f"((choose only from these topics that I gave you))"
                                          f", give a simple answer where there will only be a topic")

                        if len(desc) >= 230:
                            description = ' '.join(desc.split()[:230])
                            print(len(desc))
                        else:
                            description = desc

                        tit = generateText(f"{data_for_title} {description}")
                        if len(tit) >= 10:
                            title = ' '.join(tit.split()[:10])
                            print(len(title))
                        else:
                            title = tit
                        generateImagePrompt = f"generate prompt for generate beauty crypto image with this text: {title}"
                        print(generateImagePrompt)
                        generateImagePromptExe = generateText(generateImagePrompt)

                        theme = generateText(data_for_theme)
                        theme = find_word_in_text(themes, theme)
                        print(theme)
                        message_date = datetime.datetime.strptime(str(message.date), "%Y-%m-%d %H:%M:%S")
                        milliseconds = message_date.timestamp() * 1000
                        image = generateImage(
                            f"{generateImagePromptExe}, crypto photo, btc, etherium, blockchain, nft, crypto, cyberpunk style, crypto cyber,")

                        if language == "ru":
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
                    print("Error in Pars")
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


async def clone_content_sait(sait, themes, channel_go_to, language):
    if sait in available_saits:
        en_saits = {
            ihodi: parse_ihodi_article,
            cointelegraph: parse_coinTelegraph_article,
            coindesk: parse_coindesk_article,
            bitcoinist: parse_bitcoinist_article,
            decrypt: parse_decrypt_article,
        }
        ru_saits = {
            forklog: parse_forklog,
            coindeskru: parse_coindesk_articleru,
            ttrcoin: parse_ttrcoin_article,
            altcoinlog: parse_altcoinlog_article,
        }
        text = ""
        if sait in en_saits:
            text = en_saits[sait]()
        elif sait in ru_saits:
            text = ru_saits[sait]()
        await go_to_admin(themes, sait, channel_go_to, language, text)
    else:
        print(f"sait: {sait} is not available")


async def parse(channels_en_id: dict, channel_go_to, language, list_links_site_parsing: list):
    client = Client(name='client', api_id=API_ID, api_hash=API_HASH)
    await client.start()
    try:
        themes = get_themes()
        for channel_name, channel_id in channels_en_id.items():
            await clone_content(client, channel_id, themes, channel_name, channel_go_to, language)
        for sait in list_links_site_parsing:
            await clone_content_sait(sait, themes, channel_go_to, language)
    finally:
        await client.stop()



