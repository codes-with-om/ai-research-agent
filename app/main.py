from fastapi import FastAPI
from pydantic import BaseModel,Field, field_validator
from app.graph import build_graph
from app.tools.web_search import web_search
from app.llm.client import call_llm
from app.logger import logger
import time
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

research_graph = build_graph()

app = FastAPI(
    title="AI Research Agent API",
    version="0.1.0"
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
def serve_ui():
    return FileResponse("app/static/index.html")


class ResearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=500)

    @field_validator("query")
    @classmethod
    def query_must_not_be_empty(cls, value: str) -> str:
        cleaned_value = value.strip()

        if not cleaned_value:
            raise ValueError("Query cannot be empty")

        return cleaned_value


class ResearchResponse(BaseModel):
    query: str
    status: str
    execution_path: str
    execution_time: float
    message: str
    sources: list[str]

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "ai-research-agent"
    }


@app.post("/research", response_model=ResearchResponse)
def research(request: ResearchRequest):
    start_time = time.time()
    initial_state = {
        "query": request.query
    }

    try:
        logger.info(f"Research request received: {request.query}")

        final_state = research_graph.invoke(initial_state)

        execution_time = round(time.time() - start_time, 2)

        logger.info("Research request completed successfully")

        return {
            "query": final_state["query"],
            "status": "completed",
            "message": final_state["final_answer"],
            "execution_path": final_state["execution_path"],
            "execution_time": execution_time,
            "sources": final_state.get("web_results", [])
        }

    except Exception as e:
        logger.error(f"Research request failed: {str(e)}")

        return {
            "query": request.query,
            "status": "failed",
            "message": "Unable to process request right now. Please try again later.",
            "execution_path": "unknown",
            "execution_time": 0,
            "sources": []
        }

@app.get("/test_llm")
def test_llm():
    response = call_llm("Say hello in one short sentence.")
    return {
        "response" : response
    }

@app.get("/test-search")
def test_search():
    results = web_search("latest AI news", max_results=3)

    return {
        "type": str(type(results)),
        "count": len(results),
        "results": results
    }

@app.post("/debug-research")
def debug_research(request: ResearchRequest):
    initial_state = {
        "query": request.query
    }

    final_state = research_graph.invoke(initial_state)

    return {
        "query": final_state.get("query"),
        "query_analysis": final_state.get("query_analysis"),
        "plan": final_state.get("plan"),
        "search_query": final_state.get("search_query"),
        "web_results": final_state.get("web_results"),
        "research_notes": final_state.get("research_notes"),
        "draft_answer": final_state.get("draft_answer"),
        "review_feedback": final_state.get("review_feedback"),
        "final_answer": final_state.get("final_answer"),
    }