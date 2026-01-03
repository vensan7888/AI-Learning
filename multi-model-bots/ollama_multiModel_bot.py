from run_ollama import LLM_Util 
import ollama

class OllamaMultiModelBot:
    
    def __init__(self):
        creativeModelName = "mistral:7b"
        reasoningModelName = "llama3.2"
        self.creativellm = LLM_Util(creativeModelName)
        self.reasoningllm = LLM_Util(reasoningModelName)

    def _askLLM(self, query, llm):
        return llm.ask(query)

    def chat(self):
        print("=== Agent Chatbot ===")
        print("Type 'exit' to quit.")

        while True:
            print("Waiting for User Input")
            user_input = input("\nUser: ")
            if user_input.lower() in ["exit", "quit"]:
                break
            # 1 step:
            creativeAnswer = self._askLLM(user_input, self.creativellm)
            print(f"creativeAnswer: \n{creativeAnswer}\n")
            # 2 step:
            reasoningInput = f"Evaluate & respond with most relavant information from {creativeAnswer}"
            reasoningAnswer = self._askLLM(reasoningInput, self.reasoningllm)
            print(f"\nreasoningAnswer: \n{reasoningAnswer}\n")
        

if __name__ == "__main__":
    bot = OllamaMultiModelBot()
    bot.chat()
