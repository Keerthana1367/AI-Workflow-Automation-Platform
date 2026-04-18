from nodes.base_node import BaseNode, WorkflowState
from services.llm_service import generate_response
from schemas import SearchOutput, SearchResult
from duckduckgo_search import DDGS
import traceback

class WebSearchNode(BaseNode):
    """
    A persistent and robust Web Search Node using DuckDuckGo with structured output.
    """
    def __init__(self):
        super().__init__("Web Search")

    def execute(self, state: WorkflowState) -> WorkflowState:
        self.log("Initializing Agentic Search...")
        raw_input = state.output or state.input
        
        # 1. Smarter Query Extraction
        query_prompt = f"Given: '{raw_input}'. Extract 3-5 keywords for a Google search. Output keywords ONLY."
        
        try:
            keywords = generate_response(query_prompt).strip().strip('"')
            self.log(f"Extracted Keywords: '{keywords}'")
            
            ddgs = DDGS()
            raw_results = list(ddgs.text(keywords, max_results=5))
            
            if not raw_results:
                # Fallback to broader search
                raw_results = list(ddgs.text(state.input[:30], max_results=3))

            if raw_results:
                search_results = [
                    SearchResult(title=r['title'], link=r['href'], snippet=r['body'])
                    for r in raw_results
                ]
                
                # 2. Synthesize results with LLM for structured output
                synth_prompt = f"Synthesize these search results into a summary:\n{raw_results}"
                summary: SearchOutput = generate_response(synth_prompt, schema=SearchOutput)
                
                if isinstance(summary, SearchOutput):
                    # Ensure the results list is the actual real results we found
                    summary.results = search_results
                    summary.query = keywords
                    
                    formatted = f"🌐 SEARCH SUMMARY: {summary.summary_of_findings}\n\n"
                    for r in summary.results:
                        formatted += f"- [{r.title}]({r.link})\n"
                    
                    state.update(self.name, formatted)
                    state.variables["search_data"] = summary.model_dump()
                else:
                    state.update(self.name, str(summary), error="Search synthesis failed")
            else:
                state.update(self.name, f"⚠️ No results found for '{keywords}'.", error="ZERO_RESULTS")

        except Exception as e:
            error_msg = f"Web Search Failed: {str(e)}\n{traceback.format_exc()}"
            self.log(error_msg)
            state.update(self.name, f"Error: {str(e)}", error="SEARCH_ERROR")
            
        return state
