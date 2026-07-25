# Bitcoin Trading Agent — System Architecture

## 1. Purpose & Design Philosophy

This system is an AI-assisted Bitcoin trading platform. It combines deterministic,
rule-based trading logic with an LLM-based advisory and conversational layer.

The core design principle is a **strict separation of concerns**:

> **Rules trade. AI explains.**

- All trade execution (buys, sells, stop losses, DCA, swing entries/exits) is handled
  exclusively by deterministic Python logic.
- The AI layer (Groq Llama 3.3 70B) never places trades. It only reasons over
  structured data to produce summaries, recommendations, and natural-language
  explanations for the user.

This separation keeps trading behavior auditable, reproducible, and testable,
while still giving the user a conversational, explainable interface into what
the system is doing and why.

---

## 2. High-Level Architecture

```
                          ┌───────────────────────────┐
                          │      Streamlit Frontend    │
                          │   Dashboard   +   Chatbot  │
                          └──────────────┬─────────────┘
                                         │
                          ┌──────────────▼─────────────┐
                          │         Core Engine         │
                          └──────────────┬─────────────┘
                                         │
        ┌────────────────────────────────┼────────────────────────────────┐
        │                                │                                │
        ▼                                ▼                                ▼
  ┌─────────────┐               ┌────────────────┐              ┌──────────────────┐
  │ Market Data │               │ Portfolio Mgmt │              │   AI Components   │
  │             │               │                │              │                   │
  │ Data fetch  │               │ Portfolio      │              │ Groq LLM Agent    │
  │ Indicators  │               │ Storage        │              │ AI Advisor        │
  │ Regime      │               │ Order Executor │              │ News Sentiment    │
  │ Strategy    │               │ Trade History  │              │ Chat Assistant    │
  └─────┬───────┘               └───────┬────────┘              └─────────┬─────────┘
        │                               │                                 │
        └───────────────┬───────────────┴────────────────┬────────────────┘
                        ▼                                ▼
                ┌───────────────┐                ┌──────────────────┐
                │ Telegram Alert│                │ Streamlit Dashboard│
                └───────────────┘                └──────────────────┘
```

Three columns, one pipeline: **data flows in**, **rules decide**, **AI explains**.

---

## 3. Project Structure

```
project/
├── app.py                     # Entry point
├── dashboard.py                # Streamlit dashboard UI
├── chatbot.py                  # Streamlit chat UI
├── live_trading.py             # Live trading cycle orchestrator
│
└── core/
    ├── market_data.py          # Historical/live price data
    ├── indicators.py           # Technical indicators
    ├── regime.py                # Market regime detection
    ├── strategy.py              # Regime → strategy mapping
    │
    ├── portfolio.py             # Portfolio state (cash, BTC, trades)
    ├── portfolio_storage.py     # Persistence for portfolio.json
    ├── portfolio_history.py     # Historical portfolio snapshots
    │
    ├── order_executor.py        # Executes paper trades
    ├── paper_order.py           # Paper order log (CSV)
    │
    ├── swing.py                  # Swing trade entries/exits
    ├── atr_sell.py                # ATR-based trailing stop exits
    ├── risk_manager.py            # Portfolio-level risk controls
    │
    ├── news.py                    # News ingestion (NewsAPI)
    ├── news_sentiment.py          # LLM-based sentiment summarization
    │
    ├── market_context.py          # Aggregates state for the AI layer
    ├── ai_advisor.py               # Produces AI trading recommendation
    ├── llm_agent.py                 # Groq API communication layer
    ├── assistant_prompt.py          # System prompts for the assistant
    ├── prompt.py                     # Shared prompt templates
    │
    ├── tools.py                       # Tool definitions for the chat agent
    ├── tool_dispatcher.py              # Routes LLM tool calls to functions
    ├── agent.py                         # Chat agent reasoning loop
    │
    └── telegram_bot.py                  # Trade/alert notifications

data/
├── portfolio.json
├── paper_orders.csv
├── portfolio_history.csv
├── trade_log.csv
└── news_sentiment.json
```

