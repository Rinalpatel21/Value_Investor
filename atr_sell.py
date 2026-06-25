from telegram_bot import send_message
from trade_logger import log_trade


def manage_active_trades(
        portfolio,
        current_price,
        current_time,
        atr):

    remaining_trades = []

    for trade in portfolio.active_trades:

        # PARTIAL PROFIT: Take 50% at 3*ATR
        if not trade["partial_taken"] and current_price >= trade.get("partial_target", trade["entry"] + 3*atr):
            partial_qty = trade["quantity"] * 0.5
            partial_pnl = (current_price - trade["entry"]) * partial_qty
            portfolio.cash += current_price * partial_qty
            portfolio.btc_swing -= partial_qty
            trade["quantity"] -= partial_qty
            trade["partial_taken"] = True
            print(f"PARTIAL PROFIT | Exit={current_price:.2f} | PnL={partial_pnl:.2f}")

        # IMPROVED: Only trail stop after small profit
        if current_price > trade["entry"] + 0.5 * atr:
            trade["stop"] = max(trade["stop"], current_price - 1.5 * atr)

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

            log_trade("STOP LOSS",
                       current_price,
                       trade["quantity"],
                       pnl,
                      current_time
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

            log_trade("TAKE PROFIT",
                       current_price,
                       trade["quantity"],
                       pnl,
                       current_time
                    )

            send_message(f"TAKE PROFIT | Exit={current_price:.2f} | PnL={pnl:.2f}")

        
        
        else:

            remaining_trades.append(trade)
        
        


    portfolio.active_trades = remaining_trades
    
    
    