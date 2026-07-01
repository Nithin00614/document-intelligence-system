"""
Request schemas for API endpoints.
"""

from typing import Literal

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):

    question: str = Field(
        default=""
    )

    mode: Literal[
        "answer",
        "answer_insights",
    ] = "answer"