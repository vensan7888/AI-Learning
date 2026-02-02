
---

# 🚀 LangChain & LangGraph Workflow Demos

This repository is a hands-on learning project designed to provide **deep, practical understanding of LangChain and LangGraph workflows** through real-world applications.

The goal is to help developers understand **how modern LLM application pipelines are built**, how workflows differ between LangChain and LangGraph, and when to use each approach.

---

## 🎯 Project Objectives

* Understand core **LangChain workflow concepts**
* Learn how to design **stateful and persistent LLM applications**
* Explore **LangGraph workflow patterns** for complex, cyclic, and state-driven flows
* Highlight **key differences between LangChain and LangGraph**
* Build production-style AI applications using best practices

---

## 📦 Applications Included

### 1️⃣ LangChain Document Search Application

A Retrieval-Augmented Generation (RAG) based document search system.

**Key Concepts Covered:**

* Document loading
* Chunking & text splitting
* Embeddings generation
* Vector storage (FAISS)
* Similarity search
* Context injection into LLM prompts

**Workflow:**

```
Documents
 → Chunking
 → Embeddings
 → Vector DB (FAISS)
 → User Query → Embedding
 → Similarity Search
 → Relevant Context
 → LLM
 → Final Answer
```

---

### 2️⃣ LangChain Conversation Bot Application

A simple conversational chatbot built using LangChain.

**Key Concepts Covered:**

* Prompt templates
* Conversation memory
* LLM chains
* Basic conversational context handling

---

### 3️⃣ LangChain Persistent Conversation Bot Application

An enhanced conversational bot with **persistent memory across sessions**.

**Key Concepts Covered:**

* Persistent memory storage
* Session-based conversations
* Long-term context retention
* Stateful chatbot design

---

### 4️⃣ Content Writer Application with LangChain Workflow

A content generation pipeline using LangChain’s linear and tool-based workflow model.

**Key Concepts Covered:**

* Multi-step chains
* Tool calling
* Prompt chaining
* Sequential content generation
* Workflow orchestration with LangChain

---

### 5️⃣ Content Writer Application with LangGraph Workflow

A content generation system built using **LangGraph’s graph-based workflow engine**.

**Key Concepts Covered:**

* Graph-based execution
* Nodes and edges
* State management
* Cycles and conditional flows
* Advanced workflow orchestration

---

## 🔍 LangChain vs LangGraph — Key Differences

| Feature          | LangChain                       | LangGraph                              |
| ---------------- | ------------------------------- | -------------------------------------- |
| Workflow Style   | Linear / Chain-based            | Graph-based                            |
| Control Flow     | Mostly sequential               | Cyclic, conditional, and branching     |
| State Management | Basic / manual                  | First-class state handling             |
| Best For         | Simple to medium pipelines      | Complex, multi-step agent workflows    |
| Cycles & Loops   | Limited                         | Native support                         |
| Use Cases        | RAG, chatbots, simple pipelines | Agents, planners, multi-step reasoning |

---

## 🧠 What You’ll Learn

* How LangChain chains are constructed and executed
* How LangGraph models workflows as graphs
* How state flows through LangGraph nodes
* When to choose LangChain vs LangGraph
* How to design scalable LLM application architectures

---

## 🛠 Tech Stack

* **LangChain**
* **LangGraph**
* **FAISS Vector Database**
* **Ollama (Local LLMs)**
* **Python**

---

## 🎓 Who This Is For

* Developers learning LLM application development
* Engineers exploring RAG systems
* AI practitioners building conversational agents
* Anyone wanting a practical understanding of LangChain & LangGraph
* Teams evaluating workflow orchestration patterns for AI systems

---

## 🚀 Getting Started

1. Clone the repository
2. Install dependencies
3. Configure LLM providers (Ollama / OpenAI)
4. Run individual applications to explore workflows
5. Compare LangChain vs LangGraph implementations

---

## 📌 Final Note

This project is built for **learning by building**. Each application is intentionally simple yet realistic - so you can clearly see how workflows evolve from basic chains to advanced graph-based systems.

If you’re serious about mastering modern LLM application architecture, this repo is a great practical foundation. 💡
