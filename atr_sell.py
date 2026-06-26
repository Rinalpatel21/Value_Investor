from telegram_bot import send_message
from trade_logger import log_trade


def manage_active_trades(
        portfolio,
        current_price,
        current_time,
        atr):

    remaining_trades = []

    for trade in portfolio.active_trades:


        if current_price <= trade["stop"]:

            pnl = (
                current_price -
                trade["entry"]
            ) * trade["quantity"]

            portfolio.cash += (
                current_price *
                trade["quantity"]
            )

            portfolio.btc_swing -= trade["quantity"]

            portfolio.closed_trades.append(
                {
                    "entry": trade["entry"],
                    "exit": current_price,
                    "pnl": pnl
                }
            )

            portfolio.last_trade_time = current_time

            print(f"STOP LOSS | Exit={current_price:.2f} | PnL={pnl:.2f}")

            log_trade(current_time,
                      "STOP LOSS",
                       current_price,
                       round(current_price * trade["quantity"], 2),
                       round(trade["quantity"], 5),
                       round(pnl, 2)
                    )

            send_message(f"STOP LOSS | Exit={current_price:.2f} | PnL={pnl:.2f}")

            

        elif current_price >= trade["final_target"]:

            pnl = (
                current_price -
                trade["entry"]
            ) * trade["quantity"]

            portfolio.cash += (
                current_price *
                trade["quantity"]
            )

            portfolio.btc_swing -= trade["quantity"]

            portfolio.closed_trades.append(
                {
                    "entry": trade["entry"],
                    "exit": current_price,
                    "pnl": pnl
                }
            )

            portfolio.last_trade_time = current_time

            print(f"TAKE PROFIT | Exit={current_price:.2f} | PnL={pnl:.2f}")

            log_trade(current_time,
                      "TAKE PROFIT",
                       current_price,
                       round(current_price * trade["quantity"], 2),
                       round(trade["quantity"], 5),
                       round(pnl, 2)
                    )

            send_message(f"TAKE PROFIT | Exit={current_price:.2f} | PnL={pnl:.2f}")

        
        
        else:

            remaining_trades.append(trade)
        
        


    portfolio.active_trades = remaining_trades
    
    
    