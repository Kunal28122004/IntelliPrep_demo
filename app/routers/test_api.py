"""
API endpoints for test flow:
- GET /api/next_question/{session_id} : returns next question JSON
- POST /api/submit_answer : accepts answer and stores attempt, returns next question or completion
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from ..services.session_service import SessionService
from ..services.attempt_service import AttemptService
from ..services.skill_service import SkillService
from ..test_engine.baseline_generator import BaselineGenerator
from ..test_engine.adaptive_generator import AdaptiveGenerator
from ..db import SessionLocal, Question, User
from ..test_engine.model_loader import ModelLoader

router = APIRouter()


class SubmitAnswerRequest(BaseModel):
    session_id: int
    username: str
    question_id: int
    selected_option: int
    time_taken: float


@router.get("/next_question/{session_id}")
def api_next_question(session_id: int, username: Optional[str] = None):
    """
    Returns next question for the given session.
    On diagnostic phase, baseline generator supplies questions.
    After that adaptive generator chooses questions using ML predictions.
    """
    session = SessionService.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == session["username"]).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # If session in diagnostic mode, use baseline; after diagnostic use adaptive
        if not session.get("diagnostic_done"):
            q = BaselineGenerator.next_question(db, session)
            if q is None:
                # mark diagnostic done
                SessionService.mark_diagnostic_done(session_id)
                # fallback to adaptive selection
                q = AdaptiveGenerator.next_question(db, user.id, session)
        else:
            q = AdaptiveGenerator.next_question(db, user.id, session)

        if q is None:
            return {"complete": True}
        return {
            "complete": False,
            "question": {
                "id": q.id,
                "text": q.text,
                "options": q.get_options(),
                "difficulty": q.difficulty,
                "domain": q.domain,
            },
        }
    finally:
        db.close()


@router.post("/submit_answer")
def submit_answer(payload: SubmitAnswerRequest):
    """
    Store attempt, recompute stats and return next question hint.
    """
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == payload.username).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        question = db.query(Question).get(payload.question_id)
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")

        correct = payload.selected_option == question.correct_option
        # Store attempt
        AttemptService.record_attempt(
            user_id=user.id,
            question_id=question.id,
            correct=correct,
            time_taken=payload.time_taken,
        )

        # Add to session record
        SessionService.add_attempt_to_session(payload.session_id, question.id)

        # After storing attempt we can compute stats (used by adaptive generator)
        attempts = AttemptService.get_attempts_by_user(user.id)
        stats = SkillService.compute_overall_stats(attempts)

        # For convenience return correctness and a next_question flag
        next_info = {"correct": correct, "stats": stats}
        return next_info
    finally:
        db.close()