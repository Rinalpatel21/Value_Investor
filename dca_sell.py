from trade_logger import log_trade
from telegram_bot import send_message
import trade_logger


from trade_logger import log_trade
from telegram_bot import send_message


def dca_protective_sell(
        portfolio,
        current_price,
        current_time,
        atr):

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


        # Calculate realized PnL on the sold portion for logging
        pnl_on_sell = (current_price - average_cost) * sell_qty

        portfolio.last_trade_time = current_time 

        print(f"DCA PROTECTIVE SELL | Exit={current_price:.2f} | PnL={pnl_on_sell:.2f}")

        log_trade(current_time,
                  "DCA PROTECTIVE SELL",
                   current_price,
                   round(current_price * sell_qty, 2),
                   round(sell_qty, 5),
                   round(pnl_on_sell, 2)
                )

        send_message(f"DCA PROTECTIVE SELL\nExit={current_price:.2f}\nPnL={pnl_on_sell:.2f}")