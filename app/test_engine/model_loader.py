"""
Model loader for Logistic Regression inference.

- Uses joblib to load the model file at app/test_engine/logreg.joblib.
- If model file is missing, creates a simple deterministic "model" object
  with a predict_proba method (no training), saves it with joblib for future runs.

This approach avoids training on startup while keeping inference deterministic
and explainable for the academic setting.
"""

import joblib
import numpy as np
from pathlib import Path
from typing import Any

from ..config import MODEL_PATH


class _SimpleLogistic:
    """
    Simple logistic-like model which computes sigmoid(w.x + b)
    Coefficients are preset constants chosen for demonstration.
    """

    def __init__(self, coef=None, intercept: float = 0.0):
        # If coef is None expect 6 features by convention
        if coef is None:
            # Chosen to give sensible probabilities: emphasize accuracy features
            self.coef = np.array([2.0, 1.5, 1.0, -0.01, -0.5, 0.0])
        else:
            self.coef = np.array(coef)
        self.intercept = float(intercept)
        # classes for predict_proba compatibility
        self.classes_ = np.array([0, 1])

    def predict_proba(self, X):
        # X: (n_samples, n_features)
        logits = X.dot(self.coef) + self.intercept
        probs = 1.0 / (1.0 + np.exp(-logits))
        # Return shape (n_samples, 2)
        probs_stack = np.vstack([1 - probs, probs]).T
        return probs_stack


class ModelLoader:
    _model: Any = None
    _model_path = Path(MODEL_PATH)

    @classmethod
    def load_model(cls):
        """
        Load model from disk using joblib. If not present, create simple model and save it.
        """
        if cls._model is not None:
            return cls._model
        # Ensure parent folder exists (should per project layout)
        cls._model_path.parent.mkdir(parents=True, exist_ok=True)
        if cls._model_path.exists():
            try:
                cls._model = joblib.load(cls._model_path)
                return cls._model
            except Exception:
                # Corrupt model — fallback to simple model
                pass
        # Create deterministic simple logistic-like model (no training)
        model = _SimpleLogistic()
        joblib.dump(model, cls._model_path)
        cls._model = model
        return cls._model

    @classmethod
    def predict_probability(cls, features):
        """
        Returns probability of correct answer for given features.
        features: numpy array (1, n_features) or (n, n_features)
        """
        model = cls.load_model()
        probs = model.predict_proba(features)
        # return probability of class '1' (correct)
        return probs[:, 1] if probs.ndim == 2 else float(probs[1])