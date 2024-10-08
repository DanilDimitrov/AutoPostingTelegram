import requests
import io
from PIL import Image

to_generate_image = "http://127.091.00.11:5555/generate_image"
to_generate_text = "http://127.091.00.11:5555/generate_text"
get_all_themes = "http://127.091.00.11:999/themes"
get_all_channels = "http://127.091.00.11:999/channels"
get_parsed_item = "http://127.091.00.11:999/get_ParsedItems"
create_parse_item = "http://127.091.00.11:999/create_parse_item/"
get_all_posts_url = "http://127.091.00.11:999/get_all_posts/"

# get_all_posts_url = "http://127.0.0.1:8000/get_all_posts/"
# get_all_themes = "http://127.0.0.1:8000/themes"
# get_all_channels = "http://127.0.0.1:8000/channels"
# get_parsed_item = "http://127.0.0.1:8000/get_ParsedItems"
# create_parse_item = "http://127.0.0.1:8000/create_parse_item/"

API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
headers = {"Authorization": "Bearer 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"}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content


def generateImage(prompt):
    data = {"prompt": prompt}
    response = requests.post(to_generate_image, json=data)
    if response.status_code == 200:
        data = response.content
        return data
    else:
        print('Error:', response.status_code)


def generateText(prompt) -> str:
    data_to_load = {"prompt": prompt}
    response = requests.post(to_generate_text, json=data_to_load)
    if response.status_code == 200:
        parse_data = response.text
        return parse_data
    else:
        print('Error:', response.status_code)


def get_themes():
    response = requests.get(get_all_themes)
    if response.status_code == 200:
        data: list = response.json()["themes"]
        return data
    else:
        print('Error:', response.status_code)


def getParseItem(channelGoTo):
    url = f"{get_parsed_item}/?channelGoTo={channelGoTo}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()["parsed_items"]
        return data
    else:
        print('Error:', response.status_code)


def parsed_item(title, description, date, image_bytes, channelParsed, channel_go_to, prediction_theme):
    image = Image.open(io.BytesIO(image_bytes))

    buf = io.BytesIO()
    image.save(buf, format='PNG')
    buf.seek(0)
    files = {'image': ('image.png', buf, 'image/png')}
    data_to_load = {
        "title": title,
        "description": description,
        "date": date,
        "channelParsed": channelParsed,
        "channel_go_to": channel_go_to,
        "prediction_theme": prediction_theme
    }
    response = requests.post(create_parse_item, files=files, data=data_to_load)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None


def getAllChannels():
    response = requests.get(get_all_channels)
    if response.status_code == 200:
        data = response.json()["channels"]
        return data
    else:
        print('Error:', response.status_code)


def get_all_posts() -> list:
    response = requests.get(get_all_posts_url)
    if response.status_code == 200:
        data = response.json()["parsed_items"]
        return data
    else:
        print('Error:', response.status_code)
