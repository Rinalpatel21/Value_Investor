import csv
import os

def get_data_path(filename):
    base_dir = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_dir, "data", filename)

def log_trade(
        current_time,
        action,
        price,
        amount,
        btc):

    csv_path = get_data_path("trade_log.csv")
    file_exists = os.path.isfile(csv_path)

    with open(
            csv_path,
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