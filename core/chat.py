from core.agent import run_agent

print("="*50)

print("BTC AI Assistant")

print("="*50)

while True:

    question = input("\nYou: ")

    if question == "exit":

        break

    answer = run_agent(question)

    print("\nAI:")

    print(answer)