"""
PDF Parsing Service

Responsible only for extracting text from uploaded PDFs.
"""

from pathlib import Path

import fitz  # PyMuPDF

from app.core.logger import logger
from app.utils.helpers import clean_text


class PDFParser:
    """
    PDF text extraction service.
    """

    def parse(self, pdf_path: str):
        """
        Extract page-wise text from a PDF.

        Returns
        -------
        list[dict]
            [
                {
                    "page_number": 1,
                    "text": "..."
                }
            ]
        """

        pdf_path = Path(pdf_path)

        pages = []

        try:

            document = fitz.open(pdf_path)

            logger.info(
                f"Opened PDF: {pdf_path.name} ({document.page_count} pages)"
            )

            for page in document:

                text = page.get_text("text")

                text = clean_text(text)


                # Skip completely empty pages
                if not text:
                    continue

                pages.append(
                    {
                        "page_number": page.number + 1,
                        "text": text,
                    }
                )
            
            if not pages:
                    raise RuntimeError(
                        "No extractable text found in the uploaded PDF."
                    )
            
            document.close()

            logger.info(
                f"Extracted text from {len(pages)} pages."
            )

            return pages

        except Exception as e:
            logger.exception(e)

            raise RuntimeError(
                f"Unable to parse PDF: {pdf_path.name}"
            ) from e