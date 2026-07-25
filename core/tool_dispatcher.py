from .market_data import download_btc_data
from .tools import buy_bitcoin, sell_bitcoin, show_portfolio, show_orders, show_trade_history, show_market_context, show_news, show_ai_report, get_market_summary
from .indicators import add_indicators
from .regime import detect_market_regime
from .strategy import select_strategy


TOOLS = {
            "market_buy": buy_bitcoin,

            "buy_bitcoin": buy_bitcoin,

            "market_sell": sell_bitcoin,
            
            "sell_bitcoin": sell_bitcoin,

            "show_portfolio": show_portfolio,

            "show_orders": show_orders,

            "show_trade_history": show_trade_history,

            "show_market_context": show_market_context,

            "show_news": show_news,

            "show_ai_report": show_ai_report,

            "get_market_summary": get_market_summary,

            

}


TOOL_ALIASES = {

    "buy_bitcoin": "market_buy",
    "sell_bitcoin": "market_sell",

    "show_portfolio": "show_portfolio",

    "portfolio":"show_portfolio",

    "recent_orders":"show_orders",

    "orders":"show_orders",

    "show_market_context":"show_market_context"

}

def execute_tool(tool_request):

    tool_name = tool_request["tool"]

    tool_name = TOOL_ALIASES.get(tool_name, tool_name)
    

    if tool_name not in TOOLS:
        raise Exception(f"Unknown tool: {tool_name}")

    fn = TOOLS[tool_name]

    args = tool_request.get("args", {})

    return fn(**args)

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
