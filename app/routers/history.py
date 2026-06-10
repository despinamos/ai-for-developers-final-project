from sqlmodel import select
import logging
from fastapi import APIRouter

from app.dependencies import SessionDep, CurrentUser
from app.models.history import History

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/history", tags=["History"])

@router.get("/")
def get_user_history(
    session: SessionDep,
    current_user: CurrentUser
):
    records = session.exec(
        select(History)
        .where(History.user_id == current_user.id)
        .order_by(History.created_at.desc())
    ).all()

    return records