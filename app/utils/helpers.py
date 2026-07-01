"""
Reusable helper functions for the application.
"""

import hashlib
import re
import time
from pathlib import Path
from fastapi import UploadFile

from app.core.config import settings


def is_allowed_file(filename: str) -> bool:
    """
    Check whether the uploaded file has a valid extension.
    """
    return Path(filename).suffix.lower() in settings.ALLOWED_EXTENSIONS


def calculate_file_hash(file_path: str) -> str:
    """
    Calculate SHA-256 hash of a file.
    Used for duplicate detection.
    """
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while chunk := file.read(8192):
            sha256.update(chunk)

    return sha256.hexdigest()


def clean_text(text: str) -> str:
    """
    Remove excessive whitespace while preserving content.
    """
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def current_timestamp() -> float:
    """
    Return current timestamp.
    """
    return time.time()


def elapsed_time(start_time: float) -> float:
    """
    Return elapsed processing time in seconds.
    """
    return round(time.time() - start_time, 3)


def bytes_to_mb(size: int) -> float:
    """
    Convert bytes to megabytes.
    """
    return round(size / (1024 * 1024), 2)



def is_pdf_file(file: UploadFile) -> bool:
    """
    Validate uploaded file is a PDF.
    """

    return (
        file.filename is not None
        and file.filename.lower().endswith(".pdf")
    )


def calculate_file_hash(file_bytes: bytes) -> str:
    """
    Generate SHA-256 hash of uploaded file.
    """

    return hashlib.sha256(file_bytes).hexdigest()


def save_uploaded_file(
    file_bytes: bytes,
    destination: Path,
) -> None:
    """
    Save uploaded PDF to disk.
    """

    destination.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(destination, "wb") as file:
        file.write(file_bytes)


def is_duplicate(
    file_hash: str,
    uploaded_directory: Path,
) -> bool:
    """
    Check whether a PDF with identical hash
    has already been uploaded.
    """

    hash_file = uploaded_directory / "document_hashes.txt"

    if not hash_file.exists():
        return False

    with open(hash_file, "r") as file:

        hashes = {
            line.strip()
            for line in file.readlines()
        }

    return file_hash in hashes


def store_file_hash(
    file_hash: str,
    uploaded_directory: Path,
) -> None:
    """
    Store SHA-256 hash after successful upload.
    """

    hash_file = uploaded_directory / "document_hashes.txt"

    with open(hash_file, "a") as file:
        file.write(file_hash + "\n")    