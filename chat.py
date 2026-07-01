
from llm_agent import ask_agent

print("="*50)

print("BTC AI Assistant")

print("Type exit to quit")

print("="*50)


while True:

    prompt = input("\nYou: ")

    if prompt.lower() == "exit":

        break

    response = ask_agent(prompt)

    print()

    print("AI:")

    print(response)

    # python chat.py