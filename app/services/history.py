from sqlmodel import Session
from app.models.history import History

class HistoryService:

    @staticmethod
    def save(
        session: Session,
        user_id: int, 
        action: str,
        input_text: str,
        ai_response: str
    ):
        history = History(
            user_id=user_id,
            action=action,
            input_text=input_text,
            ai_response=ai_response,
        )

        session.add(history)
        session.commit()
        session.refresh(history)

        return history