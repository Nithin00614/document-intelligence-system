"""
Retriever Service

Converts user queries into embeddings and retrieves
the most relevant document chunks.
"""

from app.core.logger import logger


class Retriever:
    """
    Retrieval service.
    """

    def __init__(
        self,
        embedding_service,
        vector_store,
    ):
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    def retrieve(
        self,
        question: str,
    ):
        """
        Retrieve relevant chunks for a question.
        """

        logger.info(
            f"Retrieving documents for query: {question}"
        )

        query_embedding = (
            self.embedding_service.model.encode(
                question,
                convert_to_numpy=True,
                normalize_embeddings=True,
            )
        )

        results = self.vector_store.search(
            query_embedding
        )

        logger.info(
            f"Retrieved {len(results)} chunks."
        )

        return results