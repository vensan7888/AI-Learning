# 📘 Run Mistral 7B Locally Using LLaMA.cpp (.gguf)**

### *Build Your Own ChatGPT-like System on a Laptop — No API Keys, No Limits, Full Privacy*

This repository guides you through running **Mistral 7B** completely **offline**, using **llama.cpp** and **GGUF models**, on a standard laptop (tested on **32GB RAM**).

---

## ⭐ Overview

This repo gives you:

* 🎯 Clear startup instructions
* 📥 How to download quantized language model in **GGUF**.
* ⚙️ Using **llama.cpp** locally
* 💬 Chat mode (ChatGPT-like)
* 🧠 Cognitive memory
* 🧪 Python example

Perfect for beginners & AI enthusiasts.

---

# 🚀 1. **Introduction**

Running large language models was once limited to tech giants…
But thanks to **llama.cpp**, you can now run state-of-the-art LLMs **locally**, even on CPUs.

This repo documents how I built a **ChatGPT-like assistant locally** using **Mistral 7B**, with:

* No OpenAI keys
* No API limits
* No external dependencies
* Complete privacy

---

# 🧩 2. **System Requirements**

### **Minimum**

* 16 GB RAM
* macOS / Windows / Linux

### **Recommended**

* **32 GB RAM**
* Python 3.10+
* Git
* CMake
* huggingface

---

# 📥 3. **Installation Steps**

install hugging face python package 

```
pip install huggingface_hub
```

login to huggingface (After running it, it will prompt you to enter your Hugging Face access token. You can get your token from https://huggingface.co/settings/tokens) <token>
```
huggingface-cli login
```
 
Execute below command to download the .gguf version of mistral 7b model
```
wget https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf -O /myDirectory/mistral-7b_model.Q4_K_M.gguf
```

Clone the official repository of llama.cpp:

```
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
```
### Build (macOS / Linux)

```
mkdir build
cd build
cmake ..
cmake --build . --config Release
```

### Build (Windows)

```
cmake -B build
cmake --build build --config Release
```

# 💬 4. **Run Your First Prompt**

You will now be able to run below command with a prompt:

```
llama.cpp/build/bin/llama-cli -m /myDirectory/mistral-7b_model.Q4_K_M.gguf -p "Prompt text" --gpu-layers 35
```

---

# 💬 5. **Run in Chat Mode (ChatGPT-like)**

Run mistral_bot.py example demonstrating 

### Simple chat
### Setting Context
### Enabling Cognitive memory. 

```
python mistral_bot.py
```

Now type continuously.
Like ChatGPT, but offline.

---

# 🧠 6. **Add Cognitive Memory**

Memory works by **adding conversation history** back into the context window.

Basic structure:

```
User: Hi
Assistant: Hello!

User: What is AI?
Assistant: ...
```

Append and re-send full history each time.

---

# ⚡ 7. **Performance Tips**

### For faster inference:

* Use `Q4_K_M` or `Q5_K_M`
* Reduce context from 4096 → 2048
* Close heavy apps
* Enable Metal on macOS:

Build llama cpp with Metal

---

# 🛠 8. **Troubleshooting**

| Issue                   | Fix                         |
| ----------------------- | --------------------------- |
| “Killed” during loading | Use lower quant (Q4).       |
| Slow response           | Reduce `--ctx-size`.        |
| Model not found         | Check path & filename.      |
| Python errors           | Upgrade `llama-cpp-python`. |

---

# 🏁 **Conclusion**

After completing this setup, you now have:

✔ A completely offline Mistral 7B
✔ Zero API keys or limits
✔ ChatGPT-style chat
✔ Inference, context, & memory
✔ Python integration

This is a powerful base for:

* AI agents
* RAG systems
* Custom chatbots
* Developer tools
* Offline assistants

---
