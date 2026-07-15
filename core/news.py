import os
import requests
from dotenv import load_dotenv
from pprint import pprint

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(ROOT_DIR + "/.env")


NEWS_API_KEY = os.environ.get("NEWS_API_KEY")

URL = "https://newsapi.org/v2/everything?q=bitcoin&apiKey=" + NEWS_API_KEY


def get_bitcoin_news(limit=10):

    params = {
        "q": "Bitcoin OR BTC",
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": limit,
        "apiKey": NEWS_API_KEY
    }

    response = requests.get(URL, params=params)

    response.raise_for_status()

    data = response.json()

    articles = []

    for article in data.get("articles", []):

        articles.append({

            "title": article.get("title"),

            "description": article.get("description"),

            "source": article["source"]["name"],

            "published": article.get("publishedAt")

        })

    return articles


if __name__ == "__main__":
    # pass
    news = get_bitcoin_news()

    for article in news:
        print(article)
        