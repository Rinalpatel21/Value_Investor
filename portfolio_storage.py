import json
from portfolio import Portfolio
import pandas as pd


def save_portfolio(portfolio):

    data = {

        "cash": portfolio.cash,

        "btc_dca": portfolio.btc_dca,

        "btc_swing": portfolio.btc_swing,

        "dca_total_cost": portfolio.dca_total_cost,

        "dca_avg_cost": portfolio.dca_avg_cost,

        "last_dca_buy_price": portfolio.last_dca_buy_price,

        "active_trades": portfolio.active_trades,

        "last_dca_buy_time": str(portfolio.last_dca_buy_time)

    }

    with open("portfolio.json", "w") as f:

        json.dump(data, f, indent=4)


def load_portfolio(initial_capital):

    try:

        with open("portfolio.json", "r") as f:

            data = json.load(f)

        portfolio = Portfolio(initial_capital)

        portfolio.cash = data.get("cash",0)

        portfolio.btc_dca = data.get("btc_dca",0)

        portfolio.btc_swing = data.get("btc_swing",0)

        portfolio.dca_total_cost = data.get("dca_total_cost",0)

        portfolio.dca_avg_cost = data.get("dca_avg_cost",0)

        portfolio.last_dca_buy_price = data.get( "last_dca_buy_price", None)

        portfolio.active_trades = data.get("active_trades",[])

        last_buy_time = data.get("last_dca_buy_time")

        if last_buy_time is not None:

            portfolio.last_dca_buy_time = pd.Timestamp(last_buy_time)

        else:

            portfolio.last_dca_buy_time = None

        print("Portfolio Loaded")

        print("Cash:", portfolio.cash)

        print("BTC:", portfolio.btc_dca)

        print("Avg Cost:", portfolio.dca_avg_cost)

        print("Last Buy Price:", portfolio.last_dca_buy_price)

        print("Last Buy Time:", portfolio.last_dca_buy_time)

        return portfolio

    except FileNotFoundError:

        print("New Portfolio Created")

        return Portfolio(initial_capital)