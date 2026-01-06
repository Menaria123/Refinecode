from pydantic import BaseModel
from typing import Optional, List

class CodeRequest(BaseModel):
    code: str
    language: str = "python"

class AnalysisResult(BaseModel):
    bug_probability: float
    syntax_valid: bool
    syntax_error: Optional[str] = None
    review_comments: List[str] = []
