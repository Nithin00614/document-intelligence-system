"""
Main Application

Initializes the FastAPI application,
shared services and API routers.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.health import router as health_router
from app.api.upload import router as upload_router
from app.api.query import router as query_router

from app.core.logger import logger

from app.services.parser import PDFParser
from app.services.chunker import DocumentChunker
from app.services.embeddings import EmbeddingService
from app.services.vector_store import VectorStore
from app.services.generator import AnswerGenerator
from app.services.retriever import Retriever

from app.validator.validator import RetrievalValidator
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Initialize shared services once when the application starts.
    """

    logger.info("Starting Document Intelligence System...")

    # ------------------------------------------
    # Core Services
    # ------------------------------------------

    app.state.parser = PDFParser()

    app.state.chunker = DocumentChunker()

    app.state.embedding_service = EmbeddingService()

    app.state.generator = AnswerGenerator()

    app.state.vector_store = VectorStore()

    # ------------------------------------------
    # Load Existing Vector Database (Optional)
    # ------------------------------------------

    try:

        app.state.vector_store.load()

        logger.info(
            "Existing vector database loaded."
        )

    except Exception:

        logger.info(
            "No existing vector database found. "
            "A new index will be created after upload."
        )

    # ------------------------------------------
    # Shared Services
    # ------------------------------------------

    app.state.retriever = Retriever(
        app.state.embedding_service,
        app.state.vector_store,
    )

    app.state.validator = RetrievalValidator()

    logger.info("Application started successfully.")

    yield

    logger.info("Application shutting down.")


app = FastAPI(

    title="Document Intelligence System",

    version="1.0.0",

    description="RAG-based Document Intelligence System",

    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)

# ------------------------------------------
# Static Files
# ------------------------------------------

app.mount(
    "/static",
    StaticFiles(directory="frontend"),
    name="static",
)

# ------------------------------------------
# Routers
# ------------------------------------------

app.include_router(health_router)

app.include_router(upload_router)

app.include_router(query_router)


@app.get("/")
async def root():
    """
    Root endpoint.
    """

    return {
        "message": "Document Intelligence System API",
        "docs": "/docs",
    }