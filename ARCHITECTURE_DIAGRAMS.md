# InterviewAce - Architecture & System Design

## System Architecture Diagram

```
┌───────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                          │
├───────────────────────────────────────────────────────────────┤
│  Browser (Chrome, Firefox, Safari, Edge)                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────────┐    │
│  │   HTML5  │  │   CSS3   │  │JavaScript│  │  Toast      │    │
│  │ Templates│  │  Styles  │  │  Logic   │  │Notifications│    │
│  └──────────┘  └──────────┘  └──────────┘  └─────────────┘    │
└───────────────────────────────────────────────────────────────┘
                              ↕ HTTP/HTTPS
┌───────────────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                        │
├───────────────────────────────────────────────────────────────┤
│                      Flask Application                        │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │                    app.py (Entry Point)                 │  │
│  └─────────────────────────────────────────────────────────┘  │
│                              ↓                                │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │                    Controllers Layer                    │  │
│  │  ┌────────────────────┐    ┌───────────────────────┐    │  │
│  │  │ auth_controller.py │    │interview_controller.py│    │  │
│  │  │  - /api/auth/*     │    │  - /api/interview/*   │    │  │
│  │  │  - Login/Signup    │    │  - Start/Submit       │    │  │
│  │  │  - OAuth Callbacks │    │  - Results/History    │    │  │
│  │  └────────────────────┘    └───────────────────────┘    │  │
│  └─────────────────────────────────────────────────────────┘  │
│                              ↓                                │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │                    Services Layer                       │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │  │
│  │  │user_service  │  │interview_    │  │email_service │   │  │
│  │  │   .py        │  │service.py    │  │   .py        │   │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘   │  │
│  │  ┌──────────────┐  ┌──────────────┐                     │  │
│  │  │oauth_service │  │  ai_service  │                     │  │
│  │  │   .py        │  │    .py       │                     │  │
│  │  └──────────────┘  └──────────────┘                     │  │
│  └─────────────────────────────────────────────────────────┘  │
│                              ↓                                │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │                     Models Layer                        │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │  │
│  │  │ database.py  │  │   user.py    │  │  result.py   │   │  │
│  │  │ (DB Manager) │  │  (User Model)│  │(Result Model)│   │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘   │  │
│  └─────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────┘
                              ↕
┌───────────────────────────────────────────────────────────────┐
│                       DATA LAYER                              │
├───────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┐  │
│  │              PostgreSQL Database                        │  │
│  │  ┌────────────────┐         ┌────────────────┐          │  │
│  │  │  users table   │───────▶ │ results table │          │  │
│  │  │  (Primary)     │  FK     │  (Foreign Key) │          │  │
│  │  └────────────────┘         └────────────────┘          │  │
│  └─────────────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │              Static Data Files                          │  │
│  │  ┌────────────────┐                                     │  │
│  │  │questions.json  │  (900+ Interview Questions)         │  │
│  │  └────────────────┘                                     │  │
│  └─────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────┘
                              ↕
┌───────────────────────────────────────────────────────────────┐
│                    EXTERNAL SERVICES                          │
├───────────────────────────────────────────────────────────────┤
│  ┌───────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │  Brevo SMTP   │  │Google OAuth  │  │GitHub OAuth  │        │
│  │(Email Service)│  │   (Auth)     │  │   (Auth)     │        │
│  └───────────────┘  └──────────────┘  └──────────────┘        │
│  ┌──────────────┐                                             │
│  │  Groq API    │                                             │
│  │(AI Service)  │                                             │
│  └──────────────┘                                             │
└───────────────────────────────────────────────────────────────┘
```

## Application Flow Diagram

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────┐
│         Flask Application               │
│                                         │
│  ┌───────────────────────────────────┐  │
│  │  1. Request Received              │  │
│  │     - URL routing                 │  │
│  │     - Method validation           │  │
│  └───────────────────────────────────┘  │
│                 ↓                       │
│  ┌───────────────────────────────────┐  │
│  │  2. Controller Processing         │  │
│  │     - Parse request data          │  │
│  │     - Validate input              │  │
│  │     - Check authentication        │  │
│  └───────────────────────────────────┘  │
│                 ↓                       │
│  ┌───────────────────────────────────┐  │
│  │  3. Service Layer Logic           │  │
│  │     - Business logic execution    │  │
│  │     - Data processing             │  │
│  │     - External API calls          │  │
│  └───────────────────────────────────┘  │
│                 ↓                       │
│  ┌───────────────────────────────────┐  │
│  │  4. Database Operations           │  │
│  │     - Query execution             │  │
│  │     - Data retrieval/storage      │  │
│  │     - Transaction management      │  │
│  └───────────────────────────────────┘  │
│                 ↓                       │
│  ┌───────────────────────────────────┐  │
│  │  5. Response Generation           │  │
│  │     - Format data (JSON/HTML)     │  │
│  │     - Set status codes            │  │
│  │     - Add headers                 │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
                 ↓
         ┌───────────────┐
         │  JSON/HTML    │
         │   Response    │
         └───────────────┘
