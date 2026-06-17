"""
History router - History endpoints

GET /history/ → return user's records
"""

from sqlmodel import select
import logging
from fastapi import APIRouter, HTTPException, status

from app.dependencies import SessionDep, CurrentUser
from app.models.history import History

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/history", tags=["History"])

@router.get("/")
def get_user_history(
    session: SessionDep,
    current_user: CurrentUser
):
    """Returns all records of user's history."""

    try: 
        records = session.exec(
            select(History)
            .where(History.user_id == current_user.id)
            .order_by(History.created_at.desc())
        ).all()

        return records
    except Exception as e:
        logger.exception(
            f"Failed to retrieve history for user {current_user.id}"
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user history."
        )