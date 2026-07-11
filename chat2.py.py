from agent import run_agent

import streamlit as st

from agent import run_agent

print("="*50)

print("BTC AI Assistant")

print("="*50)

while True:

  st.title("AI Trading Assistant")

  question = st.chat_input("Ask something...")

  if question:

     answer = run_agent(question)

     st.chat_message("user").write(question)

     st.chat_message("assistant").write(answer)

  if question == "exit":

     break

  answer = run_agent(question)

  print("\nAI:")

  print(answer)