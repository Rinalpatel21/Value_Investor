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
from decision_engine import make_decision
from llm_agent import _parse_json_response

def run_agent(user_prompt):

    clear_messages()

    add_message("user", user_prompt)

    while True:

       
       response = ask_agent()
       add_message("assistant", response)

       try:
          data = _parse_json_response(response)

       except json.JSONDecodeError:
          print("LLM returned:")
          print(response)
          return response

       if data.get("done"):

          add_message("assistant", data["answer"])

          return data["answer"]

       try:
          result = execute_tool(data)
       except Exception as e:
          return f"Tool execution failed: {e}"

       log_event({"prompt": user_prompt,
                  "tool": data,
                 "result": json.loads(json.dumps(result, default=str))})
       
       add_message("tool",
                   json.dumps(
        {
            "tool": data["tool"],
            "result": result
        },
        default=str )
                   )
    




def run_trading_agent(market_state):

    return make_decision(
        market_state,
        execute=True
    )