# 🔧 Supabase Email Template Fix Guide

## 🚨 **Issue**: Email templates not showing custom design

### **Root Cause:**
Supabase email templates need to be **enabled** and **configured properly** in the dashboard.

---

## ✅ **Step-by-Step Fix:**

### **1. Enable Custom Email Templates**
1. Go to [Supabase Dashboard](https://app.supabase.com)
2. Select your project: `drfniemrrdjrwvlszdvy`
3. Navigate to **Authentication** → **Settings**
4. Scroll to **Email Templates** section
5. **Enable** the toggle for "Use custom email templates"

### **2. Configure Email Templates**
Go to **Authentication** → **Email Templates** and update:

#### **Confirm Signup Template:**
- **Subject**: `🎯 Welcome to InterviewAce - Verify Your Professional Account`
- **Body**: Copy the HTML from `EMAIL_TEMPLATES.md` (Confirm Signup section)

#### **Reset Password Template:**
- **Subject**: `🔐 Secure Password Reset - InterviewAce Account`
- **Body**: Copy the HTML from `EMAIL_TEMPLATES.md` (Reset Password section)

### **3. Update Redirect URLs**
In **Authentication** → **URL Configuration**:

- **Site URL**: `http://localhost:5000`
- **Redirect URLs**: 
  ```
  http://localhost:5000/auth/callback
  http://localhost:5000/reset-password
  http://localhost:5000/
  ```

### **4. Test Email Templates**
1. **Clear browser cache** and cookies
2. **Test signup** with a new email
3. **Test password reset** with existing email
4. Check email inbox for new template design

---

## 🎯 **Password Reset Flow Fixed:**

### **Before (Broken):**
Reset link → Home page ❌

### **After (Fixed):**
Reset link → `/reset-password` page → Update password → Login ✅

### **New Flow:**
1. User clicks "Forgot Password"
2. Enters email → Reset email sent
3. Clicks reset link in email
4. Redirected to `/reset-password` page
5. Enters new password
6. Password updated → Redirected to login

---

## 🔍 **Troubleshooting:**

### **If templates still look plain:**
1. Check if "Use custom email templates" is **enabled**
2. Verify HTML is saved correctly (no syntax errors)
3. Test with **incognito/private browser**
4. Wait 5-10 minutes for changes to propagate

### **If reset doesn't work:**
1. Check browser console for errors
2. Verify redirect URLs in Supabase settings
3. Test with fresh email address
4. Check if access_token is in URL parameters

---

## 📧 **Email Template Status Check:**

After implementing the fix, your emails should have:
- ✅ **Custom InterviewAce branding**
- ✅ **Green gradient backgrounds**
- ✅ **Glass morphism effects**
- ✅ **Professional typography**
- ✅ **Interactive buttons**
- ✅ **Mobile responsive design**

The password reset flow will now work properly with a dedicated reset password page!