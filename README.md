# AI Research Agent

An AI-powered Research Assistant built using FastAPI, LangGraph, Groq LLM, and Web Search.

The agent automatically decides whether a query requires external research or can be answered directly from the language model.

---

## Features

- Query Analysis
- Intelligent Routing
- Web Search Integration
- Direct LLM Responses
- Research-based Answers
- Execution Path Tracking
- Response Time Tracking
- Source Attribution
- Logging System
- Modern Chat Interface
- Dynamic User Profile
- Clickable Sources

---

## Tech Stack

### Backend

- FastAPI
- LangGraph
- Groq API
- DDGS Web Search
- Pydantic

### Frontend

- HTML
- CSS
- JavaScript
- SweetAlert2
- Marked.js

---

## Architecture

User Query
↓
Query Analyzer
↓
Router

├── Direct Path
│ ↓
│ Writer
│ ↓
│ Final Answer
│
└── Research Path
↓
Web Search
↓
Writer
↓
Final Answer

---

## Example Response

```json
{
  "query": "What is RAG?",
  "status": "completed",
  "execution_path": "research",
  "execution_time": 7.32,
  "message": "...",
  "sources": [
    "...",
    "...",
    "..."
  ]
}
```

## Project Structure

```text
AI-Research-Agent/
│
├── app/
│ ├── main.py
│ ├── graph.py
│ ├── nodes.py
│ ├── state.py
│ │
│ ├── llm/
│ │ └── client.py
│ │
│ ├── tools/
│ │ └── web_search.py
│ │
│ └── utils/
│ └── logger.py
│
├── static/
│ ├── style.css
│ └── script.js
│
├── templates/
│ └── index.html
│
├── logs/
│ └── app.log
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-research-agent.git
cd ai-research-agent
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows

```bash
venv\Scripts\activate
```

Linux/Mac

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Add Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key_here
```

### Run Application

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

---

## API Endpoint

### Research Endpoint

```http
POST /research
```

Request

```json
{
  "query": "Compare GPT and Claude"
}
```

Response

```json
{
  "query": "Compare GPT and Claude",
  "status": "completed",
  "execution_path": "research",
  "execution_time": 6.14,
  "message": "...",
  "sources": [...]
}
```

---

## Learning Outcomes

Through this project I learned:

- FastAPI API Development
- LangGraph Workflows
- State Management
- Agent Routing
- LLM Integration
- Web Search Tools
- Error Handling
- Logging
- Frontend Integration
- End-to-End AI Application Development

---

## Future Improvements

- Streaming Responses
- Conversation Memory
- Multi-Agent Workflow
- PDF Research Support
- Research Report Export
- Deployment on Cloud

---

## Author

Om Pratap Singh

GitHub:
https://github.com/codes-with-om