import json
import os
from datetime import datetime

FILE_PATH = "workflows/workflows.json"

def load_workflows():
    if not os.path.exists(FILE_PATH):
        return []
    
    try:
        with open(FILE_PATH, "r") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_workflow(name, steps):
    # Ensure directory exists
    os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)
    
    workflows = load_workflows()
    
    # Add new workflow with timestamp
    workflows.append({
        "name": name,
        "steps": steps,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    with open(FILE_PATH, "w") as f:
        json.dump(workflows, f, indent=4)

def get_workflow_by_name(name):
    workflows = load_workflows()
    
    for wf in workflows:
        if wf["name"] == name:
            return wf["steps"]
    
    return None

def get_all_workflows():
    """Returns all workflows, newest first."""
    workflows = load_workflows()
    # Handle older entries without timestamp
    return sorted(workflows, key=lambda x: x.get("timestamp", ""), reverse=True)

def delete_workflow(index):
    """Deletes workflow by index in the loaded list."""
    # Note: Index should map to the full list, but usually we manage this in the UI
    workflows = load_workflows()
    if 0 <= index < len(workflows):
        workflows.pop(index)
        with open(FILE_PATH, "w") as f:
            json.dump(workflows, f, indent=4)
        return True
    return False