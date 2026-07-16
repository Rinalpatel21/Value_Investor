from .portfolio_storage import load_portfolio

from .news import get_bitcoin_news
from .news_sentiment import analyze_news
from .fear_greed import get_fear_greed


def build_market_context(portfolio, row):

    news = get_bitcoin_news()

    sentiment = analyze_news(news)

    fear_greed = get_fear_greed()

    return {

        "market":{

            "price":float(row["Close"]),
            "RSI":float(row["RSI"]),
            "ATR":float(row["ATR"]),
            "EMA50":float(row["EMA50"]),
            "SMA50":float(row["SMA50"])

        },

        "portfolio":{

            "cash":portfolio.cash,
            "btc":portfolio.total_btc(),
            "average_cost":portfolio.dca_avg_cost

        },

        "news":news,

        "news_sentiment":sentiment,

        "fear_greed":fear_greed

    }


if __name__ == "__main__":

    
    from  .indicators import add_indicators
    from .market_data import download_btc_data


    df = download_btc_data()
    df = add_indicators(df)
    row = df.iloc[-1]

    portfolio = load_portfolio(10000)

    context = build_market_context(portfolio, row)

    print(context)