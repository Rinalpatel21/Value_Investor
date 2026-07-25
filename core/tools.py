from .portfolio_storage import load_portfolio
from .market_data import download_btc_data
from .indicators import add_indicators
from .regime import detect_market_regime
from .strategy import select_strategy
from .order_executor import market_buy, market_sell
import pandas as pd
import json
from .portfolio_storage import save_portfolio
from .news import get_bitcoin_news
import os


def get_data_path(filename):
    base_dir = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_dir, "data", filename)


def show_portfolio():

    portfolio = load_portfolio(10000)

    df = download_btc_data()
    df = add_indicators(df)

    price = float(df.iloc[-1]["Close"])

    btc = portfolio.total_btc()

    return {

        "cash": portfolio.cash,

        "btc": btc,

        "average_cost": portfolio.dca_avg_cost,

        "current_price": price,

        "btc_value": btc * price,

        "portfolio_value":
            portfolio.cash + btc * price

    }

def show_orders():

    df = pd.read_csv(get_data_path("paper_orders.csv"))

    return df.tail(10).to_dict("records")





def show_trade_history():

    df = pd.read_csv(get_data_path("paper_orders.csv"))

    return df.iloc[-1].to_dict()





def show_market_context():

    portfolio = load_portfolio(10000)

    df = download_btc_data()
    df = add_indicators(df)

    row = df.iloc[-1]

    regime = detect_market_regime(row)

    strategy = select_strategy(regime)

    price = float(row["Close"])

    portfolio_value = (
        portfolio.cash +
        portfolio.total_btc() * price
    )

    return {

    "price": price,

    "RSI": float(row["RSI"]),

    "ATR": float(row["ATR"]),

    "EMA50": float(row["EMA50"]),

    "SMA50": float(row["SMA50"]),

    "regime": regime,

    "strategy": strategy,

    "cash": portfolio.cash,

    "btc": portfolio.total_btc(),

    "average_cost": portfolio.dca_avg_cost,

    "portfolio_value": portfolio_value,

    "current_time": str(row.name)}


def show_ai_report():

    with open(
        "core/data/news_sentiment.json"
    ) as f:

        return json.load(f)

def show_news():

    return get_bitcoin_news()



def buy_bitcoin(amount):

    portfolio = load_portfolio(10000)

    df = download_btc_data()
    df = add_indicators(df)

    price = float(df.iloc[-1]["Close"])
    now = df.iloc[-1].name

    result = market_buy(
        portfolio,
        price,
        amount,
        now,
        source="chatbot"
    )

    save_portfolio(portfolio)

    return result

def sell_bitcoin(amount=None, quantity=None):

    if quantity is not None:
        amount = quantity

    if amount is None:
        raise ValueError("Missing amount")

    portfolio = load_portfolio(10000)

    df = download_btc_data()
    df = add_indicators(df)

    price = float(df.iloc[-1]["Close"])
    now = df.iloc[-1].name

    result = market_sell(
        portfolio,
        price,
        amount,
        current_time=now,
        source="chatbot"
    )

    save_portfolio(portfolio)

    return result

def get_market_summary():

    df = download_btc_data()
    df = add_indicators(df)

    row = df.iloc[-1]

    return {
        "price": float(row["Close"]),
        "RSI": float(row["RSI"]),
        "ATR": float(row["ATR"]),
        "EMA50": float(row["EMA50"]),
        "SMA50": float(row["SMA50"]),
        "current_time": str(row.name)
    }



