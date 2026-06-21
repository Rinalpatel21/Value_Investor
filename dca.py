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

    