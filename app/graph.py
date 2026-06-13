from langgraph.graph import StateGraph,START,END

from app.state import ResearchState
from app.nodes import planner_node,researcher_node,writer_node,reviewer_node,finalizer_node

def build_graph():
    graph = StateGraph(ResearchState)

    graph.add_node("Planner",planner_node)
    graph.add_node("Researcher",researcher_node)
    graph.add_node("Writer",writer_node)
    graph.add_node("Reviewer",reviewer_node)
    graph.add_node("Finalizer",finalizer_node)

    graph.add_edge(START,"Planner")
    graph.add_edge("Planner","Researcher")
    graph.add_edge("Researcher","Writer")
    graph.add_edge("Writer","Reviewer")
    graph.add_edge("Reviewer","Finalizer")
    graph.add_edge("Finalizer",END)

    return graph.compile()