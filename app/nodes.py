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
    plan_text = "\n".join(plan)

    prompt = f"""
    Based on the research plan below, create detailed research notes.

    Research Plan:
    {plan_text}

    Return one research note per line.
    Do not add introduction or conclusion.
    """        

    llm_response = call_llm(prompt)

    research_notes = [
        note.strip()
        for note in llm_response.split("\n")
        if note.strip()
    ]

    state['research_notes'] = research_notes

    return state

def writer_node(state: ResearchState)-> ResearchState:
    query = state["query"]
    research_notes = state['research_notes']
    notes_text = "\n".join(research_notes)

    prompt = f"""
    Using the research notes below, write a clear and well-structured answer for the user's query.

    User Query:
    {query}

    Research Notes:
    {notes_text}

    Write a complete answer.
    Use clear paragraphs.
    Do not mention that these are research notes.
    """

    llm_response = call_llm(prompt)

    state["draft_answer"] = llm_response

    return state



def reviewer_node(state: ResearchState) -> ResearchState:
    query = state['query']
    draft_answer = state["draft_answer"]

    prompt = f"""
    Review the draft answer for the user's query.

    User Query:
    {query}

    Draft Answer:
    {draft_answer}

    Give short, practical feedback.
    Mention what is good and what should be improved.
    Do not rewrite the answer.
    """

    review_feedback = call_llm(prompt)
    state['review_feedback'] = review_feedback

    return state

def finalizer_node(state: ResearchState)-> ResearchState:
    query = state['query']
    draft_answer = state['draft_answer']
    review_feedback = state['review_feedback']

    prompt = f"""
    Improve the draft answer using the reviewer feedback.

    User Query:
    {query}

    Draft Answer:
    {draft_answer}

    Reviewer Feedback:
    {review_feedback}

    Return only the final improved answer.
    Do not mention reviewer feedback.
    Do not include phrases like "Feedback Applied".
    """

    final_answer = call_llm(prompt)
    state['final_answer'] = final_answer

    return state