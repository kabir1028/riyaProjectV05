# 🎯 InterviewAce - AI Mock Interview Platform

> A production-ready, full-stack web application that provides AI-powered mock interviews with intelligent scoring, instant feedback, and company recommendations.

[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12+-blue.svg)](https://www.postgresql.org/)
[![Python](https://img.shields.io/badge/Python-3.8+-yellow.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Educational-red.svg)](LICENSE)

## ✨ Key Features

### 🎓 Interview System
- **900+ Curated Questions** across 3 roles and 3 difficulty levels
- **Intelligent Scoring Algorithm** with instant feedback
- **Company Recommendations** based on performance
- **Interview History** tracking (last 5 results)
- **Mixed Question Types** (Multiple Choice + Short Answer)

### 🔐 Authentication
- **Local Authentication** with email verification
- **Google OAuth 2.0** integration
- **GitHub OAuth** integration
- **Unified Account System** (one email = one account)
- **Password Reset** with OTP
- **Professional Email Templates** via Brevo SMTP

### 📊 Roles & Difficulty Levels
- **Software Engineer** (Beginner, Intermediate, Advanced)
- **AI Scientist** (Beginner, Intermediate, Advanced)
- **Data Scientist** (Beginner, Intermediate, Advanced)

## 🏗️ Project Structure
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
    ├── README.md
    ├── PROJECT_DETAILS.md
    ├── SETUP_GUIDE.md
    ├── VERIFICATION_SYSTEM.md
    ├── UNIFIED_ACCOUNT_SYSTEM.md
    ├── OAUTH_SETUP.md
    └── FEATURES_IMPLEMENTED.md
```

## 🚀 Quick Start

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

## 🗄️ Database Schema

### Users Table
```sql
CREATE TABLE users (
    id VARCHAR(255) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    name VARCHAR(255),
    avatar_url TEXT,
    auth_provider VARCHAR(50) DEFAULT 'local',
    oauth_id VARCHAR(255),
    is_guest BOOLEAN DEFAULT FALSE,
    is_verified BOOLEAN DEFAULT FALSE,
    verification_token VARCHAR(255),
    reset_otp VARCHAR(10),
    otp_expiry TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Results Table
```sql
CREATE TABLE results (
    id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    score INTEGER NOT NULL,
    feedback TEXT,
    companies TEXT,
    answers TEXT,
    questions TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);
```

**Note:** Automatically keeps last 5 results per user

## 🎯 How It Works

### Interview Flow
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

### Authentication Options
1. **Local Signup** - Email + password with verification
2. **Google Login** - One-click OAuth authentication
3. **GitHub Login** - Developer-friendly OAuth

**Unified Accounts:** One email = one account across all login methods

## 🛠️ Technology Stack

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

## 📚 Documentation

For detailed information, check out:
- **[PROJECT_DETAILS.md](PROJECT_DETAILS.md)** - Comprehensive project documentation
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Detailed setup instructions
- **[VERIFICATION_SYSTEM.md](VERIFICATION_SYSTEM.md)** - Email verification details
- **[UNIFIED_ACCOUNT_SYSTEM.md](UNIFIED_ACCOUNT_SYSTEM.md)** - Account merging explanation
- **[OAUTH_SETUP.md](OAUTH_SETUP.md)** - OAuth configuration guide
- **[FEATURES_IMPLEMENTED.md](FEATURES_IMPLEMENTED.md)** - Feature checklist

## 🔐 Security Features

- ✅ Werkzeug password encryption
- ✅ Email verification enforcement
- ✅ Token-based authentication
- ✅ OAuth 2.0 security
- ✅ SQL injection prevention
- ✅ Session management
- ✅ OTP expiry (10 minutes)
- ✅ Single-use verification tokens

## 📊 Project Statistics

- **900+** Interview questions
- **3** Career roles
- **3** Difficulty levels per role
- **14** HTML pages
- **3** Authentication methods
- **2** Professional email templates
- **5** Results stored per user

## 🎯 Key Achievements

✅ Complete authentication system (Local + OAuth)  
✅ Email verification with professional templates  
✅ Unified account system (one email = one account)  
✅ Intelligent scoring algorithm  
✅ Company recommendations  
✅ Interview history tracking  
✅ Password reset with OTP  
✅ Responsive UI design  
✅ Production-ready codebase  

## 🚀 Future Enhancements

- [ ] AI-powered answer analysis with GPT
- [ ] Video interview recording
- [ ] Live coding challenges
- [ ] Peer-to-peer mock interviews
- [ ] Company-specific interview prep
- [ ] Advanced analytics dashboard
- [ ] Mobile applications (iOS/Android)
- [ ] Resume analysis and feedback

## 📄 License

This project is built for educational and portfolio purposes.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## 📞 Support

For questions or support, please refer to the documentation files or open an issue.

---

**Built with ❤️ using Flask, PostgreSQL, and dedication to helping candidates succeed in their interviews.**

**Status:** ✅ Production-Ready | 🎉 Fully Functional
