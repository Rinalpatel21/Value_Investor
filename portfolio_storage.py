import json
from portfolio import Portfolio


def save_portfolio(portfolio):

    data = {

        "cash": portfolio.cash,

        "btc_dca": portfolio.btc_dca,

        "btc_swing": portfolio.btc_swing,

        "dca_total_cost": portfolio.dca_total_cost,

        "dca_avg_cost": portfolio.dca_avg_cost,

        "last_dca_buy_price": portfolio.last_dca_buy_price,

        "active_trades": portfolio.active_trades

    }

    with open("portfolio.json", "w") as f:

        json.dump(data, f, indent=4)


def load_portfolio(initial_capital):

    try:

        with open("portfolio.json", "r") as f:

            data = json.load(f)

        portfolio = Portfolio(initial_capital)

        portfolio.cash = data["cash"]

        portfolio.btc_dca = data["btc_dca"]

        portfolio.btc_swing = data["btc_swing"]

        portfolio.dca_total_cost = data["dca_total_cost"]

        portfolio.dca_avg_cost = data["dca_avg_cost"]

        portfolio.last_dca_buy_price = data["last_dca_buy_price"]

        portfolio.active_trades = data["active_trades"]

        print("Portfolio Loaded")

        return portfolio

    except FileNotFoundError:

        print("New Portfolio Created")

        return Portfolio(initial_capital)