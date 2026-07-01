"""
Vector Store Service

Handles FAISS index creation, storage, loading and similarity search.
"""

from pathlib import Path
import pickle

import faiss
import numpy as np

from app.core.config import settings
from app.core.logger import logger


class VectorStore:
    """
    FAISS Vector Store.
    """

    def __init__(self):

        self.index = None

        self.metadata = []

        self.dimension = None

        self.index_path = (
            settings.VECTOR_DB_DIR / "faiss.index"
        )

        self.metadata_path = (
            settings.VECTOR_DB_DIR / "metadata.pkl"
        )

    # =====================================================
    # Create Index
    # =====================================================

    def _initialize_index(self, embedding_dimension: int):
        """
        Initialize FAISS index.
        """

        self.dimension = embedding_dimension

        self.index = faiss.IndexFlatIP(
            embedding_dimension
        )

        logger.info(
            f"Initialized FAISS index ({embedding_dimension} dimensions)"
        )

    # =====================================================
    # Add Documents
    # =====================================================

    def add_documents(self, chunks: list):
        """
        Add embedded chunks to FAISS.
        """

        if not chunks:
            return

        if self.index is None:

            self._initialize_index(
                len(chunks[0]["embedding"])
            )

        embeddings = np.array(
            [
                chunk["embedding"]
                for chunk in chunks
            ],
            dtype="float32",
        )

        self.index.add(embeddings)

        for chunk in chunks:

            self.metadata.append(
                {
                    "chunk_id": chunk["chunk_id"],
                    "filename": chunk["filename"],
                    "page_number": chunk["page_number"],
                    "chunk_text": chunk["chunk_text"],
                    "document_id": chunk["filename"]
                }
            )

        logger.info(
            f"Stored {len(chunks)} embeddings."
        )

    # =====================================================
    # Save Index
    # =====================================================

    def save(self):
        """
        Save FAISS index and metadata.
        """

        if self.index is None:
            return

        faiss.write_index(
            self.index,
            str(self.index_path),
        )

        with open(
            self.metadata_path,
            "wb",
        ) as file:

            pickle.dump(
                self.metadata,
                file,
            )

        logger.info(
            "Vector database saved."
        )

    # =====================================================
    # Load Index
    # =====================================================

    def load(self):
        """
        Load FAISS index and metadata.
        """

        if (
            not self.index_path.exists()
            or
            not self.metadata_path.exists()
        ):

            raise FileNotFoundError(
                "Vector database not found."
            )

        self.index = faiss.read_index(
            str(self.index_path)
        )
        self.dimension = self.index.d

        with open(
            self.metadata_path,
            "rb",
        ) as file:

            self.metadata = pickle.load(file)

        logger.info(
            "Vector database loaded."
        )

    # =====================================================
    # Search
    # =====================================================

    def search(
        self,
        query_embedding,
        top_k=settings.TOP_K,
    ):
        """
        Perform similarity search.
        """

        if self.index is None:

            raise RuntimeError(
                "Vector database is empty."
            )

        query = np.array(
            [query_embedding],
            dtype="float32",
        )

        scores, indices = self.index.search(
            query,
            top_k,
        )

        results = []

        for score, index in zip(
            scores[0],
            indices[0],
        ):

            if index == -1:
                continue

            if index >= len(self.metadata):
                continue

            item = self.metadata[index].copy()

            item["score"] = float(score)

            results.append(item)

        return results