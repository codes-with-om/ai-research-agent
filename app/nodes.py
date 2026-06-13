from app.state import ResearchState

def planner_node(state: ResearchState)-> ResearchState:
    query = state["query"]

    plan = [
        f"Understand the topic: {query}",
        "Find key concepts and definitions",
        "Find benefits, limitations, and use cases",
    ]

    state["plan"] = plan

    return state

def researcher_node(state: ResearchState)-> ResearchState:
    plan = state['plan']

    research_notes = [
        f"Research note based on: {step}"
        for step in plan
    ]

    state['research_notes'] = research_notes

    return state

def writer_node(state: ResearchState)-> ResearchState:
    research_notes = state['research_notes']

    draft_answer = "Draft Answer:\n" + "\n".join(research_notes)

    state['draft_answer'] = draft_answer

    return state

def reviewer_node(state: ResearchState)-> ResearchState:
    draft_answer = state['draft_answer']

    review_feedback = f"Review completed for: {draft_answer}"

    state['review_feedback'] = review_feedback

    return state

def finalizer_node(state: ResearchState)-> ResearchState:
    draft_answer = state['draft_answer']
    review_feedback = state['review_feedback']

    final_answer = f"Final Answer:\n{draft_answer}\n\nFeedback Applied: {review_feedback}"

    state['final_answer'] = final_answer

    return state