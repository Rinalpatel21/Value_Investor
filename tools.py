from portfolio_storage import load_portfolio
import pandas as pd


def get_portfolio():

    portfolio = load_portfolio(10000)

    return {
        "cash": portfolio.cash,
        "btc": portfolio.total_btc(),
        "average_cost": portfolio.dca_avg_cost,
        "portfolio_value":
            portfolio.cash
    }

def get_recent_orders():

    df = pd.read_csv("paper_orders.csv")

    return df.tail(10).to_dict("records")

def get_market_state(row):

    return {

        "price": row["Close"],

        "RSI": row["RSI"],

        "ATR": row["ATR"],

        "EMA50": row["EMA50"],

        "SMA50": row["SMA50"]

    }