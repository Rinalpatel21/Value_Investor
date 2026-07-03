import json

from llm_agent import ask_agent
from llm_agent import explain_tool_result

from conversation import (
    add_message,
    get_messages,
    clear_messages
)

from tool_dispatcher import execute_tool

from logs import log_event


def run_agent(user_prompt):

    clear_messages()

    add_message("system", user_prompt)

    while True:

        response = ask_agent()

        print(response)

        add_message("assistant",
                    json.dumps(
        {
            "tool_result": {
                "tool": data["tool"],
                "result": result
            }
        }
    )
)

        try:

            data = json.loads(response)

        except:

            return response

        if data.get("done"):

            return data["answer"]

        result = execute_tool(data)

        log_event({"prompt": user_prompt,

                   "tool": data,

                   "result": result})

        print(result)

        add_message(
            "user",
            f"Tool Result:\n{result}"
        )


from llm_agent import get_ai_decision

def run_trading_agent(market_state):

    decision = get_ai_decision(market_state)

    result = execute_tool(
        decision,
        portfolio=market_state["portfolio"],
        price=market_state["price"],
        current_time=market_state["current_time"]
    )

    log_event({ "market_state": market_state,

                "decision": decision,

                 "execution": result})

    return decision, result