"""
History Model — SQLModel table definition.
"""


from datetime import datetime, UTC
from typing import Optional
from sqlmodel import SQLModel, Field

class History(SQLModel, table=True):
    """History record belonging to a user."""
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    action: str  # explain, review, improve, ask_rag
    input_text: str
    ai_response: str

    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))