from core.portfolio_storage import load_portfolio, save_portfolio
from core.market_data import download_btc_data
from core.indicators import add_indicators

from core.regime import detect_market_regime
from core.strategy import select_strategy

from core.config_loader import load_config

from core.decision_engine import make_decision


from core.telegram_bot import send_message

from core.portfolio_history import save_portfolio_history
from core.risk_manager import portfolio_stop

from core.atr_sell import manage_active_trades
from core.swing import swing_entry_signal, open_swing_trade

from core.order_executor import market_buy


def build_market_state(portfolio, row):

    

    price = float(row["Close"])

    regime = detect_market_regime(row)
    strategy = select_strategy(regime)

    portfolio_value = (
        portfolio.cash +
        portfolio.total_btc() * price
    )

    max_buy_amount = min(
        portfolio.cash,
        portfolio_value * 0.10,
        500
    )

    max_sell_quantity = min(
        portfolio.total_btc(),
        portfolio.total_btc() * 0.25
    )

    return {
        "price": price,
        "RSI": float(row["RSI"]),
        "ATR": float(row["ATR"]),
        "EMA50": float(row["EMA50"]),
        "SMA50": float(row["SMA50"]),

        "regime": regime,
        "strategy": strategy,

        "cash": portfolio.cash,
        "btc": portfolio.total_btc(),
        "average_cost": portfolio.dca_avg_cost,

        "portfolio_value": portfolio_value,

        "max_buy_amount": max_buy_amount,
        "max_sell_quantity": max_sell_quantity,
        "has_cash": portfolio.cash > 10,
        "has_btc": portfolio.total_btc() > 0,
        "position_value": portfolio.total_btc() * price,
        "allocation_pct": (portfolio.total_btc() * price) / (portfolio.cash + 1e-9),
        "trend_strength": abs(row["EMA50"] - row["SMA50"]),
        "momentum": row["RSI"] - 50
        
    }


def run_live_agent():

    try:

        print("=" * 50)
        print("Starting new trading cycle...")

        portfolio = load_portfolio(10000)

        config = load_config()

        df = download_btc_data()
        df = add_indicators(df)

        row = df.iloc[-1]

        current_price = float(row["Close"])
        current_time = row.name

        print(f"Cash: {portfolio.cash:.2f}")
        print(f"DCA BTC: {portfolio.btc_dca:.6f}")
        print(f"Average Cost: {portfolio.dca_avg_cost:.2f}")

        ####################################
        # Initial Buy
        ####################################

        if portfolio.last_dca_buy_price is None:

            market_buy(
                portfolio,
                current_price,
                500,
                current_time
            )

            save_portfolio(portfolio)

            send_message("Initial DCA Buy Executed")

        ####################################
        # LLM Decision
        ####################################

        market_state = build_market_state(
            portfolio,
            row
        )

        decision, result = make_decision(market_state,
                                        portfolio=portfolio,
                                        current_time=current_time,
                                        execute=True)

        save_portfolio(portfolio)

        tool = decision["decision"]["tool"]
        confidence = decision["analysis"]["confidence"]
        summary = decision["explanation"]["summary"]

        send_message(
            f"""
AI Decision

Action: {tool}

Confidence: {confidence:.2f}

Execution:
{result}

Reason:
{summary}
"""
        )

        ####################################
        # Existing Strategy Logic
        ####################################

        regime = detect_market_regime(row)
        strategy = select_strategy(regime)

        if strategy in ["HYBRID", "DCA_ONLY"]:

            if portfolio.dca_avg_cost > 0:

                drop_pct = (
                    portfolio.dca_avg_cost -
                    current_price
                ) / portfolio.dca_avg_cost

            else:
                drop_pct = 0

            if drop_pct >= config["drop_3"]:
                amount = config["dca_buy_3"]

            elif drop_pct >= config["drop_2"]:
                amount = config["dca_buy_2"]

            elif drop_pct >= config["drop_1"]:
                amount = config["dca_buy_1"]

            else:
                amount = 0

            if amount > 0:

                market_buy(
                    portfolio,
                    current_price,
                    amount,
                    current_time
                )

                save_portfolio(portfolio)

        ####################################
        # Weekly DCA
        ####################################

        if portfolio.last_dca_buy_time is not None:

            days_since_buy = (
                current_time -
                portfolio.last_dca_buy_time
            ).days

            if days_since_buy >= 7:

                market_buy(
                    portfolio,
                    current_price,
                    500,
                    current_time
                )

                save_portfolio(portfolio)

        ####################################
        # Swing Trades
        ####################################

        if strategy == "HYBRID":

            if len(portfolio.active_trades) == 0:

                if swing_entry_signal(row):

                    open_swing_trade(
                        portfolio,
                        current_price,
                        row["ATR"],
                        current_time
                    )

                    save_portfolio(portfolio)

        manage_active_trades(
            portfolio,
            current_price,
            current_time,
            row["ATR"]
        )

        save_portfolio(portfolio)

        ####################################
        # Risk Management
        ####################################

        portfolio_value = (
            portfolio.cash +
            portfolio.total_btc() * current_price
        )

        if portfolio_stop(
            portfolio_value,
            config["initial_capital"]
        ):

            print("PORTFOLIO STOP TRIGGERED")

        ####################################
        # Save History
        ####################################

        save_portfolio_history(
            current_time,
            portfolio_value,
            current_price,
            portfolio.cash,
            portfolio.total_btc()
        )

        ####################################
        # Status
        ####################################

        send_message(
            f"""
BTC Agent Status

Price: ${current_price:.2f}

Regime: {regime}

Strategy: {strategy}

Portfolio: ${portfolio_value:.2f}

Cash: ${portfolio.cash:.2f}

BTC: {portfolio.total_btc():.6f}
"""
        )

        print("Trading cycle complete.")

    except Exception as e:

        print("ERROR:", e)