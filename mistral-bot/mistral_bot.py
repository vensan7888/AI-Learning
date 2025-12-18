# Install llama-cpp-python if not installed
# pip install llama-cpp-python

from llama_cpp import Llama
from datetime import datetime
import requests

# Path to your GGUF model
MODEL_PATH = "/Users/Work/Documents/AgentTransformer/mistral-7b_model.Q4_K_M.gguf"

# Load model
llm = Llama(
    model_path=MODEL_PATH,
    n_threads=7,      # adjust based on your CPU cores
    n_ctx=10240,       # context size
    verbose=True      # prints per-token timing
)

def printTime():
    now = datetime.now()
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
    print(f"\nCurrent Date and Time (YYYY-MM-DD HH:MM:SS): {formatted_time}\n")

def chat():
    print("=== Mistral 7B Chatbot ===")
    print("Type 'exit' to quit.")

    today = datetime.now().strftime("%Y-%m-%d")
    aboutMe = """
        Sandeep is A Software engineering leader well experienced in Mobile application development,
        AI Engineering, Architecture, team management. Born on 07-08-1988, in village name dippakayalapadu near koyalagudem town.
        Graduated from Prathyusha Institute of technology & management (PITAM) affiliated to Anna University in the year 2009.
        First job as junior iOS application developer at Buddies Infotech in santhome, chennai. Second job as Software Engineer at Xinthe Technologies in Vishakapatnam (Vizag).
        Authered a youtube channel "The Art of Engineering Efficiency" to educate young & experienced engineers to excel in Software development career.
        """

    # Append user input to history
    history = f"""
        User: "What is your purpose?
        Assistant: My purpose is to assist you in any way I can
        User: About Sandeep
        Assistant: {aboutMe}
        User: "What is Today's date?
        Assistant: {today}
    """
    while True:
        user_input = input("\nYou: ")
        printTime()
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting chatbot. Bye!")
            break
        
        # Build augmented prompt with Custom Context as additional knowledge base to LLM.
        prompt = f"Context: {history}\nUser: {user_input}\nAssistant:"
        # Plain prompt to interact with LLM
        #prompt = f"\nUser: {user_input}\nAssistant:"

        output = llm(
            prompt,
            max_tokens=500,
            stop=["\nUser:", "\nAssistant:"]
        )
        print(f"Response: {output}")
        response = output["choices"][0]["text"]
        printTime()
        print(f"Assistant: {response}")
        
        # Update history with assistant response
        history += f"\nUser: {user_input}"
        history += f"\nAssistant: {response}"

if __name__ == "__main__":
    chat()
