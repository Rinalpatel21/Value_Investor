import os
import json

from groq import Groq
from assistant_prompt import ASSISTANT_PROMPT
from prompt import SYSTEM_PROMPT
from conversation import add_message
from conversation import get_messages

client = Groq(
    api_key=os.environ["GROQ_API_KEY"],
)

MODEL = "llama-3.3-70b-versatile"


def _parse_json_response(content):
    cleaned = content.strip()

    if cleaned.startswith("```"):
        cleaned = cleaned.replace("```json", "").replace("```", "").strip()

    return json.loads(cleaned)


def get_ai_decision(market_state):

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": str(market_state)
            }
        ]
    )

    decision = response.choices[0].message.content

    print(decision)

    parsed = _parse_json_response(decision)

    if "decision" not in parsed:
        raise ValueError("LLM response missing decision object.")

    if "tool" not in parsed["decision"]:
        raise ValueError("LLM decision missing tool name.")

    return parsed


def ask_agent():

    messages = [
        {
            "role": "system",
            "content": ASSISTANT_PROMPT
        }
    ]

    messages.extend(get_messages())

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages
    )

    answer = response.choices[0].message.content

    return answer


def explain_tool_result(user_question, tool_result):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": ASSISTANT_PROMPT
            },
            {
                "role": "user",
                "content": user_question
            },
            {
                "role": "assistant",
                "content": "I executed the requested tool."
            },
            {
                "role": "user",
                "content": f"Tool Result:\n{tool_result}\n\nExplain this to me."
            }
        ]
    )

    return response.choices[0].message.content