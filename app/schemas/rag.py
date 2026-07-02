"""
RAG Schemas — Pydantic models for RAG.
"""

from pydantic import BaseModel, Field

class RAGQuestionRequest(BaseModel):
    question: str = Field(..., min_length=3)
    document_id: str
    top_k: int = 4


class RAGQuestionResponse(BaseModel):
    answer: str
    sources: list[str]


class RAGUploadResponse(BaseModel):
    document_id: str
    filename: str
    chunk_count: int
    chunks_stored: int
    preview: str