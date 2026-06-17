"""
AI Router - AI functions endpoints.

POST /ai/explain → explain user's code
POST /ai/review → review user's code
POST /ai/improve → improve user's code

POST /ai/explain/stream → explain user's code with stream response
POST /ai/review/stream → review user's code with stream response
POST /ai/improve/stream → improve user's code with stream response
"""

import logging
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.schemas.explain import CodeExplainRequest, CodeExplainResponse
from app.schemas.review import CodeReviewRequest, CodeReviewResponse
from app.schemas.improve import CodeImproveRequest, CodeImproveResponse
from app.services.history import HistoryService
from app.services.llm_service import LLMService

from app.dependencies import CurrentUser, SessionDep

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/ai", tags=["LLM"])

@router.post(
    "/explain",
    response_model=CodeExplainResponse
)
def explain_code(
    request: CodeExplainRequest,
    session: SessionDep,
    current_user: CurrentUser
):
    """
    Calls LLM to explain code provided by user.
    Saves user input and ai response in user's history.
    """

    try:
        explanation = LLMService.explain_code(
            system_prompt=request.system_prompt,
            code=request.code,
            language=request.language,
            level=request.level
        )

        HistoryService.save(
            session=session,
            user_id=current_user.id,
            action="explain",
            input_text=request.code,
            ai_response=explanation,
        )

        return CodeExplainResponse(
            explanation=explanation,
            language=request.language,
            level=request.level
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception:
        logger.exception("Explain code failed")

        raise HTTPException(
            status_code=500,
            detail="Failed to explain code."
        )

@router.post("/explain/stream")
def explain_code_stream(
    request: CodeExplainRequest,
    session: SessionDep,
    current_user: CurrentUser
):
    """
    Calls LLM to explain code provided by user.
    Saves user input and ai response in user's history.
    Returns streaming answer.
    """
    try:
        def generate():
            full_response = ""

            for chunk in LLMService.explain_code_stream(
                system_prompt=request.system_prompt,
                code=request.code,
                language=request.language,
                level=request.level
            ):
                full_response += chunk
                yield chunk

            HistoryService.save(
                session=session,
                user_id=current_user.id,
                action="explain",
                input_text=request.code,
                ai_response=full_response,
            )

        return StreamingResponse(
            generate(),
            media_type="text/plain"
        )
    except Exception:
        logger.exception("Explain code stream failed")

        raise HTTPException(
            status_code=500,
            detail="Failed to stream code explanation."
        )

@router.post(
    "/review",
    response_model=CodeReviewResponse
)
def review_code(
    request: CodeReviewRequest,
    session: SessionDep,
    current_user: CurrentUser
):
    """
    Calls LLM to review code provided by user.
    Saves user input and AI response in user history.
    """
    try:
        review = LLMService.review_code(
            system_prompt=request.system_prompt,
            code=request.code,
            language=request.language,
            level=request.level
        )

        HistoryService.save(
            session=session,
            user_id=current_user.id,
            action="review",
            input_text=request.code,
            ai_response=review,
        )

        return CodeReviewResponse(
            review=review,
            language=request.language,
            level=request.level
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception:
        logger.exception("Review code failed")

        raise HTTPException(
            status_code=500,
            detail="Failed to review code."
        )

@router.post("/review/stream")
def review_code_stream(
    request: CodeReviewRequest,
    session: SessionDep,
    current_user: CurrentUser
):
    """
    Calls LLM to review code provided by user.
    Saves user input and ai response in user's history.
    Returns streaming answer.
    """
    try:
        def generate():
            full_response = ""

            for chunk in LLMService.review_code_stream(
                system_prompt=request.system_prompt,
                code=request.code,
                language=request.language,
                level=request.level
            ):
                full_response += chunk
                yield chunk

            HistoryService.save(
                session=session,
                user_id=current_user.id,
                action="review",
                input_text=request.code,
                ai_response=full_response,
            )

        return StreamingResponse(
            generate(),
            media_type="text/plain"
        )
    except Exception:
        logger.exception("Review code stream failed")

        raise HTTPException(
            status_code=500,
            detail="Failed to stream code review."
        )

@router.post(
    "/improve",
    response_model=CodeImproveResponse
)
def improve_code(
    request: CodeImproveRequest,
    session: SessionDep,
    current_user: CurrentUser
):
    """
    Calls LLM to improve code provided by user.
    Saves user input and AI response to user history.
    """

    try:
        improve = LLMService.improve_code(
            system_prompt=request.system_prompt,
            code=request.code,
            language=request.language,
            level=request.level
        )

        HistoryService.save(
            session=session,
            user_id=current_user.id,
            action="improve",
            input_text=request.code,
            ai_response=improve,
        )

        return CodeImproveResponse(
            improve=improve,
            language=request.language,
            level=request.level
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception:
        logger.exception("Improve code failed")

        raise HTTPException(
            status_code=500,
            detail="Failed to improve code."
        )

@router.post("/improve/stream")
def improve_code_stream(
    request: CodeImproveRequest,
    session: SessionDep,
    current_user: CurrentUser
):
    """
    Calls LLM to improve code provided by user.
    Saves user input and ai response in user's history.
    Returns streaming answer.
    """
    try:
        def generate():
            full_response = ""

            for chunk in LLMService.improve_code_stream(
                system_prompt=request.system_prompt,
                code=request.code,
                language=request.language,
                level=request.level
            ):
                full_response += chunk
                yield chunk

            HistoryService.save(
                session=session,
                user_id=current_user.id,
                action="improve",
                input_text=request.code,
                ai_response=full_response,
            )

        return StreamingResponse(
            generate(),
            media_type="text/plain"
        )
    except Exception:
        logger.exception("Improve code stream failed")

        raise HTTPException(
            status_code=500,
            detail="Failed to stream code improvement."
        )