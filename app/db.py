"""
Database models and setup for IntelliPrep.

- Uses SQLAlchemy with SQLite.
- Models: User, Question, Attempt
- Includes a small static question bank initializer.
"""

from datetime import datetime
import json
from typing import List

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Float,
    DateTime,
    ForeignKey,
    create_engine,
    Text,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# SQLite file stored at project root
DATABASE_URL = "sqlite:///./main_website.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(128), unique=True, index=True, nullable=False)
    hashed_password = Column(String(256), nullable=False)

    attempts = relationship("Attempt", back_populates="user")


class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    # store options as JSON string for simplicity
    options = Column(Text, nullable=False)
    correct_option = Column(Integer, nullable=False)  # index of correct option
    difficulty = Column(String(32), nullable=False)  # 'easy'|'medium'|'hard'
    domain = Column(String(64), nullable=False)  # e.g., 'algebra', 'calculus'

    attempts = relationship("Attempt", back_populates="question")

    def get_options(self) -> List[str]:
        return json.loads(self.options)


class Attempt(Base):
    __tablename__ = "attempts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    correct = Column(Boolean, nullable=False)
    time_taken = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="attempts")
    question = relationship("Question", back_populates="attempts")


def init_db():
    """
    Create tables and populate static question bank if empty.
    This keeps the question bank static while allowing persistence of attempts/users.
    Also creates a default test user.
    """
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Create default user if doesn't exist
        default_user = db.query(User).filter(User.username == "Kunal12").first()
        if not default_user:
            # Use argon2 hashed password for Kunal@1212
            # This avoids bcrypt version compatibility issues
            hashed_password = "$argon2id$v=19$m=65536,t=3,p=4$VKqVUqpVKgUghHAuxThnzA$iYExBQ8MQf9mnK0WhcfczJx01H24Cf+dlas8bDCmYNE"
            new_user = User(username="Kunal12", hashed_password=hashed_password)
            db.add(new_user)
            db.commit()
            print("✓ Default user created: Kunal12 / Kunal@1212")
        
        # Create questions if empty
        q_count = db.query(Question).count()
        if q_count == 0:
            # Very small static question bank for demonstration.
            # In real deployment, replace with fuller curated bank.
            questions = [
                {
                    "text": "What is the derivative of x^2?",
                    "options": ["2x", "x", "x^2", "1"],
                    "correct_option": 0,
                    "difficulty": "easy",
                    "domain": "calculus",
                },
                {
                    "text": "Solve for x: 2x + 3 = 7",
                    "options": ["1", "2", "3", "4"],
                    "correct_option": 1,
                    "difficulty": "easy",
                    "domain": "algebra",
                },
                {
                    "text": "Integral of 1/x dx is:",
                    "options": ["ln|x| + C", "x + C", "1/x + C", "e^x + C"],
                    "correct_option": 0,
                    "difficulty": "medium",
                    "domain": "calculus",
                },
                {
                    "text": "If matrix A is 2x2 with det(A)=0, then A is:",
                    "options": ["Invertible", "Singular", "Orthogonal", "Diagonal"],
                    "correct_option": 1,
                    "difficulty": "medium",
                    "domain": "linear_algebra",
                },
                {
                    "text": "Limit: lim_{x->0} (sin x)/x = ?",
                    "options": ["0", "1", "Undefined", "Infinity"],
                    "correct_option": 1,
                    "difficulty": "easy",
                    "domain": "calculus",
                },
                {
                    "text": "Which number is prime?",
                    "options": ["21", "25", "29", "27"],
                    "correct_option": 2,
                    "difficulty": "easy",
                    "domain": "number_theory",
                },
                {
                    "text": "Find eigenvalues of [[2,0],[0,3]]",
                    "options": ["2 and 3", "5", "0", "2"],
                    "correct_option": 0,
                    "difficulty": "medium",
                    "domain": "linear_algebra",
                },
                {
                    "text": "Compute derivative of sin(x^2)",
                    "options": ["2x cos(x^2)", "cos(x)", "2 sin x", "x cos x"],
                    "correct_option": 0,
                    "difficulty": "hard",
                    "domain": "calculus",
                },
            ]
            for q in questions:
                db_q = Question(
                    text=q["text"],
                    options=json.dumps(q["options"]),
                    correct_option=q["correct_option"],
                    difficulty=q["difficulty"],
                    domain=q["domain"],
                )
                db.add(db_q)
            db.commit()
    finally:
        db.close()