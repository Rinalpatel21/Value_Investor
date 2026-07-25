import streamlit as st
import pandas as pd
import plotly.express as px

from core.portfolio_storage import load_portfolio
from core.market_data import download_btc_data
from core.indicators import add_indicators
from core.regime import detect_market_regime
from core.strategy import select_strategy
from core.ai_advisor import evaluate_portfolio
from core.news import load_news
from core.fear_greed import get_fear_greed


STARTING_BALANCE = 10000

# ---------------------------------------------------------------------------
# Styling
# ---------------------------------------------------------------------------
# A dark, trading-terminal look: monospace figures, a single amber accent for
# Bitcoin, and green/red only where they mean something (gains vs. losses).

CUSTOM_CSS = """
<style>
    [data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', 'Courier New', monospace;
        font-weight: 600;
    }

    [data-testid="stMetric"] {
        background-color: rgba(140, 140, 140, 0.08);
        border: 1px solid rgba(140, 140, 140, 0.25);
        border-radius: 10px;
        padding: 14px 16px 10px 16px;
    }

    h1, h2, h3 {
        letter-spacing: -0.02em;
    }

    .accent-divider {
        height: 2px;
        background: linear-gradient(90deg, #F2A93B, transparent);
        border: none;
        margin: 0.6rem 0 1.6rem 0;
    }

    .section-label {
        color: #8B949E;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: -0.4rem;
    }
</style>
"""


def section_divider():
    st.markdown('<hr class="accent-divider">', unsafe_allow_html=True)


def section_label(text):
    st.markdown(f'<div class="section-label">{text}</div>', unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_dashboard_data():
    """Loads portfolio state, history, orders, and the latest market data.

    Centralizing this here keeps render() focused on layout instead of
    plumbing, and gives us one place to handle missing/corrupt files.
    """
    portfolio = load_portfolio(STARTING_BALANCE)

    try:
        history = pd.read_csv("core/data/portfolio_history.csv")
        history["Time"] = pd.to_datetime(history["Time"])
    except FileNotFoundError:
        history = pd.DataFrame(columns=["Time", "Portfolio Value", "BTC Price"])

    try:
        orders = pd.read_csv("core/data/paper_orders.csv")
    except FileNotFoundError:
        orders = pd.DataFrame(columns=["Side", "Price", "Source"])

    df = add_indicators(download_btc_data())
    latest = df.iloc[-1]

    return portfolio, history, orders, latest


# ---------------------------------------------------------------------------
# Sections
# ---------------------------------------------------------------------------

def render_top_metrics(portfolio, latest, current_price):
    btc_value = portfolio.total_btc() * current_price
    portfolio_value = portfolio.cash + btc_value
    total_return = (portfolio_value - STARTING_BALANCE) / STARTING_BALANCE * 100

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Portfolio Value", f"${portfolio_value:,.2f}")
    c2.metric("Cash", f"${portfolio.cash:,.2f}")
    c3.metric("BTC Holdings", f"{portfolio.total_btc():.6f}")
    c4.metric("Return", f"{total_return:+.2f}%")

    return portfolio_value, btc_value, total_return


def render_growth_charts(history):
    section_label("Performance")
    st.subheader("Portfolio Growth")

    if history.empty:
        st.caption("No portfolio history recorded yet.")
    else:
        st.line_chart(history.set_index("Time")["Portfolio Value"])

    st.subheader("₿ Bitcoin Price")
    if history.empty:
        st.caption("No price history recorded yet.")
    else:
        st.line_chart(history.set_index("Time")["BTC Price"])


def render_rule_engine(regime, strategy, latest):
    st.subheader("Rule Engine")
    st.metric("Market Regime", regime)
    st.metric("Strategy", strategy)
    st.metric("RSI", f"{latest['RSI']:.2f}")
    st.metric("ATR", f"{latest['ATR']:.2f}")
    st.metric("EMA50", f"${latest['EMA50']:.2f}")
    st.metric("SMA50", f"${latest['SMA50']:.2f}")


def render_ai_advisor(latest, portfolio):
    context = {
        "market": {
            "price": float(latest["Close"]),
            "RSI": float(latest["RSI"]),
            "ATR": float(latest["ATR"]),
            "EMA50": float(latest["EMA50"]),
            "SMA50": float(latest["SMA50"]),
        },
        "portfolio": {
            "cash": portfolio.cash,
            "btc": portfolio.total_btc(),
            "average_cost": portfolio.dca_avg_cost,
        },
        "news_sentiment": load_news(),
    }

    ai = evaluate_portfolio(context)

    try:
        confidence = float(ai.get("confidence", 0))
    except (TypeError, ValueError):
        confidence = 0.0

    st.subheader("AI Portfolio Advisor")
    st.metric("Recommendation", ai.get("recommendation", "N/A"))
    st.metric("Confidence", f"{confidence:.2f}")
    st.metric("Risk Level", ai.get("risk_level", "Unknown"))
    st.metric("Portfolio Health", ai.get("portfolio_health", "Unknown"))

    st.markdown("**Market Summary**")
    st.info(ai.get("market_summary", "No summary available."))

    st.markdown("**AI Reasoning**")
    st.write(ai.get("reasoning", "No reasoning provided."))

    return ai


def render_news_sentiment():
    st.header("News Sentiment")

    try:
        report = load_news()
    except Exception as e:
        st.error("Couldn't load the latest news sentiment.")
        st.exception(e)
        return

    score = report.get("score", 0)

    c1, c2 = st.columns(2)
    c1.metric("Overall Sentiment", report.get("sentiment", "Unknown"))
    c2.metric("Score", f"{score:.2f}")
    st.progress((score + 1) / 2)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("⚠️ Risks")
        risks = report.get("risks", [])
        if risks:
            for risk in risks:
                st.error(risk)
        else:
            st.caption("No notable risks flagged.")

    with col2:
        st.subheader("🚀 Opportunities")
        opportunities = report.get("opportunities", [])
        if opportunities:
            for item in opportunities:
                st.success(item)
        else:
            st.caption("No notable opportunities flagged.")

    st.subheader("Important Events")
    events = report.get("important_events", [])
    if events:
        for event in events:
            st.write("•", event)
    else:
        st.caption("No major events reported.")


def render_fear_greed():
    st.subheader("Fear & Greed Index")

    fear = get_fear_greed()
    fg_value = fear.get("value", 0)

    c1, c2 = st.columns(2)
    c1.metric("Index", fg_value)
    c2.metric("Classification", fear.get("classification", "Unknown"))
    st.progress(fg_value / 100)


def render_allocation(portfolio, btc_value):
    st.subheader("Portfolio Allocation")

    allocation = px.pie(
        names=["Cash", "Bitcoin"],
        values=[portfolio.cash, btc_value],
        color_discrete_sequence=["#8B949E", "#F2A93B"],
    )
    allocation.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#31333F",
        legend=dict(orientation="h", y=-0.1),
    )
    st.plotly_chart(allocation, use_container_width=True)


