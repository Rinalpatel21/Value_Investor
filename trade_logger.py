import csv
import os


def log_trade(timestamp,
        trade_type,
        price,
        investment_amount,
        btc_bought,
        pnl):


    file_exists = os.path.isfile("trade_log.csv")

    with open(
        "trade_log.csv",
        "a",
        newline=""
    ) as f:

        writer = csv.writer(f)

        if not file_exists:

            writer.writerow([
                "Timestamp",
                "Type",
                "Price",
                "Investment Amount",
                "BTC Bought",
                "PnL"
            ])

        writer.writerow([
            timestamp,
            trade_type,
            round(price,2),
            investment_amount,
            btc_bought,
            pnl
        ])