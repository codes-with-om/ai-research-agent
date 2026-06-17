from app.state import ResearchState
from app.llm.client import call_llm
from app.tools.web_search import web_search

def query_analyzer_node(state: ResearchState) -> ResearchState:
    query = state['query']

    prompt = f"""
    Analyze the user's query for an AI research agent.

    User Query:
    {query}

    Identify:
    - Topic/domain
    - User intent
    - Important entities
    - Any ambiguity

    If the query contains common AI terms like RAG, assume the AI/ML meaning unless the user clearly means something else.

    Return a short analysis in 3 to 5 lines.

    Acronym rules:
    - Do not invent acronym expansions.
    - Prefer widely used AI/ML expansions for AI-related acronyms.
    - RAG means Retrieval-Augmented Generation in AI/ML context.
    - RLHF means Reinforcement Learning from Human Feedback.
    """

    query_analysis = call_llm(prompt)

    state["query_analysis"] = query_analysis

    return state

def planner_node(state: ResearchState)-> ResearchState:
    query = state["query"]
    query_analysis = state["query_analysis"]

    prompt = f"""
    Create a short research plan for the user query below.

    User query:
    {query}

    Query Analysis:
    {query_analysis}

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

def search_query_node(state: ResearchState) -> ResearchState:
    query = state["query"]
    plan = state["plan"]
    query_analysis = state["query_analysis"]

    plan_text = "\n".join(plan)

    prompt = f"""
    Create one focused web search query for researching the user's question.
    Use the identified user intent from Query Analysis.

    If intent is Explanation:
    - create an explanation-focused search query

    If intent is Comparison:
    - create a comparison-focused search query

    If intent is Current Events:
    - create a news-focused search query

    Use the entity meaning from Query Analysis. Do not reinterpret acronyms.

    User Question:
    {query}

    Research Plan:
    {plan_text}

    Query Analysis:
    {query_analysis}

    Rules:
    - Return only the search query.
    - Do not add explanation.
    - Prefer current flagship products and models.
    - Avoid outdated model names unless the user asks for historical comparison.
    - For OpenAI, Anthropic, and Google AI comparisons, prefer terms like GPT, Claude, and Gemini.
    - The search query should be practical and current, not academic.
    - Prefer company/product comparison keywords.
    - Avoid benchmark names unless the user specifically asks for benchmarks.
    - Make Output under 12 words.
    - If the user asks "what is", "explain", or "define", create a definition/explanation search query.
    - Do not create comparison queries unless the user explicitly asks to compare.
    """

    search_query = call_llm(prompt).strip()
    search_query = search_query.replace('"', "")

    words = search_query.split()
    search_query = " ".join(words[:12])

    state["search_query"] = search_query

    return state

def researcher_node(state: ResearchState)-> ResearchState:
    plan = state['plan']
    plan_text = "\n".join(plan)

    search_query = state["search_query"]
    search_results = web_search(search_query, max_results=3)
    search_text = "\n\n".join(search_results)

    state["web_results"] = search_results

    prompt = f"""
    You are a research assistant.

    Use the research plan and web search results below to create grounded research notes.

    Research Plan:
    {plan_text}

    Web Search Results:
    {search_text}

    Rules:
    - Return one research note per line.
    - Use only information supported by the web search results.
    - Do not invent statistics, model sizes, funding numbers, or benchmark scores.
    - If the search results do not contain enough information, say that clearly.
    - Do not add introduction or conclusion.
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

    Rules:
    - Use only the provided research notes.
    - Do not invent statistics, parameter counts, benchmark scores, pricing, or dataset sizes.
    - If the notes do not contain exact numbers, avoid exact numbers.
    - Keep the answer practical and concise.
    - If a statement is uncertain or not clearly supported, phrase it cautiously.
    - Avoid naming specific versions unless present in the research notes.
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

    Rules:
    - Do not add new facts that are not present in the draft answer.
    - Do not invent statistics, parameter counts, benchmark scores, pricing, or dataset sizes.
    - Preserve factual caution.
    - Remove unsupported or overly specific claims.
    """

    final_answer = call_llm(prompt)
    state['final_answer'] = final_answer

    return state

def router_node(state: ResearchState) -> ResearchState:
    query = state["query"]
    query_analysis = state["query_analysis"]

    prompt = f"""
    Decide whether web search is required.

    User Query:
    {query}

    Query Analysis:
    {query_analysis}

    Rules:
    - Return YES if the question needs current information, recent events, web research, company information, product comparisons, or external facts.
    - Return NO if the question can be answered from general knowledge, explanations, coding help, or writing tasks.
    - Return only YES or NO.

    Answer:
    """

    decision = call_llm(prompt).strip().upper()
    state["needs_web_search"] = decision == "YES"

    return state
