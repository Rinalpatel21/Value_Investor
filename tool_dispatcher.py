from order_executor import market_buy
from order_executor import market_sell

from tools import (
    get_portfolio,
    get_recent_orders
)

TOOLS = {

    "market_buy": market_buy,

    "market_sell": market_sell,

    "get_portfolio": get_portfolio,

    "get_recent_orders": get_recent_orders

}

def execute_tool(

        tool_name,

        **kwargs

):

    if tool_name not in TOOLS:

        raise ValueError(

            f"Unknown tool {tool_name}"

        )

    return TOOLS[tool_name](**kwargs)