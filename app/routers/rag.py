from fastapi import APIRouter, UploadFile, File, HTTPException, status
from fastapi.responses import StreamingResponse

import logging
from app.dependencies import CurrentUser, SessionDep
from app.services.rag_service import RAGService
from app.services.history import HistoryService
from app.schemas.rag import (
    RAGQuestionRequest,
    RAGQuestionResponse,
    RAGUploadResponse
)

router = APIRouter(prefix="/rag", tags=["RAG"])
logger = logging.getLogger(__name__)


@router.post("/upload", response_model=RAGUploadResponse)
async def upload_file(current_user: CurrentUser, file: UploadFile = File(...)):
    try:
        result = await RAGService.index_uploaded_file(
            file=file,
            user_id=current_user.id
        )

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


@router.post("/ask", response_model=RAGQuestionResponse)
def ask_question(request: RAGQuestionRequest, current_user: CurrentUser, session: SessionDep):
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