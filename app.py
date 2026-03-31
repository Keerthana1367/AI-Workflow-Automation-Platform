import streamlit as st
from workflow_engine import run_workflow
from utils.file_parser import parse_file
from utils.workflow_manager import load_workflows, save_workflow, get_workflow_by_name, get_all_workflows, delete_workflow
import traceback

# --- Configuration ---
st.set_page_config(page_title="AI Workflow Automation Platform", layout="wide")
st.title("🚀 AI Workflow Automation Platform")

# --- Constants ---
SUPPORTED_FILE_TYPES = [
    "pdf", "jpg", "jpeg", "png", "csv", "json", "xlsx", "pptx", "txt", "py"
]
AVAILABLE_WORKFLOW_STEPS = ["Summarizer", "Email Generator", "Code Analyzer", "Condition"]
AVAILABLE_WORKFLOW_STEPS.sort()

# --- Session State Initialization ---
if 'user_input' not in st.session_state:
    st.session_state.user_input = ""
if 'file_processing_error' not in st.session_state:
    st.session_state.file_processing_error = None
if 'selected_steps' not in st.session_state:
    st.session_state.selected_steps = []
if 'active_wf_name' not in st.session_state:
    st.session_state.active_wf_name = "New Workflow"

# --- Callback for Quick Load ---
def on_quick_load_change():
    selected_wf = st.session_state.get("quick_load_select")
    if selected_wf and selected_wf != "None":
        loaded_steps = get_workflow_by_name(selected_wf)
        if loaded_steps:
            st.session_state.selected_steps = loaded_steps
            st.session_state.active_wf_name = selected_wf

# --- Callback for Sidebar Load ---
def load_historical_workflow(wf_name, steps):
    st.session_state.selected_steps = steps
    st.session_state.active_wf_name = wf_name

# --- Sidebar: Workflow History ---
with st.sidebar:
    st.header("🕒 Workflow History")
    history = get_all_workflows()
    
    if not history:
        st.info("No saved workflows yet.")
    else:
        for i, wf in enumerate(history):
            display_name = wf.get("name", "Unnamed")
            timestamp = wf.get("timestamp", "N/A")
            
            with st.expander(f"{display_name}"):
                st.caption(f"Saved at: {timestamp}")
                st.write("**Steps:**")
                for step in wf.get("steps", []):
                    st.write(f"- {step}")
                
                col1, col2 = st.columns(2)
                # Using on_click to avoid state modification error
                col1.button("Load", key=f"load_history_{i}", 
                            on_click=load_historical_workflow, 
                            args=(display_name, wf["steps"]))
                
                if col2.button("Delete", key=f"delete_history_{i}"):
                    all_wfs = load_workflows()
                    for idx, original_wf in enumerate(all_wfs):
                        if (original_wf.get("timestamp") == wf.get("timestamp") and 
                            original_wf.get("name") == wf.get("name") and
                            original_wf.get("steps") == wf.get("steps")):
                            delete_workflow(idx)
                            st.warning(f"Deleted: {display_name}")
                            st.rerun()
                            break

# --- Main Layout ---
col_main, col_spacer = st.columns([3, 1])

with col_main:
    # --- Input Section ---
    input_type = st.radio(
        "Select Input Type",
        ["Text", "File"],
        key="input_type_radio",
        horizontal=True
    )

    if input_type == "Text":
        st.session_state.user_input = st.text_area(
            "Enter your input",
            key="text_input_area",
            height=200,
            value=st.session_state.user_input
        )
        st.session_state.file_processing_error = None

    else: # File input
        uploaded_file = st.file_uploader(
            "Upload File",
            type=SUPPORTED_FILE_TYPES,
            key="file_uploader"
        )

        if uploaded_file:
            try:
                with st.spinner("Processing file..."):
                    st.session_state.user_input = parse_file(uploaded_file)
                st.success("File processed successfully!")
                st.session_state.file_processing_error = None
            except Exception as e:
                error_details = f"Error processing file: {e}\n{traceback.format_exc()}"
                st.session_state.file_processing_error = error_details
                st.error(error_details)
                st.session_state.user_input = ""
        else:
            if st.session_state.get("input_type_radio") == "File":
                st.session_state.user_input = ""

    # --- Workflow Steps Selection ---
    st.write(f"### ⚙️ Current Workflow: `{st.session_state.active_wf_name}`")
    
    def on_steps_change():
        if not st.session_state.active_wf_name.endswith("(Modified)") and st.session_state.active_wf_name != "New Workflow":
            st.session_state.active_wf_name = f"{st.session_state.active_wf_name} (Modified)"

    st.multiselect(
        "Select Workflow Steps",
        AVAILABLE_WORKFLOW_STEPS,
        key="selected_steps",
        on_change=on_steps_change
    )

    # --- Run Workflow Button ---
    if st.button("Run Workflow", key="run_workflow_button", type="primary"):
        has_input = bool(st.session_state.user_input)
        has_steps = bool(st.session_state.selected_steps)
        has_file_error = bool(st.session_state.file_processing_error)

        if not has_input and not has_file_error:
            st.warning("Please provide input (text or upload a file).")
        elif not has_steps:
            st.warning("Please select at least one workflow step.")
        elif has_file_error:
            st.error("Cannot run workflow due to previous file processing error.")
        else:
            try:
                with st.spinner("Running workflow..."):
                    output, logs = run_workflow(st.session_state.selected_steps, st.session_state.user_input)

                st.subheader("✨ Final Output")
                with st.container(border=True):
                    st.write(output)

                st.subheader("📝 Execution Logs")
                if logs:
                    for log_entry in logs:
                        if isinstance(log_entry, dict) and "step" in log_entry:
                            with st.expander(f"Step: {log_entry['step']}"):
                                st.write(log_entry.get("output", "No output."))
                else:
                    st.info("No logs generated.")

            except Exception as e:
                st.error(f"Execution Error: {e}")
                st.error(traceback.format_exc())

    st.divider()

    # --- Save Section ---
    st.subheader("💾 Save Workflow")
    c1, c2 = st.columns([3, 1])
    wf_name = c1.text_input("Workflow Name", placeholder="e.g. Analysis Pipeline v1")
    if c2.button("Save", use_container_width=True):
        if wf_name and st.session_state.selected_steps:
            save_workflow(wf_name, st.session_state.selected_steps)
            st.session_state.active_wf_name = wf_name
            st.success(f"Workflow '{wf_name}' saved!")
            st.rerun() 
        else:
            st.warning("Provide name and select steps")

    # --- Load Section ---
    st.subheader("📂 Quick Load")
    saved_workflows = load_workflows()
    unique_wf_names = sorted(list(set(wf["name"] for wf in saved_workflows)))
    st.selectbox(
        "Select by name", 
        ["None"] + unique_wf_names, 
        key="quick_load_select",
        on_change=on_quick_load_change
    )