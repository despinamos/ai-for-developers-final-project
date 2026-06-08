from fastapi import APIRouter, UploadFile, File

from app.services.rag_service import RAGService
from app.schemas.rag import (
    RAGQuestionRequest,
    RAGQuestionResponse,
    RAGUploadResponse
)

router = APIRouter(prefix="/rag", tags=["RAG"])


@router.post("/upload", response_model=RAGUploadResponse)
async def upload_file(file: UploadFile = File(...)):
    result = await RAGService.index_uploaded_file(file)

    return RAGUploadResponse(**result)


@router.post("/ask", response_model=RAGQuestionResponse)
def ask_question(request: RAGQuestionRequest):
    result = RAGService.answer_question(
        question=request.question,
        top_k=request.top_k
    )

    return RAGQuestionResponse(**result)