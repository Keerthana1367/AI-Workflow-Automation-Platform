# ⚡ AI Workflow Orchestration Engine (Core v2.0)

[![Production Ready](https://img.shields.io/badge/Status-Production--Ready-green?style=for-the-badge)](https://github.com/Keerthana1367/AI-Workflow-Automation-Platform)
[![Docker](https://img.shields.io/badge/Infrastructure-Docker-blue?style=for-the-badge&logo=docker)](https://www.docker.com/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?style=for-the-badge&logo=sqlite)](https://www.sqlite.org/)
[![Pydantic](https://img.shields.io/badge/Validation-Pydantic-E92063?style=for-the-badge)](https://docs.pydantic.dev/)

> **Standardizing the operationalization of AI.** This platform transforms brittle, one-off LLM scripts into a production-grade orchestration engine with structured observability, persistence, and containerization.

---

##  Architecture Overview

Our platform treats AI processing as a **Directed Acyclic Graph (DAG)** of independently testable, composable nodes. Each node operates on a shared `WorkflowState`, ensuring data integrity and lineage across the entire pipeline.

### Core Components:
- **Orchestration Engine**: A state-management core that handles node transitions, error recovery, and timing.
- **Structured IO (Pydantic)**: Every node enforces strict output schemas, ensuring the system is "composable by design" and ready for downstream API consumption.
- **Persistent Observability**: Integrated SQLite backend tracks every `execution` and detailed `step_logs` (input, output, duration, errors) for auditability.
- **Containerized Runtime**: Standardized

## Cloud Deployment (Render)

This platform is ready for one-click deployment using the included `render.yaml` blueprint:

1. **Push code to GitHub**: Ensure your project is in a repository.
2. **Open Render Dashboard**: Go to [dashboard.render.com](https://dashboard.render.com).
3. **Blueprints**: Click **"Blueprints"** -> **"New Blueprint Instance"**.
4. **Connect Repo**: Select your repository.
5. **Configure Secrets**:
   - `GEMINI_API_KEY`: Your Google AI API Key.
6. **Deploy**: Render will automatically launch the Backend (FastAPI) and the Frontend (Streamlit), linking them together.

> [!TIP]
> The UI will be available at `https://ai-workflow-automation-platform-gxgq.onrender.com`.

##  Key Features

- ** Deterministic Output**: Powered by Gemini's JSON mode and validated via Pydantic models.
- ** Execution Tracking**: Full visibility into latency and error rates at the node level.
- ** Universal Parsing**: Native support for PDF, Image (OCR), XLSX, PPTX, and Source Code.
- ** Configuration Persistence**: Save, load, and version workflow definitions.
- ** Pro UI**: Premium Streamlit interface with real-time Graphviz visualization of active pipelines.

---

##  Quick Start (Docker)

The fastest way to deploy the engine:

1. **Clone & Config**:
   ```bash
   git clone https://github.com/Keerthana1367/AI-Workflow-Automation-Platform.git
   cd AI-Workflow-Automation-Platform
   cp .env.example .env # Add your GEMINI_API_KEY
   ```

2. **Launch**:
   ```bash
   docker-compose up --build
   ```

3. **Access**:
   Navigate to [http://localhost:8501](http://localhost:8501)

---

##  Pipeline Schema Example (Production Proof)

Unlike prototypes that return raw strings, our nodes return structured objects. Example `SummarizerOutput`:

```json
{
  "summary": "The platform utilizes a modular node architecture...",
  "key_points": ["SQLite for persistence", "Pydantic for validation"],
  "word_count": 42,
  "confidence": 0.98
}
```

---

## 📈 Roadmap

- [ ] **Phase 2**: FastAPI backend layer + Async job queues (Redis/Celery).
- [ ] **Phase 2**: RAG Node integration with Vector Search (ChromaDB).
- [ ] **Phase 3**: Prompt Versioning & Automated Evaluation (LLM-as-a-judge).

---

## 🤝 Contributing

We build for scale. Please see our contribution guidelines for adding new `BaseNode` implementations.

---

*Built with ❤️ for AI Engineers who care about structure.*
