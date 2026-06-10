from datetime import datetime, UTC
from typing import Optional
from sqlmodel import SQLModel, Field

class History(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    action: str  # explain, review, improve, rag_ask
    input_text: str
    ai_response: str

    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))