def detect_market_regime(row):

    if row["RSI"] < 30:
        return "PANIC"

    elif (
        row["MACD"] > 0
        and row["RSI"] > 55
        and row["EMA50"] > row["SMA50"]
        and row["VOL_RATIO"] > 1.1
    ):
        return "TRENDING"

    else:
        return "RANGING"