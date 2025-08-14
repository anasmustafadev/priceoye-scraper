import requests
from bs4 import BeautifulSoup
import http.client, urllib
import os
from dotenv import load_dotenv

load_dotenv()

USER_KEY = os.getenv("USER_KEY")
APP_TOKEN = os.getenv("APP_TOKEN")


def main():
    response = fetch()
    result = parse(response)
    sendNotification(result)


def fetch():
    url = "https://priceoye.pk/search"

    params = {
        "q": "nothing buds 2 pro",
    }

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "priority": "u=0, i",
        "referer": "https://priceoye.pk/",
        "sec-ch-ua": '"Not;A=Brand";v="99", "Brave";v="139", "Chromium";v="139"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "sec-gpc": "1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    }

    response = requests.get(url, params=params, headers=headers)

    return response


def parse(response):
    soup = BeautifulSoup(response.text, "html.parser")
    product = soup.select_one('[data-slug="nothing-buds-2-pro"]')
    is_oos = product.select_one('[alt="out of stock"]')
    display_text = "are out of stock" if is_oos else "are in stock"
    emoji = "🥲" if is_oos else "🎉"
    result = f"{emoji} Nothing Buds 2 Pro {display_text}"
    return result


def sendNotification(message):
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request(
        "POST",
        "/1/messages.json",
        urllib.parse.urlencode(
            {
                "token": APP_TOKEN,
                "user": USER_KEY,
                "title": "Scraped PriceOye!",
                "message": message,
            }
        ),
        {"Content-type": "application/x-www-form-urlencoded"},
    )
    conn.getresponse()


if __name__ == "__main__":
    main()
