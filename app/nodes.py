from app.state import ResearchState
from app.llm.client import call_llm

def planner_node(state: ResearchState)-> ResearchState:
    query = state["query"]

    prompt = f"""
    Create a short research plan for the user query below.

    User query:
    {query}

    Return only 3 to 5 research steps.
    Each step should be on a new line.
    Do not add explanation.
    """

    llm_response = call_llm(prompt)

    plan = [
        step.strip()
        for step in llm_response.split("\n")
        if step.strip()
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