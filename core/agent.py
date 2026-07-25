import json
from .llm_agent import ask_agent
from .conversation import add_message, clear_messages
from .tool_dispatcher import execute_tool
from .logs import log_event
from .llm_agent import _parse_json_response
from .guardrails import is_off_topic


def run_agent(user_prompt):

    clear_messages()

    add_message("user", user_prompt)

    if is_off_topic(user_prompt):

       return """I'm a Bitcoin trading assistant.

                I can only help with:
               • Portfolio
               • BTC trades
               • Profit & Loss
               • Market analysis
               • Technical indicators
               • Trading strategies
               • Orders
               • Risk management"""
    while True:

       
       response = ask_agent()
       print(response)
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
       
       add_message("user",
            json.dumps(
    {
        "tool_result_for": data["tool"],
        "result": result
    },
    default=str )
            )
    



