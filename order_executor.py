import random

from paper_orders import save_order

from telegram_bot import send_message

PAPER_MODE = True


def market_buy(portfolio, price, amount, current_time):

    fee = amount * 0.001

    execution_price = price * (
        1 + random.uniform(-0.0005, 0.0005)
    )

    actual_amount = amount - fee

    from dca import execute_dca_buy

    execute_dca_buy(
        portfolio,
        execution_price,
        actual_amount,
        current_time
    )

    send_message(f""" PAPER BUY

                 Price: ${execution_price:.2f}

                 Amount: ${actual_amount:.2f}

                 Cash Left: ${portfolio.cash:.2f}

                 BTC Holdings: {portfolio.total_btc():.6f}""")

    save_order("BUY",

               execution_price,

               actual_amount,

               portfolio.cash,

               portfolio.total_btc(),

               current_time)


def market_sell(
    portfolio,
    quantity,
    price,
    current_time
):

    fee = quantity * price * 0.001

    execution_price = price * (
        1 + random.uniform(-0.0005, 0.0005)
    )

    cash_received = (
        quantity *
        execution_price
    ) - fee

    portfolio.cash += cash_received

    portfolio.btc_swing -= quantity

    print("PAPER SELL")

    save_order("SELL",

               execution_price,

                quantity,

                portfolio.cash,

                portfolio.total_btc(),

                current_time)
    
    send_message(f""" PAPER SELL

                 Price: ${execution_price:.2f}

                 Quantity: {quantity:.6f}

                 Cash Left: ${portfolio.cash:.2f}

                 BTC Holdings: {portfolio.total_btc():.6f}""")