---

## 4. Layer Breakdown

### Layer 1 — Data Ingestion

| Component | Responsibility | Source | Output |
|---|---|---|---|
| `market_data.py` | Downloads historical/live BTC price data | Yahoo Finance | OHLCV data |
| `indicators.py` | Computes technical indicators | OHLCV data | RSI, ATR, EMA50, SMA50, MACD, volume metrics |
| `news.py` | Fetches recent Bitcoin news | NewsAPI | List of articles |
| `news_sentiment.py` | LLM-based summarization of news into sentiment, risks, and opportunities | News articles | `news_sentiment.json` |

This is the only layer that talks to external data providers. Everything downstream
consumes its output, so upstream failures (e.g., API rate limits) are isolated here.

---

### Layer 2 — Trading Engine (Deterministic Core)

This is the layer responsible for **all trading decisions**. No LLM involvement.

| Component | Responsibility | Output |
|---|---|---|
| `regime.py` | Classifies current market state | `TRENDING`, `RANGING`, or `PANIC` |
| `strategy.py` | Maps regime to an active strategy | `DCA_ONLY`, `HYBRID`, or `SWING_ONLY` |
| `portfolio.py` | Tracks cash, BTC holdings, DCA average cost, open/closed trades | In-memory portfolio state |
| `portfolio_storage.py` | Reads/writes portfolio state to disk | `portfolio.json` |
| `order_executor.py` | Executes `market_buy()` / `market_sell()`, logs every order | Paper trade execution |
| `paper_order.py` | Persists each order (time, side, amount, price, source) | `paper_orders.csv` |
| `swing.py` | Manages swing-trade entries, exits, stop losses | Trade signals |
| `atr_sell.py` | Manages ATR-based trailing stop exits | Exit signals |
| `risk_manager.py` | Enforces portfolio-level stop-loss / risk limits | Risk overrides |

**Why this matters:** Regime detection and strategy selection form a simple state
machine — the market's condition determines which trading approach is active,
without requiring the AI to be in the loop. This keeps trading behavior consistent
and easy to backtest.

---

### Layer 3 — AI Advisory Layer

The AI layer sits *alongside* the trading engine, not inside it. It reads state,
never writes it.

**`market_context.py`** aggregates everything the AI needs into a single structured
object:
- Market indicators
- Portfolio state
- Recent news
- Fear & Greed index
- News sentiment summary

**`ai_advisor.py`** takes that context and, via Groq's LLM, returns a structured
recommendation:

```json
{
  "recommendation": "",
  "confidence": 0,
  "risk_level": "",
  "market_summary": "",
  "reasoning": ""
}
```

**`llm_agent.py`** is the single point of contact with the Groq API, exposing:
```python
ask_agent()
explain_tool_result()
get_ai_decision()
```

Centralizing all LLM calls in one module means prompt formats, retries, and model
config changes only need to happen in one place.

> **Guardrail:** `ai_advisor.py` has no access to `order_executor.py`. This is
> enforced structurally, not just by convention — the advisor module simply isn't
> given a reference to anything that can place trades.

---

### Layer 4 — Conversational Agent (Tool-Calling Chatbot)

The chatbot lets users query the system in natural language, using a standard
tool-calling loop:

```
User prompt
    → LLM
    → Tool request (e.g. {"tool": "show_portfolio"})
    → Tool Dispatcher
    → Python function execution
    → Result
    → LLM explains result in natural language
    → User
```

| Component | Responsibility |
|---|---|
| `tools.py` | Defines available tools: portfolio, trades, orders, performance, news, AI report, market summary, buy/sell BTC, trading context |
| `tool_dispatcher.py` | Maps a tool name from the LLM's response to the corresponding Python function |
| `agent.py` | Owns the full reasoning loop: receive prompt → call LLM → parse tool call → execute → return result → get explanation |

