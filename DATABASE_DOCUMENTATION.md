# InterviewAce - Database Documentation

## Database Overview

**Database Type:** PostgreSQL 12+  
**Database Name:** `interviewace`  
**Tables:** 2 (users, results)  
**Relationships:** 1:N (One user to many results)

---

## Database Schema

### Complete Schema Diagram

```
┌────────────────────────────────────────────────────────────────┐
│                     DATABASE: interviewace                     │
└────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────┐
│ TABLE: users                                                   │
├──────────────────────┬──────────────────┬──────────────────────┤
│ Column               │ Type             │ Constraints          │
├──────────────────────┼──────────────────┼──────────────────────┤
│ id                   │ VARCHAR(255)     │ PRIMARY KEY          │
│ email                │ VARCHAR(255)     │ UNIQUE, NOT NULL     │
│ password_hash        │ VARCHAR(255)     │                      │
│ name                 │ VARCHAR(255)     │                      │
│ avatar_url           │ TEXT             │                      │
│ auth_provider        │ VARCHAR(50)      │ DEFAULT 'local'      │
│ oauth_id             │ VARCHAR(255)     │                      │
│ is_guest             │ BOOLEAN          │ DEFAULT FALSE        │
│ is_verified          │ BOOLEAN          │ DEFAULT FALSE        │
│ verification_token   │ VARCHAR(255)     │                      │
│ reset_otp            │ VARCHAR(10)      │                      │
│ otp_expiry           │ TIMESTAMP        │                      │
│ phone                │ VARCHAR(50)      │                      │
│ user_role            │ VARCHAR(255)     │                      │
│ experience           │ VARCHAR(50)      │                      │
│ location             │ VARCHAR(255)     │                      │
│ bio                  │ TEXT             │                      │
│ created_at           │ TIMESTAMP        │ DEFAULT NOW()        │
└──────────────────────┴──────────────────┴──────────────────────┘
                                │
                                │ 1:N Relationship
                                │ (One user → Many results)
                                ▼
┌────────────────────────────────────────────────────────────────┐
│ TABLE: results                                                 │
├──────────────────────┬──────────────────┬──────────────────────┤
│ Column               │ Type             │ Constraints          │
├──────────────────────┼──────────────────┼──────────────────────┤
│ id                   │ VARCHAR(255)     │ PRIMARY KEY          │
│ user_id              │ VARCHAR(255)     │ FOREIGN KEY → users  │
│ score                │ INTEGER          │ NOT NULL             │
│ feedback             │ TEXT             │                      │
│ companies            │ TEXT             │ (JSON array)         │
│ answers              │ TEXT             │ (JSON array)         │
│ questions            │ TEXT             │ (JSON array)         │
│ created_at           │ TIMESTAMP        │ DEFAULT NOW()        │
└──────────────────────┴──────────────────┴──────────────────────┘

Foreign Key Constraint:
results.user_id → users.id ON DELETE CASCADE
```

---

## Table Details

### 1. Users Table

**Purpose:** Store user account information and authentication data

**SQL Definition:**
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
    phone VARCHAR(50),
    user_role VARCHAR(255),
    experience VARCHAR(50),
    location VARCHAR(255),
    bio TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Column Descriptions:**

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `id` | VARCHAR(255) | Unique user identifier (UUID) | `5e434644-4ec6-4e34-a201-c36991804674` |
| `email` | VARCHAR(255) | User's email address (unique) | `john@example.com` |
| `password_hash` | VARCHAR(255) | Werkzeug hashed password | `pbkdf2:sha256:...` |
| `name` | VARCHAR(255) | User's display name | `John Doe` |
| `avatar_url` | TEXT | Profile picture URL | `https://lh3.googleusercontent.com/...` |
| `auth_provider` | VARCHAR(50) | Authentication method | `local`, `google`, `github` |
| `oauth_id` | VARCHAR(255) | OAuth provider's user ID | `1234567890` |
| `is_guest` | BOOLEAN | Guest user flag | `FALSE` |
| `is_verified` | BOOLEAN | Email verification status | `TRUE` |
| `verification_token` | VARCHAR(255) | Email verification token | `abc123...` |
| `reset_otp` | VARCHAR(10) | Password reset OTP | `123456` |
| `otp_expiry` | TIMESTAMP | OTP expiration time | `2024-10-23 10:30:00` |
| `phone` | VARCHAR(50) | User's phone number | `+1-555-0123` |
| `user_role` | VARCHAR(255) | Current job role | `Software Engineer` |
| `experience` | VARCHAR(50) | Experience level | `mid`, `senior` |
| `location` | VARCHAR(255) | User's location | `San Francisco, CA` |
| `bio` | TEXT | User biography | `Passionate developer...` |
| `created_at` | TIMESTAMP | Account creation date | `2024-10-01 08:00:00` |

