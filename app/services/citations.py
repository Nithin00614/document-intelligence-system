"""
Citation Service

Formats retrieved document chunks into structured
citation objects for API responses.
"""

from typing import List

from app.schemas.response import Citation
from app.core.logger import logger


class CitationService:
    """
    Build citations from retrieved chunks.
    """

    @staticmethod
    def generate(
        retrieved_chunks: List[dict],
    ) -> List[Citation]:
        """
        Convert retrieved chunks into Citation objects.
        """

        citations = []

        seen = set()

        for chunk in retrieved_chunks:

            key = (
                chunk["document_id"],
                chunk["filename"],
                chunk["page_number"],
                chunk["chunk_id"],
            )

            if key in seen:
                continue

            seen.add(key)

            preview = chunk["chunk_text"][:200].strip()

            if len(chunk["chunk_text"]) > 200:
                preview += "..."

            citations.append(

                Citation(

                    document_id=chunk["document_id"],

                    filename=chunk["filename"],

                    page_number=chunk["page_number"],

                    chunk_id=chunk["chunk_id"],

                    source_preview=preview

                )

            )

        logger.info(
            f"Generated {len(citations)} citations."
        )

        return citations