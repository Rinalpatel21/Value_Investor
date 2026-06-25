import pandas as pd


def generate_report():

    df = pd.read_csv(
        "trade_log.csv"
    )

    total_trades = len(df)

    wins = len(
        df[df["PnL"] > 0]
    )

    total_profit = df["PnL"].sum()

    win_rate = (
        wins / total_trades * 100
        if total_trades > 0
        else 0
    )

    report = f"""
BTC Trading Agent Weekly Report

Trades: {total_trades}

Win Rate: {win_rate:.2f}%

Profit: ${total_profit:.2f}
"""

    return report