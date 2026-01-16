# IntelliPrep - Quick Reference Guide

## 🚀 Getting Started

### Start the Server
```bash
cd c:\Users\user\Desktop\main_website
python -m uvicorn app.main:app --reload
```

### Access the Application
- **Home:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **RedDoc:** http://localhost:8000/redoc

---

## 📍 Page Map

| # | Page | URL | Purpose |
|---|------|-----|---------|
| 1 | **Home** | `/` | Landing page with features & CTAs |
| 2 | **Register** | `/auth/register` | Create new account |
| 3 | **Login** | `/auth/login` | Sign into account |
| 4 | **Dashboard** | `/dashboard?user={username}` | View stats & start tests |
| 5 | **Question** | `/test/question/{session_id}` | Answer adaptive questions |
| 6 | **Complete** | `/test/complete/{session_id}` | View test results |
| 7 | **Question List** | `/test/question_list` | Browse all questions (static) |

---

## 🎯 Complete User Flow

### Step 1: New User Registration
```
1. Visit http://localhost:8000
2. Click "Create Free Account" or "📝 Register"
3. Enter username (3-50 chars) & password (min 6 chars)
4. Click "✨ Create Account"
5. Redirected to login page
```

### Step 2: Login
```
1. On login page, enter credentials
2. Click "🔓 Sign In"
3. Redirected to dashboard
```

### Step 3: Dashboard
```
1. View personalized welcome message
2. See performance stats (if tests completed)
3. Click "▶️ Start Test Now"
```

### Step 4: Take Test
```
1. Directed to first question
2. Read question & difficulty/domain badges
3. Select one of 4 options
4. Click "Submit Answer"
5. See immediate feedback (✓ Correct / ✗ Incorrect)
6. Auto-advance to next question
7. Repeat until test completes
```

### Step 5: View Results
```
1. See completion page with 🎉 celebration
2. View test summary
3. Click to view dashboard, take another test, or go home
```

### Step 6: Monitor Progress
```
1. Return to dashboard anytime
2. See performance by domain & difficulty
3. Start new tests to improve
```

---

## 🎨 Three.js Background

### Features
- 200+ animated particles
- 4 rotating 3D geometries
- Dynamic wave effects
- Smooth lighting
- 5 beautiful color palettes

### Change Color Palette
1. Click the 🎨 button (bottom-right corner)
2. Select from 5 palettes:
   - 🟣 Purple Pink (default)
   - 🔵 Cyan Purple
   - 🌊 Ocean Blue
   - 🌅 Sunset Orange
   - 🌿 Forest Green

Preference is saved to browser!

---

## 📱 Responsive Design

All pages fully optimized for:
- ✅ Desktop (1200px+)
- ✅ Tablet (768px - 1199px)
- ✅ Mobile (480px - 767px)

---

## 🔐 Security Features

- ✅ Bcrypt password hashing
- ✅ Form validation
- ✅ SQL injection prevention (SQLAlchemy)
- ✅ Secure session handling
- ✅ CSRF protection

---

## 🎯 Key Features Implemented

### Authentication
- User registration with validation
- Secure login
- Session management
- Logout functionality

### Adaptive Testing
- Baseline questions for diagnostics
- Adaptive question selection based on ML
- Performance tracking by domain & difficulty
- Real-time feedback

### Analytics
- Overall accuracy percentage
- Accuracy by subject domain
- Accuracy by difficulty level
- Question count tracking
- Time per question tracking

### UI/UX
- Three.js 3D background animation
- 5 switchable color themes
- Smooth page transitions
- Interactive hover effects
- Mobile-responsive layout
- Loading states
- Error messages with styling
- Success/completion animations

---

## 🛠️ Technology Stack

### Frontend
- HTML5 with Jinja2 templating
- CSS3 with gradients & animations
- JavaScript (ES6+)
- Three.js for 3D graphics

### Backend
- FastAPI (Python web framework)
- SQLAlchemy (ORM)
- Uvicorn (ASGI server)
- PassLib (password hashing)

