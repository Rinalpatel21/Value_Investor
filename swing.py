from logging import config

from config import load_config
from telegram_bot import send_message


def swing_entry_signal(row):
    """Entry on strong momentum - STRICTLY RESTRICTED TO TRENDING MARKETS"""
    
    # NEW FILTER: If the market is chopping or panicking, do not swing trade
    if "REGIME" in row and row["REGIME"] != "TRENDING":
        return False

    if (
        row["RSI"] > 60
        and row["RSI"] < 75
        and row["MACD"] > 0
        and row["VOL_RATIO"] > 1.5
        and row["Close"] > row["EMA50"]
        and row["EMA50"] > row["SMA50"]
    ):
        return True

    return False


def open_swing_trade(
        portfolio,
        current_price,
        atr,
        current_time):

    config = load_config()
    
    stop_distance = config["atr_stop_multiplier"] * atr

    quantity=portfolio.cash/current_price

    cost = quantity * current_price

    if cost > portfolio.cash:
        print("Not enough cash to open swing trade.")
        return

    trade = {

        "entry": current_price,

        "stop": current_price - stop_distance,

        "partial_target": current_price + 3 * atr,
        
        "target": current_price + config["take_profit_multiplier"] * atr,

        "final_target": current_price + (config["final_target_multiplier"] * atr),

        "quantity": quantity,

        "partial_taken": False

              }

    portfolio.active_trades.append(trade)

    portfolio.cash -= cost

    portfolio.btc_swing += quantity

    print(

        f"SWING BUY | "

        f"Price={current_price:.2f} "

        f"Qty={quantity:.5f}"

    )

    if config.get("environment") != "BACKTEST":
        send_message(f"SWING BUY\nPrice={current_price:.2f}\nQty={quantity:.5f}")

    from trade_logger import log_trade

    log_trade(current_time,
              "SWING_BUY",
              current_price,
              round(cost, 2),
              round(quantity, 5),
              "BTC Bought")