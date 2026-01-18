from common import LLM_Util 
import ollama
from RAG_Dynamic_Knowledge import DynamicKnowledge

class OllamaBot:
    
    def __init__(self):
        self._knowledge = DynamicKnowledge()
        # Set model name supported by ollama
        model = "llama3.2"
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
            
            # **** Retrive from Knowledge ****
            # 1: Retrieve matching docs by setting count
            retrieved = self._knowledge.retrieve(user_input, k=3)
            # 2: Retrieve all matching docs
            #retrieved = self._knowledge.retrieve(user_input)
            if retrieved == None or len(retrieved) == 0 : 
                print(f"Assistant: No relevant news found.")
                continue
            context = retrieved
            print(f"\nRetrived:: {context}\n")
            # Build prompt
            prompt = f"""
            Don't add any additional description other than answer, 
            Explain in structural format from context, to answer User's ask.
            
            Context:\n{context}\nUser: {user_input}\nAssistant:
            """
            
            answer = self._askLLM(prompt)
            print(f"\nAssistant: {answer}\n")  

if __name__ == "__main__":
    bot = OllamaBot()
    bot.chat()
    