def atr_opportunity_buy(
        portfolio,
        current_price,
        current_time,
        atr):
    """Buy on significant dips (2*ATR)"""
    if portfolio.dca_avg_cost == 0:
        return

    drop_amount = (
        portfolio.dca_avg_cost -
        current_price
    )

    if drop_amount > 2.5 * atr:

        if portfolio.cash >= 300:

            btc_bought = 300 / current_price

            portfolio.cash -= 300

            portfolio.btc_dca += btc_bought

            portfolio.last_dca_buy_price = current_price

            portfolio.last_dca_buy_time = current_time

            print("ATR OPPORTUNITY BUY")

def dca_protective_sell(
        portfolio,
        current_price,
        atr):
    """Protective sell at 3*ATR loss to limit damage"""
    if portfolio.btc_dca == 0:

        return

    average_cost = portfolio.dca_avg_cost

    protection_level = average_cost - 3 * atr

    ##################################
    # Reset cooldown
    ##################################

    if current_price > average_cost:

        portfolio.dca_protective_sell_active = False

    ##################################
    # Protective sell
    ##################################

    if (
        current_price < protection_level
        and
        portfolio.dca_protective_sell_active == False
    ):

        sell_qty = portfolio.btc_dca * 0.20

        cost_reduction = sell_qty * average_cost

        portfolio.btc_dca -= sell_qty

        portfolio.cash += sell_qty * current_price

        ##################################
        # Adjust cost basis
        ##################################

        portfolio.dca_total_cost -= cost_reduction

        if portfolio.btc_dca > 0:

            portfolio.dca_avg_cost = (

                portfolio.dca_total_cost

                /

                portfolio.btc_dca

            )

        ##################################
        # Activate cooldown
        ##################################

        portfolio.dca_protective_sell_active = True

        print("DCA PROTECTIVE SELL")