```

## 🔐 Authentication Flow Diagram

### Local Authentication Flow

```
┌──────────┐                                    ┌──────────────┐
│  User    │                                    │   System     │
└────┬─────┘                                    └──────┬───────┘
     │                                                 │
     │  1. Click "Sign Up"                             │
     ├────────────────────────────────────────────────▶
     │                                                 │
     │  2. Enter email + password                      │
     ├────────────────────────────────────────────────▶
     │                                                 │
     │                              3. Hash password   │
     │                              4. Generate token  │
     │                              5. Save to DB      │
     │                              6. Send email      │
     │                                                 │
     │  7. "Check your email" message                  │
     ◀────────────────────────────────────────────────┤
     │                                                 │
     │  8. Open email inbox                            │
     │  9. Click verification link                     │
     ├────────────────────────────────────────────────▶
     │                                                 │
     │                              10. Verify token   │
     │                              11. Mark verified  │
     │                                                 │
     │  12. "Email verified!" message                  │
     ◀────────────────────────────────────────────────┤
     │                                                 │
     │  13. Click "Login"                              │
     ├────────────────────────────────────────────────▶
     │                                                 │
     │  14. Enter credentials                          │
     ├────────────────────────────────────────────────▶
     │                                                 │
     │                              15. Check verified │
     │                              16. Verify password│
     │                              17. Create session │
     │                                                 │
     │  18. Redirect to dashboard                      │
     ◀────────────────────────────────────────────────┤                                                 
```

### OAuth Authentication Flow

```
┌──────────┐         ┌──────────────┐         ┌──────────────┐
│  User    │         │   System     │         │OAuth Provider│
└────┬─────┘         └──────┬───────┘         └──────┬───────┘
     │                      │                        │
     │  1. Click "Login     │                        │
     │     with Google"     │                        │
     ├─────────────────────▶                        │
     │                      │                        │
     │                      │  2. Redirect to Google │
     │                      ├────────────────────────▶
     │                      │                        │
     │  3. Google login page                         │
     ◀──────────────────────────────────────────────┤
     │                     │                         │
     │  4. Enter Google    │                         │
     │     credentials     │                         │
     ├──────────────────────────────────────────────▶
     │                      │                        │
     │                      │  5. Authorization code │
     │                      ◀───────────────────────┤
     │                      │                        │
     │                      │  6. Exchange for token │
     │                      ├────────────────────────▶
     │                      │                        │
     │                      │  7. User info (email,  │
     │                      │     name, picture)     │
     │                      ◀───────────────────────┤
     │                      │                        │
     │       8. Check if email exists in DB          │
     │       9. Create/update user                   │
     │       10. Mark as verified                    │
     │       11. Create session                      │
     │                      │                        │
     │  12. Redirect to     │                        │
     │      dashboard       │                        │
     ◀─────────────────────┤                        │
```

## Interview Flow Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                    INTERVIEW PROCESS                          │
└──────────────────────────────────────────────────────────────┘

    ┌─────────────┐
    │   START     │
    └──────┬──────┘
           │
           ▼
    ┌─────────────────┐
    │  User Logged In?│
    └────────┬────────┘
             │
        ┌────┴────┐
        │   NO    │   YES
        ▼         ▼
    ┌─────────┐  ┌──────────────────┐
    │ Redirect│  │ Show Start Page  │
    │to Login │  │ - Select Role    │
    └─────────┘  │ - Select Level   │
                 └────────┬─────────┘
                          │
                          ▼
                ┌─────────────────────┐
                │ Load Questions      │
                │ - Role-based        │
                │ - Difficulty-based  │
                │ - Random 10 Qs      │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Display Question 1  │
                │ - Show timer        │
                │ - Show progress     │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ User Answers        │
                │ - MCQ: Select option│
                │ - Text: Type answer │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ More Questions?     │
                └──────────┬──────────┘
                           │
                      ┌────┴────┐
                      │   YES   │   NO
                      ▼         ▼
            ┌──────────────┐  ┌──────────────────┐
            │Next Question │  │ Calculate Score  │
            │(Repeat loop) │  │ - MCQ: 20 pts    │
            └──────────────┘  │ - Text: 10-20 pts│
                              └────────┬─────────┘
                                       │
                                       ▼
                              ┌──────────────────┐
                              │ Generate Feedback│
                              │ - Performance    │
                              │ - Strengths      │
                              │ - Improvements   │
                              └────────┬─────────┘
                                       │
                                       ▼
                              ┌──────────────────┐
                              │ Recommend        │
                              │ Companies        │
                              │ - Based on score │
                              │ - Based on role  │
                              └────────┬─────────┘
                                       │
                                       ▼
                              ┌──────────────────┐
                              │ Save Result      │
                              │ - Store in DB    │
                              │ - Keep last 5    │
                              └────────┬─────────┘
                                       │
                                       ▼
                              ┌──────────────────┐
                              │ Display Results  │
                              │ - Score          │
                              │ - Feedback       │
                              │ - Companies      │
                              │ - Q&A Review     │
                              └────────┬─────────┘
                                       │
                                       ▼
                                  ┌────────┐
                                  │  END   │
                                  └────────┘
```

