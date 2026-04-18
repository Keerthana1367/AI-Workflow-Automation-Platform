from nodes.base_node import BaseNode, WorkflowState
from services.llm_service import generate_response
from schemas import ConditionOutput

class ConditionNode(BaseNode):
    """
    An Agentic Condition Node. 
    It uses an LLM to decide if the workflow should continue or change path.
    """
    def __init__(self):
        super().__init__("Condition")

    def execute(self, state: WorkflowState) -> WorkflowState:
        self.log("Agent is performing structured evaluation...")
        
        eval_prompt = f"""
        You are a Quality Control Agent.
        Assess the following content for depth, accuracy, and professional tone.
        ---
        {state.output or state.input}
        ---
        Task: 
        Assign a label (PASS/FAIL) and provide reasoning.
        """
        
        try:
            result: ConditionOutput = generate_response(eval_prompt, schema=ConditionOutput)
            
            if isinstance(result, ConditionOutput):
                is_pass = "PASS" in result.label.upper()
                msg = f"Decision: {result.label}\nReasoning: {result.reasoning}"
                
                state.variables["is_quality_pass"] = is_pass
                state.update(self.name, msg)
            else:
                state.update(self.name, str(result), error="Schema validation failed")
            
        except Exception as e:
            state.update(self.name, f"Error in condition logic: {str(e)}", error=str(e))
            
        return state