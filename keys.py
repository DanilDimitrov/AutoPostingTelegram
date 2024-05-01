import re

from aiogram.types import Message

# API_ID = 22879221
# API_HASH = "77a7cb48de2329dfa0bab369cd084962"
API_ID = 28640102
API_HASH = "ae3821b446c57a6725347b12ab6aa93b"


#TOKEN = "7156398040:AAHkMiQ4ORAaN3OnXqK0hr45KaTWY1D9QCI"
TOKEN = "6506417602:AAEoALt6bdbgC_rsTjxUNSGh5VGxP8nIVKo"


keys = ["#BTC", "#Binance", "#LTC", "#listing", "#airdrop"]
ad = ["ad", "partner", "promotion", "learn more", "to learn more",
      "exchanges", "free", "win", "reward", "insider", "subscription",
      "exclusive", "special", "vip", "premium", "limited",
      "invitation", "join", "coach", "channel", "product", "play", "bot", "draw", "network",
      "реклама", "партнер", "повышение", "узнать больше", "обмен", "бесплатн", "побед",
      "наград", "инсайдер", "подписк", "премиум", "ограниченное", "эксклюзивн", "особенн",
      "приглашен", "присоедин", "тренер", "канал", "продукт", "игра", "бот", "розыгрыш",
      "социальная", "detail", "детали", "link", "ссылк"]


def contains_keywords(message_text):
    message_text = message_text
    for keyword in keys:
        if keyword.lower() in message_text:
            return True
    return False


def containsAD(message_text):
    message_text = message_text
    for key in ad:
        if key.lower() in message_text:
            return False
    return False


def validate_photo_and_len(message: Message):
    if len(message.caption) > 100 and message.photo:
        return True
    elif len(message.caption) > 100 and not message.photo:
        return True
    else:
        return False


def remove_links_and_text(html_text):
    pattern = r'<a\s+(?:[^>]*?\s+)?href="([^"]*)"([^>]*)>(.*?)</a>'

    def replace_link_and_text(match):
        return ''

    cleaned_text = re.sub(pattern, replace_link_and_text, html_text)
    return cleaned_text


def find_word_in_text(word_array, text):
    for word in word_array:
        if word in text:
            return word
    return None