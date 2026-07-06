from llm_agent import get_ai_decision
from tool_dispatcher import execute_tool
from logs import log_event


def make_decision(
    market_state,
    portfolio=None,
    current_time=None,
    execute=False
):
    """
    Gets an AI decision and optionally executes it.
    """

    decision = get_ai_decision(market_state)

    result = None

    if execute:

        result = execute_tool(
            decision,
            portfolio=portfolio,
            price=market_state["price"],
            current_time=current_time
        )

    log_event({
        "market_state": market_state,
        "decision": decision,
        "execution": result
    })

    return decision, result


def get_ai_recommendation():

    from tools import get_trading_context

    context = get_trading_context()

    decision, _ = make_decision(
        context,
        execute=False
    )

    return decision