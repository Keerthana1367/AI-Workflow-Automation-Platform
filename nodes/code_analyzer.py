from nodes.base_node import BaseNode, WorkflowState
from services.llm_service import generate_response
from schemas import CodeAnalysisOutput

class CodeAnalyzerNode(BaseNode):
    def __init__(self):
        super().__init__("Code Analyzer")

    def execute(self, state: WorkflowState) -> WorkflowState:
        self.log("Performing structured code analysis...")
        prompt = f"""
        You are an expert software engineer.
        Analyze the following code for bugs, smells, and optimizations.
        Code: {state.output or state.input}
        """
        try:
            result: CodeAnalysisOutput = generate_response(prompt, schema=CodeAnalysisOutput)
            
            if isinstance(result, CodeAnalysisOutput):
                formatted_output = f"CORE ISSUES:\n" + "\n".join([f"- {i}" for i in result.issues])
                formatted_output += f"\n\nIMPROVEMENTS:\n" + "\n".join([f"- {i}" for i in result.improvements])
                formatted_output += f"\n\nQUALITY SCORE: {result.score}/100"
                
                if result.refactored_code:
                    formatted_output += f"\n\nREFACTORED SNIPPET:\n```python\n{result.refactored_code}\n```"
                
                state.update(self.name, formatted_output)
                state.variables["code_analysis"] = result.model_dump()
            else:
                state.update(self.name, str(result), error="Schema validation failed")
                
        except Exception as e:
            state.update(self.name, f"Error: {str(e)}", error=str(e))
        return state