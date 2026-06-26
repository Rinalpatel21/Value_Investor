
from portfolio_storage import (
    load_portfolio,
    save_portfolio
)



def run_live_agent():

    portfolio = load_portfolio(10000)

    # market data

    # indicators

    # DCA

    # swing trades

    save_portfolio(portfolio)

    print("Portfolio Saved")