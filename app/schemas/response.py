"""
Response schemas for API endpoints.
"""

from typing import List, Optional

from pydantic import BaseModel


class Citation(BaseModel):
    """
    Citation metadata returned with an answer.
    """

    document_id: str
    filename: str
    page_number: int
    chunk_id: int
    source_preview: str


class UploadResponse(BaseModel):
    """
    Response after successful upload.
    """

    success: bool

    uploaded_files: int

    processed_chunks: int

    message: str


class QueryResponse(BaseModel):
    """
    Response returned after answering a question.
    """

    answer: str

    confidence: str

    confidence_score: float

    citations: List[Citation]

    processing_time: float
