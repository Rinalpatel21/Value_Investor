from .portfolio_storage import load_portfolio
from .market_data import download_btc_data
from .indicators import add_indicators
from .regime import detect_market_regime
from .strategy import select_strategy
import pandas as pd





import os


def get_data_path(filename):
    base_dir = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_dir, "data", filename)


def get_portfolio():

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

def get_recent_orders():

    df = pd.read_csv(get_data_path("paper_orders.csv"))

    return df.tail(10).to_dict("records")

def get_market_state(row):

    return {

        "price": row["Close"],

        "RSI": row["RSI"],

        "ATR": row["ATR"],

        "EMA50": row["EMA50"],

        "SMA50": row["SMA50"]

    }





def get_performance():

    portfolio = load_portfolio(10000)

    df = download_btc_data()
    df = add_indicators(df)

    price = float(df.iloc[-1]["Close"])

    btc = portfolio.total_btc()

    value = portfolio.cash + btc * price

    pnl = value - 10000

    return {

        "portfolio_value": value,

        "profit_loss": pnl,

        "return_percent": pnl / 10000 * 100

    }

def get_market_summary():

    df = download_btc_data()

    df = add_indicators(df)

    row = df.iloc[-1]

    regime = detect_market_regime(row)

    strategy = select_strategy(regime)

    return {

        "price": float(row["Close"]),

        "RSI": float(row["RSI"]),

        "EMA50": float(row["EMA50"]),

        "SMA50": float(row["SMA50"]),

        "ATR": float(row["ATR"]),

        "regime": regime,

        "strategy": strategy

    }

def get_last_trade():

    df = pd.read_csv(get_data_path("paper_orders.csv"))

    return df.iloc[-1].to_dict()


def get_profit_loss():

    portfolio = load_portfolio(10000)

    df = download_btc_data()

    df = add_indicators(df)

    price = float(df.iloc[-1]["Close"])

    value = portfolio.cash + portfolio.total_btc() * price

    pnl = value - 10000

    return {

        "portfolio_value": value,

        "profit_loss": pnl

    }




def get_trading_context():

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

    "current_time": str(row.name)
}







