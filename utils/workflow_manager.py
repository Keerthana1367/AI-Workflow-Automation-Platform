import json
from database import (
    save_workflow_def, 
    get_all_workflow_defs, 
    delete_workflow_def, 
    get_execution_history,
    get_connection
)

# Bridge old functions to the NEW SQLite database for persistence

def load_workflows():
    """Wrapper for backward compatibility in UI."""
    return get_all_workflows()

def save_workflow(name, steps, output=None, history=None):
    """Saves a workflow definition."""
    return save_workflow_def(name, steps)

def get_workflow_by_name(name):
    """Retrieves steps for a specific workflow name."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT steps FROM workflows WHERE name = ?", (name,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return json.loads(row['steps'])
    return None

def get_all_workflows():
    """Maps SQL rows to the format expected by the Streamlit UI."""
    defs = get_all_workflow_defs()
    # Map 'created_at' to 'timestamp' and parse 'steps'
    for d in defs:
        d['timestamp'] = d.pop('created_at')
        d['steps'] = json.loads(d['steps'])
    return defs

def delete_workflow(index):
    """Deletes a workflow. In SQLite, we use the ID from the loaded list."""
    # This index approach is brittle, but for migration we'll handle it
    workflows = get_all_workflows()
    if 0 <= index < len(workflows):
        wf_id = workflows[index]['id']
        delete_workflow_def(wf_id)
        return True
    return False

def get_recent_executions(limit=10):
    """New functionality: fetch structured run history."""
    return get_execution_history(limit)