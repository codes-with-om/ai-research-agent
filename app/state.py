from typing import TypedDict, Optional


class ResearchState(TypedDict):
    query: str
    plan: Optional[list[str]]
    research_notes: Optional[list[str]]
    draft_answer: Optional[str]
    review_feedback: Optional[str]
    final_answer: Optional[str]