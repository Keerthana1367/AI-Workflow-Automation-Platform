# ⚡ AI Workflow Orchestration Engine (v3.0)

[![Live Demo](https://img.shields.io/badge/Live-Demo-brightgreen?style=flat-square&logo=railway)](https://ai-workflow-backend-production-11e3.up.railway.app)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue?style=flat-square&logo=docker)](https://www.docker.com/)
[![Gemini](https://img.shields.io/badge/AI-Google_Gemini-blueviolet?style=flat-square)](https://ai.google.dev/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)

**The ultimate production-grade orchestrator for AI agents.** This platform standardizes how LLM workflows are built, tracked, and deployed using a robust DAG-based architecture.

| Feature | Description |
| :--- | :--- |
| **🚀 Deployment** | One-click deployment to Railway/Render with Docker |
| **🛡️ Validation** | Strict schema enforcement via Pydantic & Gemini JSON mode |
| **📊 Traceability** | Granular execution logs stored in SQLite for full auditability |
| **🎨 Interface** | Premium Glassmorphism Streamlit UI for real-time monitoring |

![Platform Overview](static/overview.png)

---

## 🏗️ Architecture Visualization

```mermaid
graph LR
    Input[Input] --> Engine[Workflow Engine]
    Engine --> N1[AI Nodes]
    N1 --> State[Structured State]
    State --> DB[(SQLite)]
    State --> UI[Streamlit Hub]
```

---

## 🛠️ Tech Stack

- **Core**: Python 3.11, FastAPI
- **Intelligence**: Google Gemini 2.5 Flash Lite
- **Observability**: SQL & Pydantic
- **Infrastructure**: Docker, Railway, Render

---

## 🏁 Quick Start

1. **Clone**: `git clone https://github.com/Keerthana1367/AI-Workflow-Automation-Platform.git`
2. **Setup**: Create a `.env` with your `GEMINI_API_KEY`.
3. **Run**: Double-click `start.bat` (Windows) or `docker-compose up`.

---

## 📈 Current Progress

- [x] **Asynchronous DAG Engine**: Highly scalable non-blocking orchestration.
- [x] **Relational Persistence**: Full execution history and error tracking.
- [x] **Containerized Runtime**: Seamless local and cloud execution.
- [ ] **Multi-Agent RAG**: Integrated vector search (Upcoming).

---
*Built for scale and structure.*
