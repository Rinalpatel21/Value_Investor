from market_data import download_btc_data

df = download_btc_data()

print(df.head())

print()

print(df.tail())

print()

print(df.info())

print(df.describe())

from market_data import download_btc_data
from indicators import add_indicators

df = download_btc_data()

df = add_indicators(df)

print(
    df[
        ["Close",
         "ATR",
         "RSI",
         "MACD",
         "EMA50",
         "SMA50",
         "VOL_RATIO"]
    ].tail().to_string()
)
print(df.info())
print(df.describe().to_string())

from portfolio import Portfolio

portfolio = Portfolio(10000)

print("Cash =", portfolio.cash)

print("BTC DCA =", portfolio.btc_dca)

print("BTC Swing =", portfolio.btc_swing)

print("Active Trades =", portfolio.active_trades)

print("Closed Trades =", portfolio.closed_trades)

from portfolio import Portfolio
from dca import execute_dca_buy

portfolio = Portfolio(10000)

execute_dca_buy(
    portfolio,
    current_price=80000,
    amount=500,
    current_time="2025-01-01"
)

print()

print("Cash =", portfolio.cash)

print("BTC DCA =", portfolio.btc_dca)

print("Average Cost =", portfolio.dca_avg_cost)

from portfolio import Portfolio
from dca import execute_dca_buy
from dca_atr import (
    atr_opportunity_buy,
    dca_protective_sell
)

portfolio = Portfolio(10000)

execute_dca_buy(
    portfolio,
    80000,
    500,
    "today"
)

atr = 500

current_price = 78500

atr_opportunity_buy(
    portfolio,
    current_price,
    "today",
    atr
)

print()

print("Cash =", portfolio.cash)

print("BTC =", portfolio.btc_dca)

from regime import detect_market_regime

row = {

    "RSI":28,

    "MACD":-100,

    "Close":60000,

    "EMA50":65000

}

regime = detect_market_regime(row)

print(regime)

from strategy import select_strategy

print(select_strategy("TRENDING"))

print(select_strategy("RANGING"))

print(select_strategy("PANIC"))

from portfolio import Portfolio
from swing import (
    swing_entry_signal,
    open_swing_trade
)

portfolio = Portfolio(10000)

row = {

    "RSI":70,

    "MACD":100,

    "VOL_RATIO":2,

    "Close":80000,

    "EMA50":79000,

    "SMA50":78000

}

print(
    swing_entry_signal(row)
)

open_swing_trade(
    portfolio,
    80000,
    500
)

print()

print(portfolio.active_trades)

from portfolio import Portfolio
from swing import open_swing_trade
from atr_sell import manage_active_trades

portfolio = Portfolio(10000)

open_swing_trade(
    portfolio,
    80000,
    500
)

manage_active_trades(
    portfolio,
    current_price=79000,
    current_time="today",
    atr=500
)

print()

print(portfolio.closed_trades)

from risk_manager import portfolio_stop

value = 7000

print(
    portfolio_stop(
        value,
        10000
    )
)

from performance import calculate_metrics

values = [

10000,
10200,
10100,
10300,
10500

]

trades = [

{"pnl":100},

{"pnl":50},

{"pnl":-25}

]

sharpe,max_dd,win_rate = calculate_metrics(
    values,
    trades
)

print()

print("Sharpe =",sharpe)

print("Max DD =",max_dd)

print("Win Rate =",win_rate)


