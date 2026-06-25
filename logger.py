import csv
import os


def log_trade(
        current_time,
        action,
        price,
        amount,
        btc):

    file_exists = os.path.isfile("trade_log.csv")

    with open(
            "trade_log.csv",
            "a",
            newline=""
    ) as file:

        writer = csv.writer(file)

        if not file_exists:

            writer.writerow([
                "Time",
                "Action",
                "Price",
                "Amount",
                "BTC"
            ])

        writer.writerow([
            current_time,
            action,
            round(price,2),
            round(amount,2),
            round(btc,6)
        ])