"""
Application configuration values.

Kept simple so settings are easy to explain at viva.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "test_engine" / "logreg.joblib"

# Security / auth simple constants
PWD_HASH_SCHEME = "argon2"