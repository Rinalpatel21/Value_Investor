


# Full Test
from market_data import download_btc_data
from indicators import add_indicators

from portfolio import Portfolio

from dca import execute_dca_buy
from dca_atr import (
    atr_opportunity_buy,
    dca_protective_sell
    
)

from regime import detect_market_regime
from strategy import select_strategy

from swing import (
    swing_entry_signal,
    open_swing_trade
)

from atr_sell import manage_active_trades

from risk_manager import portfolio_stop

from performance import calculate_metrics

from config_loader import load_config

config = load_config()


########################################
# LOAD DATA
########################################

df = download_btc_data()



df = add_indicators(df)


########################################
# INITIALIZE PORTFOLIO
########################################

initial_capital = config["initial_capital"]

portfolio = Portfolio(initial_capital)

portfolio_values = []

trend_count = 0
range_count = 0
panic_count = 0


########################################
# BACKTEST LOOP
########################################

for i in range(0, len(df)):

    row = df.iloc[i]

    current_price = row["Close"]

    current_time = row.name

    atr = row["ATR"]


    ####################################
    # MARKET REGIME
    ####################################

    regime = detect_market_regime(row)

    if regime == "TRENDING":

        trend_count += 1

    elif regime == "RANGING":

        range_count += 1

    else:

        panic_count += 1


    ####################################
    # STRATEGY SELECTION
    ####################################

    strategy = select_strategy(regime)


    ####################################
    # FIRST BUY
    ####################################

    if portfolio.last_dca_buy_price is None:

        execute_dca_buy(
            portfolio,
            current_price,
            500,
            current_time
        )

        continue


    ####################################
    # DCA SECTION
    ####################################
    
    
    if strategy in ["HYBRID", "DCA_ONLY"]:

        drop_pct = (portfolio.last_dca_buy_price - current_price) / portfolio.last_dca_buy_price

        # Regular DCA Buy

        if drop_pct >= config["drop_3"]:

          amount = config["dca_buy_3"]

        elif drop_pct >= config["drop_2"]:

            amount = config["dca_buy_2"]

        elif drop_pct >= config["drop_1"]:

           amount = config["dca_buy_1"]

        else:

           amount = 0

    if amount > 0:

           execute_dca_buy(
             portfolio,
             current_price,
             amount,
             current_time
                          )


        # ATR Opportunity Buy

           atr_opportunity_buy(

            portfolio,

            current_price,

            current_time,

            atr

        )


        # DCA Protective Sell

           dca_protective_sell(

            portfolio,

            current_price,

            atr

        )


    ####################################
    # SWING TRADES
    ####################################

    if strategy in ["HYBRID", "SWING_ONLY"]:

      allow_trade = True

    ##################################
    # Cooldown check
    ##################################

      if portfolio.last_trade_time is not None:

            time_since_last_trade = (

            current_time

            -

            portfolio.last_trade_time

        )

            if time_since_last_trade.total_seconds() < 21600:

              allow_trade = False
 
    ##################################
    # Open trade
    ##################################

      if strategy == "HYBRID":

          if len(portfolio.active_trades) == 0:

            if portfolio.last_trade_time is None or (
            current_time -
            portfolio.last_trade_time
            ).total_seconds() >= 21600:

             if swing_entry_signal(row):

                open_swing_trade(
                    portfolio,
                    current_price,
                    atr, 
                    current_time
                )
    ####################################
    # MANAGE ACTIVE TRADES
    ####################################
    manage_active_trades(
             portfolio,
             current_price,
             current_time,
             atr)

    ####################################
    # PORTFOLIO VALUE
    ####################################

    value = (

        portfolio.cash

        +

        portfolio.total_btc() * current_price

    )

    portfolio_values.append(value)


    ####################################
    # PORTFOLIO STOP
    ####################################

    if portfolio_stop(

            value,

            initial_capital):

        print()

        print("PORTFOLIO STOP TRIGGERED")

        break


########################################
# PERFORMANCE METRICS
########################################

sharpe, max_dd, win_rate = calculate_metrics(

    portfolio_values,

    portfolio.closed_trades

)


########################################
# RESULTS
########################################

print()

print("========== RESULTS ==========")

print()

print("Final Portfolio Value =", round(portfolio_values[-1], 2))

print()

print("Sharpe Ratio =", round(sharpe, 3))

print()

print("Max Drawdown =", round(max_dd * 100, 2), "%")

print()

print("Win Rate =", round(win_rate * 100, 2), "%")

print()

print("Closed Trades =", len(portfolio.closed_trades))

print()

print("Cash Remaining =", round(portfolio.cash, 2))

print()

print("BTC Holdings =", round(portfolio.total_btc(), 6))


print()

print("========== MARKET REGIMES ==========")

print()

print("TRENDING =", trend_count)

print()

print("RANGING =", range_count)

print()

print("PANIC =", panic_count)

