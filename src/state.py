import operator
from typing import Annotated, List, TypedDict
from pydantic import BaseModel, Field


class SearchQueries(BaseModel):
    """Structured output for the Planner node."""
    queries: List[str] = Field(
        description="3 targeted, distinct web search queries to thoroughly investigate the topic."
    )


class CritiqueResult(BaseModel):
    """Structured output for the Critic node to control graph routing."""
    score: int = Field(
        description="Quality and factual completeness score from 1 to 10.",
        ge=1,
        le=10,
    )
    feedback: str = Field(
        description="Specific gaps, missing data points, or verification needed if score < 8."
    )
    follow_up_queries: List[str] = Field(
        default_factory=list,
        description="1 to 2 targeted search queries to fill the gaps if score < 8.",
    )


class ResearchState(TypedDict):
    topic: str
    queries: List[str]
    # operator.add appends new findings across loop iterations instead of overwriting
    research_notes: Annotated[List[str], operator.add]
    sources: Annotated[List[str], operator.add]
    draft: str
    critique_feedback: str
    quality_score: int
    revision_count: int
    max_revisions: int