Note that "Buy Bitcoin" / "Sell Bitcoin" appear as *tools* the chatbot can invoke —
these still route through `order_executor.py`, meaning even user-initiated trades
via chat go through the same deterministic execution path as automated trades.
The LLM decides *when to call* the tool; it does not execute the trade itself.

---

### Layer 5 — Live Trading Cycle

`live_trading.py` orchestrates one full trading cycle:

```
 1. Load portfolio
 2. Download market data
 3. Calculate indicators
 4. Detect regime
 5. Select strategy
 6. Execute DCA
 7. Execute swing trades
 8. Apply risk management
 9. Save portfolio
10. Build AI context
11. Generate AI advisory
12. Send Telegram notification
```

Steps 1–9 are pure trading logic. Steps 10–12 are advisory/notification only —
by the time the AI is invoked, all trades for the cycle have already executed
and been persisted. The AI is reporting on what happened, not influencing it.

---

### Layer 6 — Dashboard

Built with Streamlit + Plotly. Read-only view into system state, organized into
four panels:

| Panel | Contents |
|---|---|
| **Portfolio** | Portfolio value, cash, BTC holdings, return |
| **Market** | Price, RSI, ATR, EMA, SMA, active strategy, current regime |
| **AI Advisor** | Recommendation, confidence, risk level, portfolio health, market summary, reasoning |
| **News** | Sentiment, risks, opportunities, notable events |
| **Performance** | Portfolio history, allocation, recent orders |

---

### Layer 7 — Chat Interface

Also Streamlit-based. Supports:
- Natural-language portfolio queries
- Buy/sell commands (routed through the tool-calling agent)
- Trade history lookup
- AI-generated explanations of trades and market conditions
- Strategy explanations

---

## 5. End-to-End Data Flow

```
Yahoo Finance
     │
     ▼
Market Data ──▶ Indicators ──▶ Regime Detection ──▶ Strategy Selection
                                                          │
                                                          ▼
                                                    Trading Rules
                                                          │
                                                          ▼
                                                  Portfolio Update
                                                          │
                                                          ▼
                                                  Portfolio Storage
                                                          │
                                                          ▼
                                                   Market Context
                                                          │
                                                          ▼
                                                     AI Advisor
                                                     /        \
                                                    ▼          ▼
                                              Dashboard      Chatbot
```

---

## 6. Design Principles

| Principle | What it means here |
|---|---|
| **Modularity** | Each concern (data, indicators, regime, strategy, portfolio, execution, AI, chat) lives in its own module with one job. |
| **Deterministic execution** | Trades are decided and placed by rule-based logic only — never by the LLM. |
| **AI as advisory, not authority** | The LLM explains, summarizes, and recommends. It has no execution privileges. |
| **Persistent state** | Portfolio, orders, and history are written to disk (JSON/CSV) so the system survives restarts and remains inspectable. |
| **Extensibility** | New indicators, strategies, tools, or AI capabilities can be added as new modules without touching existing ones. |
| **Observability** | Trade logs, portfolio history, Telegram alerts, and the dashboard together give full visibility into system behavior at any point in time. |

---

## 7. Technology Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Language | Python |
| Data handling | Pandas, NumPy |
| Technical analysis | TA library |
| Visualization | Plotly |
| AI / LLM | Groq — Llama 3.3 70B |
| News | NewsAPI |
| Market data | Yahoo Finance |
| Notifications | Telegram Bot API |
| Storage | JSON + CSV |
| Trading mode | Paper trading engine |

---

## 8. Summary

The platform pairs a deterministic quantitative trading core with an explainable
AI layer. Rule-based components own market analysis, portfolio management, and
trade execution; the LLM layer sits beside that core, translating structured
state into natural-language insight — news interpretation, portfolio
recommendations, and conversational Q&A. Because execution and explanation are
architecturally separate, the system's trading behavior stays consistent and
auditable regardless of what the AI layer says or does.