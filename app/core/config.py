"""
Application Configuration

Central place for all configurable settings.
"""

from pathlib import Path
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()


class Settings:
    """
    Global application settings.
    """

    # ==========================================================
    # Project Directories
    # ==========================================================

    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    UPLOAD_DIR = BASE_DIR / "uploads"
    VECTOR_DB_DIR = BASE_DIR / "vector_db"
    LOG_DIR = BASE_DIR / "logs"

    # Create directories automatically
    UPLOAD_DIR.mkdir(exist_ok=True)
    VECTOR_DB_DIR.mkdir(exist_ok=True)
    LOG_DIR.mkdir(exist_ok=True)

    # ==========================================================
    # Upload Settings
    # ==========================================================

    MAX_UPLOAD_FILES = 50

    ALLOWED_EXTENSIONS = {".pdf"}

    # ==========================================================
    # Chunking Configuration
    # ==========================================================

    CHUNK_SIZE = 800

    CHUNK_OVERLAP = 120

    MAX_CONTEXT_CHARS = 4000

    # ==========================================================
    # Retrieval Configuration
    # ==========================================================

    TOP_K = 5

    SIMILARITY_THRESHOLD = 0.70

    HIGH_CONFIDENCE_THRESHOLD = 0.75

    MEDIUM_CONFIDENCE_THRESHOLD = 0.60

    # ==========================================================
    # Embedding Model
    # ==========================================================

    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

    # ==========================================================
    # Local LLM
    # ==========================================================

    LLM_MODEL = "google/flan-t5-base"

    MAX_NEW_TOKENS = 256

    MAX_INPUT_TOKENS = 2048

    # ==========================================================
    # Logging
    # ==========================================================

    LOG_LEVEL = "INFO"

    # ==========================================================
    # Application
    # ==========================================================

    APP_NAME = "Document Intelligence System"

    VERSION = "1.0.0"


settings = Settings()