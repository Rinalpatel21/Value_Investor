import csv
import os


def save_order(
    side,
    price,
    amount,
    cash,
    btc,
    current_time
):

    file_exists = os.path.exists("paper_orders.csv")

    with open(
        "paper_orders.csv",
        "a",
        newline=""
    ) as f:

        writer = csv.writer(f)

        if not file_exists:

            writer.writerow([
                "Time",
                "Side",
                "Price",
                "Amount",
                "Cash",
                "BTC"
            ])

        writer.writerow([
            current_time,
            side,
            price,
            amount,
            cash,
            btc
        ])