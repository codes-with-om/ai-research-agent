from typing import TypedDict, Optional


class ResearchState(TypedDict):
    query: str
    query_analysis: Optional[str]
    plan: Optional[list[str]]
    search_query: Optional[str]
    research_notes: Optional[list[str]]
    draft_answer: Optional[str]
    review_feedback: Optional[str]
    final_answer: Optional[str]
    web_results: Optional[list[str]]