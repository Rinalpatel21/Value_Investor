import csv
import os

def get_data_path(filename):
    base_dir = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_dir, "data", filename)


def save_portfolio_history(
    current_time,
    portfolio_value,
    btc_price,
    cash,
    btc_holdings
):

    csv_path = get_data_path("portfolio_history.csv")
    data_dir = os.path.dirname(csv_path)

    # ensure data directory exists
    os.makedirs(data_dir, exist_ok=True)

    file_exists = os.path.exists(csv_path)

    with open(csv_path, "a", newline="") as f:

        writer = csv.writer(f)

        if not file_exists:

            writer.writerow([
                "Time",
                "Portfolio Value",
                "BTC Price",
                "Cash",
                "BTC Holdings"
            ])

        writer.writerow([
            current_time,
            portfolio_value,
            btc_price,
            cash,
            btc_holdings
        ])