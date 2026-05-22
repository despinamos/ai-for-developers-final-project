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
from app.llm_client import LLMClient
from app.services.llm_service import LLMService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/ai", tags=["LLM"])

# def build_user_prompt(request: CodeExplainRequest) -> str:
#     """Build the user prompt for code explanator"""
#     language = request.language
#     level = request.level
#     return f"""Explain the following code step by step:
#     Language: {language}
#     User level: {level}
#     Code to explain:
#         \"\"\"
#     {request.text}
#     \"\"\"

#     Explanation: """

@router.post(
    "/explain",
    response_model=CodeExplainResponse
)
def explain_code(request: CodeExplainRequest):
    """
    Calls LLM to explain code provided by user.
    """

    explanation = LLMService.explain_code(
        code=request.code,
        language=request.language,
        level=request.level
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
        code=request.code,
        language=request.language,
        level=request.level
    )

    return CodeImproveResponse(
        improve=improve,
        language=request.language,
        level=request.level
    )