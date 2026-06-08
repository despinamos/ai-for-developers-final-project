from pydantic import BaseModel, Field

class RAGQuestionRequest(BaseModel):
    question: str = Field(..., min_length=3)
    top_k: int = 4


class RAGQuestionResponse(BaseModel):
    answer: str
    sources: list[str]


class RAGUploadResponse(BaseModel):
    filename: str
    chunk_count: int
    chunks_stored: int
    preview: str