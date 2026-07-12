# System Architecture

## Overview

The BTC AI Trading Agent is a hybrid trading framework that combines:

- Large Language Models (Groq Llama 3.3 70B)
- Traditional algorithmic trading
- Technical analysis
- Portfolio management
- Interactive dashboard
- AI trading assistant

The system separates decision-making from execution, allowing the LLM to recommend actions while deterministic trading rules continue to manage risk and execution.

---

## High-Level Architecture

```
                Streamlit UI
        ┌─────────────────────────┐
        │ Dashboard │ AI Chat     │
        └───────────┬─────────────┘
                    │
                    ▼
            Decision Engine
                    │
         ┌──────────┴───────────┐
         │                      │
         ▼                      ▼
   Traditional Engine       LLM Agent
         │                      │
         └──────────┬───────────┘
                    ▼
             Tool Dispatcher
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
     Market Buy          Market Sell
                    │
                    ▼
             Portfolio Storage
                    │
          Portfolio / Trade Logs
```

---

## Major Components

### User Interface

- Streamlit Dashboard
- AI Chat Assistant
- Performance Metrics
- Trade History
- Portfolio Monitoring

---

### LLM Layer

Responsible for:

- Portfolio analysis
- Market interpretation
- Strategy recommendations
- Natural language interaction
- Tool selection

Files:

- llm_agent.py
- assistant_prompt.py
- prompt.py

---

### Decision Engine

Acts as the bridge between AI reasoning and execution.

Responsibilities:

- Request AI recommendation
- Validate AI output
- Execute tools
- Record decisions

Files:

- decision_engine.py
- agent.py

---

### Tool Dispatcher

Provides secure execution of approved actions.

Supported tools:

- market_buy
- market_sell
- get_portfolio
- get_market_summary
- get_recent_orders
- get_performance
- get_profit_loss
- get_last_trade
- get_trading_context

---

### Trading Engine

Contains deterministic strategies.

Modules include:

- DCA Buying
- Swing Trading
- ATR Exits
- Portfolio Stop Loss
- Market Regime Detection

---

### Portfolio Management

Responsible for:

- Cash balance
- BTC holdings
- Average cost
- Active swing trades
- Portfolio persistence

---

### Logging

Every decision is recorded.

Logs include:

- AI recommendations
- Executed trades
- Portfolio history
- Paper orders
- Chat interactions

---

## Design Philosophy

The project intentionally combines AI reasoning with deterministic trading logic.

The AI provides flexibility and interpretation while algorithmic strategies ensure repeatable execution and risk control.

This hybrid architecture improves transparency, reliability, and extensibility.