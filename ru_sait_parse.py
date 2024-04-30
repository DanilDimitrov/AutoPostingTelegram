import requests
from bs4 import BeautifulSoup


forklog = "https://forklog.com"
coindeskru = "https://www.coindesk.com/ru"
coinspot = "https://coinspot.io/"
ttrcoin = "https://ttrcoin.com/"
altcoinlog = "https://altcoinlog.com/"


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


def parse_forklog_article():
    html_content = get_html_content(f"{forklog}")
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        divs = soup.find_all('div', class_='cell has_recent')
        if divs:
            first_post = divs[0]
            href = first_post.find_all('a')[0].get('href')
            if href:
                print(href)
                return href
            else:
                print("No data-id.")
        else:
            print("No div elements")
    else:
        print("Failed.")
def parse_forklog():
    html_content = get_html_content(parse_forklog_article())
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        article = soup.find_all('div', class_='post_content')
        paragraphs = article[0].find_all('p')
        if paragraphs:
            text_paragraphs = [p for p in paragraphs if p.text.strip()]
            post = ""
            for p in text_paragraphs:
                post += p.text.strip()
            return post.replace("Подписывайтесь на ForkLog в социальных сетяхРассылки ForkLog: держите руку на пульсе биткоин-индустрии!", "")
        else:
            print("No <p>.")
    else:
        print("Failed.")


def parse_last_coindesk_articles():
    html_content = get_html_content(coindeskru)
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        article = soup.find_all('div', class_='featured-cardstyles__FeaturedCardWrapper-sc-caozbq-2 cRlwbG')
        href = article[0].find_all('a', class_='card-imagestyles__CardImageWrapper-sc-1kbd3qh-0 WDSwd')[0]
        if href:
            href = f"{coindeskru.replace('/ru', '')}{href.get('href')}"
            print(href)
            return href
        else:
            print("No <p>.")
    else:
        print("Failed.")
def parse_coindesk_articleru():
    html_content = get_html_content(parse_last_coindesk_articles())
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        article = soup.find_all('div', class_='contentstyle__StyledWrapper-sc-g5cdrh-0 gkcZwU composer-content')
        paragraphs = article[0].find_all('p')
        if paragraphs:
            text_paragraphs = [p for p in paragraphs if p.text.strip()]
            post = ""
            for p in text_paragraphs:
                post += p.text.strip()
            print(post)
            return post
        else:
            print("No <p>.")
    else:
        print("Failed.")


def parse_last_coinspot_articles():
    html_content = get_html_content(coinspot)
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        article = soup.find_all('div', class_='content-box preview-box')
        href = article[0].find_all('a', class_='text-c-base')[0]
        if href:
            href = f"{href.get('href')}"
            print(href)
            return href
        else:
            print("No <p>.")
    else:
        print("Failed.")
def parse_coinspot_article():
    html_content = get_html_content(parse_last_coinspot_articles())
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        article = soup.find_all('div', class_='content-box typography article-content')
        paragraphs = article[0].find_all('p')
        if paragraphs:
            text_paragraphs = [p for p in paragraphs if p.text.strip()]
            post = ""
            for p in text_paragraphs:
                post += p.text.strip()
            print(post)
            return post
        else:
            print("No <p>.")
    else:
        print("Failed.")


def parse_last_ttrcoin_articles():
    html_content = get_html_content(ttrcoin)
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        article = soup.find_all('div', class_='posts-list--item')
        href = article[0].find_all('a', class_='posts-list__img')[0]
        if href:
            href = f"{href.get('href')}"
            print(href)
            return href
        else:
            print("No <p>.")
    else:
        print("Failed.")
def parse_ttrcoin_article():
    html_content = get_html_content(parse_last_ttrcoin_articles())
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        article = soup.find_all('article', class_='post-entry')
        paragraphs = article[0].find_all('p')
        if paragraphs:
            text_paragraphs = [p for p in paragraphs if p.text.strip()]
            post = ""
            for p in text_paragraphs:
                post += p.text.strip()
            print(post)
            return post
        else:
            print("No <p>.")
    else:
        print("Failed.")


def parse_last_altcoinlog_articles():
    html_content = get_html_content(altcoinlog)
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        article = soup.find_all('div', class_='item-inner clearfix')
        href = article[0].find_all('a', class_='post-url post-title')[0]
        if href:
            href = f"{href.get('href')}"
            print(href)
            return href
        else:
            print("No <p>.")
    else:
        print("Failed.")
def parse_altcoinlog_article():
    html_content = get_html_content(parse_last_altcoinlog_articles())
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        article = soup.find_all('div', class_='entry-content clearfix single-post-content')
        paragraphs = article[0].find_all('p')
        if paragraphs:
            text_paragraphs = [p for p in paragraphs if p.text.strip()]
            post = ""
            for p in text_paragraphs:
                post += p.text.strip()
            print(post)
            return post
        else:
            print("No <p>.")
    else:
        print("Failed.")

