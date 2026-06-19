"""
RAG Document Model — SQLModel table definition.
"""


from datetime import datetime, UTC
from typing import Optional
from sqlmodel import SQLModel, Field


class RagDocument(SQLModel, table=True):
    """Document uploaded by use to RAG assistant."""
    id: Optional[int] = Field(default=None, primary_key=True)

    document_id: str = Field(index=True, unique=True)
    user_id: int = Field(foreign_key="user.id")

    filename: str
    chunk_count: int

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )