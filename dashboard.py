from portfolio_storage import load_portfolio
import streamlit as st
import pandas as pd

df = pd.read_csv("trade_log.csv")

st.title("BTC Trading Agent Dashboard")

st.metric(
    "Total Trades",
    len(df)
)

if "PnL" in df.columns:

    st.metric(
        "Total PnL",
        round(df["PnL"].sum(), 2)
    )

st.dataframe(df)

if "PnL" in df.columns:

    st.line_chart(
        df["PnL"].cumsum()
    )


portfolio = load_portfolio(10000)

st.title("BTC Trading Agent")

st.metric(
    "Cash",
    f"${portfolio.cash:.2f}"
)

st.metric(
    "BTC",
    portfolio.total_btc()
)

st.metric(
    "Portfolio Value",
    portfolio.cash + portfolio.total_btc()*60000
)

import pandas as pd

df = pd.read_csv("trade_log.csv")

st.dataframe(df)

st.title("BTC Trading Dashboard")

history = pd.read_csv(
    "portfolio_history.csv"
)

st.subheader("Portfolio Value")

st.line_chart(

    history["Portfolio Value"]

)

st.subheader("BTC Price")

st.line_chart(

    history["BTC Price"]

)

st.subheader("Portfolio History")

st.dataframe(history)

st.subheader("BTC Holdings")

st.line_chart(

    history["BTC Holdings"]

)

st.subheader("Trade History")

trades = pd.read_csv(
    "trade_log.csv"
)

st.dataframe(trades)

import pandas as pd
import streamlit as st

orders = pd.read_csv("paper_orders.csv")

st.subheader("Paper Orders")

st.dataframe(orders)