import time
import asyncio
from typing import List, Optional
from nodes.base_node import WorkflowState
from nodes.summarizer import SummarizerNode
from nodes.email_generator import EmailGeneratorNode
from nodes.code_analyzer import CodeAnalyzerNode
from nodes.condition_node import ConditionNode
from nodes.web_search_node import WebSearchNode
from nodes.rag_node import RagNode
from database import init_db, create_execution, update_execution, log_step

# Ensure DB is ready
init_db()

# Node mapping
NODE_MAP = {
    "Summarizer": SummarizerNode,
    "Email Generator": EmailGeneratorNode,
    "Code Analyzer": CodeAnalyzerNode,
    "Condition": ConditionNode,
    "Web Search": WebSearchNode,
    "RAG Node": RagNode,
}

AVAILABLE_WORKFLOW_STEPS = sorted(list(NODE_MAP.keys()))

async def run_workflow_async(selected_steps: List[str], input_text: str, workflow_name: Optional[str] = None):
    """
    Asynchronous Orchestration Engine.
    Executes nodes in a non-blocking way for the API.
    """
    # 1. Initialize DB Record
    from database import get_connection
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM workflows WHERE name = ?", (workflow_name,))
    row = cursor.fetchone()
    workflow_id = row['id'] if row else None
    conn.close()

    exec_id = create_execution(workflow_id, input_text[:100])
    state = WorkflowState(input_text)
    
    try:
        for step_name in selected_steps:
            if step_name in NODE_MAP:
                node_input = state.output or state.input
                start_time = time.time()
                
                # Run node in a thread pool to avoid blocking the event loop 
                # (since Gemini calls are blocking HTTP currently)
                node_class = NODE_MAP[step_name]
                node = node_class()
                
                # Execute node logic
                state = await asyncio.to_thread(node.execute, state)
                
                duration = int((time.time() - start_time) * 1000)
                
                node_error = None
                if state.history and "error" in state.history[-1]:
                    node_error = state.history[-1]["error"]

                log_step(
                    exec_id=exec_id,
                    node_name=step_name,
                    input_data=node_input,
                    output_data=state.output,
                    duration_ms=duration,
                    error=node_error
                )
            else:
                state.update(step_name, f"Error: Node {step_name} not found.", error="NODE_NOT_FOUND")

        update_execution(exec_id, "COMPLETED", state.output)
        
    except Exception as e:
        update_execution(exec_id, "FAILED", str(e))
        state.errors.append(str(e))

    return state.output, state.history, exec_id