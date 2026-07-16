import json

from .llm_agent import client
from .llm_agent import MODEL


SYSTEM_PROMPT = """
You are a professional crypto analyst.

Analyze these Bitcoin news headlines.

Return ONLY JSON.

{
    "sentiment":"Bullish/Bearish/Neutral",
    "score":0.0,
    "summary":"",
    "risks":[],
    "opportunities":[],
    "important_events":[]
}
"""


def analyze_news(news_articles):

    news_text = ""

    for article in news_articles:

        news_text += f"""
Title:
{article['title']}

Description:
{article['description']}

Source:
{article['source']}

"""

    response = client.chat.completions.create(

        model=MODEL,

        messages=[

            {

                "role":"system",

                "content":SYSTEM_PROMPT

            },

            {

                "role":"user",

                "content":news_text

            }

        ]

    )

    result = response.choices[0].message.content

    if result.startswith("```"):
        result = result.replace("```json","")
        result = result.replace("```","").strip()
    
    
    parsed = json.loads(result)

    with open("core/data/news_sentiment.json", "w") as f:
        json.dump(parsed, f, indent=4)

        return parsed

    return json.loads(result)
    

    

if __name__ == "__main__":
    # Ensure it resolves path issues when running this script directly
    
    from core.news import get_bitcoin_news

    from core.news_sentiment import analyze_news

    news = get_bitcoin_news()

    result = analyze_news(news)

    print(result)