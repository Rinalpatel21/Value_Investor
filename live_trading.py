import time





from dca import execute_dca_buy
from portfolio_storage import load_portfolio
from portfolio_storage import save_portfolio
from portfolio import Portfolio

from market_data import download_btc_data
from indicators import add_indicators

from regime import detect_market_regime
from strategy import select_strategy

from telegram_bot import send_message
from config import load_config

from market_data import download_btc_data
from indicators import add_indicators

from paper_orders import save_order

from order_executor import market_buy


from regime import detect_market_regime
from strategy import select_strategy

from swing import (
    swing_entry_signal,
    open_swing_trade
)

from atr_sell import manage_active_trades

from risk_manager import portfolio_stop



from config_loader import load_config

from portfolio_history import save_portfolio_history


def run_live_agent():
    

    try:

      print("=" * 50)
      print("Starting new trading cycle...")

    # Load saved portfolio
      portfolio = load_portfolio(10000)

    # Load latest config
      config = load_config()

    # Download market data
      df = download_btc_data()

    # Calculate indicators
      df = add_indicators(df)

    # Latest candle
      row = df.iloc[-1]

      current_price = row["Close"]

      print(f"Cash: {portfolio.cash:.2f}")
      print(f"DCA BTC: {portfolio.btc_dca:.6f}")
      print(f"Average Cost: {portfolio.dca_avg_cost:.2f}")

####################################
# First DCA Buy
####################################

      if portfolio.last_dca_buy_price is None:

          market_buy(
                      portfolio,
                      current_price,
                      500,
                      row.name
                     )

          save_portfolio(portfolio)

          print("Initial DCA Buy Executed")

          send_message("Initial DCA Buy Executed")

    

# Detect regime
      regime = detect_market_regime(row)

    # Select strategy
      strategy = select_strategy(regime)

      print(f"Price: {row['Close']:.2f}")
      print(f"Regime: {regime}")
      print(f"Strategy: {strategy}")

    # Execute DCA / Swing logic here

       
      if strategy in ["HYBRID", "DCA_ONLY"]:

         if portfolio.dca_avg_cost > 0:

           drop_pct = (
              portfolio.dca_avg_cost -
              row["Close"]
              ) / portfolio.dca_avg_cost

         else:

            drop_pct = 0

         if drop_pct >= config["drop_3"]:

             amount = config["dca_buy_3"]

         elif drop_pct >= config["drop_2"]:

              amount = config["dca_buy_2"]

         elif drop_pct >= config["drop_1"]:

             amount = config["dca_buy_1"]

         else:

             amount = 0

         if amount > 0:

           market_buy(portfolio,
                      row["Close"],
                      amount,
                      row.name)
           
           print(f"Drop % = {drop_pct:.4f}")
           print(f"Buy Amount = {amount}")

    
####################################
# Weekly DCA
####################################

      current_time = row.name

      if portfolio.last_dca_buy_time is not None:

           days_since_buy = (
           current_time -
           portfolio.last_dca_buy_time).days

           if days_since_buy >= 7:

              market_buy(portfolio,
                         current_price,
                         500,
                         current_time)

              save_portfolio(portfolio)
         

      if strategy == "HYBRID":

              if len(portfolio.active_trades) == 0:

                 if swing_entry_signal(row):
                     open_swing_trade(
                                     portfolio,
                                     row["Close"],
                                     row["ATR"]
                               )
                     save_portfolio(portfolio)

      manage_active_trades(
                         portfolio,
                         row["Close"],
                         row.name,
                         row["ATR"]
                        )
      save_portfolio(portfolio)

      initial_capital = config["initial_capital"]

      current_time = row.name

      value = (

          portfolio.cash

          +

          portfolio.total_btc() * current_price

      )

    


      if portfolio_stop(

              value,

              initial_capital):

          print()

          print("PORTFOLIO STOP TRIGGERED")

         

# Save updated portfolio
      save_portfolio(portfolio)

      portfolio_value = (portfolio.cash +
      portfolio.total_btc() * current_price)

      save_portfolio_history(

      current_time,

      portfolio_value,

      current_price,

      portfolio.cash,

      portfolio.total_btc()

                          )

      status = f"""BTC Agent Status

             Price: ${current_price:.2f}

             Regime: {regime}

             Strategy: {strategy}

             Portfolio: ${portfolio_value:.2f}

             Cash: ${portfolio.cash:.2f}

             BTC: {portfolio.total_btc():.6f}
                 """

      send_message(status)

      print("Trading cycle complete.")

    except Exception as e:

        print("ERROR:", e)