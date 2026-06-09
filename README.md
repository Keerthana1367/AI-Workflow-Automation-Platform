# 🚀 AI Workflow Automation Platform

> **Build and run multi-step AI pipelines without writing a single prompt — chain specialized AI agents where the output of one becomes the input of the next.**

---
## Live link-
##  Demo-

### Pipeline: ADAS.json → Summarizer → Web Search → Email Generator

<img width="1918" height="862" alt="image" src="https://github.com/user-attachments/assets/5f6feb91-7dce-49a9-85a1-62eadcc7b7a6" />

*Input configuration with live pipeline execution — Status: COMPLETED*

<img width="1917" height="862" alt="image" src="https://github.com/user-attachments/assets/6e6a4592-330e-41c2-a086-a868e488df44" />

*Node-by-node execution logs with real web references pulled automatically*

**Total execution time: ~5.2 seconds across 3 nodes**

---

##  What is This?

This is an **Agentic AI Orchestration Platform** — think Zapier or n8n, but powered by LLMs instead of fixed integrations.

Instead of writing one massive prompt, users chain together specialized **Nodes** where each agent handles one job and passes its result to the next. Upload a file, select your pipeline, hit execute — the system handles the rest asynchronously.

---

##  Architecture

```
┌─────────────────────────────────────────────────────┐
│              Streamlit Frontend (app.py)             │
│   File Upload │ Node Builder │ Live Progress Monitor │
└───────────────────────┬─────────────────────────────┘
                        │ POST /execute
                        ▼
┌─────────────────────────────────────────────────────┐
│              FastAPI Backend (main.py)               │
│   Returns execution_id immediately (non-blocking)    │
│   Runs workflow_engine.py in BackgroundTasks         │
└───────────────────────┬─────────────────────────────┘
                        │
              ┌─────────▼──────────┐
              │  workflow_engine   │
              │  Node 1 → Node 2   │
              │  → Node 3 → ...    │
              └─────────┬──────────┘
                        │ logs latency + output per node
                        ▼
              ┌─────────────────────┐
              │ PostgreSQL / SQLite  │
              │ Execution logs       │
              │ Workflow templates   │
              └─────────────────────┘
```

---

##  Available Pipeline Nodes

| Node | What It Does |
|---|---|
|  **Summarizer** | Condenses large documents into structured bullet-point summaries |
|  **Web Search** | Auto-generates search queries, scrapes live web, summarizes findings with references |
|  **Email Generator** | Drafts professional, ready-to-send business emails from any context |
|  **Code Analyzer** | Reviews code for bugs, vulnerabilities, and suggests refactored improvements |
|  **RAG Node** | Semantic document Q&A using ChromaDB vector search |
|  **Condition** | Logical routing node — makes decisions mid-pipeline |

---

##  How Execution Works

```
1. User uploads file (PDF, Excel, CSV, JSON, Image) or pastes text
        ↓
2. file_parser.py extracts and cleans text (OCR for images via pytesseract)
        ↓
3. Frontend POSTs to FastAPI → receives execution_id instantly
        ↓
4. workflow_engine.py runs nodes sequentially in background:
   [Summarizer] → output → [Web Search] → output → [Email Generator]
        ↓
5. Each node's input, output, and latency logged to database
        ↓
6. Frontend polls /status/{execution_id} → displays live progress
```

---

##  What Makes This Stand Out

**Self-Healing Web Search**
The Web Search node auto-generates a clean 3-5 word query from the pipeline context, bypasses DuckDuckGo bot-blockers, and returns real references — not just text.

**Pydantic-Enforced Structured Output**
Every LLM response is validated against a strict Pydantic schema before passing to the next node. No conversational garbage breaks the pipeline.

**Graceful Degradation**
If one node fails (e.g. web search returns nothing), the pipeline continues with whatever context is available. The system doesn't crash — it adapts.

**Real-Time Observability**
Every node shows its execution time in milliseconds. You can see exactly where time is spent across the pipeline.

---

##  Project Structure

```
AI-Workflow-Automation-Platform/
├── app.py                    # Streamlit frontend
├── main.py                   # FastAPI async backend
├── workflow_engine.py        # Core pipeline orchestration
├── database.py               # PostgreSQL / SQLite operations
├── services/
│   └── llm_service.py        # Groq LLM client + Pydantic schemas
├── utils/
│   └── file_parser.py        # PDF, Excel, CSV, Image (OCR) parser
├── Dockerfile
├── render.yaml
└── requirements.txt
```

---

##  Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/Keerthana1367/AI-Workflow-Automation-Platform.git
cd AI-Workflow-Automation-Platform
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set environment variables
Create a `.env` file:
```env
GROQ_API_KEY=your_groq_api_key
DATABASE_URL=sqlite:///./workflow.db   # or PostgreSQL URL for production
```

### 4. Start the backend
```bash
uvicorn main:app --reload --port 8000
```

### 5. Start the frontend
```bash
streamlit run app.py
```

Open `http://localhost:8501` → upload a file → select nodes → execute!

---

##  Sample Pipeline Results

**Input:** `ADAS.json` (39.7KB automotive systems data)
**Pipeline:** Summarizer → Web Search → Email Generator

| Node | Time | Result |
|---|---|---|
| Summarizer | 1605ms | Structured summary of ADAS features |
| Web Search | 2808ms | 5 real references (Wikipedia, NHTSA, etc.) |
| Email Generator | 833ms | Professional email ready to send |
| **Total** | **~5.2s** | **Status: COMPLETED** |

---

##  Tech Stack

- **LLM:** Llama 3.1 8B Instant via [Groq API](https://console.groq.com)
- **Backend:** FastAPI + BackgroundTasks
- **Frontend:** Streamlit
- **Database:** PostgreSQL (production) / SQLite (local)
- **Vector DB:** ChromaDB (RAG node)
- **File Parsing:** PyPDF2, python-pptx, pandas, pytesseract
- **Validation:** Pydantic v2
- **Deployment:** Docker + Render

---



**T. Keerthana**
- GitHub: [@Keerthana1367](https://github.com/Keerthana1367)
- LinkedIn: [keerthanatadkal](https://linkedin.com/in/keerthanatadkal)
