"""
Request and response models for code explainator AI function.
"""

from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum

class UserSkillLevel(str, Enum):
    """Possible user skill levels"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class CodeExplainRequest(BaseModel):
    """Request model for code explanator"""
    code: str = Field(..., min_length=10, description="The code to be explained.")
    language: Optional[str] = Field(default="python", description="Programming language")
    level: Optional[UserSkillLevel] = Field(
        default=UserSkillLevel.BEGINNER,
        description="User level skill."
    ) 

class CodeExplainResponse(BaseModel):
    """Response model for code explanator"""
    explanation: str
    language: str = "python"
    level: UserSkillLevel = "beginner"