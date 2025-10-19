# 🔧 Password Reset Fix Guide

## 🚨 **Issue**: Reset link not showing password reset page

The reset link `https://drfniemrrdjrwvlszdvy.supabase.co/auth/v1/verify?token=...&type=recovery&redirect_to=http://localhost:5000` is redirecting to home page instead of reset password page.

---

## ✅ **Solution Applied:**

### **1. Updated Auth Callback Handler**
- Now properly detects `type=recovery` parameter
- Handles both `access_token` and `token` parameters
- Redirects to `/reset-password` page with token

### **2. Enhanced Reset Password Page**
- Accepts both `access_token` and `token` parameters
- Stores token globally for form submission
- Better error handling for invalid tokens

### **3. Updated Home Route**
- Checks for password reset redirects
- Automatically forwards to reset page when needed

---

## 🔧 **Supabase Configuration Needed:**

### **CRITICAL: Update Email Template Redirect URL**
1. Go to [Supabase Dashboard](https://app.supabase.com)
2. Select your project: `drfniemrrdjrwvlszdvy`
3. Navigate to **Authentication** → **Email Templates**
4. Edit **Reset Password** template
5. **Change the button URL from:**
   ```
   {{ .ConfirmationURL }}
   ```
   **To:**
   ```
   http://localhost:5000/reset-password?token={{ .TokenHash }}&type=recovery
   ```

### **Alternative: Update Site URL**
Or change **Site URL** in **Authentication** → **URL Configuration** to:
```
http://localhost:5000/reset-password
```

---

## 🧪 **Test the Fix:**

### **Step 1: Request Password Reset**
1. Go to `/forgot-password`
2. Enter your email
3. Check email for reset link

### **Step 2: Click Reset Link**
The link should now:
1. ✅ Redirect to `/reset-password` page
2. ✅ Show password reset form
3. ✅ Allow you to enter new password
4. ✅ Update password successfully

### **Expected Flow:**
```
Email Reset Link → Supabase Verification → /reset-password Page → New Password Form → Success
```

---

## 🔍 **Troubleshooting:**

### **If still redirecting to home:**
1. Clear browser cache and cookies
2. Check Supabase redirect URLs are saved
3. Try with incognito/private browser
4. Verify Flask app is running on port 5000

### **If token is invalid:**
1. Request a new password reset
2. Use the link within 1 hour
3. Don't refresh the reset page multiple times

### **Check Browser Console:**
- Look for JavaScript errors
- Verify token is being extracted from URL
- Check network requests to `/api/auth/reset-password`

The password reset flow should now work completely from email to password update!