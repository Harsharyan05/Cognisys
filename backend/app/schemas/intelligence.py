"""
Intelligence API Schemas.

Author: Harsh Aryan
Project: Cognisys
"""

from typing import Any, List, Optional

from pydantic import BaseModel, HttpUrl


class IntelligenceAskRequest(BaseModel):
    """
    Request model for repository intelligence questions.
    """

    repository_url: HttpUrl
    question: str


class IntelligenceAskResponse(BaseModel):
    """
    Response model for repository intelligence questions.
    """

    status: str
    category: str
    answer: Optional[str] = None
    raw_answer: Optional[str] = None
    citations: List[Any] = []
    architecture: Optional[Any] = None
    architecture_context: Optional[Any] = None
    impact: Optional[Any] = None