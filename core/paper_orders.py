import csv
import os


def get_data_path(filename):
    base_dir = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_dir, "data", filename)


def save_order(
    side,
    price,
    amount,
    cash,
    btc,
    current_time
):

    csv_path = get_data_path("paper_orders.csv")
    data_dir = os.path.dirname(csv_path)
    os.makedirs(data_dir, exist_ok=True)
    file_exists = os.path.exists(csv_path)

    with open(
        csv_path,
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