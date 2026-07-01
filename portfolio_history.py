import csv
import os

def save_portfolio_history(
    current_time,
    portfolio_value,
    btc_price,
    cash,
    btc_holdings
):

    file_exists = os.path.exists("portfolio_history.csv")

    with open(
        "portfolio_history.csv",
        "a",
        newline=""
    ) as f:

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