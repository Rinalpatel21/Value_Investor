from .market_data import download_btc_data
from .order_executor import market_buy, market_sell
from .portfolio_storage import load_portfolio, save_portfolio
from .tools import get_last_trade, get_performance, get_portfolio, get_recent_orders, get_last_trade, get_profit_loss, get_trading_context
from .tools import get_performance, get_market_summary
from .indicators import add_indicators
from .regime import detect_market_regime
from .strategy import select_strategy


TOOLS = {

         "market_buy": market_buy,

         "market_sell": market_sell,

         "hold": None,

         "get_portfolio": get_portfolio,

         "get_recent_orders": get_recent_orders,

         "get_performance": get_performance,

         "get_market_summary": get_market_summary,

         "get_last_trade": get_last_trade,

         "get_profit_loss": get_profit_loss,

         "get_trading_context": get_trading_context,

         

        
        

}


TOOL_ALIASES = {
    "execute_dca_buy": "market_buy",
    "buy_bitcoin": "market_buy",
    "sell_bitcoin": "market_sell"
}


def _normalize_trade_request(tool_request):
    if "decision" in tool_request:
        return tool_request["decision"]

    return tool_request


def _get_default_trade_context(context):
    if all(key in context for key in ["portfolio", "price", "current_time"]):
        return context

    df = download_btc_data()
    df = add_indicators(df)
    row = df.iloc[-1]

    context["portfolio"] = load_portfolio(10000)
    context["price"] = float(row["Close"])
    context["current_time"] = row.name

    return context


def execute_tool(tool_request, **context):

    tool_request = _normalize_trade_request(tool_request)

    tool_name = TOOL_ALIASES.get(tool_request["tool"], tool_request["tool"])

    if tool_name not in TOOLS:
        raise ValueError(f"Unknown tool: {tool_name}")

    if tool_name == "hold":
        return {"status": "held"}

    if tool_name == "market_buy":

        context = _get_default_trade_context(context)

        amount = float(tool_request.get("amount", 500))
        portfolio = context["portfolio"]

        if portfolio.cash <= 0:
           return {"status": "rejected", "reason": "No cash available"}

        if amount <= 0:
            return {"status": "rejected", "reason": "Buy amount must be positive."}

        if amount > portfolio.cash:
            return {"status": "rejected", "reason": "Buy amount exceeds available cash."}

        result = market_buy(
            portfolio=portfolio,
            price=context["price"],
            amount=amount,
            current_time=context["current_time"]
        )

        save_portfolio(portfolio)

        return result
    
    

    elif tool_name == "market_sell":

        context = _get_default_trade_context(context)

        quantity = float(tool_request["quantity"])
        portfolio = context["portfolio"]

        if quantity <= 0:
            return {"status": "rejected", "reason": "Sell quantity must be positive."}

        if quantity > portfolio.total_btc():
            return {"status": "rejected", "reason": "Sell quantity exceeds BTC holdings."}

        result = market_sell(
            portfolio=portfolio,
            quantity=quantity,
            price=context["price"],
            current_time=context["current_time"]
        )

        save_portfolio(portfolio)

        return result

    else:

        return TOOLS[tool_name]()
    

def get_market_summary():

    df = download_btc_data()

    df = add_indicators(df)

    row = df.iloc[-1]

    regime = detect_market_regime(row)

    strategy = select_strategy(regime)

    return {

        "price": float(row["Close"]),

        "RSI": float(row["RSI"]),

        "EMA50": float(row["EMA50"]),

        "SMA50": float(row["SMA50"]),

        "ATR": float(row["ATR"]),

        "regime": regime,

        "strategy": strategy

    }