**Indexes:**
```sql
CREATE UNIQUE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_auth_provider ON users(auth_provider);
CREATE INDEX idx_users_is_verified ON users(is_verified);
```

**Sample Data:**
```sql
INSERT INTO users (id, email, password_hash, name, auth_provider, is_verified)
VALUES (
    '5e434644-4ec6-4e34-a201-c36991804674',
    'john@example.com',
    'pbkdf2:sha256:600000$...',
    'John Doe',
    'local',
    TRUE
);
```

---

### 2. Results Table

**Purpose:** Store interview results and performance data

**SQL Definition:**
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

**Column Descriptions:**

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `id` | VARCHAR(255) | Unique result identifier (UUID) | `result-abc123...` |
| `user_id` | VARCHAR(255) | Foreign key to users table | `5e434644-4ec6-...` |
| `score` | INTEGER | Interview score (0-100) | `85` |
| `feedback` | TEXT | Performance feedback | `Excellent performance!` |
| `companies` | TEXT | JSON array of companies | `["Google","Microsoft"]` |
| `answers` | TEXT | JSON array of user answers | `[{"question":"..."}]` |
| `questions` | TEXT | JSON array of questions | `[{"text":"..."}]` |
| `created_at` | TIMESTAMP | Result timestamp | `2024-10-23 14:30:00` |

**Indexes:**
```sql
CREATE INDEX idx_results_user_id ON results(user_id);
CREATE INDEX idx_results_created_at ON results(created_at DESC);
CREATE INDEX idx_results_score ON results(score);
```

**Sample Data:**
```sql
INSERT INTO results (id, user_id, score, feedback, companies, answers, questions)
VALUES (
    'result-xyz789',
    '5e434644-4ec6-4e34-a201-c36991804674',
    85,
    'Excellent performance! Strong understanding of core concepts.',
    '["Google","Microsoft","Amazon","Meta"]',
    '[{"question":"What is...","answer":"...","correct":true}]',
    '[{"text":"What is...","type":"multiple-choice"}]'
);
```

---

## Relationships

### One-to-Many: Users → Results

```
┌──────────────┐         ┌──────────────┐
│    users     │         │   results    │
├──────────────┤         ├──────────────┤
│ id (PK)      │───────▶│ user_id (FK) │
│ email        │    1:N  │ score        │
│ name         │         │ feedback     │
│ ...          │         │ ...          │
└──────────────┘         └──────────────┘

Relationship Rules:
- One user can have multiple results
- Each result belongs to exactly one user
- Deleting a user cascades to delete all their results
- Results cannot exist without a user
```

**SQL Constraint:**
```sql
ALTER TABLE results
ADD CONSTRAINT fk_results_user
FOREIGN KEY (user_id)
REFERENCES users(id)
ON DELETE CASCADE;
```

---

## Data Flow Diagrams

### User Registration Flow

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │ POST /api/auth/signup
       │ {email, password}
       ▼
┌─────────────────────────────┐
│   auth_controller.py        │
│   signup()                  │
└──────┬──────────────────────┘
       │ UserService.create_user()
       ▼
┌─────────────────────────────┐
│   user_service.py           │
│   create_user()             │
│   - Generate UUID           │
│   - Hash password           │
│   - Generate token          │
└──────┬──────────────────────┘
       │ INSERT INTO users
       ▼
┌─────────────────────────────┐
│   PostgreSQL Database       │
│   users table               │
│   ┌───────────────────────┐ │
│   │ id: uuid              │ │
│   │ email: john@ex.com    │ │
│   │ password_hash: ...    │ │
│   │ is_verified: FALSE    │ │
│   │ verification_token: ..│ │
│   └───────────────────────┘ │
└─────────────────────────────┘
```

### Interview Submission Flow

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │ POST /api/interview/submit
       │ {answers: [...]}
       ▼
┌─────────────────────────────┐
│   interview_controller.py   │
│   submit_interview()        │
└──────┬──────────────────────┘
       │ InterviewService.calculate_score()
       ▼
┌─────────────────────────────┐
│   interview_service.py      │
│   - Calculate score         │
│   - Generate feedback       │
│   - Get companies           │
└──────┬──────────────────────┘
       │ INSERT INTO results
       ▼
┌─────────────────────────────┐
│   PostgreSQL Database       │
│   results table             │
│   ┌───────────────────────┐ │
│   │ id: result-uuid       │ │
│   │ user_id: user-uuid    │ │
│   │ score: 85             │ │
│   │ feedback: "Excellent" │ │
│   │ companies: [...]      │ │
│   └───────────────────────┘ │
└──────┬──────────────────────┘
       │ Cleanup old results
       │ DELETE WHERE count > 5
       ▼
┌─────────────────────────────┐
│   Keep only last 5 results  │
│   per user                  │
└─────────────────────────────┘
```

