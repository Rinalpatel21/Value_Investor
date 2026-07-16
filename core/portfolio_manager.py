import json

from .llm_agent import client
from .llm_agent import MODEL

SYSTEM_PROMPT = """
You are a professional Bitcoin Portfolio Manager.

Your responsibility is NOT simply to tell users to Buy or Sell.

You evaluate:

• Technical indicators

• Portfolio allocation

• News sentiment

• Fear & Greed

• Market risks

• Current holdings

Provide ONLY JSON.

{
    "recommendation":"",
    "confidence":0.0,
    "market_summary":"",
    "portfolio_health":"",
    "risk_level":"",
    "reasoning":"",
    "action":"BUY/HOLD/SELL"
}
"""


def evaluate_portfolio(context):

    response = client.chat.completions.create(

        model=MODEL,

        messages=[

            {

                "role":"system",

                "content":SYSTEM_PROMPT

            },

            {

                "role":"user",

                "content":json.dumps(context)

            }

        ]

    )

    result = response.choices[0].message.content

    if result.startswith("```"):

        result = result.replace("```json","")
        result = result.replace("```","").strip()

    return json.loads(result)


if __name__ == "__main__":

    from .market_context import build_market_context
    from .portfolio_storage import load_portfolio
    from .market_data import download_btc_data
    from .indicators import add_indicators

    df = download_btc_data()
    df = add_indicators(df)

    portfolio = load_portfolio(10000)

    latest_row = df.iloc[-1]

    context = build_market_context(portfolio, latest_row)

    evaluation = evaluate_portfolio(context)

    print(json.dumps(evaluation, indent=4))