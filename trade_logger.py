import csv
import os


def log_trade(
        trade_type,
        price,
        quantity,
        pnl,
        timestamp):

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
                "Quantity"
            ])

        writer.writerow([
            timestamp,
            trade_type,
            round(price,2),
            round(quantity,6)
        ])