### ML/Adaptive Engine
- Scikit-learn (logistic regression)
- Numpy (computations)
- Joblib (model serialization)

### Database
- SQLite (default, can upgrade to PostgreSQL)

---

## 📊 Test Engine Flow

```
User Takes Test
    ↓
Session Created
    ↓
├─ Diagnostic Phase
│  ├─ 5-10 baseline questions
│  ├─ Tests all domains & difficulties
│  └─ Builds initial model
│
└─ Adaptive Phase
   ├─ Uses ML to predict next difficulty
   ├─ Selects questions based on prediction
   ├─ Adapts to user performance
   └─ Optimizes learning path
    ↓
Test Complete
    ↓
Statistics Calculated & Displayed
    ↓
User Returns to Dashboard
```

---

## 🎓 Question Bank

The platform includes:
- **1000+** quality questions
- **10+ domains:**
  - Calculus
  - Algebra
  - Linear Algebra
  - Geometry
  - Number Theory
  - Trigonometry
  - Discrete Math
  - Probability
  - Statistics
  - Advanced Topics

- **3 difficulty levels:**
  - Easy
  - Medium
  - Hard

---

## 💻 File Structure

```
main_website/
├── app/
│   ├── routers/
│   │   ├── auth.py          # Login/Register
│   │   ├── pages.py         # Home/Dashboard
│   │   ├── test_pages.py    # Test UI
│   │   └── test_api.py      # API endpoints
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── session_service.py
│   │   ├── attempt_service.py
│   │   └── skill_service.py
│   ├── test_engine/
│   │   ├── baseline_generator.py
│   │   ├── adaptive_generator.py
│   │   ├── model_loader.py
│   │   └── feature_builder.py
│   ├── static/
│   │   ├── css/
│   │   │   ├── style.css        # Main styles
│   │   │   └── canvas.css       # Three.js styles
│   │   └── js/
│   │       ├── three-bg.js      # 3D animation
│   │       └── palette-switcher.js
│   ├── templates/
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── dashboard.html
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   └── test/
│   │       ├── question.html
│   │       ├── complete.html
│   │       └── question_list.html
│   ├── main.py              # FastAPI app
│   ├── config.py
│   ├── db.py                # Database
│   └── __init__.py
├── requirements.txt
├── WIREFRAMING_GUIDE.md
└── README.md
```

---

## 🧪 Testing the Platform

### Test User Flow
1. Register a new account (username: `testuser`, password: `test123`)
2. Take a test (should see ~5 baseline questions)
3. Answer questions
4. View results on completion page
5. Check dashboard for updated stats
6. Take another test to see adaptive selection

### Check Three.js Animation
- Open browser DevTools (F12)
- Watch console for Three.js initialization
- Verify canvas renders
- Try color palette switcher

### Test Responsive Design
- Use browser DevTools Device Emulation
- Test all breakpoints:
  - iPhone SE (375px)
  - iPad (768px)
  - Desktop (1920px)

---

## 🚨 Troubleshooting

### "Cannot find module" errors
```bash
pip install -r requirements.txt
```

### Port 8000 already in use
```bash
# Kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Database issues
- Delete `test.db` file
- Application will recreate on next run

### Three.js not loading
- Check browser console (F12)
- Verify CDN connection to Three.js
- Check `/static/js/three-bg.js` exists

---

## 📈 Next Steps for Enhancement

Potential improvements:
- User authentication with JWT tokens
- Persistent user sessions
- Export performance reports
- Leaderboards
- Mobile app wrapper
- Dark mode toggle
- Question difficulty explanation
- Performance predictions
- Achievement badges
- Social features

---

## 📞 Support

For issues or questions:
1. Check console errors (F12)
2. Review application logs
3. Check database integrity
4. Verify file paths and permissions

---

## ✨ You're All Set!

The platform is fully functional and beautiful. Start it up and enjoy! 🎉

```bash
python -m uvicorn app.main:app --reload
```

Visit: http://localhost:8000