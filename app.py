import streamlit as st
import httpx
import time
import traceback
from utils.file_parser import parse_file
from utils.workflow_manager import load_workflows, save_workflow, get_workflow_by_name, get_all_workflows, delete_workflow

import os

# --- Configuration ---
st.set_page_config(page_title="AI Workflow | System v3", layout="wide", page_icon="⚡")

# On Render, the backend URL will be provided via Environment Variable
API_URL = os.getenv("API_URL", "http://localhost:8000/api")

# Handle missing protocol or trailing slashes
if API_URL.startswith("ai-workflow-backend"): # Handle Render internal hostname if passed raw
    API_URL = f"http://{API_URL}"
elif not (API_URL.startswith("http://") or API_URL.startswith("https://")):
    API_URL = f"http://{API_URL}"

if not API_URL.endswith("/api"):
    API_URL = f"{API_URL.rstrip('/')}/api"

# --- Premium Glassmorphism CSS ---
st.markdown("""
    <style>
    .main { background: #0f172a; color: #f1f5f9; }
    .stButton>button { border-radius: 8px; border: 1px solid #38bdf8; background: rgba(56,189,248,0.1); }
    [data-testid="stExpander"] { background: rgba(30,41,59,0.5); border: 1px solid #334155; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ AI Workflow Orchestrator")
st.caption("Architecture: Streamlit (Frontend) + FastAPI (Async Engine)")

# --- State ---
if 'exec_id' not in st.session_state: st.session_state.exec_id = None
if 'user_input' not in st.session_state: st.session_state.user_input = ""

# --- Sidebar: History ---
with st.sidebar:
    st.header("🕒 Recent Executions")
    try:
        resp = httpx.get(f"{API_URL}/history", timeout=5.0)
        if resp.status_code == 200:
            history = resp.json()
            if not history:
                st.caption("No recent runs.")
            for ex in history:
                with st.expander(f"{ex.get('workflow_name') or 'Custom Run'}"):
                    st.caption(f"ID: {ex['id'][:8]} | {ex['status']}")
                    if st.button("View", key=f"view_{ex['id']}"):
                        st.session_state.exec_id = ex['id']
        else:
            st.error(f"Backend Error: {resp.status_code}")
    except httpx.ConnectError:
        st.error("🔌 Backend Offline (Connection Refused)")
        st.info("Run `start.bat` to start the backend.")
    except Exception as e:
        st.error(f"API Error: {str(e)}")

# --- Main Logic ---
col_main, col_res = st.columns([2, 2])

with col_main:
    st.subheader("📥 Input Configuration")
    input_mode = st.radio("Mode", ["Text", "File"], horizontal=True)
    
    if input_mode == "Text":
        inner_input = st.text_area("Content", height=150, value=st.session_state.user_input)
    else:
        uploaded = st.file_uploader("Upload", type=["pdf", "png", "jpg", "txt"])
        if uploaded:
            inner_input = parse_file(uploaded)
        else: inner_input = ""

    st.session_state.user_input = inner_input

    # --- Template Loader ---
    st.write("### 📂 Load Template")
    try:
        wf_resp = httpx.get(f"{API_URL}/workflows").json()
        if wf_resp:
            template_names = [t["name"] for t in wf_resp]
            selected_template = st.selectbox("Quick Load Configuration", ["None"] + template_names)
            
            if selected_template != "None":
                # Find the steps for the selected template
                for t in wf_resp:
                    if t["name"] == selected_template:
                        st.session_state.current_template_steps = t["steps"]
                        st.info(f"Loaded: **{selected_template}**")
                        break
        else:
            st.caption("No templates saved yet.")
    except Exception:
        st.caption("Error loading templates")

    # Get nodes from API
    try:
        nodes_resp = httpx.get(f"{API_URL}/nodes").json()
        available_nodes = nodes_resp["available_nodes"]
    except:
        available_nodes = ["Summarizer", "Email Generator", "Code Analyzer", "Condition", "Web Search", "RAG Node"]

    # Initialize multiselect with loaded template if exists
    default_steps = st.session_state.get("current_template_steps", [])
    selected_nodes = st.multiselect("Select Pipeline Nodes", available_nodes, default=default_steps)

    if st.button("🚀 Execute Pipeline", type="primary"):
        if not inner_input or not selected_nodes:
            st.warning("Input and Nodes required.")
        else:
            payload = {"nodes": selected_nodes, "input_text": inner_input}
            with st.spinner("Dispatching to Async Engine..."):
                res = httpx.post(f"{API_URL}/workflows/run", json=payload)
                if res.status_code == 200:
                    st.session_state.exec_id = res.json()["execution_id"]
                    st.success(f"Job Dispatched: {st.session_state.exec_id[:8]}")
                else:
                    st.error("API Dispatch Failed")

with col_res:
    st.subheader("📑 Results & Observability")
    if st.session_state.exec_id:
        # Polling for results
        placeholder = st.empty()
        
        while True:
            try:
                status_res = httpx.get(f"{API_URL}/executions/{st.session_state.exec_id}").json()
                status = status_res["status"]
                
                with placeholder.container():
                    st.info(f"Status: **{status}**")
                    
                    if status == "COMPLETED":
                        st.markdown("### ✨ Output")
                        st.markdown(status_res["final_output"])
                        
                        st.markdown("### 📝 Detailed Logs")
                        for step in status_res["steps"]:
                            with st.expander(f"Node: {step['node_name']} ({step['duration_ms']}ms)"):
                                st.code(step["output_data"])
                        break
                    elif status == "FAILED":
                        st.error("Workflow failed. Check logs.")
                        break
                    else:
                        st.write("Processing... 🔄")
                        time.sleep(2)
            except Exception as e:
                st.error(f"Polling error: {e}")
                break
    else:
        st.info("Run a workflow to see results here.")

# --- Save Logic ---
st.divider()
wf_name = st.text_input("Save this sequence as a template")
if st.button("Save Template"):
    if wf_name and selected_nodes:
        save_workflow(wf_name, selected_nodes)
        st.toast("Template Saved!")