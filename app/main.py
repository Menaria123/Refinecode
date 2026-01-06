from fastapi import FastAPI, HTTPException
from app.schemas import CodeRequest, AnalysisResult
from models.analyzer import CodeReviewModel
from engine.syntax_checker import SyntaxChecker
import uvicorn
import logging

app = FastAPI(title="Automatic Code Review System")

# Initialize models and engines
# We do this at startup. In a real app we might use lifespan events or dependencies.
logger = logging.getLogger("uvicorn")

try:
    model_engine = CodeReviewModel(use_cuda=False) # Force CPU for compatibility in unknown envs
    syntax_engine = SyntaxChecker()
except Exception as e:
    logger.error(f"Failed to initialize engines: {e}")
    model_engine = None
    syntax_engine = None

@app.get("/")
def read_root():
    return {"message": "Welcome to the NLP Code Review System API"}

@app.post("/analyze", response_model=AnalysisResult)
async def analyze_code(request: CodeRequest):
    if not model_engine or not syntax_engine:
        raise HTTPException(status_code=500, detail="Analysis engine not initialized")

    # 1. Syntax Check
    syntax_res = syntax_engine.check_syntax(request.code, request.language)
    
    # 2. Bug Prediction (CodeBERT)
    bug_prob = model_engine.predict_bug_probability(request.code)

    # 3. Generate comments (heuristic based on prob or other rules)
    comments = []
    if not syntax_res['valid']:
        comments.append(f"Syntax Error: {syntax_res['error']}")
    
    if bug_prob > 0.5:
        comments.append("High probability of potential bugs detected by CodeBERT.")
    
    # Simple rule-based addition
    if "todo" in request.code.lower():
        comments.append("Found TODO comment - ensure this is addressed.")

    return AnalysisResult(
        bug_probability=bug_prob,
        syntax_valid=syntax_res['valid'],
        syntax_error=syntax_res['error'],
        review_comments=comments
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
