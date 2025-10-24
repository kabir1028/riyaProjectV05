# Complete Setup Guide - InterviewAce

> **Step-by-step manual to set up InterviewAce from scratch**  
> Follow this guide to get the application running with all features enabled.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [PostgreSQL Setup](#postgresql-setup)
3. [Project Installation](#project-installation)
4. [Brevo SMTP Setup (Email Service)](#brevo-smtp-setup)
5. [Google OAuth Setup](#google-oauth-setup)
6. [GitHub OAuth Setup](#github-oauth-setup)
7. [Groq AI API Setup](#groq-ai-api-setup)
8. [Environment Configuration](#environment-configuration)
9. [Running the Application](#running-the-application)
10. [Testing the Setup](#testing-the-setup)
11. [Troubleshooting](#troubleshooting)

---

## 1️⃣ Prerequisites

Before starting, ensure you have:

- ✅ **Python 3.8+** installed ([Download](https://www.python.org/downloads/))
- ✅ **PostgreSQL 12+** installed ([Download](https://www.postgresql.org/download/))
- ✅ **Git** installed ([Download](https://git-scm.com/downloads))
- ✅ A **text editor** (VS Code, Sublime, etc.)
- ✅ **Internet connection** for OAuth and email services

### Verify Installations

```bash
# Check Python version
python --version
# Should show: Python 3.8.x or higher

# Check PostgreSQL
psql --version
# Should show: psql (PostgreSQL) 12.x or higher

# Check Git
git --version
# Should show: git version 2.x.x
```

---

## 2️⃣ PostgreSQL Setup

### Step 1: Install PostgreSQL

**Windows:**
1. Download installer from [postgresql.org](https://www.postgresql.org/download/windows/)
2. Run installer and follow wizard
3. Remember the password you set for `postgres` user
4. Default port: `5432`

**Mac:**
```bash
brew install postgresql
brew services start postgresql
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

### Step 2: Create Database

Open PostgreSQL command line:

**Windows:**
```bash
# Open Command Prompt as Administrator
psql -U postgres
```

**Mac/Linux:**
```bash
sudo -u postgres psql
```

**Create the database:**
```sql
-- Create database
CREATE DATABASE interviewace;

-- Verify database created
\l

-- Exit PostgreSQL
\q
```

### Step 3: Test Connection

```bash
psql -U postgres -d interviewace
# If successful, you'll see: interviewace=#
# Type \q to exit
```

**Note:** Remember your PostgreSQL credentials:
- Host: `localhost`
- Port: `5432`
- Database: `interviewace`
- User: `postgres`
- Password: `[your password]`

---

## 3️⃣ Project Installation

### Step 1: Clone Repository

```bash
# Navigate to your projects folder
cd /path/to/your/projects

# Clone the repository
git clone <repository-url>

# Navigate into project
cd resume-mock-interviewer
```

### Step 2: Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed Flask-2.3.3 Werkzeug-2.3.7 psycopg2-binary-2.9.7 ...
```

---

## 4️⃣ Brevo SMTP Setup (Email Service)

Brevo (formerly Sendinblue) provides free SMTP service for sending emails.

### Step 1: Create Brevo Account

1. Go to [brevo.com](https://www.brevo.com/)
2. Click **"Sign up free"**
3. Fill in your details:
   - Email address
   - Password
   - Company name (can be anything)
4. Verify your email address

### Step 2: Get SMTP Credentials

1. **Login to Brevo dashboard**
2. Click on your **profile icon** (top right)
3. Select **"SMTP & API"**
4. Click **"SMTP"** tab
5. You'll see:
   ```
   Server: smtp-relay.brevo.com
   Port: 587
   Login: [your-email]@smtp-brevo.com
   Password: [click "Generate" to create]
   ```

### Step 3: Generate SMTP Key

1. Click **"Generate a new SMTP key"**
2. Give it a name: `InterviewAce`
3. Click **"Generate"**
4. **Copy the key immediately** (you won't see it again!)
5. Save it somewhere safe

### Step 4: Verify Sender Email

1. Go to **"Senders & IP"** in left menu
2. Click **"Senders"**
3. Click **"Add a sender"**
4. Enter your email (e.g., `noreply@yourdomain.com` or your personal email)
5. Verify the email by clicking link sent to your inbox

**Your Brevo credentials:**
```
SMTP_HOST: smtp-relay.brevo.com
SMTP_PORT: 587
SMTP_USER: [your-email]@smtp-brevo.com
SMTP_PASSWORD: [generated SMTP key]
FROM_EMAIL: [verified sender email]
```

---

## 5️⃣ Google OAuth Setup

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **"Select a project"** → **"New Project"**
3. Enter project name: `InterviewAce`
4. Click **"Create"**
5. Wait for project creation (30 seconds)

### Step 2: Enable Google+ API

1. In left menu, go to **"APIs & Services"** → **"Library"**
2. Search for **"Google+ API"**
3. Click on it
4. Click **"Enable"**

### Step 3: Configure OAuth Consent Screen

1. Go to **"APIs & Services"** → **"OAuth consent screen"**
2. Select **"External"**
3. Click **"Create"**
4. Fill in required fields:
   - **App name:** `InterviewAce`
   - **User support email:** Your email
   - **Developer contact:** Your email
5. Click **"Save and Continue"**
6. **Scopes:** Click **"Save and Continue"** (skip this)
7. **Test users:** Add your email for testing
8. Click **"Save and Continue"**

### Step 4: Create OAuth Credentials

1. Go to **"APIs & Services"** → **"Credentials"**
2. Click **"Create Credentials"** → **"OAuth client ID"**
3. Select **"Web application"**
4. Fill in:
   - **Name:** `InterviewAce Web Client`
   - **Authorized JavaScript origins:**
     ```
     http://localhost:5000
     ```
   - **Authorized redirect URIs:**
     ```
     http://localhost:5000/api/auth/google/callback
     ```
5. Click **"Create"**
6. **Copy your credentials:**
   - Client ID: `xxxxx.apps.googleusercontent.com`
   - Client Secret: `xxxxx`
7. Click **"OK"**

**Your Google OAuth credentials:**
```
GOOGLE_CLIENT_ID: [your-client-id].apps.googleusercontent.com
GOOGLE_CLIENT_SECRET: [your-client-secret]
```

---

## 6️⃣ GitHub OAuth Setup

### Step 1: Create OAuth App

1. Go to [GitHub Settings](https://github.com/settings/developers)
2. Click **"OAuth Apps"** in left menu
3. Click **"New OAuth App"**

### Step 2: Fill Application Details

```
Application name: InterviewAce
Homepage URL: http://localhost:5000
Application description: AI Mock Interview Platform
Authorization callback URL: http://localhost:5000/api/auth/github/callback
```

### Step 3: Register Application

1. Click **"Register application"**
2. You'll see your **Client ID**
3. Click **"Generate a new client secret"**
4. **Copy the client secret immediately** (you won't see it again!)

**Your GitHub OAuth credentials:**
```
GITHUB_CLIENT_ID: [your-client-id]
GITHUB_CLIENT_SECRET: [your-client-secret]
```

---

## 7️⃣ Groq AI API Setup

Groq provides **FREE** and **FAST** AI for question generation and evaluation.

### Step 1: Create Groq Account

1. Go to [console.groq.com](https://console.groq.com)
2. Click **"Sign Up"**
3. Sign up with Google, GitHub, or Email

### Step 2: Get API Key

1. After login, go to [console.groq.com/keys](https://console.groq.com/keys)
2. Click **"Create API Key"**
3. Name it: `InterviewAce`
4. Click **"Submit"**
5. **Copy the API key immediately!**

**Your Groq API key:**
```
GROQ_API_KEY: gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Note:** Groq is 100% FREE with generous limits (30 requests/min, 14,400/day)

---

## 8️⃣ Environment Configuration

### Step 1: Create .env File

```bash
# In project root directory
cp .env.example .env
```

Or create manually:
```bash
# Windows
type nul > .env

# Mac/Linux
touch .env
```

### Step 2: Edit .env File

Open `.env` in your text editor and fill in all values:

```env
# ============================================
# DATABASE CONFIGURATION
# ============================================
DB_HOST=localhost
DB_PORT=5432
DB_NAME=interviewace
DB_USER=postgres
DB_PASSWORD=your_postgres_password_here

# ============================================
# FLASK CONFIGURATION
# ============================================
FLASK_SECRET_KEY=your_random_secret_key_here_make_it_long_and_random
FLASK_HOST=localhost
FLASK_PORT=5000
FLASK_DEBUG=True

# ============================================
# EMAIL CONFIGURATION (BREVO SMTP)
# ============================================
SMTP_HOST=smtp-relay.brevo.com
SMTP_PORT=587
SMTP_USER=your_brevo_login@smtp-brevo.com
SMTP_PASSWORD=your_brevo_smtp_key_here
FROM_EMAIL=noreply@yourdomain.com

# ============================================
# GOOGLE OAUTH (OPTIONAL)
# ============================================
GOOGLE_CLIENT_ID=your_google_client_id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_google_client_secret

# ============================================
# GITHUB OAUTH (OPTIONAL)
# ============================================
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret

# ============================================
# AI CONFIGURATION (GROQ API - FREE)
# ============================================
GROQ_API_KEY=gsk_your_groq_api_key_here
```

### Step 3: Generate Secret Key

**Python method:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output and paste it as `FLASK_SECRET_KEY` value.

### Step 4: Verify .env File

Make sure:
- ✅ No spaces around `=` sign
- ✅ No quotes around values
- ✅ All passwords are correct
- ✅ File is named exactly `.env` (not `.env.txt`)

---

## 9️⃣ Running the Application

### Step 1: Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### Step 2: Start the Application

```bash
python app.py
```

**Expected output:**
```
Starting InterviewAce Application...
Server URL: http://localhost:5000
Database: SQLite
PostgreSQL database initialized
Tables: users (with OAuth support), results
Application ready!
 * Running on http://localhost:5000
```

### Step 3: Open Browser

Navigate to:
```
http://localhost:5000
```

You should see the InterviewAce landing page! 🎉

---

## 🔟 Testing the Setup

### Test 1: Local Signup (Email Verification)

1. Click **"Sign Up"**
2. Enter email and password
3. Click **"Create Account"**
4. Check your email inbox
5. Click verification link
6. Login with credentials

**Expected:** ✅ Verification email received and account verified

### Test 2: Google OAuth

1. Click **"Login with Google"**
2. Select your Google account
3. Authorize the app
4. Redirected to dashboard

**Expected:** ✅ Logged in successfully without email verification

### Test 3: GitHub OAuth

1. Click **"Login with GitHub"**
2. Authorize the app
3. Redirected to dashboard

**Expected:** ✅ Logged in successfully

### Test 4: Password Reset

1. Click **"Forgot Password"**
2. Enter your email
3. Check email for OTP
4. Enter OTP and new password
5. Login with new password

**Expected:** ✅ Password reset email received and password changed

### Test 5: Take Interview

1. Login to account
2. Click **"Start Interview"**
3. Select role and difficulty
4. Answer 10 questions
5. Submit interview
6. View results

**Expected:** ✅ Score, feedback, and company recommendations displayed

### Test 6: AI Question Generation

1. Start a written interview
2. Check console logs for "AI questions generated"
3. Questions should be unique each time

**Expected:** ✅ AI generates 10 questions (3 MCQ + 7 written)

### Test 7: AI Answer Evaluation

1. Complete an interview
2. Submit answers
3. Wait for AI evaluation (10-20 seconds)
4. View comprehensive report

**Expected:** ✅ Detailed feedback with strengths, improvements, recommendations

### Test 8: View History

1. Go to **"History"** page
2. See your past interviews
3. Click on any result
4. View detailed breakdown

**Expected:** ✅ Interview history displayed correctly

---

## 1️⃣1️⃣ Troubleshooting

### Issue 1: Database Connection Error

**Error:**
```
psycopg2.OperationalError: could not connect to server
```

**Solution:**
1. Check PostgreSQL is running:
   ```bash
   # Windows
   services.msc
   # Look for "postgresql" service
   
   # Mac
   brew services list
   
   # Linux
   sudo systemctl status postgresql
   ```
2. Verify credentials in `.env` file
3. Test connection: `psql -U postgres -d interviewace`

### Issue 2: Email Not Sending

**Error:**
```
SMTPAuthenticationError: Username and Password not accepted
```

**Solution:**
1. Verify Brevo SMTP credentials
2. Check if SMTP key is correct (regenerate if needed)
3. Verify sender email is verified in Brevo
4. Check `.env` file has correct values

### Issue 3: Google OAuth Not Working

**Error:**
```
redirect_uri_mismatch
```

**Solution:**
1. Go to Google Cloud Console
2. Check **Authorized redirect URIs** includes:
   ```
   http://localhost:5000/api/auth/google/callback
   ```
3. Make sure there are no trailing slashes
4. Wait 5 minutes for changes to propagate

### Issue 4: GitHub OAuth Not Working

**Error:**
```
The redirect_uri MUST match the registered callback URL
```

**Solution:**
1. Go to GitHub OAuth App settings
2. Verify callback URL is exactly:
   ```
   http://localhost:5000/api/auth/github/callback
   ```
3. No trailing slash
4. Save changes

### Issue 5: Module Not Found

**Error:**
```
ModuleNotFoundError: No module named 'flask'
```

**Solution:**
1. Activate virtual environment
2. Reinstall dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Issue 6: Port Already in Use

**Error:**
```
OSError: [Errno 48] Address already in use
```

**Solution:**
1. Change port in `.env`:
   ```env
   FLASK_PORT=5001
   ```
2. Or kill process using port 5000:
   ```bash
   # Windows
   netstat -ano | findstr :5000
   taskkill /PID [PID] /F
   
   # Mac/Linux
   lsof -ti:5000 | xargs kill -9
   ```

### Issue 7: Groq API Error

**Error:**
```
401 Unauthorized: Invalid API key
```

**Solution:**
1. Verify Groq API key in `.env`
2. Check for extra spaces
3. Regenerate key from [console.groq.com/keys](https://console.groq.com/keys)
4. Restart application

### Issue 8: AI Timeout

**Error:**
```
Timeout after 30 seconds
```

**Solution:**
1. Check internet connection
2. System falls back to static questions automatically
3. Try again after 1 minute

### Issue 9: Secret Key Error

**Error:**
```
RuntimeError: The session is unavailable because no secret key was set
```

**Solution:**
1. Generate new secret key:
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
2. Add to `.env`:
   ```env
   FLASK_SECRET_KEY=[generated_key]
   ```

---

## 📝 Quick Reference

### Start Application
```bash
# Activate virtual environment
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Run application
python app.py
```

### Stop Application
```
Press Ctrl + C in terminal
```

### View Database
```bash
psql -U postgres -d interviewace

# View users
SELECT email, auth_provider, is_verified FROM users;

# View results
SELECT user_id, score, created_at FROM results;

# Exit
\q
```

### Reset Database
```bash
# Connect to PostgreSQL
psql -U postgres -d interviewace

# Drop tables
DROP TABLE results;
DROP TABLE users;

# Exit and restart application
\q
python app.py
# Tables will be recreated automatically
```

---

## Production Deployment

### For Production Environment:

1. **Change Debug Mode:**
   ```env
   FLASK_DEBUG=False
   ```

2. **Use Strong Secret Key:**
   ```bash
   python -c "import secrets; print(secrets.token_hex(64))"
   ```

3. **Update OAuth Redirect URIs:**
   - Google: `https://yourdomain.com/api/auth/google/callback`
   - GitHub: `https://yourdomain.com/api/auth/github/callback`

4. **Use Production Database:**
   - Consider managed PostgreSQL (AWS RDS, Heroku Postgres)
   - Update `DB_HOST`, `DB_USER`, `DB_PASSWORD`

5. **Use Production SMTP:**
   - Brevo works for production
   - Or use AWS SES, SendGrid, Mailgun

6. **Deploy to:**
   - Heroku
   - AWS Elastic Beanstalk
   - DigitalOcean App Platform
   - Google Cloud Run
   - Azure App Service

---

## Setup Checklist

Before running the application, ensure:

- [ ] Python 3.8+ installed
- [ ] PostgreSQL 12+ installed and running
- [ ] Database `interviewace` created
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Brevo account created and SMTP credentials obtained
- [ ] Google OAuth app created (optional)
- [ ] GitHub OAuth app created (optional)
- [ ] `.env` file created with all credentials
- [ ] Secret key generated
- [ ] Application starts without errors
- [ ] Can access http://localhost:5000
- [ ] Email verification works
- [ ] OAuth login works (if configured)
- [ ] Can take interview and see results

---

## Setup Complete!

successfully set up InterviewAce! 

**Next Steps:**
- Take your first mock interview
- Explore different roles and difficulty levels
- Check your interview history
- Customize the application to your needs

**Need Help?**
- Check [PROJECT_DETAILS.md](PROJECT_DETAILS.md) for architecture details
- Review [FEATURES_IMPLEMENTED.md](FEATURES_IMPLEMENTED.md) for feature list
- See [VERIFICATION_SYSTEM.md](VERIFICATION_SYSTEM.md) for email verification details

---


