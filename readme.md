# 🤖 AI/GENAI - Agentic AI & AI Agents — Learning Journey

A hands-on learning repository covering **LLMs, LangChain, LangGraph, RAG, AI Agents, Agentic AI, Tool Calling, MCP, and production-oriented AI application development**.

This repository documents my journey from **LLM fundamentals to building practical AI agents and agentic applications** using Python and local/cloud LLMs.

---

## 🚀 About This Repository

The goal of this repository is to learn how to build AI systems that can go beyond simple question-answering.

Instead of only generating text, these systems can:

* Understand user goals
* Reason about tasks
* Decide which tools to use
* Retrieve relevant information
* Execute actions
* Maintain state and memory
* Work through multi-step workflows
* Interact with external tools through MCP
* Evaluate and improve their results

The repository contains learning examples, experiments, reusable components, and complete projects.

---

# 🧠 Technologies & Concepts

## Large Language Models

* LLM fundamentals
* Prompt engineering
* Zero-shot prompting
* Few-shot prompting
* System / user / assistant messages
* Temperature
* Top-K
* Top-P
* Structured output
* Local LLMs with Ollama
* Cloud-based LLM APIs

### Models explored

* Qwen
* Llama
* Gemma
* Other open-source / API-based models

---

# 🔗 LangChain

Topics covered:

* Chat models
* Prompt templates
* Messages
* Output parsers
* Structured output
* Chains
* LCEL
* Document loaders
* Text splitters
* Embeddings
* Vector stores
* Retrievers
* RAG pipelines
* Tools
* Tool calling
* Agents
* Memory
* LangChain integrations

---

# 🕸️ LangGraph

Learning how to build stateful AI workflows using graph-based architectures.

Topics include:

* Graphs
* Nodes
* Edges
* State
* Conditional routing
* Agent loops
* Tool execution
* Checkpoints
* Human-in-the-loop
* Multi-step workflows
* Agent orchestration
* Multi-agent architectures

Example:

```text
                 User
                   |
                   v
              Agent Node
                   |
          +--------+--------+
          |                 |
      Need Tool?          No Tool
          |                 |
          v                 v
      Tool Node         Final Answer
          |
          v
      Observation
          |
          +-------> Agent
```

---

# 📚 Retrieval-Augmented Generation (RAG)

Built and experimented with document-based question-answering systems.

Topics covered:

* Document ingestion
* PDF / TXT / DOCX processing
* Chunking
* Embeddings
* Vector databases
* Similarity search
* Metadata filtering
* Retriever design
* Query transformation
* Query expansion
* Hybrid search
* Reranking
* Cross-encoder reranking
* Context compression
* Multi-document RAG
* Conversational RAG
* RAG evaluation

Basic architecture:

```text
Documents
    |
    v
Document Loader
    |
    v
Text Splitting
    |
    v
Embeddings
    |
    v
Vector Database
    |
    v
Retriever
    |
    v
Relevant Context
    |
    v
LLM
    |
    v
Answer + Sources
```

---

# 🛠️ AI Agents

Learning how AI agents can use tools and perform multi-step tasks.

Topics covered:

* What is an AI Agent?
* Agent vs chatbot
* Agent loop
* Reasoning and action
* Tool selection
* Tool calling
* Agent state
* Memory
* Planning
* Routing
* Multi-step execution
* Error handling
* Retries
* Reflection
* Human-in-the-loop

General agent architecture:

```text
User Goal
    |
    v
Agent
    |
    +------> Decide Action
    |
    v
Select Tool
    |
    v
Execute Tool
    |
    v
Observe Result
    |
    v
Agent
    |
    +------> More Actions?
    |             |
   Yes            No
    |             |
    +------->   Final Answer
```

---

# 🔧 Tool Calling

Learning how LLMs can interact with external functionality.

Examples:

* Calculator
* Date/time
* Database
* File system
* Search
* APIs
* Custom Python functions
* RAG retrieval
* External services

Example:

```text
User
 |
 v
LLM
 |
 | "I need a tool"
 v
Tool Selection
 |
 v
Tool Execution
 |
 v
Tool Result
 |
 v
LLM
 |
 v
Final Response
```

---

# 🔌 Model Context Protocol (MCP)

Learning the fundamentals of **Model Context Protocol (MCP)** and how AI applications can interact with external tools and resources through a standardized protocol.

Topics explored:

