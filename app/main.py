from fastapi import FastAPI
from pydantic import BaseModel
from app.graph import build_graph

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
        "message": final_state["final_answer"]
    }

from app.llm.client import call_llm

@app.get("/test_llm")
def test_llm():
    response = call_llm("Say hello in one short sentence.")
    return {
        "response" : response
    }