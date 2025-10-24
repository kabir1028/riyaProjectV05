# InterviewAce - AI Mock Interview Platform

> A production-ready, full-stack web application that provides AI-powered mock interviews with intelligent scoring, instant feedback, and company recommendations.

[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12+-blue.svg)](https://www.postgresql.org/)
[![Python](https://img.shields.io/badge/Python-3.8+-yellow.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Educational-red.svg)](LICENSE)

## Key Features

### Interview System
- **900+ Curated Questions** across 3 roles and 3 difficulty levels
- **Intelligent Scoring Algorithm** with instant feedback
- **Company Recommendations** based on performance
- **Interview History** tracking (last 5 results)
- **Mixed Question Types** (Multiple Choice + Short Answer)

### Authentication
- **Local Authentication** with email verification
- **Google OAuth 2.0** integration
- **GitHub OAuth** integration
- **Unified Account System** (one email = one account)
- **Password Reset** with OTP
- **Professional Email Templates** via Brevo SMTP

### Roles & Difficulty Levels
- **Software Engineer** (Beginner, Intermediate, Advanced)
- **AI Scientist** (Beginner, Intermediate, Advanced)
- **Data Scientist** (Beginner, Intermediate, Advanced)

## System Architecture

### High-Level Architecture
```
┌─────────────┐
│   Browser   │ ← User Interface
└──────┬──────┘
       │ HTTP/HTTPS
       ▼
┌─────────────────────────────┐
│   Flask Application         │
│  ┌────────────────────────┐ │
│  │ Controllers (Routes)   │ │ ← API Endpoints
│  └────────────────────────┘ │
│  ┌────────────────────────┐ │
│  │ Services (Logic)       │ │ ← Business Logic
│  └────────────────────────┘ │
│  ┌────────────────────────┐ │
│  │ Models (Data)          │ │ ← Data Layer
│  └────────────────────────┘ │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│   PostgreSQL Database       │ ← Data Storage
│   - users table             │
│   - results table           │
└─────────────────────────────┘

┌─────────────────────────────┐
│   External Services         │
│   - Brevo SMTP (Email)      │ ← Email Delivery
│   - Google OAuth            │ ← Authentication
│   - GitHub OAuth            │ ← Authentication
│   - Groq AI API             │ ← AI Features
└─────────────────────────────┘
```

### Project Structure
```
resume-mock-interviewer/
├── app.py                      # Main application entry point
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (gitignored)
├── .env.example               # Environment template
│
├── config/                    # Configuration
│   ├── __init__.py
│   └── config.py              # App configuration
│
├── models/                    # Data layer
│   ├── __init__.py
│   ├── database.py            # PostgreSQL connection & schema
│   ├── user.py                # User model
│   └── result.py              # Interview result model
│
├── services/                  # Business logic layer
│   ├── __init__.py
│   ├── user_service.py        # User operations
│   ├── interview_service.py   # Interview logic & scoring
│   ├── email_service.py       # Email operations (Brevo)
│   └── oauth_service.py       # OAuth providers
│
├── controllers/               # Route handlers
│   ├── __init__.py
│   ├── auth_controller.py     # Authentication routes
│   └── interview_controller.py # Interview routes
│
├── templates/                 # HTML templates (14 pages)
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── start_interview.html
│   ├── interview.html
│   ├── results.html
│   ├── history.html
│   ├── profile.html
│   ├── forgot_password.html
│   ├── reset_password.html
│   ├── verify_email.html
│   ├── verify_otp.html
│   └── error.html
│
├── static/
│   ├── css/                   # Stylesheets
│   └── js/                    # JavaScript files
│
├── data/
│   └── questions.json         # Question bank (900+ questions)
│
└── docs/                      # Documentation
    ├── README.md                      # Main documentation
    ├── PROJECT_DETAILS.md             # Comprehensive details
    ├── COMPLETE_SETUP_GUIDE.md        # Setup instructions
    ├── ARCHITECTURE_DIAGRAMS.md       # System diagrams
    ├── DATABASE_DOCUMENTATION.md      # Database details
    ├── PROJECT_TIMELINE.md            # Development timeline
    ├── AI_INTERVIEW_SYSTEM.md         # AI features
    └── GROQ_API_SETUP.md             # AI API setup
```

## Quick Start

### Prerequisites
- Python 3.8 or higher
- PostgreSQL 12 or higher
- Brevo SMTP account (for emails)
- Google OAuth credentials (optional)
- GitHub OAuth credentials (optional)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd resume-mock-interviewer
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your credentials
```

4. **Run the application**
```bash
python app.py
```
Database tables will be created automatically on first run.

5. **Open your browser**
```
http://localhost:5000
```

### Environment Variables

Create a `.env` file with the following:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=interviewace
DB_USER=postgres
DB_PASSWORD=your_password

# Flask Configuration
FLASK_SECRET_KEY=your_secret_key_here
FLASK_HOST=localhost
FLASK_PORT=5000
FLASK_DEBUG=True

# Email Configuration (Brevo SMTP)
SMTP_HOST=smtp-relay.brevo.com
SMTP_PORT=587
SMTP_USER=your_brevo_email
SMTP_PASSWORD=your_brevo_password
FROM_EMAIL=noreply@interviewace.com

# OAuth Configuration (Optional)
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
```

## Database Schema

### Entity Relationship Diagram
```
┌─────────────────────────────────────┐
│          users (Primary)            │
├─────────────────────────────────────┤
│ PK  id                VARCHAR(255)  │
│ UQ  email             VARCHAR(255)  │
│     password_hash     VARCHAR(255)  │
│     name              VARCHAR(255)  │
│     avatar_url        TEXT          │
│     auth_provider     VARCHAR(50)   │
│     oauth_id          VARCHAR(255)  │
│     is_guest          BOOLEAN       │
│     is_verified       BOOLEAN       │
│     verification_token VARCHAR(255) │
│     reset_otp         VARCHAR(10)   │
│     otp_expiry        TIMESTAMP     │
│     phone             VARCHAR(50)   │
│     user_role         VARCHAR(255)  │
│     experience        VARCHAR(50)   │
│     location          VARCHAR(255)  │
│     bio               TEXT          │
│     created_at        TIMESTAMP     │
└──────────────┬──────────────────────┘
               │ 1:N
               │ (One user → Many results)
               ▼
┌─────────────────────────────────────┐
│        results (Foreign)            │
├─────────────────────────────────────┤
│ PK  id                VARCHAR(255)  │
│ FK  user_id           VARCHAR(255)  │ → users.id
│     score             INTEGER       │
│     feedback          TEXT          │
│     companies         TEXT (JSON)   │
│     answers           TEXT (JSON)   │
│     questions         TEXT (JSON)   │
│     created_at        TIMESTAMP     │
└─────────────────────────────────────┘

Constraints:
- Foreign Key: results.user_id → users.id ON DELETE CASCADE
- Unique: users.email
- Auto-cleanup: Keep only last 5 results per user
```

**See [DATABASE_DOCUMENTATION.md](DATABASE_DOCUMENTATION.md) for complete schema details**

## How It Works

### Interview Flow Diagram
```
┌─────────────┐
│   START     │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│ User Logged In? │
└────────┬────────┘
         │
    ┌────┴────┐
    NO        YES
    │         │
    ▼         ▼
┌────────┐  ┌──────────────────┐
│Redirect│  │ Select Role      │
│to Login│  │ - Software Eng   │
└────────┘  │ - AI Scientist   │
            │ - Data Scientist │
            └────────┬─────────┘
                     │
                     ▼
            ┌──────────────────┐
            │ Select Difficulty│
            │ - Beginner       │
            │ - Intermediate   │
            │ - Advanced       │
            └────────┬─────────┘
                     │
                     ▼
            ┌──────────────────┐
            │ Answer 10 Qs     │
            │ (MCQ + Text)     │
            └────────┬─────────┘
                     │
                     ▼
            ┌──────────────────┐
            │ Calculate Score  │
            │ Generate Feedback│
            └────────┬─────────┘
                     │
                     ▼
            ┌──────────────────┐
            │ Show Results     │
            │ - Score (0-100)  │
            │ - Feedback       │
            │ - Companies      │
            └────────┬─────────┘
                     │
                     ▼
            ┌──────────────────┐
            │ Save to History  │
            │ (Last 5 results) │
            └────────┬─────────┘
                     │
                     ▼
                ┌────────┐
                │  END   │
                └────────┘
```

### Step-by-Step Process
1. **Select Role** - Choose from Software Engineer, AI Scientist, or Data Scientist
2. **Choose Difficulty** - Beginner, Intermediate, or Advanced
3. **Answer Questions** - 10 questions (mix of MCQ and short-answer)
4. **Get Results** - Instant score, feedback, and company recommendations
5. **Review History** - Access your last 5 interview results

### Scoring System
- **Multiple Choice**: 20 points per correct answer
- **Short Answer**: 10-20 points based on answer quality
- **Maximum Score**: 100 points
- **Performance Tiers**:
  - 80-100: Excellent (top-tier companies)
  - 60-79: Good (mid-tier companies)
  - 0-59: Needs improvement

### Authentication Flow
```
┌──────────────────────────────────────────────────────┐
│              Authentication Methods                  │
└──────────────────────────────────────────────────────┘

1. Local Authentication:
   User → Signup → Email Verification → Login → Access

2. Google OAuth:
   User → Google Login → Auto-Verified → Access

3. GitHub OAuth:
   User → GitHub Login → Auto-Verified → Access

┌──────────────────────────────────────────────────────┐
│           Unified Account System                     │
│  One Email = One Account (All Methods Work)          │
└──────────────────────────────────────────────────────┘
```

### Authentication Options
1. **Local Signup** - Email + password with verification
2. **Google Login** - One-click OAuth authentication
3. **GitHub Login** - Developer-friendly OAuth

**Unified Accounts:** One email = one account across all login methods  
**See [ARCHITECTURE_DIAGRAMS.md](ARCHITECTURE_DIAGRAMS.md) for detailed flow diagrams**

## Technology Stack

### Backend
- **Flask 2.3.3** - Web framework
- **PostgreSQL** - Relational database
- **psycopg2-binary 2.9.7** - PostgreSQL adapter
- **Werkzeug 2.3.7** - Password encryption
- **Python-dotenv 1.0.0** - Environment management
- **Requests 2.31.0** - HTTP client for OAuth

### Frontend
- **HTML5** - Structure
- **CSS3** - Modern styling with gradients
- **JavaScript** - Interactivity
- **Responsive Design** - Mobile-friendly

### External Services
- **Brevo SMTP** - Email delivery
- **Google OAuth 2.0** - Social authentication
- **GitHub OAuth** - Developer authentication

## Documentation

For detailed information, check out:
- **[PROJECT_DETAILS.md](PROJECT_DETAILS.md)** - Comprehensive project documentation
- **[COMPLETE_SETUP_GUIDE.md](COMPLETE_SETUP_GUIDE.md)** - Detailed setup instructions with troubleshooting
- **[ARCHITECTURE_DIAGRAMS.md](ARCHITECTURE_DIAGRAMS.md)** - System architecture, flowcharts, and diagrams
- **[DATABASE_DOCUMENTATION.md](DATABASE_DOCUMENTATION.md)** - Complete database schema and queries
- **[PROJECT_TIMELINE.md](PROJECT_TIMELINE.md)** - Day-by-day development timeline (Oct 1-19)
- **[AI_INTERVIEW_SYSTEM.md](AI_INTERVIEW_SYSTEM.md)** - AI integration details
- **[GROQ_API_SETUP.md](GROQ_API_SETUP.md)** - Groq AI API configuration

## Security Features

- Werkzeug password encryption
- Email verification enforcement
- Token-based authentication
- OAuth 2.0 security
- SQL injection prevention
- Session management
- OTP expiry (10 minutes)
- Single-use verification tokens

## Project Statistics

### Content
- **900+** Interview questions
- **3** Career roles (Software Engineer, AI Scientist, Data Scientist)
- **3** Difficulty levels per role (Beginner, Intermediate, Advanced)
- **10** Questions per interview
- **5** Results stored per user

### Technical
- **14** HTML templates
- **12** Python modules
- **5** JavaScript files
- **2** CSS stylesheets
- **3** Authentication methods
- **2** Professional email templates
- **2** Database tables
- **4** External service integrations

**See [PROJECT_TIMELINE.md](PROJECT_TIMELINE.md) for day-by-day breakdown**

## Key Achievements

- Complete authentication system (Local + OAuth)  
- Email verification with professional templates  
- Unified account system (one email = one account)  
- Intelligent scoring algorithm  
- Company recommendations  
- Interview history tracking  
- Password reset with OTP  
- Responsive UI design  
- Production-ready codebase  

## 🚀 Future Enhancements

-  AI-powered answer analysis with GPT
-  Video interview recording
-  Live coding challenges
-  Peer-to-peer mock interviews
-  Company-specific interview prep
-  Advanced analytics dashboard
-  Mobile applications (iOS/Android)
-  Resume analysis and feedback

## License

This project is built for educational and portfolio purposes.

## Contributing

Contributions, issues, and feature requests are welcome!

## Support

For questions or support, please refer to the documentation files or open an issue.

---