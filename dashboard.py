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