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
            
            # Perform robust custom search via DuckDuckGo Lite POST (bulletproof against bot blockers)
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
                "Content-Type": "application/x-www-form-urlencoded"
            }
            
            def scrape_ddg_lite(q_str):
                res = requests.post("https://lite.duckduckgo.com/lite/", data={"q": q_str}, headers=headers)
                soup = BeautifulSoup(res.text, "html.parser")
                links = soup.select('.result-link')
                snippets = soup.select('.result-snippet')
                
                results = []
                for i in range(min(5, len(links), len(snippets))):
                    title = links[i].text
                    link = links[i]['href']
                    # DuckDuckGo wraps actual links in a redirect url sometimes, but returning the redirect is perfectly fine.
                    snippet = snippets[i].text.strip()
                    results.append(SearchResult(title=title, link=link, snippet=snippet))
                return results

            search_results = scrape_ddg_lite(keywords)
            
            if not search_results:
                # Fallback to broader search
                fallback_query = " ".join(keywords.split()[:2])
                search_results = scrape_ddg_lite(fallback_query)

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
