# Deployment Guide

This project can be deployed locally or on Hugging Face Spaces.

---

# Local Deployment

## Clone Repository

```bash
git clone https://github.com/yourusername/BTC-AI-Trading-Agent.git

cd BTC-AI-Trading-Agent
```

---

## Create Virtual Environment

```bash
python -m venv .venv
```

Activate

Windows

```bash
.venv\Scripts\activate
```

Mac/Linux

```bash
source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure API Keys

Create

```
.env
```

Example

```
GROQ_API_KEY=xxxxxxxx
```

---

## Launch Dashboard

```bash
streamlit run app.py
```

---

## Launch Trading Engine

```bash
python run_bot.py
```

---

# Hugging Face Deployment

## Create a Space

SDK:

Docker (Streamlit)

---

## Push Repository

```bash
git add .

git commit -m "Deploy application"

git push
```

---

## Add Secrets

Settings

↓

Secrets

Add

```
GROQ_API_KEY
```

Value

```
xxxxxxxx
```

---

## Environment Variables

The project automatically reads:

```python
import os

api_key = os.environ.get("GROQ_API_KEY")
```

which works locally with `.env` and in Hugging Face Spaces with Secrets.

---

# Dashboard Features

The deployed application includes:

- Portfolio Dashboard
- Trading Performance
- BTC Price Charts
- Portfolio Growth
- Trade History
- Paper Orders
- AI Chat Assistant

---

# AI Chat Features

Users can ask:

- Show my portfolio
- Analyze my portfolio
- Show recent trades
- Profit and loss
- Should I buy Bitcoin?
- Should I sell Bitcoin?
- Explain the AI recommendation
- Current market regime
- Active strategy

The assistant only answers cryptocurrency trading-related questions.

---

# Future Improvements

Potential enhancements include:

- Multi-asset trading
- Live exchange integration
- Broker APIs
- Approval Mode
- Multi-agent collaboration
- Reinforcement learning
- News sentiment analysis
- Risk dashboards
- Trade visualization
- Automated backtesting