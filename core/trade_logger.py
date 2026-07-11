import csv
import os

def get_data_path(filename):
    base_dir = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_dir, "data", filename)

def log_trade(timestamp,
        trade_type,
        price,
        investment_amount,
        btc_bought,
        pnl):


    csv_path = get_data_path("trade_log.csv")
    file_exists = os.path.isfile(csv_path)

    with open(
        csv_path,
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