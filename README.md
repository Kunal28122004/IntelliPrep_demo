# IntelliPrep - Adaptive Assessment System

An AI-powered adaptive testing platform that uses Machine Learning to dynamically select questions based on user performance. Built with FastAPI and Logistic Regression.

## 🎯 Project Overview

IntelliPrep is a college-level adaptive assessment system that:
- Tracks individual user performance
- Uses Logistic Regression ML model to predict success probability
- Dynamically selects optimal questions (0.4-0.7 success probability range)
- Provides real-time adaptive testing experience

## 📁 Project Structure

```
main_website/
│
├── app/
│   ├── routers/              # API endpoints
│   │   ├── auth.py           # Login/Register
│   │   ├── pages.py          # Dashboard
│   │   ├── test_api.py       # Test API endpoints
│   │   └── test_pages.py     # Test HTML pages
│   │
│   ├── services/             # Business logic
│   │   ├── attempt_service.py   # Record attempts
│   │   ├── auth_service.py      # Authentication
│   │   ├── session_service.py   # Session management
│   │   └── skill_service.py     # User statistics
│   │
│   ├── test_engine/          # ML components
│   │   ├── adaptive_generator.py  # ML-based selection
│   │   ├── baseline_generator.py  # Diagnostic questions
│   │   ├── feature_builder.py     # Feature engineering
│   │   └── model_loader.py        # ML model loader
│   │
│   ├── static/css/style.css  # Styling
│   ├── templates/            # HTML templates
│   ├── config.py             # Configuration
│   ├── db.py                 # Database models
│   └── main.py               # FastAPI app
│
├── .gitignore
└── requirements.txt
```

## 🚀 Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
cd main_website
python -m uvicorn app.main:app --reload
```

Or:

```bash
python app/main.py
```

### 3. Access the Application

Open your browser and navigate to:
```
http://localhost:8000
```

## 📊 How It Works

### Test Flow

1. **Registration/Login**
   - Users create account or login
   - JWT token-based authentication

2. **Diagnostic Phase** (5 questions)
   - Random mixed-difficulty questions
   - Establishes baseline performance
   - No ML involved yet

3. **Adaptive Phase** (10 questions)
   - ML model predicts success probability for each question
   - Selects questions with 0.4-0.7 probability (sweet spot)
   - Adjusts difficulty based on real-time performance

4. **Results**
   - Immediate feedback
   - Performance statistics
   - Accuracy by topic and difficulty

### Machine Learning Component

**Algorithm:** Logistic Regression

**Features (6 total):**
1. Difficulty encoded (1=Easy, 2=Medium, 3=Hard)
2. Domain encoded (1=Math, 2=Physics, 3=CS, etc.)
3. User accuracy on this topic (%)
4. User accuracy on this difficulty (%)
5. User avg time on this topic (seconds)
6. User avg time on this difficulty (seconds)

**Output:** Probability of correct answer (0-1)

**Selection Strategy:** Choose question with probability closest to target range (0.4-0.7)

## 🗄️ Database Schema

### Users Table
- id, username, email, hashed_password, created_at

### Questions Table
- id, text, option_a/b/c/d, correct_answer
- difficulty, domain, topic (metadata for ML)

### Attempts Table
- id, user_id, question_id, selected_answer
- is_correct, time_taken, attempted_at

## 🧪 For Viva/Demo

### Key Points to Explain:

1. **Why Logistic Regression?**
   - Binary classification (correct/incorrect)
   - Outputs probability directly
   - Interpretable coefficients
   - Fast inference

2. **Feature Engineering**
   - Combines question metadata with user history
   - Accuracy stats show user's strength areas
   - Time stats indicate difficulty level for user

3. **Adaptive Logic**
   - Too easy (>0.7 prob) = No learning
   - Too hard (<0.4 prob) = Frustration
   - Sweet spot (0.4-0.7) = Optimal challenge

4. **Architecture Benefits**
   - Separation of concerns (services vs routers)
   - Reusable components
   - Easy to extend with new ML models

### Demo Flow:

1. Register new user
2. Start test → Show diagnostic phase
3. Complete 5 questions → Switch to adaptive
4. Explain how ML selected next question
5. Show results and statistics
6. Navigate to practice mode

## 🔧 Configuration

Edit `app/config.py` to customize:
- `DIAGNOSTIC_QUESTION_COUNT` - Number of baseline questions
- `ADAPTIVE_QUESTION_COUNT` - Number of ML-selected questions
- `TARGET_PROBABILITY_MIN/MAX` - Success probability range

## 📝 Adding More Questions

Edit `app/db.py` and add to `seed_sample_questions()`:

```python
Question(
    text="Your question here?",
    option_a="Option A", option_b="Option B",
    option_c="Option C", option_d="Option D",
    correct_answer="A",  # or B, C, D
    difficulty="Medium",  # Easy, Medium, or Hard
    domain="Math",
    topic="Algebra"
)
```

## 🎓 GTU Academic Project Features

- ✅ Complete working system
- ✅ ML integration (Logistic Regression)
- ✅ Database with proper relationships
- ✅ User authentication
- ✅ Adaptive algorithm implementation
- ✅ Clean code with comments
- ✅ Professional UI
- ✅ Suitable for viva demonstration

## 🔐 Default Test Account

After first run, register your own account or seed a test user.

## 📦 Tech Stack

- **Backend:** FastAPI
- **Database:** SQLite + SQLAlchemy
- **ML:** Scikit-learn (Logistic Regression)
- **Auth:** JWT + Passlib
- **Frontend:** Jinja2 Templates + CSS

## 🐛 Troubleshooting

**Model not found error:**
- Application creates dummy model automatically on first run
- Check `app/test_engine/logistic_model.pkl` is created

**Database errors:**
- Delete `intelliprep.db` and restart to recreate

**Import errors:**
- Ensure you're running from `main_website/` directory
- Check all `__init__.py` files exist

## 📈 Future Enhancements

- Item Response Theory (IRT) instead of Logistic Regression
- Deep Learning models (Neural Networks)
- More sophisticated feature engineering
- Real-time progress visualization
- Detailed analytics dashboard
- Export results to PDF
- Timed questions with countdown

## 👨‍💻 Developer Notes

This system is designed for educational purposes and GTU project requirements. The code emphasizes:
- Clarity over complexity
- Comments for viva explanation
- Standard patterns and practices
- Separation of ML logic from web logic

## 📄 License

Academic Project - GTU College

---

**Developed by:** Kunal Chuahan
**Project:** IntelliPrep - Adaptive Assessment System
**Year:** 2026
