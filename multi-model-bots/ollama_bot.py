from run_ollama import LLM_Util 
import ollama
import requests
# Regex
import re
from datetime import date
import json

class OllamaBot:
    
    def __init__(self):
        model = "Sitara"#"llama3.2"
        self.llm = LLM_Util(model)

    def _askLLM(self, query):
        return self.llm.ask(query)

    def chat(self):
        print("=== Agent Chatbot ===")
        print("Type 'exit' to quit.")
        history = ""
        while True:
            print("Waiting for User Input")
            user_input = input("\nUser: ")
            if user_input.lower() in ["exit", "quit"]:
                break
            answer = self._askLLM(user_input)
            print(f"\nAssistant: {answer}\n")        

if __name__ == "__main__":
    bot = OllamaBot()
    bot.chat()
    