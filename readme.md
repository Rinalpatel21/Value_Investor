#  AI-Powered Bitcoin Trading Agent

**A hybrid AI + algorithmic trading system that combines LLM reasoning with rule-based quantitative strategies to analyze markets, manage trading portfolio, execute a live trading loop, send real-time notifications, and answer questions through a conversational assistant.**

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/LLM-Groq%20Llama%203.3%2070B-orange" />
  <img src="https://img.shields.io/badge/Notifications-Telegram-26A5E4?logo=telegram&logoColor=white" />
  <img src="https://img.shields.io/badge/Status-Active%20Development-brightgreen" />
  <img src="https://img.shields.io/badge/License-Educational%20Use-lightgrey" />
</p>

---

##  Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Trading Strategies](#-hybrid-trading-strategies)
- [Live Trading Loop](#-live-trading-loop)
- [Telegram Notifications](#-telegram-notifications)
- [AI Chat Assistant](#-ai-chat-assistant)
- [Dashboard](#-dashboard)
- [Architecture](#-project-architecture)
- [Trading Workflow](#-trading-workflow)
- [Project Structure](#-project-structure)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
- [Running the App](#-running-the-app)
- [Skills Demonstrated](#-skills-demonstrated)
- [Images](#-Images)


---

##  Overview

This project is a complete, end-to-end **AI-assisted algorithmic trading system** for Bitcoin, built to demonstrate how large language models can be integrated responsibly alongside deterministic, risk-managed trading logic rather than being given free rein over real capital.

The system combines:

- Quantitative trading strategies (DCA, Swing Trading, ATR-based exits)
- LLM-based market reasoning and decision explanation (Groq / Llama 3.3 70B)
- A **live trading loop** that runs on a schedule, evaluates the market, and acts autonomously within configured risk limits
- Portfolio and risk management
- Real-time **Telegram notifications** for every decision and status update
- A live Streamlit dashboard for performance monitoring
- A conversational AI assistant for querying portfolio and trade data
- A trading execution engine with full trade logging

Unlike a typical "black box" trading bot, this system lets the LLM **analyze and recommend**, while deterministic guardrails and risk rules retain final control over execution — a pattern closer to how AI is used responsibly in real trading and finance environments.

---

##  Features

### AI Trading Decision Engine

Uses an LLM (Groq — Llama 3.3 70B) to:

- Analyze current market conditions (price, RSI, ATR, EMA50, SMA50, trend strength, momentum)
- Evaluate live portfolio status (cash, BTC held, average cost, allocation %)
- Recommend Buy / Sell / Hold decisions, constrained to a maximum buy/sell size derived from portfolio risk limits
- Return a structured decision with a **confidence score**
- Explain every trading decision in plain English
- Answer trading-related questions conversationally

---

##  Hybrid Trading Strategies

###  Dollar Cost Averaging (DCA)

Automatically buys Bitcoin when:

- The portfolio has never made an initial buy (auto-triggers a starting DCA buy)
- A weekly DCA schedule triggers (7+ days since the last buy)
- Price drops below one of several configurable drawdown thresholds, each with its own buy size (tiered dip-buying)

Supports:

- Dynamic buy sizing based on how far price has dropped from average cost
- Running average cost calculation
- Cost basis tracking over time

---

###  Swing Trading

Detects short-term trading opportunities using a combination of technical indicators:

- RSI (Relative Strength Index)
- EMA (Exponential Moving Average)
- SMA (Simple Moving Average)
- ATR (Average True Range)
- Market regime detection

Features:

- Entry signal generation
- Only opens a new swing trade when no active trade already exists
- Active open-trade management on every cycle

---

###  ATR Exit Strategy

Uses Average True Range (volatility) to:

- Protect unrealized profits
- Limit downside losses
- Dynamically adjust exit points as volatility changes
- Manage all currently active/open trades on every cycle

---

###  Portfolio Risk Management

Continuously monitors:

- Total portfolio value (cash + BTC holdings at current price)
- Maximum drawdown vs. initial capital
- Capital allocation across cash/BTC
- Position sizing — every buy/sell is capped as a percentage of portfolio value, not just a fixed amount

A **portfolio stop** is triggered and logged if the portfolio's drawdown exceeds the configured risk limit, halting further risk-taking.

---

##  Live Trading Loop

The core of the system is `run_live_agent()` — a full autonomous trading cycle that runs on a schedule (e.g. via cron, Task Scheduler, or a hosted job runner). Each cycle:

1. **Loads state** — current portfolio and strategy configuration
2. **Pulls fresh market data** and computes technical indicators
3. **Runs an initial DCA buy** if the portfolio has never traded before
4. **Builds a full market state snapshot** — price, indicators, regime, strategy, portfolio metrics, and risk-adjusted max buy/sell limits
5. **Asks the LLM decision engine** for a Buy / Sell / Hold recommendation with reasoning and a confidence score, and executes it
6. **Applies tiered/weekly DCA rules** independently of the LLM, based on price drawdown from average cost
7. **Manages swing trades** — opens new positions on valid signals, manages existing ones every cycle
8. **Applies ATR-based exit management** to all active trades
9. **Checks the portfolio stop** risk control and halts trading if drawdown limits are breached
10. **Persists portfolio state and history** after every state-changing step
11. **Sends Telegram notifications** for both the AI's decision and a full status summary
12. Wraps the entire cycle in error handling so a single failed cycle doesn't crash the scheduler — it logs the error and waits for the next run

---

##  Telegram Notifications

Every trading cycle sends real-time updates to Telegram, including:

- **AI Decision alerts** — action taken, confidence score, execution result, and the AI's reasoning
- **Initial DCA buy confirmations**
- **Portfolio status summaries** — current price, market regime, active strategy, portfolio value, cash, and BTC held

This keeps a human in the loop on every autonomous decision the system makes, without needing to actively watch the dashboard.

---

##  AI Chat Assistant

An interactive assistant, scoped entirely to trading-related queries, with a guided sidebar and example-question prompts built directly into the UI so users know exactly what they can ask.

**Sidebar help panel covers:**

** Portfolio**
- Show my portfolio
- What is my portfolio value?
- How much cash do I have?
- How much BTC do I own?
- What is my average buy price?

** Market Analysis**
- What is the BTC price?
- What's the current market regime?
- What strategy is active?
- Explain today's market conditions

** Trading Performance**
- How much money have I made?
- Show my trading performance
- What is my total return?
- Am I profitable?

** Trade History**
- Show recent trades
- What was my last trade?
- Show paper orders
- When did I last buy Bitcoin?

** AI Decisions**
- Should I buy Bitcoin?
- Should I sell Bitcoin?
- Why did the AI recommend buying?
- Explain today's recommendation
- Analyze my trading account

An in-chat **"💡 Example Questions" expander** also surfaces sample prompts directly above the chat input, so first-time users aren't staring at a blank box.

The assistant is protected by **guardrails** that keep it strictly focused on cryptocurrency trading topics, politely declining anything out of scope (see [Guardrails](#-guardrails) below).

---

##  Dashboard

A live Streamlit dashboard providing full visibility into portfolio and strategy performance:

**Portfolio Snapshot**
- Portfolio Value
- Cash on hand
- BTC Holdings
- Total Return %

**Trade Statistics**
- Total Trades
- Win Rate
- Average Win / Average Loss
- Profit Factor

**Charts**
- Portfolio growth over time
- BTC price history
- Portfolio allocation — Cash vs. BTC (pie chart)
- Buy vs. Sell activity (bar chart)

**Tables**
- Portfolio snapshot (cash, BTC, average cost, current price)
- Recent trade log (last 10 trades)
- Full paper order history

**Sidebar Status**
- Live cash and BTC holdings shown persistently in the sidebar while browsing the dashboard

---

## Project Architecture

```
                           +---------------------------+
                           |        Streamlit UI       |
                           |---------------------------|
                           | Dashboard   | AI Chat     |
                           +-------------+-------------+
                                         |
                                         |
                                         v
                         +-------------------------------+
                         |         Agent Layer           |
                         |-------------------------------|
                         | agent.py                     |
                         | decision_engine.py           |
                         | tool_dispatcher.py           |
                         +---------------+--------------+
                                         |
                  +----------------------+----------------------+
                  |                                             |
                  |                                             |
                  v                                             v
      +-----------------------+                     +----------------------+
      |      Groq LLM         |                     | Traditional Engine   |
      |-----------------------|                     |----------------------|
      | Market Analysis       |                     | DCA                 |
      | Risk Evaluation       |                     | Swing Trading       |
      | Portfolio Analysis    |                     | ATR Exit            |
      | Tool Selection        |                     | Risk Manager        |
      +-----------+-----------+                     +----------+----------+
                  |                                             |
                  +----------------------+----------------------+
                                         |
                                         v
                           +---------------------------+
                           |    Order Executor         |
                           |---------------------------|
                           | Paper Buy                |
                           | Paper Sell               |
                           +------------+-------------+
                                        |
                     +------------------+--------------------+
                     |                                       |
                     v                                       v
        +------------------------+              +------------------------+
        | Portfolio Storage      |              | CSV Logs              |
        |------------------------|              |------------------------|
        | portfolio.json         |              | trade_log.csv          |
        | portfolio_history.csv  |              | paper_orders.csv       |
        +------------------------+              +------------------------+
```

---

##  Trading Workflow

```
                    Start Trading Cycle
                           |
                           |
                           v
              Download Latest BTC Market Data
                           |
                           v
              Calculate Technical Indicators
          (RSI, EMA50, SMA50, ATR, Volume)
                           |
                           v
               Detect Market Regime
      (Trending / Ranging / Panic Market)
                           |
                           v
             Select Trading Strategy
       (Hybrid / DCA / Swing / Hold)
                           |
                           |
          +----------------+----------------+
          |                                 |
          |                                 |
          v                                 v
   Traditional Trading              LLM Analysis
   --------------------             -------------------
   • DCA Logic                     • Analyze Market
   • Swing Logic                   • Analyze Portfolio
   • ATR Exit                      • Choose Tool
   • Risk Checks                   • Explain Reasoning
          |                                 |
          +----------------+----------------+
                           |
                           v
                 Decision Engine
                           |
                           v
                 Tool Dispatcher
                           |
         +-----------------+----------------+
         |                                  |
         |                                  |
         v                                  v
     Market Buy                       Market Sell
         |                                  |
         +-----------------+----------------+
                           |
                           v
                 Update Portfolio
                           |
                           v
                 Save Trade Logs
                           |
                           v
         Update Dashboard & AI Chat
                           |
                           v
                  Next 30 Minute Cycle
```

---
 ## LLM Architecture
```
Explain

System Prompt

↓

Conversation Memory

↓

Market State

↓

Portfolio

↓

LLM

↓

JSON Decision

↓

Validation

↓

Tool Dispatcher

↓

Execution

↓

Explanation
```
---

##  Project Structure

```
Trading_Agent/
│
├── app.py                        # Single entry point — sidebar navigation (Dashboard / AI Chat)
├── dashboard.py                   # Dashboard page (render())
├── chatbot.py                      # AI Chat page (render()) — sidebar help + example questions
├── run_bot.py                       # Entry point for the autonomous live trading loop
│
├── core/
│   ├── agent.py                       # Orchestrates the chat agent's reasoning loop
│   ├── live_agent.py                   # run_live_agent() — the autonomous trading cycle
│   ├── decision_engine.py               # LLM-driven trade decision + confidence scoring
│   ├── tool_dispatcher.py                # Routes LLM tool calls to real functions
│   ├── tools.py                           # Tool implementations available to the LLM
│   │
│   ├── llm_agent.py                        # Groq API wrapper / LLM calls
│   ├── assistant_prompt.py                  # System prompt for the chat assistant
│   ├── prompt.py                              # System prompt for the trading decision engine
│   │
│   ├── market_data.py                          # Market data ingestion (yfinance)
│   ├── indicators.py                            # Technical indicator calculations
│   ├── regime.py                                  # Market regime detection
│   ├── strategy.py                                 # Strategy selection logic
│   │
│   ├── order_executor.py                            # Executes paper trades (market_buy, etc.)
│   ├── paper_orders.py                                # Paper order management
│   ├── portfolio.py                                    # Portfolio object / calculations
│   ├── portfolio_storage.py                              # Portfolio load/save (persistence)
│   ├── portfolio_history.py                                # Historical portfolio tracking
│   │
│   ├── risk_manager.py                                       # portfolio_stop() risk control
│   ├── atr_sell.py                                             # manage_active_trades() — ATR exits
│   ├── swing.py                                                  # Swing trading entry + open logic
│   ├── dca.py                                                      # DCA strategy logic
│   │
│   ├── config_loader.py                                              # Loads strategy/risk config
│   ├── telegram_bot.py                                                 # send_message() — Telegram alerts
│   │
│   ├── guardrails.py                                                     # Topic-scoping for the chat assistant
│   ├── conversation.py                                                    # Chat message history management
│   ├── logs.py                                                              # Structured event logging
│   │
│   └── data/
│       ├── trade_log.csv                                                      # Trade history
│       ├── paper_orders.csv                                                    # Paper order history
│       ├── portfolio.json                                                       # Portfolio state
│       └── portfolio_history.csv                                                  # Portfolio value over time
│
├── requirements.txt
└── README.md
```

---

##  Guardrails

The LLM assistant is deliberately restricted to cryptocurrency trading topics only.

**Allowed:**
- Bitcoin & crypto markets
- Portfolio state and performance
- Orders and trade history
- Trading strategies and technical indicators
- AI decision explanations

**Politely refused:**
- Personal questions
- Politics
- Homework / general coding help
- Medical advice
- General knowledge unrelated to trading
- Any other off-topic conversation

This ensures the assistant behaves predictably and stays within its intended domain — an important consideration when deploying LLMs in any user-facing product.

---

##  Tech Stack

| Category              | Tools / Libraries                     |
|------------------------|----------------------------------------|
| **Language**            | Python                                |
| **AI / LLM**             | Groq API, Llama 3.3 70B              |
| **Data Processing**       | Pandas, NumPy                       |
| **Market Data**            | Yahoo Finance (`yfinance`)         |
| **Technical Analysis**      | `ta` library                      |
| **Dashboard / UI**           | Streamlit, Plotly                |
| **Notifications**             | Telegram Bot API               |
| **Persistence**                 | CSV, JSON                    |

---

##  Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Rinalpatel21/Trading_Agent.git
cd Trading_Agent
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate it

**Windows**
```bash
.venv\Scripts\activate
```

**macOS / Linux**
```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_CHAT_ID=your_telegram_chat_id_here
```

> Update the exact variable names above to match what `core/telegram_bot.py` and `core/config_loader.py` actually read — adjust if your implementation names them differently.

For deployment on **Hugging Face Spaces**, add each of these under **Settings → Secrets** instead of a `.env` file.

### 6. Configure strategy & risk settings

Strategy thresholds (drawdown tiers, DCA buy sizes, risk limits) are loaded via `core/config_loader.py`. Review and adjust your config file to set:

- Drop-percentage tiers (`drop_1`, `drop_2`, `drop_3`) and their corresponding buy sizes
- Initial capital
- Risk/drawdown stop limits

---

## Running the App

The dashboard and AI chat live in a **single Streamlit app** with sidebar navigation:

```bash
streamlit run app.py
```

Then, in the sidebar, switch between:

- ** Dashboard** — portfolio value, charts, trade analytics
- ** AI Chat** — ask questions like *"Should I buy Bitcoin?"* or *"Show my recent trades"*, guided by the built-in sidebar help panel and example-question expander

### Running the autonomous trading bot

```bash
python run_bot.py
```

Each cycle, the bot will:

1. Load the current portfolio and config
2. Download the latest BTC market data and calculate indicators
3. Execute an initial DCA buy if this is the first run
4. Build a full market state and request an AI-generated recommendation with a confidence score
5. Execute the recommended trade (subject to risk-adjusted position limits)
6. Apply tiered/weekly DCA rules independently of the LLM
7. Manage swing trade entries and exits
8. Apply ATR-based exit management to open positions
9. Check the portfolio risk stop
10. Update and persist portfolio state and history
11. Send Telegram notifications for the decision and overall status

Schedule `run_bot.py` with cron, Windows Task Scheduler, or a hosted job runner to keep the loop running continuously.

---

##  Skills Demonstrated

- **LLM integration with guardrails** — combining generative reasoning with deterministic control and topic scoping
- **Tool-calling / function-dispatch architecture** for LLM-driven actions, including confidence-scored decisions
- **Autonomous scheduled agent design** — a live trading loop with layered strategy logic, error handling, and state persistence
- **Quantitative strategy design** (tiered DCA, swing trading, volatility-based exits)
- **Risk management logic** independent of the LLM's recommendations, including portfolio-level stop conditions
- **Third-party API integration** for real-time notifications (Telegram Bot API)
- **Full-stack Python application design** with a clearly separated `core/` package structure
- **Interactive data visualization** with Streamlit and Plotly
- **Stateful conversational AI** with session and conversation history management, and UX-focused onboarding (sidebar help, example prompts)
- **Structured logging and auditability** for a system making financial decisions

---

## Images 
<img width="1882" height="839" alt="chatbot" src="https://github.com/user-attachments/assets/2420fb8e-c09a-4ca8-9556-be5440f48f2d" />
<img width="1565" height="796" alt="dashboard" src="https://github.com/user-attachments/assets/94c2ce26-0e9c-425f-a104-d12971a32486" />
<img width="1466" height="846" alt="performance" src="https://github.com/user-attachments/assets/2502b400-e5f8-433f-977e-f020430e4537" />
<img width="652" height="778" alt="telegram" src="https://github.com/user-attachments/assets/c9373937-0e99-4790-8c60-04cddc7aa4fb" />


##  Author

**Rinal Patel**
Data Science • Machine Learning • Business Analytics • AI

- GitHub: [Rinalpatel21](https://github.com/Rinalpatel21)
- LinkedIn: [rinalpatel-datascientist](https://www.linkedin.com/in/rinalpatel-datascientist)

# Test Edit
