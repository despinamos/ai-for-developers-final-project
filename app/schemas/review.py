"""
Review Schemas — Request and response pydantic models for code reviewing with AI.
"""

from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum

class UserSkillLevel(str, Enum):
    """Possible user skill levels"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class CodeReviewRequest(BaseModel):
    """Request model for code reviewer"""
    system_prompt: str
    code: str = Field(..., min_length=10, description="The code to be explained.")
    language: Optional[str] = Field(default="python", description="Programming language")
    level: Optional[UserSkillLevel] = Field(
        default=UserSkillLevel.BEGINNER,
        description="User level skill."
    ) 

class CodeReviewResponse(BaseModel):
    """Response model for code reviewer"""
    review: str
    language: str = "python"
    level: UserSkillLevel = "beginner"