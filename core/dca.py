from datetime import datetime
from .config import load_config
from .logger import log_trade
from .telegram_bot import send_message


def execute_dca_buy(
        portfolio,
        current_price,
        amount,
        current_time):

    if portfolio.cash < amount:

        return

    btc_bought = amount / current_price

    portfolio.cash -= amount

    portfolio.btc_dca += btc_bought

    portfolio.dca_total_cost += amount

    portfolio.dca_avg_cost = (
    portfolio.dca_total_cost /
    portfolio.btc_dca
   )

    portfolio.last_dca_buy_price = current_price

    portfolio.last_dca_buy_time = current_time

    print(
        f"DCA BUY | {current_time} | Price={current_price:.2f}"
    )

    from .logger import log_trade

    from .telegram_bot import send_message

    log_trade(current_time,
    "DCA BUY",
    current_price,
    amount,
    btc_bought
    )
    send_message(f"DCA BUY\nPrice={current_price:.2f}\nAmount=${amount}")

    