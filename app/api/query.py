"""
Query API

Handles question answering and document insights
using the indexed PDF documents.
"""

import time

from fastapi import (
    APIRouter,
    HTTPException,
    Request,
)

from app.core.logger import logger

from app.schemas.request import QueryRequest
from app.schemas.response import QueryResponse

from app.prompts.prompt_template import PromptTemplate

from app.services.retriever import Retriever
from app.services.citations import CitationService

from app.validator.validator import RetrievalValidator

router = APIRouter(
    prefix="/query",
    tags=["Query"],
)


@router.post(
    "/",
    response_model=QueryResponse,
)
async def query_documents(
    request: Request,
    query: QueryRequest,
):
    """
    Query indexed PDF documents.
    """

    start_time = time.time()

    # ----------------------------------------------------
    # Validate Request
    # ----------------------------------------------------

    if (
        query.mode in (
            "answer",
            "answer_insights",
        )
        and
        not query.question.strip()
    ):

        raise HTTPException(
            status_code=400,
            detail="Question is required.",
        )

    # ----------------------------------------------------
    # Shared Services
    # ----------------------------------------------------

    embedding_service = request.app.state.embedding_service

    vector_store = request.app.state.vector_store

    generator = request.app.state.generator

    # ----------------------------------------------------
    # Retrieval
    # ----------------------------------------------------

    retriever = request.app.state.retriever

    if vector_store.index.ntotal == 0:
        raise HTTPException(
        status_code=400,
        detail="No documents have been uploaded yet."
    )

    retrieved_chunks = retriever.retrieve(
        query.question
    )

    # ----------------------------------------------------
    # Validation
    # ----------------------------------------------------

    validator = request.app.state.validator

    validation = validator.validate(
        retrieved_chunks
    )

    # ----------------------------------------------------
    # Low Confidence
    # ----------------------------------------------------

    if not validation["should_generate"]:

        return QueryResponse(

            answer="Insufficient evidence found in uploaded documents.",

            confidence=validation["confidence"],

            confidence_score=round(
                validation["final_score"],
                3,
            ),

            citations=[],

            processing_time=round(
                time.time() - start_time,
                2,
            ),

            source_preview=[],
        )

    # ----------------------------------------------------
    # Prompt
    # ----------------------------------------------------

    prompt = PromptTemplate.build(

        question=query.question,

        retrieved_chunks=retrieved_chunks,

        mode=query.mode,
    )

    # ----------------------------------------------------
    # Generation
    # ----------------------------------------------------

    answer = generator.generate(
        prompt
    )

    # ----------------------------------------------------
    # Citations
    # ----------------------------------------------------

    citations = CitationService.generate(
        retrieved_chunks
    )

    # ----------------------------------------------------
    # Source Preview
    # ----------------------------------------------------


    processing_time = round(
        time.time() - start_time,
        2,
    )

    logger.info(
        f"Query completed in "
        f"{processing_time}s"
    )

    return QueryResponse(

        answer=answer,

        confidence=validation["confidence"],

        confidence_score=round(
            validation["final_score"],
            3,
        ),

        citations=citations,

        processing_time=processing_time,

    )