def render_recent_orders(orders):
    st.subheader("Recent Orders")
    st.dataframe(orders.tail(20), use_container_width=True, hide_index=True)


def render_trade_statistics(orders):
    st.subheader("Trading Statistics")

    buy_orders = orders[orders["Side"] == "BUY"]
    sell_orders = orders[orders["Side"] == "SELL"]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Orders", len(orders))
    c2.metric("Buys", len(buy_orders))
    c3.metric("Sells", len(sell_orders))
    c4.metric(
        "Average Buy",
        f"${buy_orders['Price'].mean():,.2f}" if len(buy_orders) else "$0",
    )

    if len(sell_orders):
        st.metric("Average Sell", f"${sell_orders['Price'].mean():,.2f}")

    if "Source" in orders.columns and not orders.empty:
        st.markdown("**Order Source Breakdown**")
        st.bar_chart(orders["Source"].value_counts())


def render_portfolio_snapshot(portfolio, current_price, portfolio_value):
    st.subheader("Portfolio Snapshot")

    snapshot = pd.DataFrame(
        {
            "Metric": [
                "Cash",
                "BTC Holdings",
                "Average Cost",
                "Current Price",
                "Portfolio Value",
            ],
            "Value": [
                f"${portfolio.cash:,.2f}",
                f"{portfolio.total_btc():.6f}",
                f"${portfolio.dca_avg_cost:,.2f}",
                f"${current_price:,.2f}",
                f"${portfolio_value:,.2f}",
            ],
        }
    )
    st.table(snapshot)


def render_sidebar(portfolio_value, portfolio, regime, strategy, ai):
    st.sidebar.header("Live Portfolio")
    st.sidebar.metric("Portfolio", f"${portfolio_value:,.2f}")
    st.sidebar.metric("Cash", f"${portfolio.cash:,.2f}")
    st.sidebar.metric("BTC", f"{portfolio.total_btc():.6f}")
    st.sidebar.divider()
    st.sidebar.metric("Regime", regime)
    st.sidebar.metric("Strategy", strategy)
    st.sidebar.metric("AI Recommendation", ai.get("recommendation", "N/A"))
    st.sidebar.metric("Risk", ai.get("risk_level", "Unknown"))


# ---------------------------------------------------------------------------
# Main render
# ---------------------------------------------------------------------------

def render():
    st.set_page_config(
        page_title="BTC AI Trading Dashboard",
        page_icon="₿",
        layout="wide",
    )
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    st.title("₿ Bitcoin AI Trading Dashboard")
    section_divider()

    portfolio, history, orders, latest = load_dashboard_data()
    current_price = float(latest["Close"])
    regime = detect_market_regime(latest)
    strategy = select_strategy(regime)

    portfolio_value, btc_value, _ = render_top_metrics(portfolio, latest, current_price)
    section_divider()

    tabs = st.tabs(
        ["Overview", "Rules & AI", "News & Sentiment", "Trading Activity", "Snapshot"]
    )

    with tabs[0]:
        render_growth_charts(history)
        section_divider()
        render_allocation(portfolio, btc_value)

    with tabs[1]:
        left, right = st.columns(2)
        with left:
            render_rule_engine(regime, strategy, latest)
        with right:
            ai = render_ai_advisor(latest, portfolio)

    with tabs[2]:
        render_news_sentiment()
        section_divider()
        render_fear_greed()

    with tabs[3]:
        render_recent_orders(orders)
        section_divider()
        render_trade_statistics(orders)

    with tabs[4]:
        render_portfolio_snapshot(portfolio, current_price, portfolio_value)

    render_sidebar(portfolio_value, portfolio, regime, strategy, ai)


if __name__ == "__main__":
    render()