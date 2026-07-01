"""
Embedding Service

Generates vector embeddings for document chunks using
Sentence Transformers.
"""

from sentence_transformers import SentenceTransformer
from tqdm import tqdm

from app.core.config import settings
from app.core.logger import logger


class EmbeddingService:
    """
    Generate embeddings for document chunks.
    """

    def __init__(self):
        logger.info(
            f"Loading embedding model: {settings.EMBEDDING_MODEL}"
        )

        self.model = SentenceTransformer(
            settings.EMBEDDING_MODEL
        )

        logger.info("Embedding model loaded successfully.")

    def generate_embeddings(self, chunks: list) -> list:
        """
        Generate embeddings for every chunk.

        Parameters
        ----------
        chunks : list

        Returns
        -------
        list
            Updated chunks containing embeddings.
        """

        logger.info(
            f"Generating embeddings for {len(chunks)} chunks..."
        )

        # Extract all chunk texts
        texts = [
            chunk["chunk_text"]
            for chunk in chunks
        ]

        # Generate embeddings in batches
        embeddings = self.model.encode(
            texts,
            batch_size=32,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=True,
        )

        # Attach embeddings back to chunk objects
        for chunk, embedding in zip(chunks, embeddings):
            chunk["embedding"] = embedding

        logger.info(
            "Embeddings generated successfully."
        )

        return chunks