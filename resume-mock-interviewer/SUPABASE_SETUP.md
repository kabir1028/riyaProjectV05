# 🔧 Supabase Configuration Guide

## 📋 **Step 1: Configure Redirect URLs**

1. Go to [Supabase Dashboard](https://app.supabase.com)
2. Select your project: `drfniemrrdjrwvlszdvy`
3. Navigate to **Authentication** → **URL Configuration**
4. Update the following settings:

### **Site URL**
```
http://localhost:5000
```

### **Redirect URLs** (Add these)
```
http://localhost:5000/auth/callback
http://localhost:5000/
http://localhost:5000/login
```

## 📊 **Step 2: Create Database Table**

Go to **SQL Editor** and run:

```sql
-- Create results table
CREATE TABLE IF NOT EXISTS results (
    id TEXT PRIMARY KEY,
    score INTEGER,
    feedback TEXT,
    companies TEXT,
    answers TEXT,
    questions TEXT,
    user_id UUID REFERENCES auth.users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE results ENABLE ROW LEVEL SECURITY;

-- Create policy for users to see their own results
CREATE POLICY "Users can view their own results" ON results
    FOR SELECT USING (auth.uid() = user_id);

-- Create policy for users to insert their own results
CREATE POLICY "Users can insert their own results" ON results
    FOR INSERT WITH CHECK (auth.uid() = user_id);
```

## ✅ **Step 3: Test Authentication**

1. Run your Flask app: `python app.py`
2. Go to `http://localhost:5000/signup`
3. Create account with email
4. Check email for verification link
5. Click verification link (should redirect to your app now)

## 🔄 **Current Issue Fix**

The verification link was redirecting to `localhost:3000` instead of `localhost:5000`. After updating the Supabase settings above, new verification emails will redirect correctly to your Flask app.

## 📝 **Email Template Settings** (Optional)

In Supabase Dashboard → **Authentication** → **Email Templates**:

- **Confirm signup**: Update redirect URL to `{{ .SiteURL }}/auth/callback`
- **Magic Link**: Update redirect URL to `{{ .SiteURL }}/auth/callback`

This ensures all auth emails redirect to your Flask application.