* MCP architecture
* MCP client
* MCP server
* MCP tools
* Tool discovery
* Tool execution
* Connecting agents to MCP servers
* Local MCP servers
* Agent + MCP integration

Basic architecture:

```text
                  AI Agent
                     |
                     v
                 MCP Client
                     |
              MCP Protocol
                     |
                     v
                 MCP Server
                /     |      \
               /      |       \
          Tool 1    Tool 2    Tool 3
```

---

# 🧰 Technology Stack

### Programming

* Python

### AI / GenAI

* LangChain
* LangGraph
* RAG
* Ollama
* LLM APIs
* Embeddings

### Agentic AI

* AI Agents
* Tool Calling
* MCP
* Agent Workflows
* Multi-Agent Systems

### Databases

* Chroma
* FAISS
* SQLite
* PostgreSQL

### Backend

* FastAPI

### Frontend

* Streamlit

### Development

* Git
* GitHub
* Python Virtual Environments
* `.env`
* Docker



# 📈 Learning Roadmap

My learning progression is:

```text
LLM Fundamentals
       |
       v
Prompt Engineering
       |
       v
LangChain
       |
       v
RAG
       |
       v
Advanced RAG
       |
       v
LangGraph
       |
       v
Tool Calling
       |
       v
AI Agents
       |
       v
Agentic Workflows
       |
       v
MCP
       |
       v
Multi-Agent Systems
       |
       v
Agent Evaluation
       |
       v
Production AI Applications
       |
       v
Deployment
```


# 🧪 Development Philosophy

The goal of this repository is **not to collect tutorials**.

Every major concept should eventually become a working implementation.

For example:

```text
Learn Tool Calling
       ↓
Build a Tool
       ↓
Connect Tool to Agent
       ↓
Add State
       ↓
Add Error Handling
       ↓
Test Agent
       ↓
Deploy Application
```

The focus is:

> **Learn → Build → Test → Improve → Deploy**

---

# 📊 Beginner → Production Journey

```text
                 AI / GENAI ENGINEERING

                         LLM
                          |
              +-----------+-----------+
              |                       |
          LangChain                 RAG
              |                       |
              +-----------+-----------+
                          |
                      LangGraph
                          |
                    Tool Calling
                          |
                      AI Agents
                          |
                   Agentic Workflows
                          |
                         MCP
                          |
                  Multi-Agent Systems
                          |
                 Evaluation / Testing
                          |
                     FastAPI
                          |
                     Database
                          |
                       Docker
                          |
                    Cloud Deployment
```

---

# 🛠️ Local Development

## Clone the repository

```bash
git clone <your-repository-url>
cd agentic-ai
```

## Create virtual environment

```bash
python -m venv venv
```

### Linux / macOS

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Environment variables

Create a `.env` file:

```env
GROQ_API_KEY=your_key
OPENAI_API_KEY=your_key
GOOGLE_API_KEY=your_key
```

Only configure the providers required by the specific project.

For local LLM experiments, install and run Ollama separately.

Example:

```bash
ollama run qwen2.5:3b
```

---

# 🔐 Security

API keys and secrets should never be committed to GitHub.

Use:

```text
.env
```

and add it to `.gitignore`.

Provide:

```text
.env.example
```

for required environment variables.

---

# 📚 What I Want to Be Able to Build

By completing this roadmap, I aim to be able to design and develop AI applications capable of:

* Retrieval
* Reasoning
* Tool usage
* Planning
* Multi-step execution
* Memory
* External system interaction
* Agent orchestration
* Human approval workflows
* Evaluation
* Deployment

The ultimate goal is to move from:

```text
LLM Application
      ↓
RAG Application
      ↓
AI Agent
      ↓
Agentic Workflow
      ↓
Production AI System
```

---


# 📌 Important Note

This repository represents a **learning and experimentation journey**.

The objective is to understand the underlying concepts and build projects independently rather than simply copying implementations from tutorials.

As the projects mature, the focus will shift toward:

**reliability, evaluation, security, scalability, observability, and deployment.**

---

## 👨‍💻 Author

**S. Dhineshkumar M**

Computer Science & Engineering

Interested in:

* AI / Generative AI
* AI Agents & Agentic AI
* Software Engineering
* Software Testing
* Full Stack Development
* DSA & System Design

---

⭐ If you find this learning journey useful, consider starring the repository.
