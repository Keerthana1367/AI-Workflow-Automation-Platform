from nodes.base_node import BaseNode, WorkflowState
from services.llm_service import generate_response
from schemas import SearchOutput, SearchResult
import traceback
import requests
from bs4 import BeautifulSoup
import urllib.parse

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
        # Truncate input to avoid confusing the LLM
        truncated_input = raw_input[:1000] 
        query_prompt = f"Extract EXACTLY a 3-5 word search query from this text. NO conversational text. NO punctuation. JUST the 5 words:\n\n{truncated_input}"
        
        try:
            keywords = generate_response(query_prompt).strip().strip('"')
            self.log(f"Extracted Keywords: '{keywords}'")
            
            # Perform robust custom search via Wikipedia API (bulletproof against Cloud Server IP blocks)
            headers = {"User-Agent": "AI-Workflow-Bot/1.0 (https://github.com)"}
            
            def scrape_wiki(q_str):
                params = {
                    "action": "query",
                    "list": "search",
                    "srsearch": q_str,
                    "format": "json",
                    "utf8": ""
                }
                res = requests.get("https://en.wikipedia.org/w/api.php", params=params, headers=headers)
                data = res.json()
                
                results = []
                for item in data.get("query", {}).get("search", [])[:5]:
                    title = item["title"]
                    link = f"https://en.wikipedia.org/wiki/{urllib.parse.quote(title.replace(' ', '_'))}"
                    # Wikipedia returns HTML snippets, strip them cleanly
                    snippet = BeautifulSoup(item["snippet"], "html.parser").text
                    results.append(SearchResult(title=title, link=link, snippet=snippet))
                return results

            search_results = scrape_wiki(keywords)
            
            if not search_results:
                # Fallback to broader search
                fallback_query = " ".join(keywords.split()[:2])
                search_results = scrape_wiki(fallback_query)

            if search_results:
                
                # 2. Synthesize results with LLM for structured output
                # Convert the list of SearchResult objects to a string for the prompt
                results_text = "\\n".join([f"[{r.title}]({r.link}): {r.snippet}" for r in search_results])
                synth_prompt = f"Synthesize these search results into a summary:\\n{results_text}"
                summary: SearchOutput = generate_response(synth_prompt, schema=SearchOutput)
                
                if isinstance(summary, SearchOutput):
                    # Ensure the results list is the actual real results we found
                    summary.results = search_results
                    summary.query = keywords
                    
                    formatted = f"🌐 SEARCH SUMMARY (Query: '{summary.query}'): {summary.summary_of_findings}\n\n"
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
