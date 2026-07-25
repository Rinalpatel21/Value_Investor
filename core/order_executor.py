import random

from .paper_orders import save_order

from .telegram_bot import send_message

PAPER_MODE = True


def market_buy(
    portfolio,

    price,

    amount,

    current_time,

    source

):

    if amount <= 0:
        return {"status": "rejected", "reason": "Buy amount must be positive."}

    if amount > portfolio.cash:
        return {"status": "rejected", "reason": "Buy amount exceeds available cash."}

    fee = amount * 0.001

    execution_price = price * (
        1 + random.uniform(-0.0005, 0.0005)
    )

    actual_amount = amount - fee

    from .dca import execute_dca_buy

    execute_dca_buy(
        portfolio,
        execution_price,
        actual_amount,
        current_time
    )

    portfolio.cash -= fee

    send_message(f""" PAPER BUY

                 Price: ${execution_price:.2f}

                 Amount: ${actual_amount:.2f}

                 Cash Left: ${portfolio.cash:.2f}

                 BTC Holdings: {portfolio.total_btc():.6f}""")

    save_order(

                    "BUY",
                    execution_price,
                    actual_amount,
                    portfolio.cash,
                    portfolio.total_btc(),
                    current_time,
                    source)

    return {
        "status": "executed",
        "side": "BUY",
        "price": execution_price,
        "quantity": amount,
        "cash": portfolio.cash,
        "btc": portfolio.total_btc()
    }


def market_sell(
    portfolio,

    price,

    amount,

    current_time,

    source

):

    if amount <= 0:
        return {"status": "rejected", "reason": "Sell amount must be positive."}

    if amount > portfolio.total_btc():
        return {"status": "rejected", "reason": "Sell amount exceeds BTC holdings."}

    fee = amount * price * 0.001

    execution_price = price * (
        1 + random.uniform(-0.0005, 0.0005)
    )

    cash_received = (
        amount *
        execution_price
    ) - fee

    portfolio.cash += cash_received

    swing_quantity = min(amount, portfolio.btc_swing)
    dca_quantity = amount - swing_quantity

    portfolio.btc_swing -= swing_quantity

    if dca_quantity > 0:
        previous_dca_btc = portfolio.btc_dca
        portfolio.btc_dca -= dca_quantity

        if previous_dca_btc > 0:
            cost_reduction = portfolio.dca_total_cost * (
                dca_quantity / previous_dca_btc
            )
            portfolio.dca_total_cost -= cost_reduction

        if portfolio.btc_dca > 0:
            portfolio.dca_avg_cost = (
                portfolio.dca_total_cost /
                portfolio.btc_dca
            )
        else:
            portfolio.dca_total_cost = 0
            portfolio.dca_avg_cost = 0

    print("PAPER SELL")

    save_order(
        "SELL",
        execution_price,
        amount,
        portfolio.cash,
        portfolio.total_btc(),
        current_time,
        source
    )
    
    send_message(f""" PAPER SELL

                 Price: ${execution_price:.2f}

                 Quantity: {amount:.6f}

                 Cash Left: ${portfolio.cash:.2f}

                 BTC Holdings: {portfolio.total_btc():.6f}""")

    return {
        "status": "executed",
        "side": "SELL",
        "price": execution_price,
        "quantity": amount,
        "cash": portfolio.cash,
        "btc": portfolio.total_btc()
    }
