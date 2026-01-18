# Retrieval-Augmented Generation (RAG) - Practical Understanding

### *Build Your Own RAG AI System (read local documents, fetch data from API) on a Laptop - No API Keys, No Limits, Full Privacy*

The goal of this project is **learning by building**, not theory-heavy explanations.

---

## ⭐ What You Will Learn

- How RAG works as a **system**, not just a prompt trick
- How documents are:
  - Chunked
  - Embedded
  - Stored in a vector database (e.g., FAISS)
- How a user query retrieves relevant context
- How retrieved data is injected into an LLM prompt
- How RAG helps reduce **hallucinations**
- Practical examples you can run locally

Perfect for beginners & AI enthusiasts.
---

## 🏗️ High-Level RAG Architecture

Documents -> Chunking -> Embeddings -> Vector DB (FAISS) User Query -> Embedding -> Similarity Search -> Relevant Context -> LLM -> Final Answer

# 🧩 **System Requirements**

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

## 🛠️ Tech Stack (Example)

- **Python**
- **FAISS** (Vector Database)
- **LLM** (Local or API-based)
- **Embedding Model**

# 💬 **Demo 1: Build RAG pipeline using local document Demo**

In this demo:

* RAG bot will load the document to vector DB from given directory.
* Concepts included are converting document to embeddings, update the same in vector DB.
* Will answer to the queries from the Vector DB upon user's input.
* Follow the instructions mentioned in code `mistral_rag_bot_static_knowledge.py`.

```
python mistral_rag_bot_static_knowledge.py 
```
---

# 💬 **Demo 2: Build RAG pipeline using remote knowledge Demo**

In This demo:

* Fetch the knowledge through API, save them in Vector DB
* Will answer to the queries from the Vector DB upon user's input.

```
python ollama_rag_bot_dynamic_knowledge.py
```
---

# 💬 **Demo 3: Build RAG pipeline with Persistent knowledge Demo**

In This demo:

* Share the data across different sessions of the application.
* Enhance `Demo 1` bot with Persistent data setup
* Avoid data loading upon each session of the application.

```
python mistral_rag_bot_static_knowledge.py
```
---

This episode sets the foundation for:

### RAG AI
### AI orchestration frameworks (LangChain / LangGraph)

---