---

## Common Queries

### User Queries

**1. Find user by email:**
```sql
SELECT id, email, name, auth_provider, is_verified
FROM users
WHERE email = 'john@example.com';
```

**2. Check if email exists:**
```sql
SELECT EXISTS(
    SELECT 1 FROM users WHERE email = 'john@example.com'
) AS email_exists;
```

**3. Verify user credentials:**
```sql
SELECT id, email, password_hash, is_verified
FROM users
WHERE email = 'john@example.com'
  AND is_guest = FALSE;
```

**4. Get user profile:**
```sql
SELECT name, phone, user_role, experience, location, bio
FROM users
WHERE id = '5e434644-4ec6-4e34-a201-c36991804674';
```

**5. Update user profile:**
```sql
UPDATE users
SET name = 'John Doe',
    phone = '+1-555-0123',
    user_role = 'Software Engineer',
    experience = 'senior',
    location = 'San Francisco, CA',
    bio = 'Passionate developer...'
WHERE id = '5e434644-4ec6-4e34-a201-c36991804674';
```

**6. Verify email:**
```sql
UPDATE users
SET is_verified = TRUE,
    verification_token = NULL
WHERE verification_token = 'abc123...';
```

**7. Set password reset OTP:**
```sql
UPDATE users
SET reset_otp = '123456',
    otp_expiry = NOW() + INTERVAL '10 minutes'
WHERE email = 'john@example.com';
```

**8. Verify OTP:**
```sql
SELECT reset_otp, otp_expiry
FROM users
WHERE email = 'john@example.com'
  AND reset_otp = '123456'
  AND otp_expiry > NOW();
```

### Result Queries

**1. Save interview result:**
```sql
INSERT INTO results (id, user_id, score, feedback, companies, answers, questions)
VALUES (
    'result-xyz789',
    '5e434644-4ec6-4e34-a201-c36991804674',
    85,
    'Excellent performance!',
    '["Google","Microsoft"]',
    '[...]',
    '[...]'
);
```

**2. Get user's last 5 results:**
```sql
SELECT id, score, feedback, companies, created_at
FROM results
WHERE user_id = '5e434644-4ec6-4e34-a201-c36991804674'
ORDER BY created_at DESC
LIMIT 5;
```

**3. Get specific result:**
```sql
SELECT *
FROM results
WHERE id = 'result-xyz789'
  AND user_id = '5e434644-4ec6-4e34-a201-c36991804674';
```

**4. Count user's interviews:**
```sql
SELECT COUNT(*) AS total_interviews
FROM results
WHERE user_id = '5e434644-4ec6-4e34-a201-c36991804674';
```

**5. Get average score:**
```sql
SELECT AVG(score) AS average_score
FROM results
WHERE user_id = '5e434644-4ec6-4e34-a201-c36991804674';
```

**6. Cleanup old results (keep last 5):**
```sql
DELETE FROM results
WHERE user_id = '5e434644-4ec6-4e34-a201-c36991804674'
  AND id NOT IN (
    SELECT id
    FROM results
    WHERE user_id = '5e434644-4ec6-4e34-a201-c36991804674'
    ORDER BY created_at DESC
    LIMIT 5
  );
```

**7. Get results with user info:**
```sql
SELECT 
    r.id,
    r.score,
    r.feedback,
    r.created_at,
    u.name,
    u.email
FROM results r
JOIN users u ON r.user_id = u.id
WHERE r.user_id = '5e434644-4ec6-4e34-a201-c36991804674'
ORDER BY r.created_at DESC;
```

---

## Database Maintenance

### Backup Commands

**1. Backup entire database:**
```bash
pg_dump -U postgres -d interviewace > backup_$(date +%Y%m%d).sql
```

