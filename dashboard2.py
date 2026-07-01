import streamlit as st
import pandas as pd
import numpy as np

from portfolio_storage import load_portfolio

st.set_page_config(
    page_title="BTC Agent Performance Dashboard",
    layout="wide"
)

st.title("📈 BTC Trading Agent Performance Dashboard")

# ---------------------------------------------------
# Load Data
# ---------------------------------------------------

portfolio = load_portfolio(10000)

history = pd.read_csv("portfolio_history.csv")

trade_log = pd.read_csv("trade_log.csv")

paper_orders = pd.read_csv("paper_orders.csv")

# ---------------------------------------------------
# Current Portfolio
# ---------------------------------------------------

current_price = history["Price"].iloc[-1]

portfolio_value = (
    portfolio.cash +
    portfolio.total_btc() * current_price
)

initial_capital = 10000

total_return = (
    (portfolio_value - initial_capital)
    / initial_capital
) * 100

# ---------------------------------------------------
# Performance Metrics
# ---------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Portfolio Value",
    f"${portfolio_value:,.2f}"
)

col2.metric(
    "Cash",
    f"${portfolio.cash:,.2f}"
)

col3.metric(
    "BTC Holdings",
    f"{portfolio.total_btc():.6f}"
)

col4.metric(
    "Total Return",
    f"{total_return:.2f}%"
)

st.divider()

# ---------------------------------------------------
# Trade Statistics
# ---------------------------------------------------

st.header("Trade Statistics")

if "PnL" in trade_log.columns:

    pnl = trade_log["PnL"]

    total_trades = len(pnl)

    wins = pnl[pnl > 0]

    losses = pnl[pnl < 0]

    win_rate = (
        len(wins) /
        total_trades * 100
        if total_trades > 0 else 0
    )

    avg_win = wins.mean() if len(wins) else 0

    avg_loss = losses.mean() if len(losses) else 0

    profit_factor = (
        wins.sum() /
        abs(losses.sum())
        if len(losses) else np.nan
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Trades",
        total_trades
    )

    c2.metric(
        "Win Rate",
        f"{win_rate:.2f}%"
    )

    c3.metric(
        "Average Win",
        f"${avg_win:.2f}"
    )

    c4.metric(
        "Average Loss",
        f"${avg_loss:.2f}"
    )

    st.metric(
        "Profit Factor",
        round(profit_factor,2)
        if not np.isnan(profit_factor)
        else "N/A"
    )

# ---------------------------------------------------
# Portfolio Growth
# ---------------------------------------------------

st.divider()

st.header("Portfolio Value")

st.line_chart(
    history["Portfolio Value"]
)

# ---------------------------------------------------
# BTC Price
# ---------------------------------------------------

st.header("BTC Price")

st.line_chart(
    history["BTC Price"]
)

# ---------------------------------------------------
# BTC Holdings
# ---------------------------------------------------

st.header("BTC Holdings")

st.line_chart(
    history["BTC Holdings"]
)

# ---------------------------------------------------
# Cumulative PnL
# ---------------------------------------------------

if "PnL" in trade_log.columns:

    st.header("Cumulative PnL")

    trade_log["Cumulative PnL"] = (
        trade_log["PnL"].cumsum()
    )

    st.line_chart(
        trade_log["Cumulative PnL"]
    )

# ---------------------------------------------------
# Drawdown
# ---------------------------------------------------

st.header("Drawdown")

history["Peak"] = history["Portfolio Value"].cummax()

history["Drawdown"] = (
    history["Portfolio Value"]
    -
    history["Peak"]
) / history["Peak"]

st.line_chart(
    history["Drawdown"]
)

max_drawdown = history["Drawdown"].min() * 100

st.metric(
    "Maximum Drawdown",
    f"{max_drawdown:.2f}%"
)

# ---------------------------------------------------
# Sharpe Ratio
# ---------------------------------------------------

st.header("Sharpe Ratio")

returns = history["Portfolio Value"].pct_change().dropna()

if len(returns) > 1:

    sharpe = (
        returns.mean() /
        returns.std()
    ) * np.sqrt(252)

    st.metric(
        "Sharpe Ratio",
        round(sharpe,2)
    )

# ---------------------------------------------------
# Best / Worst Trade
# ---------------------------------------------------

if "PnL" in trade_log.columns:

    st.header("Best and Worst Trades")

    col1, col2 = st.columns(2)

    col1.metric(
        "Best Trade",
        f"${trade_log['PnL'].max():.2f}"
    )

    col2.metric(
        "Worst Trade",
        f"${trade_log['PnL'].min():.2f}"
    )

# ---------------------------------------------------
# Paper Orders
# ---------------------------------------------------

st.divider()

st.header("Paper Orders")

st.dataframe(
    paper_orders,
    use_container_width=True
)

# ---------------------------------------------------
# Trade Log
# ---------------------------------------------------

st.header("Trade Log")

st.dataframe(
    trade_log,
    use_container_width=True
)

# ---------------------------------------------------
# Portfolio History
# ---------------------------------------------------

st.header("Portfolio History")

st.dataframe(
    history,
    use_container_width=True
)