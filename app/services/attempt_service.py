"""
Attempt service: record and fetch attempts.

- Stores correctness and time taken.
- Provides retrieval by user id.
"""

from typing import List
from sqlalchemy.orm import Session

from ..db import SessionLocal, Attempt


class AttemptService:
    @staticmethod
    def record_attempt(user_id: int, question_id: int, correct: bool, time_taken: float):
        db: Session = SessionLocal()
        try:
            att = Attempt(
                user_id=user_id,
                question_id=question_id,
                correct=bool(correct),
                time_taken=float(time_taken),
            )
            db.add(att)
            db.commit()
            db.refresh(att)
            return att
        finally:
            db.close()

    @staticmethod
    def get_attempts_by_user(user_id: int) -> List[Attempt]:
        db: Session = SessionLocal()
        try:
            attempts = db.query(Attempt).filter(Attempt.user_id == user_id).all()
            return attempts
        finally:
            db.close()