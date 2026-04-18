from nodes.base_node import BaseNode, WorkflowState
from services.llm_service import generate_response
from schemas import EmailOutput

class EmailGeneratorNode(BaseNode):
    def __init__(self):
        super().__init__("Email Generator")

    def execute(self, state: WorkflowState) -> WorkflowState:
        self.log("Generating structured professional email...")
        prompt = f"""
        You are a professional email writer.
        Task: Write a clear and professional email based on the input.
        Input: {state.output or state.input}
        """
        try:
            result: EmailOutput = generate_response(prompt, schema=EmailOutput)
            
            if isinstance(result, EmailOutput):
                formatted_output = f"SUBJECT: {result.subject}\n\n{result.body}\n\n[Tone: {result.tone}]"
                state.update(self.name, formatted_output)
                state.variables["email_data"] = result.model_dump()
            else:
                state.update(self.name, str(result), error="Schema validation failed")
                
        except Exception as e:
            state.update(self.name, f"Error: {str(e)}", error=str(e))
        return state