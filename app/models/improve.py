"""
Request and response models for code improving AI function.
"""

from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum

class UserSkillLevel(str, Enum):
    """Possible user skill levels"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class CodeImproveRequest(BaseModel):
    """Request model for code improver"""
    code: str = Field(..., min_length=10, description="The code to be explained.")
    language: Optional[str] = Field(default="python", description="Programming language")
    level: Optional[UserSkillLevel] = Field(
        default=UserSkillLevel.BEGINNER,
        description="User level skill."
    ) 

class CodeImproveResponse(BaseModel):
    """Response model for code improver"""
    improve: str
    language: str = "python"
    level: UserSkillLevel = "beginner"
