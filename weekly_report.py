import pandas as pd


def generate_report():

    try:
        df = pd.read_csv("paper_orders.csv")
    except FileNotFoundError:
        return """
BTC Trading Agent Weekly Report

No buy or sell history found yet.
"""

    total_trades = len(df)

    if total_trades == 0:
        return """
BTC Trading Agent Weekly Report

No buy or sell orders recorded this week.
"""

    buys = df[df["Side"] == "BUY"]
    sells = df[df["Side"] == "SELL"]

    buy_total = buys["Amount"].sum()
    sell_total = (sells["Price"] * sells["Amount"]).sum()

    latest = df.iloc[-1]

    report = f"""
BTC Trading Agent Weekly Report

Total Orders: {total_trades}

Buy Orders: {len(buys)}

Sell Orders: {len(sells)}

Total Buy Amount: ${buy_total:.2f}

Estimated Sell Value: ${sell_total:.2f}

Latest Order: {latest["Side"]} at ${latest["Price"]:.2f}

Cash After Latest Order: ${latest["Cash"]:.2f}

BTC After Latest Order: {latest["BTC"]:.6f}
"""

    return report
