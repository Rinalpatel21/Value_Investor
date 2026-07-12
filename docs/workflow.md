# Trading Workflow

## Overview

The trading agent executes automatically every 30 minutes.

Each cycle consists of data collection, AI reasoning, traditional strategy evaluation, execution, and logging.

---

# Complete Workflow

```
Start Trading Cycle
        │
        ▼
Download BTC Data
        │
        ▼
Calculate Indicators
(RSI, EMA50, SMA50, ATR)
        │
        ▼
Detect Market Regime
        │
        ▼
Select Trading Strategy
        │
        ▼
Build Market State
        │
        ▼
LLM Decision Engine
        │
        ▼
Tool Dispatcher
        │
        ▼
Execute Buy / Sell
        │
        ▼
Run Rule-Based Strategies
        │
        ▼
Risk Management
        │
        ▼
Update Portfolio
        │
        ▼
Save Logs
        │
        ▼
Update Dashboard
        │
        ▼
Wait 30 Minutes
```

---

## Step 1

Download latest BTC price data.

Source:

- Yahoo Finance

---

## Step 2

Calculate technical indicators.

Indicators include:

- RSI
- EMA50
- SMA50
- ATR

---

## Step 3

Detect market regime.

Possible regimes:

- Trending
- Ranging
- Panic

---

## Step 4

Choose strategy.

Possible strategies:

- Hybrid
- DCA Only
- Swing Only
- Hold

---

## Step 5

Build Market State.

Information includes:

- Current price
- Technical indicators
- Portfolio balance
- BTC holdings
- Current strategy
- Current regime

---

## Step 6

LLM analyzes market.

The AI evaluates:

- Portfolio
- Technical indicators
- Market conditions
- Risk

It recommends:

- Buy
- Sell
- Hold

---

## Step 7

Tool Dispatcher validates the request.

Checks include:

- Available cash
- BTC holdings
- Order size
- Portfolio constraints

---

## Step 8

Execute trade.

Supported actions:

- Market Buy
- Market Sell

---

## Step 9

Run traditional strategies.

The deterministic engine continues to execute:

- DCA
- Weekly DCA
- Swing entries
- ATR exits
- Portfolio stop-loss

---

## Step 10

Save updated portfolio.

Files updated:

- portfolio.json
- trade_log.csv
- paper_orders.csv
- portfolio_history.csv

---

## Step 11

Dashboard refreshes.

Updated information includes:

- Portfolio value
- BTC holdings
- Trade history
- Performance metrics

---

## Step 12

AI Chat Assistant.

Users can ask:

- Portfolio questions
- Market questions
- Trading questions
- AI reasoning
- Historical trades

without affecting the trading engine.