# BTC AI Trading Agent Workflow

## Overview

The BTC AI Trading Agent is an automated cryptocurrency trading system designed around a **rule-based execution engine** enhanced with an **LLM-powered portfolio advisor**.

The system separates **decision making** into two layers:

1. **Deterministic Rule Engine**
   - Executes every trade.
   - Never relies on an LLM.
   - Produces repeatable decisions.

2. **AI Portfolio Advisor**
   - Reviews the market.
   - Reviews the portfolio.
   - Reviews news sentiment.
   - Explains why the current strategy makes sense.
   - Never places trades.

This architecture guarantees that the trading engine remains deterministic while still benefiting from AI explanations.

---

# High Level Workflow

```
            Scheduler

                │

                ▼

      Download Market Data

                │

                ▼

      Calculate Indicators

                │

                ▼

      Detect Market Regime

                │

                ▼

      Select Trading Strategy

                │

                ▼

      Execute Rule Engine

                │

                ▼

      Update Portfolio

                │

                ▼

      Save Portfolio

                │

                ▼

      Build Market Context

                │

                ▼

      AI Portfolio Advisor

                │

                ▼

      Telegram Notification

                │

                ▼

      Dashboard & Chatbot
```

---

# Live Trading Workflow

The file

```
live_trading.py
```

is the main execution loop.

Each cycle performs the following steps.

---

## Step 1

Load Portfolio

```
load_portfolio()
```

Loads

- cash
- BTC holdings
- average cost
- active trades
- previous DCA purchases

from storage.

---

## Step 2

Load Configuration

```
load_config()
```

Loads

- DCA thresholds

- buy sizes

- stop loss

- swing settings

- portfolio limits

---

## Step 3

Download Market Data

```
download_btc_data()
```

Downloads recent BTC price history.

---

## Step 4

Calculate Indicators

```
add_indicators()
```

Calculates

- RSI

- ATR

- EMA50

- SMA50

- MACD

- Bollinger Bands

(if enabled)

---

## Step 5

Detect Market Regime

```
detect_market_regime()
```

Possible outputs

```
TRENDING

RANGING

PANIC
```

---

## Step 6

Choose Trading Strategy

```
select_strategy()
```

Possible outputs

```
DCA_ONLY

HYBRID

SWING_ONLY
```

The strategy depends entirely on the detected market regime.

---

## Step 7

Initial Buy

If no BTC exists

```
market_buy()
```

creates the initial position.

---

## Step 8

AI Portfolio Review

The rule engine pauses briefly to collect additional context.

```
build_market_context()
```

collects

- indicators

- portfolio

- news

- fear & greed

Then

```
evaluate_portfolio()
```

asks the LLM for

- recommendation

- confidence

- risk level

- reasoning

- market summary

This information is **advisory only**.

It never influences execution.

---

## Step 9

Rule-Based DCA

If strategy

```
DCA_ONLY

or

HYBRID
```

the engine checks

```
current price

vs

average cost
```

If price drops

```
3%

6%

9%
```

the configured DCA amount is invested.

---

## Step 10

Weekly DCA

If

```
7 days
```

have elapsed since the previous DCA purchase

another fixed investment is executed.

---

## Step 11

Swing Trading

If

```
HYBRID
```

is active

and

```
swing_entry_signal()
```

returns

```
True
```

the engine opens a swing trade.

---

## Step 12

ATR Trade Management

```
manage_active_trades()
```

updates

- stop losses

- take profits

- exits

for all active swing positions.

---

## Step 13

Risk Management

```
portfolio_stop()
```

checks

overall portfolio drawdown.

If limits are exceeded

the system enters protection mode.

---

## Step 14

Persist Portfolio

Updated portfolio

is saved using

```
save_portfolio()
```

---

## Step 15

Portfolio History

Each cycle appends

```
portfolio_history.csv
```

containing

- timestamp

- portfolio value

- BTC holdings

- cash

- BTC price

---

## Step 16

Telegram Notification

The completed cycle sends

- portfolio value

- strategy

- regime

- AI recommendation

- cash

- BTC holdings

to Telegram.

---

# Dashboard Workflow

The Streamlit dashboard is entirely read-only.

It never places trades.

---

Dashboard loads

```
Portfolio

↓

Market Data

↓

Indicators

↓

Strategy

↓

News Sentiment

↓

AI Report

↓

Portfolio History

↓

Paper Orders
```

It displays

- Portfolio metrics

- Market indicators

- Strategy

- Regime

- AI recommendation

- News sentiment

- Portfolio allocation

- Portfolio value chart

- Recent trades

---

# Chatbot Workflow

The chatbot is an LLM-powered assistant capable of interacting with the trading system.

---

## User

asks

```
Should I buy Bitcoin?
```

↓

```
agent.py
```

↓

```
llm_agent.py
```

↓

LLM chooses

```
get_trading_context
```

↓

```
tool_dispatcher.py
```

↓

```
tools.py
```

↓

returns

market

portfolio

strategy

↓

```
agent.py
```

↓

```
ai_advisor.py
```

↓

LLM explains recommendation

↓

Displayed to user

---

# Tool Execution Workflow

```
User Question

↓

LLM

↓

JSON Tool Request

↓

tool_dispatcher.py

↓

tools.py

↓

Python Function

↓

Result

↓

LLM Explanation

↓

Final Answer
```

---

# News Workflow

```
News API

↓

news.py

↓

news_sentiment.py

↓

LLM Sentiment Analysis

↓

news_sentiment.json

↓

Dashboard

↓

Chatbot
```

---

# Portfolio Storage Workflow

Portfolio state is persisted after every trading cycle.

```
Portfolio Object

↓

save_portfolio()

↓

portfolio.json
```

During startup

```
load_portfolio()
```

reconstructs the complete portfolio state.

---

# Order Workflow

Whenever a trade executes

```
market_buy()

or

market_sell()
```

the following occurs

```
Execute

↓

Update Portfolio

↓

Save Portfolio

↓

Save Paper Order

↓

Save Portfolio History

↓

Telegram Notification
```

---

# AI Advisory Workflow

Unlike many AI trading bots

the LLM never executes trades.

Instead

```
Market Context

+

Portfolio

+

News

+

Fear & Greed

↓

AI Portfolio Advisor

↓

Recommendation

↓

Human Explanation
```

The recommendation is logged

displayed

and sent to Telegram

but execution remains fully rule-based.

---

# Data Files

The system continuously maintains

```
portfolio.json

portfolio_history.csv

paper_orders.csv

trade_log.csv

news_sentiment.json
```

These files power both the dashboard and chatbot.

---

# Design Philosophy

The system intentionally separates

## Deterministic Trading

Responsible for

- buying
- selling
- risk management
- portfolio updates

from

## AI Intelligence

Responsible for

- explanation
- reasoning
- portfolio analysis
- market summaries
- conversational assistance

This architecture ensures reproducible execution while still benefiting from modern Large Language Models.