# 🚀 AI Workflow Automation Platform

An interactive **Streamlit-based AI automation app** for processing text and files through reusable workflow steps powered by **Google Gemini**.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-ff4b4b)
![Gemini](https://img.shields.io/badge/LLM-Google%20Gemini-4285f4)

---

## 📌 Overview

This project lets you:

- enter raw text or upload a file,
- choose one or more AI workflow steps,
- run them in sequence,
- review the final output and step-by-step logs,
- save workflows for reuse.

It is useful for **document summarization**, **email drafting**, **code review assistance**, and simple **rule-based text routing**.

---

## ✨ Features

- **Multi-input support**: plain text or uploaded files
- **Supported file formats**: `pdf`, `txt`, `py`, `csv`, `json`, `xlsx`, `pptx`, `jpg`, `jpeg`, `png`
- **Reusable workflow pipeline** with selectable node order
- **Built-in nodes** for summarization, email generation, code analysis, and condition tagging
- **Workflow history** to save, load, and delete previous configurations
- **Execution logs** for each workflow step
- **Gemini integration** through a centralized service layer

---

## 🧠 Available Workflow Nodes

| Node | What it does |
|------|---------------|
| `Summarizer` | Creates a short bullet-point summary of the input |
| `Email Generator` | Drafts a professional email from the provided content |
| `Code Analyzer` | Reviews code, highlights issues, and suggests improvements |
| `Condition` | Performs a simple length-based check and labels input as `SHORT_TEXT` or `LONG_TEXT` |

---

## 🏗️ Project Structure

```text
AI-workflow-automation-platform/
├── app.py                    # Streamlit UI
├── config.py                 # Environment loading and Gemini model config
├── workflow_engine.py        # Sequential workflow runner
├── requirements.txt          # Python dependencies
├── test.py                   # Simple workflow execution example
├── nodes/
│   ├── summarizer.py         # Summarization node
│   ├── email_generator.py    # Email generation node
│   ├── code_analyzer.py      # Code analysis node
│   ├── condition_node.py     # Basic condition / routing node
│   └── base_node.py          # Base node placeholder
├── services/
│   └── llm_service.py        # Gemini response wrapper
├── utils/
│   ├── file_parser.py        # File parsing for supported formats
│   ├── workflow_manager.py   # Save/load workflow definitions
│   ├── helpers.py
│   ├── logger.py
│   └── template.py
├── workflows/
│   └── workflows.json        # Stored workflow configurations
└── static/
    └── styles.css
```

---

## ⚙️ Tech Stack

- **Python**
- **Streamlit**
- **Google Generative AI (`google-generativeai`)**
- **PyPDF2** for PDF parsing
- **pandas / openpyxl** for tabular files
- **Pillow / pytesseract** for OCR image parsing
- **python-pptx** for PowerPoint extraction

---

## 🚀 Getting Started

### 1) Clone the repository

```bash
git clone https://github.com/Keerthana1367/AI-Workflow-Automation-Platform.git
cd AI-Workflow-Automation-Platform
```

### 2) Create and activate a virtual environment

**Windows**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux**
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

### 4) Configure environment variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 5) Install Tesseract OCR

If you want image text extraction (`jpg`, `jpeg`, `png`), install **Tesseract OCR** and make sure it is available in your system `PATH`.

### 6) Run the app

```bash
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal.

---

## 🖥️ How It Works

1. Choose **Text** or **File** input.
2. Paste content or upload a supported file.
3. Select one or more workflow steps.
4. Click **Run Workflow**.
5. Review the **final output** and **execution logs**.
6. Save the workflow for later reuse.

---

## 📷 Example Use Cases

- Summarize a long PDF into key bullet points
- Generate a professional email from rough notes
- Analyze Python code for issues and improvement ideas
- Route short vs. long text with a simple condition node

---

## 🔐 Environment Notes

This project uses a Gemini API key from `.env`:

```env
GEMINI_API_KEY=...
```

Do **not** commit your real `.env` file to GitHub.

---

## 🛠️ Future Improvements

Potential next enhancements:

- drag-and-drop node builder
- conditional branching between nodes
- richer workflow persistence with metadata
- downloadable output reports
- test coverage and CI setup

---

## 🤝 Contributing

Contributions, issues, and suggestions are welcome.
If you fork this project, create a branch for your changes and open a pull request.

---

## 📬 Repository

GitHub: [`Keerthana1367/AI-Workflow-Automation-Platform`](https://github.com/Keerthana1367/AI-Workflow-Automation-Platform)

---

Built for showcasing practical **AI workflow automation** with a simple and extensible Python architecture.
