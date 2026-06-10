"""
AI Router - AI functions endpoints.

TODO POST /ai/explain
TODO POST /ai/review
TODO POST /ai/improve
"""

import logging
from fastapi import APIRouter, Request, HTTPException

from app.models.explain import CodeExplainRequest, CodeExplainResponse
from app.models.review import CodeReviewRequest, CodeReviewResponse
from app.models.improve import CodeImproveRequest, CodeImproveResponse
# from app.llm_client import LLMClient
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

@router.post(
    "/review",
    response_model=CodeReviewResponse
)
def review_code(request: CodeReviewRequest):
    """
    Calls LLM to review code provided by user.
    """

    review = LLMService.review_code(
        system_prompt=request.system_prompt,
        code=request.code,
        language=request.language,
        level=request.level
    )

    return CodeReviewResponse(
        review=review,
        language=request.language,
        level=request.level
    )

@router.post(
    "/improve",
    response_model=CodeImproveResponse
)
def improve_code(request: CodeImproveRequest):
    """
    Calls LLM to improve code provided by user.
    """

    improve = LLMService.improve_code(
        system_prompt=request.system_prompt,
        code=request.code,
        language=request.language,
        level=request.level
    )

    return CodeImproveResponse(
        improve=improve,
        language=request.language,
        level=request.level
    )