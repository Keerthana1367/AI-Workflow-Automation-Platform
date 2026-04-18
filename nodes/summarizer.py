from nodes.base_node import BaseNode, WorkflowState
from services.llm_service import generate_response
from schemas import SummarizerOutput

class SummarizerNode(BaseNode):
    def __init__(self):
        super().__init__("Summarizer")

    def execute(self, state: WorkflowState) -> WorkflowState:
        self.log("Summarizing content with structured output...")
        prompt = f"""
        You are an expert summarizer.
        Task: Summarize the following text clearly and concisely.
        Text: {state.output or state.input}
        """
        try:
            # Generate structured response
            result: SummarizerOutput = generate_response(prompt, schema=SummarizerOutput)
            
            if isinstance(result, SummarizerOutput):
                # Format a visible string for display, but keep object in variables if needed
                formatted_output = f"SUMMARY:\n{result.summary}\n\nKEY POINTS:\n" + "\n".join([f"- {p}" for p in result.key_points])
                state.update(self.name, formatted_output)
                state.variables["summarizer_data"] = result.model_dump()
            else:
                state.update(self.name, str(result), error="Schema validation failed")
                
        except Exception as e:
            state.update(self.name, f"Error: {str(e)}", error=str(e))
        return state