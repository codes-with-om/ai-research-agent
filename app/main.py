from fastapi import FastAPI
from pydantic import BaseModel
from app.graph import build_graph
from app.tools.web_search import web_search

research_graph = build_graph()

app = FastAPI(
    title="AI Research Agent API",
    version="0.1.0"
)


class ResearchRequest(BaseModel):
    query: str


class ResearchResponse(BaseModel):
    query: str
    status: str
    message: str
    search_query_used: str


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "ai-research-agent"
    }


@app.post("/research", response_model=ResearchResponse)
def research(request: ResearchRequest):
    initial_state = {
        "query": request.query
    }

    final_state = research_graph.invoke(initial_state)

    return {
        "query": final_state["query"],
        "status": "completed",
        "message": final_state["final_answer"],
        "search_query_used": final_state["search_query"]
    }

from app.llm.client import call_llm

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