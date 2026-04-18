from pydantic import BaseModel, Field
from typing import List, Optional

class SummarizerOutput(BaseModel):
    summary: str = Field(description="The main summary of the text")
    key_points: List[str] = Field(description="List of key bullet points")
    word_count: int = Field(description="Length of summary")
    confidence: float = Field(description="Model confidence score 0-1")

class EmailOutput(BaseModel):
    subject: str = Field(description="Professional email subject line")
    body: str = Field(description="The body content of the email")
    tone: str = Field(description="The tone used: formal, casual, or urgent")
    suggested_recipients: List[str] = Field(default_factory=list, description="List of possible recipient roles")

class CodeAnalysisOutput(BaseModel):
    issues: List[str] = Field(description="Identified bugs or code smells")
    improvements: List[str] = Field(description="Suggested optimizations")
    refactored_code: Optional[str] = Field(None, description="A refactored snippet if applicable")
    score: int = Field(description="Code quality score out of 100")

class ConditionOutput(BaseModel):
    label: str = Field(description="The label assigned to the text (e.g., PASS, FAIL)")
    reasoning: str = Field(description="Why this label was chosen")

class SearchResult(BaseModel):
    title: str
    link: str
    snippet: str

class SearchOutput(BaseModel):
    query: str
    results: List[SearchResult]
    summary_of_findings: str

class RagOutput(BaseModel):
    answer: str
    source_contexts: List[str]
    confidence_score: float
