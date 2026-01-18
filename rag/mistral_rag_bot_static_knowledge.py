from llama_cpp import Llama
from RAG_Static_Knowledge import StaticKnowledge
from pathlib import Path

# Note: This application will work only with Static knowledge base from the given directory.
# Language model's knowledge is discarded.
class MistralBot:

    def __init__(self, knowledgeDir):
        self._knowledge = StaticKnowledge()
        # Load knowledge from given folder, else will be read from default folder
        # decide the document to be stored based on valid logic
        # either by using traditional database or by any other means. 
        # else knowledge base won't be able to avoid duplicates
        # self._knowledge.load(knowledgeDir)
        # Path to your GGUF model
        model_path = "/Users/Work/Documents/AgentTransformer/mistral-7b_model.Q4_K_M.gguf"
        # Load model
        self._llm = Llama(
            model_path=model_path,
            n_threads=8,      # adjust based on your CPU cores
            n_ctx=7168,       # context size 91490
            verbose=True      # prints per-token timing
        )
        

    def chat(self):
        
        print("=== Mistral 7B - RAG Chatbot ===")
        print("Type 'exit' to quit.")
        
        while True:
            user_input = input("\nYou: ")
            if user_input.lower() in ["exit", "quit"]:
                print("Exiting chatbot. Bye!")
                break
                
            # 1: Retrieve matching docs by setting count
            retrieved = self._knowledge.retrieve(user_input, k=1)
            # 2: Retrieve all matching docs
            #retrieved = retrieve(user_input)
            if retrieved == "" or retrieved == None: 
                print(f"Assistant: No relevant news found.")
                continue
            context = retrieved
            print(f"\nRetrived:: {context}\n")
            # Build prompt
            prompt = f"Context:\n{context}\nUser: {user_input}\nAssistant:"
            
            # Generate response
            output = self._llm(
                prompt,
                max_tokens=500,
                stop=["\nUser:", "\nAssistant:"]
            )
            print(f"Response: {output}")
            response = output["choices"][0]["text"]
            print(f"Assistant: {response}")

if __name__ == "__main__":
    currentDir = Path.cwd()
    # Default Directory with in project, change it for a different path
    knowledgePath = f"{currentDir}/RAG_Static_Knowledge/Static_Knowledge"
    bot = MistralBot(knowledgePath)    
    bot.chat()