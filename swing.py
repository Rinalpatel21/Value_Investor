def swing_entry_signal(row):
    """Entry on strong momentum with quality filters"""
    if (
        row["RSI"] > 60
        and row["RSI"] < 75
        and
        row["MACD"] > 0
        and
        row["VOL_RATIO"] > 1.5
        and
        row["Close"] > row["EMA50"]
        and
        row["EMA50"] > row["SMA50"]
    ):
        return True

    return False


def open_swing_trade(
        portfolio,
        current_price,
        atr):

    #################################
    # Risk 0.5% of cash (reduced for better Sharpe)
    #################################

    risk_amount = portfolio.cash * 0.005

    #################################
    # Stop distance (tighter for better risk/reward)
    #################################

    stop_distance = 1.5 * atr

    quantity = risk_amount / stop_distance

    cost = quantity * current_price

    #################################
    # Don't exceed available cash
    #################################

    if cost > portfolio.cash:

        quantity = portfolio.cash / current_price

        cost = quantity * current_price

    trade = {

        "entry": current_price,

        "stop": current_price - stop_distance,

        "partial_target": current_price + 3 * atr,

        "target": current_price + 6 * atr,

        "final_target": current_price + 9 * atr,

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