**2. Backup specific table:**
```bash
pg_dump -U postgres -d interviewace -t users > users_backup.sql
```

**3. Restore database:**
```bash
psql -U postgres -d interviewace < backup_20241023.sql
```

### Optimization Queries

**1. Analyze table statistics:**
```sql
ANALYZE users;
ANALYZE results;
```

**2. Vacuum tables:**
```sql
VACUUM ANALYZE users;
VACUUM ANALYZE results;
```

**3. Check table sizes:**
```sql
SELECT 
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

**4. Check index usage:**
```sql
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY idx_scan DESC;
```

---

## Performance Optimization

### Recommended Indexes

```sql
-- Users table indexes
CREATE UNIQUE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_auth_provider ON users(auth_provider);
CREATE INDEX idx_users_is_verified ON users(is_verified);
CREATE INDEX idx_users_created_at ON users(created_at DESC);

-- Results table indexes
CREATE INDEX idx_results_user_id ON results(user_id);
CREATE INDEX idx_results_created_at ON results(created_at DESC);
CREATE INDEX idx_results_score ON results(score);
CREATE INDEX idx_results_user_created ON results(user_id, created_at DESC);
```

### Query Optimization Tips

1. **Use indexes for WHERE clauses**
2. **Limit result sets with LIMIT**
3. **Use prepared statements (parameterized queries)**
4. **Avoid SELECT * (specify columns)**
5. **Use JOINs instead of subqueries when possible**
6. **Regular VACUUM and ANALYZE**

---

## Security Considerations

### Data Protection

1. **Password Hashing:**
   - Never store plain-text passwords
   - Use Werkzeug's PBKDF2 with SHA-256
   - Unique salt per password

2. **SQL Injection Prevention:**
   - Always use parameterized queries
   - Never concatenate user input into SQL
   - Use psycopg2's parameter substitution

3. **Data Encryption:**
   - Sensitive data encrypted at rest (production)
   - SSL/TLS for database connections (production)

4. **Access Control:**
   - Principle of least privilege
   - Separate read/write users (production)
   - Regular password rotation

### Example: Safe Query (Parameterized)

```python
# ✅ SAFE - Parameterized query
cursor.execute(
    'SELECT * FROM users WHERE email = %s',
    (email,)
)

# ❌ UNSAFE - String concatenation
cursor.execute(
    f'SELECT * FROM users WHERE email = "{email}"'
)
```

---

## Database Statistics

### Current Schema Stats

```
Total Tables: 2
Total Columns: 26
Total Indexes: 8
Total Constraints: 3

Users Table:
- Columns: 18
- Indexes: 4
- Constraints: 2 (PK, UNIQUE)

Results Table:
- Columns: 8
- Indexes: 4
- Constraints: 2 (PK, FK)
```

### Storage Estimates

```
Average User Record: ~500 bytes
Average Result Record: ~2 KB (with JSON data)

For 10,000 users:
- Users table: ~5 MB
- Results table (5 per user): ~100 MB
- Total: ~105 MB

For 100,000 users:
- Users table: ~50 MB
- Results table: ~1 GB
- Total: ~1.05 GB
```

---

## Migration Scripts

### Add Profile Columns (Already Applied)

```sql
-- Add profile columns to users table
ALTER TABLE users ADD COLUMN IF NOT EXISTS phone VARCHAR(50);
ALTER TABLE users ADD COLUMN IF NOT EXISTS user_role VARCHAR(255);
ALTER TABLE users ADD COLUMN IF NOT EXISTS experience VARCHAR(50);
ALTER TABLE users ADD COLUMN IF NOT EXISTS location VARCHAR(255);
ALTER TABLE users ADD COLUMN IF NOT EXISTS bio TEXT;
```

### Future Migrations

**Add interview_type column:**
```sql
ALTER TABLE results ADD COLUMN interview_type VARCHAR(50) DEFAULT 'standard';
```

**Add difficulty_level column:**
```sql
ALTER TABLE results ADD COLUMN difficulty_level VARCHAR(20);
```

**Add role column:**
```sql
ALTER TABLE results ADD COLUMN role VARCHAR(100);
```

---

## Database Changelog

### Version 1.0 (October 1, 2024)
- Created users table
- Created results table
- Added foreign key constraint
- Added basic indexes

### Version 1.1 (October 15, 2024)
- Added profile columns (phone, user_role, experience, location, bio)
- Added profile indexes
- Updated documentation

---

