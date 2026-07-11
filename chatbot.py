import streamlit as st
from core.agent import run_agent


def render():

    st.title("🤖 BTC AI Trading Assistant")

    st.caption(
        "Ask questions about your portfolio, Bitcoin market, trading history, AI decisions, and trading performance."
    )

    # -----------------------------
    # Sidebar Help
    # -----------------------------
    with st.sidebar:

        st.header("📖 What can I help with?")

        st.markdown("""
### 💼 Portfolio
- Show my portfolio
- What is my portfolio value?
- How much cash do I have?
- How much BTC do I own?
- What is my average buy price?

---

### 📈 Market Analysis
- What is the BTC price?
- What's the current market regime?
- What strategy is active?
- Explain today's market conditions.

---

### 📊 Trading Performance
- How much money have I made?
- Show my trading performance.
- What is my total return?
- Am I profitable?

---

### 📑 Trade History
- Show recent trades.
- What was my last trade?
- Show paper orders.
- When did I last buy Bitcoin?

---

### 🤖 AI Decisions
- Should I buy Bitcoin?
- Should I sell Bitcoin?
- Why did the AI recommend buying?
- Explain today's recommendation.
- Analyze my trading account.

---

### 🛡 Supported Topics
This assistant only answers questions related to:

- Bitcoin
- Portfolio
- Trading
- Orders
- Performance
- Technical indicators
- AI trading decisions
""")

        st.info(
            "Questions unrelated to cryptocurrency trading will be politely declined."
        )

    # -----------------------------
    # Chat History
    # -----------------------------

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # -----------------------------
    # Suggested Questions
    # -----------------------------

    with st.expander("💡 Example Questions"):

        st.markdown("""
**Portfolio**
- Show my portfolio
- What is my portfolio value?
- How much BTC do I own?

**Market**
- What's the BTC price?
- What market regime are we in?
- Which strategy is active?

**Trades**
- Show recent trades
- What was my last trade?
- Show paper orders

**Performance**
- How much money have I made?
- What's my profit?
- Show my trading performance

**AI**
- Analyze my portfolio
- Should I buy Bitcoin?
- Should I sell Bitcoin?
- Why did the AI recommend this trade?
""")

    # -----------------------------
    # Chat Input
    # -----------------------------

    question = st.chat_input(
        "Ask about your portfolio, BTC, trades, or AI decisions..."
    )

    if question:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):
            st.write(question)

        answer = run_agent(question)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        with st.chat_message("assistant"):
            st.write(answer)