## Database Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         USERS TABLE                         │
├─────────────────────────────────────────────────────────────┤
│  PK  id                VARCHAR(255)                         │
│  UQ  email             VARCHAR(255)                         │
│      password_hash     VARCHAR(255)                         │
│      name              VARCHAR(255)                         │
│      avatar_url        TEXT                                 │
│      auth_provider     VARCHAR(50)   DEFAULT 'local'        │
│      oauth_id          VARCHAR(255)                         │
│      is_guest          BOOLEAN       DEFAULT FALSE          │
│      is_verified       BOOLEAN       DEFAULT FALSE          │
│      verification_token VARCHAR(255)                        │
│      reset_otp         VARCHAR(10)                          │
│      otp_expiry        TIMESTAMP                            │
│      phone             VARCHAR(50)                          │
│      user_role         VARCHAR(255)                         │
│      experience        VARCHAR(50)                          │
│      location          VARCHAR(255)                         │
│      bio               TEXT                                 │
│      created_at        TIMESTAMP     DEFAULT CURRENT_TS     │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ 1:N (One user has many results)
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                       RESULTS TABLE                         │
├─────────────────────────────────────────────────────────────┤
│  PK  id                VARCHAR(255)                         │
│  FK  user_id           VARCHAR(255)  → users.id             │
│      score             INTEGER                              │
│      feedback          TEXT                                 │
│      companies         TEXT          (JSON array)           │
│      answers           TEXT          (JSON array)           │
│      questions         TEXT          (JSON array)           │
│      created_at        TIMESTAMP     DEFAULT CURRENT_TS     │
└─────────────────────────────────────────────────────────────┘

Constraints:
- users.email: UNIQUE, NOT NULL
- results.user_id: FOREIGN KEY → users.id ON DELETE CASCADE
- Auto-cleanup: Keep only last 5 results per user
```

## Data Flow Diagram

### User Registration Data Flow

```
┌──────────┐      ┌──────────────┐     ┌──────────┐      ┌──────────┐
│  Browser │────▶│  Controller  │────▶│ Service  │────▶│ Database │
└──────────┘      └──────────────┘     └──────────┘      └──────────┘
     │                  │                    │                │
     │ POST /signup     │                    │                │
     │ {email,password} │                    │                │
     ├────────────────▶│                    │                │
     │                  │ create_user()      │                │
     │                  ├──────────────────▶│                │
     │                  │                    │ Hash password  │
     │                  │                    │ Generate UUID  │
     │                  │                    │ Generate token │
     │                  │                    │                │
     │                  │                    │ INSERT user    │
     │                  │                    ├──────────────▶│
     │                  │                    │                │
     │                  │                    │ User created   │
     │                  │                    ◀───────────────┤
     │                  │                    │                │
     │                  │                    │ Send email     │
     │                  │                    ├───────────────▶ Brevo
     │                  │                    │                │
     │                  │ {success: true}    │                │
     │                  ◀───────────────────┤                │
     │                  │                    │                │
     │ JSON response    │                    │                │
     ◀─────────────────┤                    │                │
```

### Interview Submission Data Flow

```
┌──────────┐      ┌──────────────┐      ┌──────────┐      ┌──────────┐
│  Browser │────▶│  Controller  │────▶ │ Service  │────▶│ Database │
└──────────┘      └──────────────┘      └──────────┘      └──────────┘
     │                  │                    │                  │
     │ POST /submit     │                    │                  │
     │ {answers[]}      │                    │                  │
     ├─────────────────▶│                   │                  │
     │                  │ submit_interview() │                  │
     │                  ├──────────────────▶│                  │
     │                  │                    │ Calculate score  │
     │                  │                    │ Generate feedback│
     │                  │                    │ Get companies    │
     │                  │                    │                  │
     │                  │                    │ INSERT result    │
     │                  │                    ├────────────────▶│
     │                  │                    │                  │
     │                  │                    │ Cleanup old      │
     │                  │                    │ results (>5)     │
     │                  │                    ├────────────────▶│
     │                  │                    │                  │
     │                  │ {score, feedback}  │                  │
     │                  ◀────────────────────┤                 │
     │                  │                    │                  │
     │ JSON response    │                    │                  │
     ◀─────────────────┤                    │                  │  
