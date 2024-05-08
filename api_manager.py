import requests
import io
from PIL import Image

to_generate_image = "http://138.201.33.30:5555/generate_image"
to_generate_text = "http://138.201.33.30:5555/generate_text"
get_all_themes = "http://138.201.33.30:999/themes"
get_all_channels = "http://138.201.33.30:999/channels"
get_parsed_item = "http://138.201.33.30:999/get_ParsedItems"
create_parse_item = "http://138.201.33.30:999/create_parse_item/"
get_all_posts_url = "http://138.201.33.30:999/get_all_posts/"

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
    try:
        image_bytes = query({
            "inputs": prompt,
        })
        image = Image.open(io.BytesIO(image_bytes))
        return image
    except:
        data = {"prompt": prompt}
        response = requests.post(to_generate_image, json=data)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print('Error:', response.status_code)


def generateText(prompt)-> str:
    data_to_load = {"prompt": prompt}
    response = requests.post(to_generate_text, json=data_to_load)
    if response.status_code == 200:
        data: list = response.json()
        parse_data: str = (data[0]["generated_text"].replace("Тема этого текста в 5 словах:", "")
                          .replace("Вот тема в 5 словах:", "").replace("Тема:", "")
                          .replace("The theme of this text in 5 words is:", "")
                          .replace("Here is a theme for this text in 5 words:", "").replace("Theme:", "")
                          .replace("Here is the rephrased text:", "").replace("Here is the rewritten text:", "")
                          .replace("Here is the text rewritten in other words, without links and hyperlinks, and without references to social networks: ","")
                          .replace("Вот перефразированный текст:", "").replace("Вот переписанный текст:", "")
                          .replace("Вот текст, переписанный другими словами, без ссылок и гиперссылок, а также без отсылок к соцсетям:", ""))


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


def parsed_item(title, description, date, image, channelParsed, channel_go_to, prediction_theme):
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


