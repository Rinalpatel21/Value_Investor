import streamlit as st
import dashboard
import chatbot

st.set_page_config(
    page_title="BTC AI Trading Agent",
    page_icon="🤖",
    layout="wide"
)

st.sidebar.title("BTC Trading Agent")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "AI Chat"]
)

if page == "Dashboard":
    dashboard.render()
else:
    chatbot.render()