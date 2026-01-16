"""
Baseline generator returns diagnostic questions without ML.

- Picks random questions of mixed difficulty.
- Ensures no repeats within session.
- Used for initial diagnostic test.
"""

import random
from typing import Optional
from sqlalchemy.orm import Session

from ..db import Question


class BaselineGenerator:
    @staticmethod
    def next_question(db: Session, session: dict) -> Optional[Question]:
        """
        Select next diagnostic question randomly across difficulties.
        """
        attempted = set(session.get("attempted", []))
        # Fetch all question ids
        all_qs = db.query(Question).all()
        candidates = [q for q in all_qs if q.id not in attempted]
        if not candidates:
            return None
        # Prefer mixed difficulties by random choice
        # pick randomly among remaining
        return random.choice(candidates)