"""
Document Chunking Service

Splits extracted PDF pages into smaller overlapping chunks.
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.config import settings
from app.core.logger import logger


class DocumentChunker:
    """
    Chunk PDF pages into overlapping text chunks.
    """

    def __init__(self):

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            length_function=len,
        )

    def chunk_document(self, pages, filename):
        """
        Convert extracted pages into chunk objects.

        Parameters
        ----------
        pages : list
            Output from PDFParser

        filename : str
            Original PDF filename

        Returns
        -------
        list
            Chunk objects with metadata
        """

        chunks = []

        chunk_id = 1

        for page in pages:

            page_chunks = self.text_splitter.split_text(page["text"])

            for chunk in page_chunks:

                chunks.append(
                    {
                        "chunk_id": chunk_id,
                        "filename": filename,
                        "page_number": page["page_number"],
                        "chunk_text": chunk,
                    }
                )

                chunk_id += 1

        logger.info(f"Generated {len(chunks)} chunks.")

        return chunks