```

## Security Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    SECURITY LAYERS                           │
└─────────────────────────────────────────────────────────────┘

Layer 1: Transport Security
├─ HTTPS (Production)
├─ Secure Headers
└─ CORS Configuration

Layer 2: Authentication
├─ Password Hashing (Werkzeug)
│  ├─ PBKDF2 algorithm
│  ├─ SHA-256 hash
│  └─ Unique salt per password
├─ OAuth 2.0 (Google, GitHub)
│  ├─ Secure token exchange
│  ├─ State parameter (CSRF protection)
│  └─ Minimal scope requests
└─ Session Management
   ├─ Secure session cookies
   ├─ HTTP-only flag
   └─ Secret key signing

Layer 3: Authorization
├─ User verification check
├─ Session validation
└─ Resource ownership validation

Layer 4: Input Validation
├─ Email format validation
├─ Password strength requirements
├─ SQL injection prevention (parameterized queries)
└─ XSS prevention (input sanitization)

Layer 5: Data Protection
├─ No plain-text passwords
├─ Token expiration (OTP: 10 min)
├─ Single-use verification tokens
└─ Secure password reset flow

Layer 6: Database Security
├─ Foreign key constraints
├─ Cascade deletes
├─ Connection pooling
└─ Prepared statements
```

## Component Interaction Diagram

```
┌────────────────────────────────────────────────────────────────┐
│                    COMPONENT INTERACTIONS                      │
└────────────────────────────────────────────────────────────────┘

┌──────────────┐
│   Browser    │
└──────┬───────┘
       │
       ├──────────────────────────────────────────────┐
       │                                              │
       ▼                                              ▼
┌──────────────┐                              ┌──────────────┐
│ auth_        │                              │ interview_   │
│ controller   │                              │ controller   │
└──────┬───────┘                              └──────┬───────┘
       │                                             │
       ├────────────┬────────────┬───────────────────┤
       │            │            │                   │
       ▼            ▼            ▼                   ▼
┌──────────┐ ┌──────────┐ ┌──────────┐      ┌──────────┐
│  user_   │ │  oauth_  │ │  email_  │      │interview_│
│ service  │ │ service  │ │ service  │      │ service  │
└────┬─────┘ └────┬─────┘ └────┬─────┘      └────┬─────┘
     │            │            │                 │
     │            │            │                 │
     └────────────┴────────────┴─────────────────┘
                              │
                              ▼
                      ┌──────────────┐
                      │  database.py │
                      │ (DB Manager) │
                      └──────┬───────┘
                             │
                             ▼
                      ┌──────────────┐
                      │  PostgreSQL  │
                      │   Database   │
                      └──────────────┘

External Services:
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│  Brevo   │  │  Google  │  │  GitHub  │  │  Groq AI │
│  SMTP    │  │  OAuth   │  │  OAuth   │  │   API    │
└──────────┘  └──────────┘  └──────────┘  └──────────┘
```

## Request-Response Cycle

```
1. HTTP Request
   ↓
2. Flask Routing
   ↓
3. Blueprint Matching
   ↓
4. Controller Function
   ↓
5. Input Validation
   ↓
6. Authentication Check
   ↓
7. Service Layer Call
   ↓
8. Business Logic
   ↓
9. Database Query
   ↓
10. Data Processing
   ↓
11. Response Formatting
   ↓
12. HTTP Response
```

## Scalability Architecture

```
Current Architecture (Single Server):
┌────────────────────────────────────┐
│         Single Server              │
│  ┌─────────────────────────────┐   │
│  │   Flask Application         │   │
│  └─────────────────────────────┘   │
│  ┌─────────────────────────────┐   │
│  │   PostgreSQL Database       │   │
│  └─────────────────────────────┘   │
└────────────────────────────────────┘

Future Scalable Architecture:
┌─────────────────────────────────────────────────┐
│              Load Balancer (Nginx)              │
└──────────┬──────────────────────────┬───────────┘
           │                          │
    ┌──────▼──────┐            ┌──────▼──────┐
    │  Flask App  │            │  Flask App  │
    │  Instance 1 │            │  Instance 2 │
    └──────┬──────┘            └──────┬──────┘
           │                          │
           └──────────┬───────────────┘
                      │
           ┌──────────▼──────────┐
           │   Redis Cache       │
           └──────────┬──────────┘
                      │
           ┌──────────▼──────────┐
           │  PostgreSQL         │
           │  (Master-Replica)   │
           └─────────────────────┘
```
---