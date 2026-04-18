from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import time

class WorkflowState:
    """Carries the memory and variables of the entire workflow execution."""
    def __init__(self, initial_input: str):
        self.input: str = initial_input
        self.output: str = ""
        self.history: List[Dict[str, Any]] = []
        self.variables: Dict[str, Any] = {}
        self.errors: List[str] = []
        self.metadata: Dict[str, Any] = {
            "start_time": time.time(),
            "step_count": 0
        }

    def update(self, node_name: str, result: Any, error: Optional[str] = None):
        """Standard way to update state after a node completes."""
        self.output = str(result)
        self.metadata["step_count"] += 1
        entry = {
            "step": self.metadata["step_count"],
            "node": node_name,
            "output": result,
            "timestamp": time.time()
        }
        if error:
            entry["error"] = error
            self.errors.append(f"[{node_name}] {error}")
        
        self.history.append(entry)

class BaseNode(ABC):
    """The standard blueprint for all Workflow Nodes."""
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def execute(self, state: WorkflowState) -> WorkflowState:
        """Each node must implement this logic."""
        pass

    def log(self, message: str):
        """Internal node logging."""
        print(f"[{self.name}] {message}")
