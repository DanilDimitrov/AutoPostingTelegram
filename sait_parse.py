import requests
from bs4 import BeautifulSoup

cryptoNews = "https://cryptonews.net"
ihodi = "https://ihodl.com"
cointelegraph = "https://cointelegraph.com"
coindesk = "https://www.coindesk.com"
bitcoinist = "https://bitcoinist.com"
decrypt = "https://decrypt.co"

def get_html_content(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        html_content = response.content
        return html_content
    else:
        print(f"Status code: {response.status_code}")



def parse_last_crypto_news():
    html_content = get_html_content(f"{cryptoNews}/news/analytics/")
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        divs = soup.find_all('div', class_='row news-item start-xs')
        if divs:
            first_post = divs[0]
            data_id = first_post.get('data-id')
            if data_id:
                url_for_last_post = f"{cryptoNews}{data_id}"
                return url_for_last_post
            else:
                print("No data-id.")
        else:
            print("No div elements")
    else:
        print("Failed.")
def parse_crypto_news():
    html_content = get_html_content(parse_last_crypto_news())
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        paragraphs = soup.find_all('p')
        if paragraphs:
            text_paragraphs = [p for p in paragraphs if p.text.strip()]
            post = ""
            for p in text_paragraphs:
                post += p.text.strip()
            return post
        else:
            print("No <p>.")
    else:
        print("Failed.")


def parse_last_ihodi():
    html_content = get_html_content(f"{ihodi}")
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        articles = soup.find_all('a', class_='articles-item__photo-link')
        if articles:
            first_post = articles[0]
            href = first_post.get('href')
            to_article = f"{ihodi}{href}"
            return to_article
def parse_ihodi_article():
    html_content = get_html_content(parse_last_ihodi())
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        divs = soup.find_all('div', class_='content-block text-block')
        if divs:
            article = divs[0]
            paragraphs = article.find_all('p')
            text_paragraphs = [p for p in paragraphs if p.text.strip()]
            post = ""
            for p in text_paragraphs:
                post += p.text.strip()
            print(post)
            return post
        else:
            print("No <p>")
    else:
        print("Failed.")


def parse_coinTelegraph():
    html_content = get_html_content(cointelegraph)
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        articles = soup.find_all('article', class_='post-card__article rounded-lg')
        if articles:
            first_post = articles[0]
            href = first_post.find_all('a', class_='post-card__figure-link')
            href = href[0]
            href = href.get('href')
            to_article = f"{cointelegraph}{href}"
            return to_article
        else:
            print("No <p>")
    else:
        print("Failed.")
def parse_coinTelegraph_article():
    html_content = get_html_content(parse_coinTelegraph())
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        divs = soup.find_all('div', class_='post-content relative')
        if divs:
            article = divs[0]
            paragraphs = article.find_all('p')
            text_paragraphs = [p for p in paragraphs if p.text.strip()]
            post = ""
            for p in text_paragraphs:
                post += p.text.strip()
            return post
        else:
            print("No <p>")
    else:
        print("Failed.")


def parse_last_coindesk():
    html_content = get_html_content(coindesk)
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        articles = soup.find_all('a', class_='card-imagestyles__CardImageWrapper-sc-1kbd3qh-0 WDSwd')
        if articles:
            href = articles[0]
            href = href.get('href')
            to_article = f"{coindesk}{href}"
            return to_article
        else:
            print("No <p>")
    else:
        print("Failed.")
def parse_coindesk_article():
    html_content = get_html_content(parse_last_coindesk())
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        divs = soup.find_all('div', class_='contentstyle__StyledWrapper-sc-g5cdrh-0 gkcZwU composer-content')
        if divs:
            article = divs[0]
            paragraphs = article.find_all('p')
            text_paragraphs = [p for p in paragraphs if p.text.strip()]
            post = ""
            for p in text_paragraphs:
                post += p.text.strip()
            print(post)
            return post
        else:
            print("No <p>")
    else:
        print("Failed.")


def parse_last_bitcoinist():
    html_content = get_html_content(bitcoinist)
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        articles = soup.find_all('div', class_='jeg_thumb')
        if articles:
            article = articles[0]
            a = article.find_all('a')
            href = a[0].get('href')
            to_article = f"{href}"
            return to_article
        else:
            print("No <p>")
    else:
        print("Failed.")
def parse_bitcoinist_article():
    html_content = get_html_content(parse_last_bitcoinist())
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        divs = soup.find_all('div', class_='content-inner')
        if divs:
            article = divs[0]
            paragraphs = article.find_all('p')
            text_paragraphs = [p for p in paragraphs if p.text.strip()]
            post = ""
            for p in text_paragraphs:
                post += p.text.strip()
            print(post)
            return post
        else:
            print("No <p>")
    else:
        print("Failed.")


def parse_last_bitcoinist():
    html_content = get_html_content(bitcoinist)
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        articles = soup.find_all('div', class_='jeg_thumb')
        if articles:
            article = articles[0]
            a = article.find_all('a')
            href = a[0].get('href')
            to_article = f"{href}"
            return to_article
        else:
            print("No <p>")
    else:
        print("Failed.")
def parse_bitcoinist_article():
    html_content = get_html_content(parse_last_bitcoinist())
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        divs = soup.find_all('div', class_='content-inner')
        if divs:
            article = divs[0]
            paragraphs = article.find_all('p')
            text_paragraphs = [p for p in paragraphs if p.text.strip()]
            post = ""
            for p in text_paragraphs:
                post += p.text.strip()
            print(post)
            return post
        else:
            print("No <p>")
    else:
        print("Failed.")


def parse_last_decrypt():
    html_content = get_html_content(decrypt)
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        articles = soup.find_all('h3', class_='font-akzidenz-grotesk font-bold text-xl leading-6 text-black md:text-2xl md:leading-6 degen-alley-dark:text-white bitcoin:hover:bg-orange-400 bitcoin:inline gg-dark:text-white')
        if articles:
            article = articles[0]
            href = article.find_all('a', class_='linkbox__overlay')
            to_article = f"{decrypt}{href[0].get('href')}"
            return to_article
        else:
            print("No <p>")
    else:
        print("Failed.")
def parse_decrypt_article():
    html_content = get_html_content(parse_last_decrypt())
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        divs = soup.find_all('div', class_='z-2 flex-1 min-w-0')
        if divs:
            article = divs[0]
            paragraphs = article.find_all('p')
            text_paragraphs = [p for p in paragraphs if p.text.strip()]
            post = ""
            for p in text_paragraphs:
                post += p.text.strip()
            print(post)
            return post
        else:
            print("No <p>")
    else:
        print("Failed.")

parse_decrypt_article()

