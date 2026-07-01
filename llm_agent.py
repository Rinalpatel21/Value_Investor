import os
from openai import OpenAI
from assistant_prompt import ASSISTANT_PROMPT
from prompt import SYSTEM_PROMPT

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
)

def get_ai_decision(market_state):

    response = client.chat.completions.create(

        model="deepseek-ai/DeepSeek-V3:novita",

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

    

    import json

    decision = response.choices[0].message.content

    print(decision)

    return json.loads(decision)


def ask_agent(question):
    response = client.chat.completions.create(

    model="deepseek-ai/DeepSeek-V3:novita",

    messages=[

        {

            "role":"system",

            "content":ASSISTANT_PROMPT

        },

        {

            "role":"user",

            "content":question

        }

    ]

)

    return response.choices[0].message.content