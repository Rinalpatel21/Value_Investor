# test_storage.py

from portfolio import Portfolio
from portfolio_storage import (
    save_portfolio,
    load_portfolio
)

portfolio = Portfolio(10000)

portfolio.cash = 8500

portfolio.btc_dca = 0.02

save_portfolio(portfolio)

loaded = load_portfolio(10000)

print(loaded.cash)
print(loaded.btc_dca)