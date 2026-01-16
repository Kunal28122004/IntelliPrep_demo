"""
Feature builder:

- Converts user stats and question metadata into a numeric feature vector
  suitable for Logistic Regression inference.

Features chosen are simple and explainable:
- overall_accuracy
- accuracy_on_question_domain (if present else overall_accuracy)
- accuracy_on_question_difficulty (if present else overall_accuracy)
- avg_time_on_domain (seconds)
- difficulty_encoded (0=easy,1=medium,2=hard)
- domain_encoded (simple hash to small integer)
"""

import numpy as np


DIFFICULTY_MAP = {"easy": 0, "medium": 1, "hard": 2}


def encode_domain(domain: str) -> int:
    """
    Deterministic encoding for domain to keep feature space small.
    Uses hash modulo to keep value bounded.
    """
    return abs(hash(domain)) % 100  # 0-99


def build_features(stats: dict, question_meta: dict) -> np.ndarray:
    """
    Given user stats (from SkillService) and question metadata (dict with difficulty, domain),
    return a 1D numpy array of features in fixed order.

    Order:
    [overall_accuracy,
     accuracy_on_domain,
     accuracy_on_difficulty,
     avg_time_on_domain,
     difficulty_encoded,
     domain_encoded]
    """
    overall = float(stats.get("overall_accuracy", 0.0))
    acc_by_domain = stats.get("accuracy_by_domain", {})
    acc_by_diff = stats.get("accuracy_by_difficulty", {})
    avg_time_by_domain = stats.get("avg_time_by_domain", {})

    domain = question_meta.get("domain", "")
    difficulty = question_meta.get("difficulty", "medium")

    acc_domain = float(acc_by_domain.get(domain, overall))
    acc_diff = float(acc_by_diff.get(difficulty, overall))
    avg_time = float(avg_time_by_domain.get(domain, 30.0))  # default average time 30s

    diff_enc = DIFFICULTY_MAP.get(difficulty, 1)
    dom_enc = encode_domain(domain)

    features = np.array([overall, acc_domain, acc_diff, avg_time, diff_enc, dom_enc], dtype=float)
    return features.reshape(1, -1)