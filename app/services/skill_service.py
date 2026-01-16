"""
Skill service computes simple aggregated statistics:

- Accuracy by topic (domain)
- Accuracy by difficulty
- Average time per topic

These features are intentionally straightforward to allow the ML model
(input to logistic regression) to be explainable for viva.
"""

from typing import Dict, List
from collections import defaultdict

from ..db import Attempt


class SkillService:
    @staticmethod
    def compute_overall_stats(attempts: List[Attempt]) -> Dict:
        """
        From a list of Attempt objects compute:
        - overall_accuracy
        - accuracy_by_domain: {domain: accuracy}
        - accuracy_by_difficulty: {difficulty: accuracy}
        - avg_time_by_domain: {domain: avg_time}
        """
        total = len(attempts)
        if total == 0:
            return {
                "overall_accuracy": 0.0,
                "accuracy_by_domain": {},
                "accuracy_by_difficulty": {},
                "avg_time_by_domain": {},
            }

        correct = 0
        domain_counts = defaultdict(int)
        domain_correct = defaultdict(int)
        domain_time = defaultdict(float)
        difficulty_counts = defaultdict(int)
        difficulty_correct = defaultdict(int)

        for a in attempts:
            q = a.question
            if a.correct:
                correct += 1
                domain_correct[q.domain] += 1
                difficulty_correct[q.difficulty] += 1
            domain_counts[q.domain] += 1
            domain_time[q.domain] += a.time_taken
            difficulty_counts[q.difficulty] += 1

        overall_accuracy = correct / total if total > 0 else 0.0

        accuracy_by_domain = {
            d: (domain_correct[d] / domain_counts[d]) if domain_counts[d] > 0 else 0.0
            for d in domain_counts
        }
        accuracy_by_difficulty = {
            diff: (difficulty_correct[diff] / difficulty_counts[diff])
            if difficulty_counts[diff] > 0
            else 0.0
            for diff in difficulty_counts
        }
        avg_time_by_domain = {
            d: (domain_time[d] / domain_counts[d]) if domain_counts[d] > 0 else 0.0
            for d in domain_counts
        }

        return {
            "overall_accuracy": overall_accuracy,
            "accuracy_by_domain": accuracy_by_domain,
            "accuracy_by_difficulty": accuracy_by_difficulty,
            "avg_time_by_domain": avg_time_by_domain,
        }