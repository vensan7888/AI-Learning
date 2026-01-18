import subprocess
import requests
import time
import ollama
from ollama._types import ResponseError

OLLAMA_HOST = "http://127.0.0.1:11434"

class LLM_Util:
    def __init__(self, modelName):
        print("LLM_Util Initialised for:: ", modelName)
        self._modelName = modelName
        self._start_ollama(modelName)

    def _ensure_model(self, model_name: str):
        try:
        # Try running simple info request to see if model exists
            ollama.show(model_name)
            print(f"✅ Model '{model_name}' is already available.")
            return True
        except ResponseError:
            print(f"⬇️ Pulling model '{model_name}'...")
            ollama.pull(model_name)
            print(f"✅ Model '{model_name}' pulled successfully.")
            return True

    def _ensure_ollama_running(self):
        """Check if Ollama is running, if not try to start it."""
        try:
            requests.get(f"{OLLAMA_HOST}/api/tags", timeout=2)
            print("✅ Ollama is running.")
            return True
        except requests.exceptions.ConnectionError:
            print("⚠️ Ollama is not running, trying to start it...")
            try:
            # Start Ollama server
                subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                time.sleep(3)  # wait a bit for it to start
            # Retry connection
                requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
                print("🚀 Ollama started successfully.")
                return True
            except Exception as e:
                print(f"❌ Failed to start Ollama: {e}")
                return False

    def _start_ollama(self, model):
        return self._ensure_ollama_running() and self._ensure_model(model_name=model)
    
    def ask(self, query, images=None):
        messages=[{"role": "user", "content": query}]
        if images:
            messages = [{"role": "user", "content": query, "images": images}]
            
        response = ollama.chat(model=self._modelName, messages=messages)
        return response['message']['content']

# Example usage
#if __name__ == "__main__":
#    reply = ask_ollama("mistral", "Hello, what’s up?")#ask_ollama("llama3.2", "Hello, what’s up?")
#    print("Ollama:", reply)
