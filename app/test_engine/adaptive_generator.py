"""
Adaptive generator uses ML predictions to pick the next question.

- For all unattempted questions predict probability of correct answer.
- Prefer questions with probability in 0.4-0.7 (moderate difficulty).
- Avoid repeated questions.
- If none fall in window, select one with probability closest to 0.55.
- If still none (edge cases), pick a medium question randomly.
"""

import random
from typing import Optional, List
from sqlalchemy.orm import Session

from .feature_builder import build_features
from .model_loader import ModelLoader
from ..services.skill_service import SkillService
from ..services.attempt_service import AttemptService
from ..db import Question


class AdaptiveGenerator:
    @staticmethod
    def next_question(db: Session, user_id: int, session: dict) -> Optional[Question]:
        """
        Choose next question using ML predictions.

        - Gather user's attempts to compute stats
        - For each candidate question build features and predict probability
        - Choose according to selection policy described above
        """
        # Fetch user attempts and compute stats
        attempts = AttemptService.get_attempts_by_user(user_id)
        stats = SkillService.compute_overall_stats(attempts)

        attempted = set(session.get("attempted", []))
        all_qs: List[Question] = db.query(Question).all()
        candidates = [q for q in all_qs if q.id not in attempted]
        if not candidates:
            return None

        # Build feature matrix and predict probabilities
        features_list = []
        q_map = []
        for q in candidates:
            q_meta = {"difficulty": q.difficulty, "domain": q.domain}
            feat = build_features(stats, q_meta)
            features_list.append(feat)
            q_map.append(q)

        import numpy as np

        X = np.vstack(features_list)
        probs = ModelLoader.predict_probability(X)  # array of probabilities

        # Pair candidates with probs
        paired = list(zip(q_map, probs))
        # Filter for moderate probability window
        moderate = [p for p in paired if 0.4 <= p[1] <= 0.7]
        if moderate:
            # choose one with probability closest to 0.55 to maximize information gain
            chosen = min(moderate, key=lambda x: abs(x[1] - 0.55))[0]
            return chosen

        # If no moderate, pick candidate closest to 0.55
        chosen = min(paired, key=lambda x: abs(x[1] - 0.55))[0]
        if chosen:
            return chosen

        # Fallback: pick random medium difficulty question
        medium = [q for q in candidates if q.difficulty == "medium"]
        if medium:
            return random.choice(medium)
        # Final fallback: random
        return random.choice(candidates)