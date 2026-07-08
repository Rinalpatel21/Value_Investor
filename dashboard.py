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

current_price = history["BTC Price"].iloc[-1]

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

st.subheader("Portfolio Growth")

history = history.rename(
    columns={
        "Portfolio Value":"Portfolio"
    }
)

st.line_chart(
    history.set_index("Time")["Portfolio"]
)

# ---------------------------------------------------
# BTC Price
# ---------------------------------------------------

st.subheader("BTC Price")

st.line_chart(
    history.set_index("Time")["BTC Price"]
)

# ---------------------------------------------------
# Recent Trades
# ---------------------------------------------------

st.header("Recent Trades")

st.dataframe(
    trade_log.tail(10),
    use_container_width=True
)

# Portfolio Holdings

import plotly.express as px
btc_value = portfolio.total_btc()*current_price

chart = px.pie(
    names=["Cash","BTC"],
    values=[portfolio.cash, btc_value]
)

st.plotly_chart(chart, use_container_width=True)

# Trading Activity
st.subheader("Buy vs Sell")

counts = paper_orders["Side"].value_counts()

st.bar_chart(counts)

# Portfolio Snapshot

snapshot = pd.DataFrame({

    "Metric":[
        "Cash",
        "BTC",
        "Average Cost",
        "Current Price"
    ],

    "Value":[

        portfolio.cash,

        portfolio.total_btc(),

        portfolio.dca_avg_cost,

        current_price
    ]

})

st.table(snapshot)