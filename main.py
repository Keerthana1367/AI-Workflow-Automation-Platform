import asyncio
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from workflow_engine import run_workflow_async, AVAILABLE_WORKFLOW_STEPS
from database import get_execution_history, get_step_logs, get_connection
import json

app = FastAPI(title="AI Workflow API", description="Production Backend for AI Automation")

# --- Schemas ---

class WorkflowRequest(BaseModel):
    nodes: List[str]
    input_text: str
    workflow_name: Optional[str] = None

class ExecutionStatus(BaseModel):
    execution_id: str
    status: str
    final_output: Optional[str] = None
    steps: List[Dict[str, Any]] = []

# --- Endpoints ---

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "engine": "async-v2"}

@app.get("/api/nodes")
def list_nodes():
    return {"available_nodes": AVAILABLE_WORKFLOW_STEPS}

@app.post("/api/workflows/run")
async def trigger_workflow(req: WorkflowRequest, background_tasks: BackgroundTasks):
    """
    Triggers a workflow asynchronously. Returns an execution ID immediately.
    """
    # Kicking off the task in the background (Task 6)
    # We use run_workflow_async which handles its own DB logging
    # Note: For a true production system, we'd use Celery/Redis here.
    # For now, FastAPI background_tasks achieves the non-blocking goal.
    
    # We need to get the execution ID first to return it
    # I'll modify run_workflow_async slightly or just generate it here.
    # Actually, run_workflow_async returns it, but we want to return BEFORE it finishes.
    
    # Let's create the execution record here so we can return the ID
    from database import create_execution
    exec_id = create_execution(None, req.input_text[:100])
    
    async def run_and_log():
        await run_workflow_async(req.nodes, req.input_text, req.workflow_name)

    background_tasks.add_task(run_and_log)
    
    return {"execution_id": exec_id, "status": "PENDING"}

@app.get("/api/executions/{exec_id}", response_model=ExecutionStatus)
async def get_execution(exec_id: str):
    """
    Polls the status of a specific execution.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT status, final_output FROM executions WHERE id = ?", (exec_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Execution not found")
        
    logs = get_step_logs(exec_id)
    
    return {
        "execution_id": exec_id,
        "status": row['status'],
        "final_output": row['final_output'],
        "steps": logs
    }

@app.get("/api/history")
async def get_history(limit: int = 10):
    """
    Returns the global execution history.
    """
    return get_execution_history(limit=limit)

@app.get("/api/workflows")
async def get_templates():
    """
    Returns all saved workflow templates.
    """
    from database import get_all_workflow_defs
    import json
    templates = get_all_workflow_defs()
    # Parse the steps JSON string back into a list
    for t in templates:
        t['steps'] = json.loads(t['steps'])
    return templates

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
