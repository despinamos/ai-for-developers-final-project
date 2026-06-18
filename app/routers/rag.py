"""
RAG router - RAG Assistant endpoints

POST /rag/upload → upload new document
GET /rag/documents → get documents uploaded by current user
POST /rag/ask → ask a question to Rag Assistant and return simple answer
POST /rag/ask/stream → ask a question to Rag Assistant and return streaming response
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlmodel import select

import logging
from app.dependencies import CurrentUser, SessionDep
from app.services.rag_service import RAGService
from app.services.history import HistoryService
from app.models.rag_document import RagDocument
from app.schemas.rag import (
    RAGQuestionRequest,
    RAGQuestionResponse,
    RAGUploadResponse
)

router = APIRouter(prefix="/rag", tags=["RAG"])
logger = logging.getLogger(__name__)


@router.post("/upload", response_model=RAGUploadResponse)
async def upload_file(
    current_user: CurrentUser, 
    session: SessionDep, 
    file: UploadFile = File(...)
):
    """Uploads a file to RAG assistant."""
    try:
        result = await RAGService.index_uploaded_file(
            file=file,
            user_id=current_user.id
        )

        doc = RagDocument(
            document_id=result["document_id"],
            user_id=current_user.id,
            filename=result["filename"],
            chunk_count=result["chunk_count"],
        )

        session.add(doc)
        session.commit()
        session.refresh(doc)

        return RAGUploadResponse(**result)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

    except Exception as e:
        print("RAG Upload Error:", repr(e))

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"File upload failed: {str(e)}"
        )
    
@router.get("/documents")
def get_user_documents(
    current_user: CurrentUser,
    session: SessionDep
):
    """Returns user uploaded documents."""
    try: 
        documents = session.exec(
            select(RagDocument)
            .where(RagDocument.user_id == current_user.id)
            .order_by(RagDocument.created_at.desc())
        ).all()

        return documents
    
    except Exception as e:
        print("Error returning user documents: ",e)


@router.post("/ask", response_model=RAGQuestionResponse)
def ask_question(
    request: RAGQuestionRequest, 
    current_user: CurrentUser, 
    session: SessionDep
):
    """Sends question to RAG assistant with simple response."""

    if not request.document_id:
        raise HTTPException(
            status_code=400,
            detail="Please upload or select a document first."
        )

    try:
        result = RAGService.answer_question(
            question=request.question,
            document_id=request.document_id,
            top_k=request.top_k,
            user_id=current_user.id
        )

        HistoryService.save(
            session=session,
            user_id=current_user.id,
            action="ask rag",
            input_text=request.question,
            ai_response=result["answer"],
        )

        return RAGQuestionResponse(**result)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception as e:
        print("RAG Ask Error:", repr(e))

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Question answering failed: {str(e)}"
        )
    
@router.post("/ask/stream")
def ask_question_stream(
    request: RAGQuestionRequest,
    current_user: CurrentUser,
    session: SessionDep
):
    """Sends question to RAG assistant and returns a streaming response."""

    if not request.document_id:
        raise HTTPException(
            status_code=400,
            detail="Please upload or select a document first."
        )
    
    try:
        def generate():
            full_response = ""

            for chunk in RAGService.answer_question_stream(
                question=request.question,
                document_id=request.document_id,
                top_k=request.top_k,
                user_id=current_user.id
            ):
                full_response += chunk
                yield chunk

            HistoryService.save(
                session=session,
                user_id=current_user.id,
                action="ask rag",
                input_text=request.question,
                ai_response=full_response,
            )

        return StreamingResponse(
            generate(),
            media_type="text/plain"
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception as e:
        logger.exception("RAG streaming ask failed")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Streaming question answering failed: {str(e)}"
        )