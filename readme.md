# Autonomous Bitcoin Trading Agent

An AI-powered Bitcoin trading system designed to operate with minimal human supervision and continuously adapt to changing market conditions. The system combines **Dollar-Cost Averaging (DCA)**, **ATR-based risk management**, **market regime detection**, and **dynamic strategy selection** to manage Bitcoin positions while protecting capital.

---

# Overview

This project simulates a fully automated cryptocurrency trading agent capable of:

- Running continuously (24/7)
- Dynamically allocating capital
- Accumulating Bitcoin using DCA
- Managing active trades with ATR-based stops
- Switching strategies based on market conditions
- Providing portfolio-level risk protection
- Sending trade notifications
- Generating weekly reports
- Supporting cloud deployment and Docker

---

# Features

## Dollar Cost Averaging (DCA)

Long-term accumulation strategy:

- Initial buy
- Buy additional BTC when price drops
- Adaptive position sizing:

| Price Drop | Buy Amount |
|------------|-----------|
| 3% | $500 |
| 6% | $700 |
| 9% | $1000 |

### ATR Opportunistic DCA

When price falls sharply relative to volatility:

```
Price Drop > 2 × ATR
```

Additional BTC is accumulated.

---

## ATR Protective Sell

Protects DCA holdings during severe drawdowns.

Rule:

```
Protection Level =
Average Cost − 3 × ATR
```

Action:

```
Sell 20% of DCA holdings
```

Cooldown logic prevents repeated selling while price remains below the threshold.

---

## Swing Trading Engine

Short-term trades are opened only when market conditions support them.

### Entry Conditions

- RSI > 60
- MACD > 0
- Volume above average
- Price > EMA50
- EMA50 > SMA50

---

## ATR Stop Loss

Dynamic volatility-based stop:

```
Stop = Entry − 2 × ATR
```

---

## Profit Targets

### Target 1

```
Entry + 3 × ATR
```

### Final Target

```
Entry + 5 × ATR
```

---

## Trailing Stop

Once price moves in favor:

```
Stop = max(
    previous_stop,
    current_price - 1.5 × ATR
)
```

This locks profits while allowing trends to continue.

---

# Market Regime Detection

The agent classifies markets into:

### TRENDING

Conditions:

- MACD > 0
- Price > EMA50

### RANGING

Neutral market conditions.

### PANIC

Oversold conditions:

```
RSI < 30
```

---

# Strategy Selection

| Regime | Strategy |
|---------|----------|
| TRENDING | HYBRID |
| RANGING | DCA_ONLY |
| PANIC | DCA_ONLY |

---

# Portfolio Safety Layer

Global protection against catastrophic losses.

Rule:

```
Portfolio Drawdown ≥ 25%
```

Action:

```
Pause Trading
```

---

# Performance Metrics

Backtesting evaluates:

### Sharpe Ratio

Risk-adjusted returns.

### Maximum Drawdown

Largest portfolio decline.

### Win Rate

Percentage of profitable trades.

### Portfolio Value

Final account balance.

---

# Technical Indicators

Feature engineering includes:

- ATR
- RSI
- MACD
- SMA50
- EMA50
- Volume Ratio

---

# Data Sources

Supported market data providers:

- Yahoo Finance (yfinance)
- Binance API
- Coinbase API
- CoinMarketCap API
- Investing.com

Current implementation uses:

```python
yfinance
```

with:

```
BTC-USD
30-minute candles
```

---

# Project Architecture

```
Configuration Manager
        ↓
State Manager
        ↓
Market Data Engine
        ↓
Feature Engineering
        ↓
Market Regime Detection
        ↓
Strategy Selector
        ↓
DCA Engine
        ↓
ATR Opportunity Buy
        ↓
Swing Trade Entry
        ↓
ATR Stop Loss
        ↓
Trade Management
        ↓
Portfolio Risk Layer
        ↓
Performance Metrics
        ↓
Telegram Alerts
        ↓
Weekly Gmail Reports
```

---

# Project Structure

```
trading-agent/

│
├── market_data.py
├── indicators.py
├── portfolio.py
├── dca.py
├── dca_atr.py
├── swing.py
├── atr_sell.py
├── regime.py
├── strategy.py
├── risk_manager.py
├── performance.py
├── config.py
├── test.py
│
├── config.json
├── requirements.txt
├── .env
├── README.md
```

---

# Technologies Used

## Python

- Pandas
- NumPy
- yfinance
- ta
- datetime

## Machine Learning / AI

- LLM-assisted strategy selection
- Feature engineering
- Market regime detection

## Trading Concepts

- Dollar Cost Averaging
- ATR-based stops
- Volatility analysis
- Portfolio risk management

---

# Future Improvements

## LLM Module

Use GPT models to:

- Select strategies dynamically
- Adjust DCA thresholds
- Generate market commentary
- Recommend allocation changes

---

## Notifications

### Telegram Bot

Trade alerts:

```
DCA BUY
ATR BUY
SWING BUY
STOP LOSS
TAKE PROFIT
```

---

## Weekly Gmail Report

Every Monday at 9 AM:

- Portfolio Value
- BTC Holdings
- Trade History
- Win Rate
- Sharpe Ratio
- Drawdown
- LLM Insights

---

## Configuration Manager

Parameters loaded from:

### Google Sheets

Hourly refresh.

Fallback:

```
config.json
```

Sensitive credentials stored in:

```
.env
```

---

## Deployment

Designed for:

- Docker
- AWS
- DigitalOcean
- Linux VPS

Continuous execution:

```
24/7 autonomous trading
```

---

# Example Workflow

```
START
 ↓
Load Config
 ↓
Load Portfolio State
 ↓
Download BTC Data
 ↓
Calculate Indicators
 ↓
Detect Market Regime
 ↓
Select Strategy
 ↓
DCA Buy Check
 ↓
ATR Opportunity Buy
 ↓
Swing Entry
 ↓
Create ATR Stops
 ↓
Manage Active Trades
 ↓
Protect Portfolio
 ↓
Calculate Performance
 ↓
Send Alerts
 ↓
Save State
 ↓
Repeat Every 30 Minutes
```

---

# Current Status

### Implemented

- ✅ Market Data Engine
- ✅ Feature Engineering
- ✅ Portfolio State Manager
- ✅ DCA Engine
- ✅ ATR Opportunity Buy
- ✅ ATR Protective Sell
- ✅ Swing Trading
- ✅ ATR Stop Loss
- ✅ Trailing Stop
- ✅ Market Regime Detection
- ✅ Strategy Selection
- ✅ Portfolio Risk Layer
- ✅ Performance Metrics
- ✅ Backtesting Framework

### Planned

- ⏳ Google Sheet Config Manager
- ⏳ Telegram Notifications
- ⏳ Weekly Gmail Reports
- ⏳ LLM Strategy Module
- ⏳ Docker Deployment
- ⏳ AWS/DigitalOcean Deployment

---

# Disclaimer

This project is for educational and research purposes only.

Cryptocurrency trading involves substantial risk. Past performance does not guarantee future results. Always conduct your own research before deploying automated trading systems with real capital.