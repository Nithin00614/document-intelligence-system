"""
Upload API

Handles PDF uploads, indexing and vector database updates.
"""

from pathlib import Path
from typing import Annotated

from fastapi import (
    APIRouter,
    File,
    HTTPException,
    Request,
    UploadFile,
)

from app.core.config import settings
from app.core.logger import logger

from app.schemas.response import UploadResponse

from app.services.parser import PDFParser
from app.services.chunker import DocumentChunker

from app.utils.helpers import (
    is_pdf_file,
    calculate_file_hash,
    save_uploaded_file,
    is_duplicate,
    store_file_hash,
)

router = APIRouter(
    prefix="/upload",
    tags=["Upload"],
)


@router.post(
    "/",
    response_model=UploadResponse,
)
async def upload_documents(
    request: Request,
    files: Annotated[list[UploadFile], File(...)],
):
    """
    Upload and index PDF documents.
    """

    # ----------------------------------------------------
    # Validate Upload Count
    # ----------------------------------------------------

    if not files:

        raise HTTPException(
            status_code=400,
            detail="No PDF files uploaded.",
        )

    if len(files) > settings.MAX_UPLOAD_FILES:

        raise HTTPException(
            status_code=400,
            detail=f"Maximum {settings.MAX_UPLOAD_FILES} PDFs allowed.",
        )

    parser = request.app.state.parser

    chunker = request.app.state.chunker

    embedding_service = request.app.state.embedding_service

    vector_store = request.app.state.vector_store

    uploaded_files = 0

    total_chunks = []

    upload_directory = settings.UPLOAD_DIR

    # ----------------------------------------------------
    # Process Each File
    # ----------------------------------------------------

    for upload in files:

        # ------------------------------------------------
        # Reject Non-PDF Files
        # ------------------------------------------------

        if not is_pdf_file(upload):

            logger.warning(
                f"Rejected non-PDF file: {upload.filename}"
            )

            raise HTTPException(
                status_code=400,
                detail=f"{upload.filename} is not a PDF file.",
            )

        file_bytes = await upload.read()

        file_hash = calculate_file_hash(
            file_bytes
        )

        if is_duplicate(
            file_hash,
            upload_directory,
        ):

            logger.info(
                f"Duplicate skipped: {upload.filename}"
            )

            continue

        destination = (
            upload_directory /
            upload.filename
        )

        # ------------------------------------------------
        # Save Uploaded File
        # ------------------------------------------------

        try:

            save_uploaded_file(
                file_bytes,
                destination,
            )

        except Exception as e:

            logger.exception(e)

            raise HTTPException(
                status_code=500,
                detail=f"Failed to save {upload.filename}.",
            )

        store_file_hash(
            file_hash,
            upload_directory,
        )

        logger.info(
            f"Saved: {upload.filename}"
        )

        pages = parser.parse(
            str(destination)
        )

        chunks = chunker.chunk_document(
            pages,
            upload.filename,
        )

        # ------------------------------------------------
        # Generate Embeddings
        # ------------------------------------------------

        try:

            chunks = embedding_service.generate_embeddings(
                chunks
            )

        except Exception as e:

            logger.exception(e)

            raise HTTPException(
                status_code=500,
                detail="Embedding generation failed.",
            )

        total_chunks.extend(
            chunks
        )

        uploaded_files += 1

    # ----------------------------------------------------
    # No New Documents
    # ----------------------------------------------------

    if uploaded_files == 0:

        raise HTTPException(
            status_code=400,
            detail="No new PDF documents were uploaded.",
        )

    # ----------------------------------------------------
    # Update Vector Store
    # ----------------------------------------------------

    try:

        vector_store.add_documents(
            total_chunks
        )

        vector_store.save()

    except Exception as e:

        logger.exception(e)

        raise HTTPException(
            status_code=500,
            detail="Failed to update vector database.",
        )

    logger.info(
        f"Indexed {len(total_chunks)} chunks."
    )

    return UploadResponse(

        success=True,

        uploaded_files=uploaded_files,

        processed_chunks=len(
            total_chunks
        ),

        message="Documents uploaded successfully.",

    )