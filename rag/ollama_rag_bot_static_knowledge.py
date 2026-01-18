from common import LLM_Util 
import ollama
from RAG_Static_Knowledge import StaticKnowledge
from pathlib import Path

class OllamaBot:
    
    def __init__(self, knowledgeDir):
        self._knowledge = StaticKnowledge()
        # Load knowledge from given folder, else will be read from default folder
        # decide the document to be stored based on valid logic
        # either by using traditional database or by any other means. 
        # else knowledge base won't be able to avoid duplicates
        #self._knowledge.load(knowledgeDir)
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
            #retrieved = self._knowledge.retrieve(user_input, k=3)
            # 2: Retrieve all matching docs
            retrieved = self._knowledge.retrieve(user_input)
            if retrieved == None or len(retrieved) == 0 : 
                print(f"Assistant: No relevant news found.")
                continue
            context = retrieved
            print(f"\nRetrived:: {context}\n")
            # Build prompt
            prompt = f"""
            Don't add any additional description other than answer, 
            Explain in detail from context, to answer User's ask.
            
            Context:\n{context}\nUser: {user_input}\nAssistant:
            """
            
            answer = self._askLLM(prompt)
            print(f"\nAssistant: {answer}\n")  

if __name__ == "__main__":
    currentDir = Path.cwd()
    # Default Directory with in project, change it for a different path
    knowledgePath = f"{currentDir}/RAG_Static_Knowledge/Static_Knowledge"
    bot = OllamaBot(knowledgePath)
    bot.chat()
    