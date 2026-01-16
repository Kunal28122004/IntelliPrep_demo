"""
Authentication service: registration and verification.

- Uses passlib bcrypt for password hashing.
- Simple, explainable logic suitable for viva.
"""

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from ..db import SessionLocal, User
from ..config import PWD_HASH_SCHEME

pwd_context = CryptContext(schemes=[PWD_HASH_SCHEME], deprecated="auto")


class AuthService:
    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def register_user(username: str, password: str) -> (bool, str):
        """
        Create new user if username is not taken.
        Returns (success, message_or_user).
        """
        db: Session = SessionLocal()
        try:
            existing = db.query(User).filter(User.username == username).first()
            if existing:
                return False, "Username already exists"
            hashed = AuthService.get_password_hash(password)
            user = User(username=username, hashed_password=hashed)
            db.add(user)
            db.commit()
            db.refresh(user)
            return True, "User registered"
        finally:
            db.close()

    @staticmethod
    def authenticate_user(username: str, password: str) -> (bool, object):
        """
        Verify username & password. Returns (True, user) on success.
        """
        db: Session = SessionLocal()
        try:
            user = db.query(User).filter(User.username == username).first()
            if not user:
                return False, "Invalid username or password"
            if not AuthService.verify_password(password, user.hashed_password):
                return False, "Invalid username or password"
            return True, user
        finally:
            db.close()