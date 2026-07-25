from core.portfolio_storage import load_portfolio, save_portfolio
from core.market_data import download_btc_data
from core.indicators import add_indicators

from core.regime import detect_market_regime
from core.strategy import select_strategy

from core.config_loader import load_config

from core.telegram_bot import send_message

from core.portfolio_history import save_portfolio_history
from core.risk_manager import portfolio_stop

from core.atr_sell import manage_active_trades
from core.swing import swing_entry_signal, open_swing_trade

from core.order_executor import market_buy
from core.market_context import build_market_context
from core.ai_advisor import evaluate_portfolio

import traceback



def get_ai_assessment(context):
    """
    LLM call — ADVISORY ONLY.
    Never used to size, gate, or trigger a trade. If this call fails or
    returns malformed data, the rule engine below runs completely unaffected.
    """
    try:
        ai_summary = evaluate_portfolio(context)
        return ai_summary
    except Exception as e:
        print("AI assessment failed (non-fatal, rules still execute):", e)
        return {
            "recommendation": "N/A",
            "confidence": None,
            "market_summary": "AI assessment unavailable this cycle.",
            "portfolio_health": "N/A",
            "risk_level": "N/A",
            "reasoning": f"Error calling AI: {e}",
            "action": "N/A",
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

        # Compute regime/strategy once for the whole cycle
        regime = detect_market_regime(row)
        strategy = select_strategy(regime)

        portfolio_changed = False

        ####################################
        # Initial Buy (rule-based)
        ####################################
        if portfolio.last_dca_buy_price is None:
            market_buy(portfolio, current_price, 500, current_time)
            portfolio_changed = True
            send_message("Initial DCA Buy Executed")

        ####################################
        # AI Portfolio Manager — ADVISORY ONLY
        # Output goes to Telegram + logs. Nothing below reads from it.
        ####################################
        context = build_market_context(portfolio, row)
        ai_summary = get_ai_assessment(context)

        print("\n===== AI Portfolio Manager (advisory) =====")
        print(ai_summary)

        ####################################
        # Rule-Based DCA on Drawdown
        ####################################
        if strategy in ["HYBRID", "DCA_ONLY"]:

            if portfolio.dca_avg_cost > 0:
                drop_pct = (
                    portfolio.dca_avg_cost - current_price
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
                market_buy(portfolio, current_price, amount, current_time)
                portfolio_changed = True

        ####################################
        # Weekly DCA
        ####################################
        if portfolio.last_dca_buy_time is not None:
            days_since_buy = (current_time - portfolio.last_dca_buy_time).days

            if days_since_buy >= 7:
                market_buy(portfolio, current_price, 500, current_time)
                portfolio_changed = True

        ####################################
        # Swing Trades
        ####################################
        if strategy == "HYBRID":
            if len(portfolio.active_trades) == 0:
                if swing_entry_signal(row):
                    open_swing_trade(
                        portfolio, current_price, row["ATR"], current_time
                    )
                    portfolio_changed = True

        manage_active_trades(portfolio, current_price, current_time, row["ATR"])
        portfolio_changed = True  # may have closed/adjusted trades

        ####################################
        # Risk Management
        ####################################
        portfolio_value = (
            portfolio.cash + portfolio.total_btc() * current_price
        )

        stop_triggered = portfolio_stop(portfolio_value, config["initial_capital"])
        if stop_triggered:
            print("PORTFOLIO STOP TRIGGERED")

        ####################################
        # Persist once per cycle
        ####################################
        if portfolio_changed:
            save_portfolio(portfolio)

        save_portfolio_history(
            current_time,
            portfolio_value,
            current_price,
            portfolio.cash,
            portfolio.total_btc(),
        )

        ####################################
        # Single consolidated notification
        ####################################
        send_message(f"""
BTC Agent Status

Price: ${current_price:.2f}
Regime: {regime}
Strategy: {strategy}
Portfolio: ${portfolio_value:.2f}
Cash: ${portfolio.cash:.2f}
BTC: {portfolio.total_btc():.6f}
{"PORTFOLIO STOP TRIGGERED" if stop_triggered else ""}

-------------------------
AI Advisory (not used for execution)
-------------------------
Recommendation: {ai_summary.get('recommendation')}
Risk view: {ai_summary.get('risk_level')}
Market: {ai_summary.get('market_summary')}
Reasoning: {ai_summary.get('reasoning')}
""")

        print("Trading cycle complete.")

    except Exception as e:
        print("ERROR:", e)
        traceback.print_exc()
        try:
            send_message(f"BTC Agent cycle FAILED: {e}")
        except Exception:
            print("Also failed to send error alert via Telegram.")