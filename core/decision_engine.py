from .llm_agent import get_ai_decision
from .tool_dispatcher import execute_tool
from .logs import log_event
from .guardrails import validate_trade


def make_decision(
    market_context,
    ai_summary,
    portfolio,
    current_time,
    execute=True
):
    """
    Gets an AI decision and optionally executes it.
    """

    decision = get_ai_decision(
        market_context,
        ai_summary
    )

    result = None

    if execute:

        approved, reason = validate_trade(
            decision,
            market_context
        )

        if approved:

            result = execute_tool(
                decision,
                portfolio=portfolio,
                price=market_context["price"],
                current_time=current_time
            )

        else:

            result = {
                "status": "blocked",
                "reason": reason
            }

    log_event({
        "market_context": market_context,
        "ai_summary": ai_summary,
        "decision": decision,
        "execution": result
    })

    return decision, result


def get_ai_recommendation():

    from .market_context import build_market_context
    # Build the context here if you use this function, or remove it if unused.
    raise NotImplementedError("Update this function to use build_market_context().")