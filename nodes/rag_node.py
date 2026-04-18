import chromadb
from nodes.base_node import BaseNode, WorkflowState
from services.llm_service import generate_response
from utils.helpers import chunk_text
from schemas import RagOutput
import uuid

class RagNode(BaseNode):
    """
    RAG (Retrieval Augmented Generation) Node.
    Indexes the input text and answers questions based on it.
    """
    def __init__(self):
        super().__init__("RAG (Document Q&A)")
        # Initialize ephemeral client
        self.client = chromadb.EphemeralClient()
        self.collection = self.client.create_collection(name=f"docs_{uuid.uuid4().hex[:8]}")

    def execute(self, state: WorkflowState) -> WorkflowState:
        self.log("Running RAG Pipeline...")
        
        # 1. Chunk and Index the current state output or input
        content_to_index = state.output or state.input
        chunks = chunk_text(content_to_index, chunk_size=500, overlap=50)
        
        self.log(f"Indexing {len(chunks)} chunks into ChromaDB...")
        self.collection.add(
            documents=chunks,
            ids=[f"id_{i}" for i in range(len(chunks))]
        )
        
        # 2. Extract query (if not explicitly provided, assume user wants an overview/QA)
        # In a real system, we'd extract a 'question' from state.variables
        query_text = state.variables.get("rag_query", "What are the most important technical details in this document?")
        
        # 3. Retrieve
        results = self.collection.query(
            query_texts=[query_text],
            n_results=3
        )
        contexts = results["documents"][0]
        
        # 4. Generate with Context
        prompt = f"""
        You are a Document Analysis Assistant.
        Context from document:
        ---
        {" ".join(contexts)}
        ---
        Question: {query_text}
        Instruction: Answer the question using ONLY the provided context.
        """
        
        try:
            result: RagOutput = generate_response(prompt, schema=RagOutput)
            if isinstance(result, RagOutput):
                result.source_contexts = contexts
                state.update(self.name, result.answer)
                state.variables["rag_data"] = result.model_dump()
            else:
                state.update(self.name, str(result), error="RAG schema validation failed")
        except Exception as e:
            state.update(self.name, f"RAG Error: {str(e)}", error=str(e))
            
        return state
