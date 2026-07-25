import streamlit as st
from core.agent import run_agent


def render():

    st.title("🤖 AI Bitcoin Trading Assistant")

    st.caption(
        "Your intelligent cryptocurrency copilot. Analyze your portfolio, explain AI recommendations, inspect market conditions, execute paper trades, and answer questions about your Bitcoin trading system."
    )

    # --------------------------------------------------
    # Sidebar
    # --------------------------------------------------

    with st.sidebar:

        st.header("🚀 Capabilities")

        st.markdown("""
### 💼 Portfolio Analysis

- Show my portfolio
- Portfolio value
- Cash balance
- BTC holdings
- Average cost
- Portfolio health

---

### 📈 Market Intelligence

- Current BTC price
- RSI
- ATR
- EMA50 / SMA50
- Current market regime
- Active strategy
- Explain today's market

---

### 🤖 AI Portfolio Advisor

- Should I buy Bitcoin?
- Should I sell?
- Explain today's recommendation
- Analyze my portfolio
- Show AI report
- What's today's risk?

---

### 📰 News Intelligence

- Show Bitcoin news
- Latest market news
- News sentiment
- Important events
- Market opportunities
- Current risks

---

### 📑 Trading Activity

- Recent trades
- Last trade
- Paper orders
- Trade history

---

### 📊 Performance

- Portfolio performance
- Profit & Loss
- Total return
- Portfolio allocation

---

### 💸 Paper Trading

- Buy $100 BTC
- Buy $500 Bitcoin
- Sell 0.01 BTC
- Sell 0.005 BTC
""")

        st.success(
            "The assistant only answers questions related to your Bitcoin trading system."
        )

    # --------------------------------------------------
    # Conversation History
    # --------------------------------------------------

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # --------------------------------------------------
    # Suggested Prompts
    # --------------------------------------------------

    with st.expander("💡 Try asking..."):

        st.markdown("""
### Portfolio

- Show my portfolio
- What is my portfolio value?
- How much BTC do I own?
- How much cash do I have?
- What's my average buy price?

---

### AI Analysis

- Analyze my portfolio
- Should I buy Bitcoin?
- Should I sell Bitcoin?
- Explain today's recommendation
- Show AI report
- What is today's risk level?

---

### Market

- Explain today's market
- Show market summary
- What's today's trading strategy?
- What's the market regime?
- Show technical indicators

---

### News

- Show today's Bitcoin news
- Summarize market news
- What's the news sentiment?
- What are today's risks?
- What opportunities exist?

---

### Trading

- Buy $100 Bitcoin
- Buy $500 BTC
- Sell 0.01 BTC
- Show my recent trades
- Show paper orders

---

### Performance

- How am I performing?
- Show portfolio performance
- What's my profit?
- What's my total return?
""")

    # --------------------------------------------------
    # Chat Input
    # --------------------------------------------------

    prompt = st.chat_input(
        "Ask anything about your Bitcoin portfolio, market, AI recommendations, news, or paper trading..."
    )

    if prompt:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):

            with st.spinner("Analyzing..."):

                response = run_agent(prompt)

                st.markdown(response)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )