"""
AI Router - AI functions endpoints.
"""

import logging
from fastapi import APIRouter, Request, HTTPException
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

@router.post("/explain/stream")
def explain_code_stream(
    request: CodeExplainRequest,
    session: SessionDep,
    current_user: CurrentUser
):
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
    """

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

@router.post("/review/stream")
def review_code_stream(
    request: CodeReviewRequest,
    session: SessionDep,
    current_user: CurrentUser
):
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
    """

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

@router.post("/improve/stream")
def improve_code_stream(
    request: CodeImproveRequest,
    session: SessionDep,
    current_user: CurrentUser
):
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