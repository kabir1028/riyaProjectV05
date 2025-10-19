# 📧 Enhanced Supabase Email Templates - InterviewAce Theme

## 🎨 **Premium Email Templates with Website Theme**

### **Step 1: Access Email Templates**
1. Go to [Supabase Dashboard](https://app.supabase.com)
2. Select your project: `drfniemrrdjrwvlszdvy`
3. Navigate to **Authentication** → **Email Templates**

---

## ✅ **Confirm Signup Template (Website Theme)**

### **Subject:**
```
🎯 Welcome to InterviewAce - Verify Your Professional Account
```

### **Body (HTML):**
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to InterviewAce</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #ffffff 0%, #f0f9f0 50%, #e8f5e8 100%); 
            padding: 40px 20px; 
            min-height: 100vh;
        }
        .email-container { 
            max-width: 650px; 
            margin: 0 auto; 
            background: rgba(255, 255, 255, 0.95); 
            backdrop-filter: blur(15px); 
            border-radius: 25px; 
            overflow: hidden; 
            box-shadow: 0 25px 50px rgba(34, 197, 94, 0.15);
            border: 1px solid rgba(34, 197, 94, 0.2);
            position: relative;
        }
        .email-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #22c55e, #16a34a);
        }
        .header { 
            background: linear-gradient(135deg, #22c55e, #16a34a); 
            padding: 50px 40px; 
            text-align: center; 
            position: relative;
            overflow: hidden;
        }
        .header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: rotate 20s linear infinite;
        }
        @keyframes rotate {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .logo { 
            font-size: 48px; 
            margin-bottom: 15px; 
            position: relative; 
            z-index: 2;
            filter: drop-shadow(0 5px 15px rgba(0,0,0,0.2));
        }
        .header h1 { 
            color: white; 
            font-size: 32px; 
            font-weight: 700; 
            margin-bottom: 10px; 
            position: relative; 
            z-index: 2;
            text-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }
        .header p { 
            color: rgba(255,255,255,0.95); 
            font-size: 18px; 
            font-weight: 500; 
            position: relative; 
            z-index: 2;
        }
        .content { 
            padding: 50px 40px; 
            background: rgba(255, 255, 255, 0.98);
        }
        .welcome-card {
            background: rgba(34, 197, 94, 0.05);
            border-radius: 20px;
            padding: 30px;
            margin: 30px 0;
            border: 1px solid rgba(34, 197, 94, 0.1);
            position: relative;
        }
        .welcome-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #22c55e, #16a34a);
            border-radius: 20px 20px 0 0;
        }
        .welcome-text { 
            font-size: 18px; 
            color: #1a1a1a; 
            line-height: 1.7; 
            margin-bottom: 30px; 
        }
        .verify-button-container {
            text-align: center;
            margin: 40px 0;
        }
        .verify-btn { 
            display: inline-block; 
            background: linear-gradient(45deg, #22c55e, #16a34a); 
            color: white; 
            padding: 20px 50px; 
            border-radius: 50px; 
            text-decoration: none; 
            font-weight: 700; 
            font-size: 18px; 
            box-shadow: 0 8px 25px rgba(34, 197, 94, 0.4);
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
            position: relative;
            overflow: hidden;
        }
        .verify-btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            transition: left 0.6s;
        }
        .verify-btn:hover::before {
            left: 100%;
        }
        .features-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); 
            gap: 25px; 
            margin: 40px 0; 
        }
        .feature-card { 
            background: rgba(255, 255, 255, 0.8); 
            padding: 25px; 
            border-radius: 15px; 
            border: 1px solid rgba(34, 197, 94, 0.1); 
            box-shadow: 0 4px 15px rgba(34, 197, 94, 0.08);
            transition: all 0.3s ease;
        }
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(34, 197, 94, 0.15);
        }
        .feature-icon { 
            font-size: 32px; 
            margin-bottom: 15px; 
            display: block;
            filter: drop-shadow(0 2px 5px rgba(34, 197, 94, 0.3));
        }
        .feature-title {
            font-size: 16px;
            font-weight: 600;
            color: #1a1a1a;
            margin-bottom: 8px;
        }
        .feature-desc {
            font-size: 14px;
            color: #6b7280;
            line-height: 1.5;
        }
        .stats-section {
            background: linear-gradient(135deg, rgba(34, 197, 94, 0.05), rgba(34, 197, 94, 0.02));
            border-radius: 20px;
            padding: 30px;
            margin: 30px 0;
            text-align: center;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-top: 20px;
        }
        .stat-item {
            padding: 20px;
            background: rgba(255, 255, 255, 0.8);
            border-radius: 15px;
            border: 1px solid rgba(34, 197, 94, 0.1);
        }
        .stat-number {
            font-size: 24px;
            font-weight: 700;
            color: #22c55e;
            display: block;
        }
        .stat-label {
            font-size: 12px;
            color: #6b7280;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-top: 5px;
        }
        .footer { 
            background: rgba(26, 26, 26, 0.95); 
            padding: 40px; 
            text-align: center; 
            color: rgba(255, 255, 255, 0.8); 
            position: relative;
        }
        .footer::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, #22c55e, #16a34a);
        }
        .footer-brand {
            font-size: 20px;
            font-weight: 700;
            color: white;
            margin-bottom: 10px;
        }
        .footer-contact {
            font-size: 14px;
            margin: 10px 0;
        }
        .footer-copyright {
            font-size: 12px;
            margin-top: 20px;
            opacity: 0.7;
        }
        .security-note {
            background: rgba(245, 158, 11, 0.05);
            border: 1px solid rgba(245, 158, 11, 0.2);
            border-radius: 10px;
            padding: 20px;
            margin: 30px 0;
            border-left: 4px solid #f59e0b;
        }
        .security-note h4 {
            color: #d97706;
            font-size: 16px;
            margin-bottom: 10px;
        }
        .security-note p {
            color: #92400e;
            font-size: 14px;
            line-height: 1.5;
        }
        @media (max-width: 600px) {
            .content { padding: 30px 25px; }
            .header { padding: 40px 25px; }
            .stats-grid { grid-template-columns: 1fr; }
            .features-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="email-container">
        <div class="header">
            <div class="logo">🎯</div>
            <h1>Welcome to InterviewAce!</h1>
            <p>Your AI-Powered Interview Success Platform</p>
        </div>
        
        <div class="content">
            <div class="welcome-card">
                <div class="welcome-text">
                    <p><strong>Congratulations! 🎉</strong></p>
                    <p>You've just joined <strong>50,000+ professionals</strong> who are mastering their interview skills with InterviewAce - the most advanced AI-powered mock interview platform.</p>
                    <p>To unlock your professional interview preparation journey, please verify your email address:</p>
                </div>
            </div>
            
            <div class="verify-button-container">
                <a href="{{ .ConfirmationURL }}" class="verify-btn">
                    ✅ Verify My Professional Account
                </a>
            </div>
            
            <div class="stats-section">
                <h3 style="color: #1a1a1a; margin-bottom: 10px;">🚀 Join Our Success Community</h3>
                <div class="stats-grid">
                    <div class="stat-item">
                        <span class="stat-number">50K+</span>
                        <span class="stat-label">Success Stories</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-number">95%</span>
                        <span class="stat-label">Success Rate</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-number">24/7</span>
                        <span class="stat-label">AI Available</span>
                    </div>
                </div>
            </div>
            
            <div class="features-grid">
                <div class="feature-card">
                    <span class="feature-icon">🤖</span>
                    <div class="feature-title">AI-Powered Questions</div>
                    <div class="feature-desc">Personalized questions based on your resume and target role</div>
                </div>
                <div class="feature-card">
                    <span class="feature-icon">📊</span>
                    <div class="feature-title">Performance Analytics</div>
                    <div class="feature-desc">Detailed insights with visual charts and benchmarking</div>
                </div>
                <div class="feature-card">
                    <span class="feature-icon">🏢</span>
                    <div class="feature-title">Company Matching</div>
                    <div class="feature-desc">Get matched with top companies based on your skills</div>
                </div>
                <div class="feature-card">
                    <span class="feature-icon">📈</span>
                    <div class="feature-title">Progress Tracking</div>
                    <div class="feature-desc">Monitor your improvement over time with detailed reports</div>
                </div>
            </div>
            
            <div class="security-note">
                <h4>🛡️ Account Security</h4>
                <p>If you didn't create an InterviewAce account, you can safely ignore this email. Your email will not be added to our system without verification.</p>
            </div>
        </div>
        
        <div class="footer">
            <div class="footer-brand">InterviewAce</div>
            <div class="footer-contact">📧 info@mockinterviewer.com | 📞 +91-98765-43210</div>
            <div class="footer-copyright">© 2025 InterviewAce. All rights reserved.</div>
        </div>
    </div>
</body>
</html>
```

---

## 🔐 **Reset Password Template (Premium Design)**

### **Subject:**
```
🔐 Secure Password Reset - InterviewAce Account
```

### **Body (HTML):**
```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reset Password - InterviewAce</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #ffffff 0%, #fef3c7 50%, #fde68a 100%); 
            padding: 40px 20px; 
            min-height: 100vh;
        }
        .email-container { 
            max-width: 650px; 
            margin: 0 auto; 
            background: rgba(255, 255, 255, 0.95); 
            backdrop-filter: blur(15px); 
            border-radius: 25px; 
            overflow: hidden; 
            box-shadow: 0 25px 50px rgba(245, 158, 11, 0.15);
            border: 1px solid rgba(245, 158, 11, 0.2);
            position: relative;
        }
        .email-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #f59e0b, #d97706);
        }
        .header { 
            background: linear-gradient(135deg, #f59e0b, #d97706); 
            padding: 50px 40px; 
            text-align: center; 
            position: relative;
            overflow: hidden;
        }
        .header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: rotate 20s linear infinite;
        }
        @keyframes rotate {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .security-icon { 
            font-size: 64px; 
            margin-bottom: 20px; 
            position: relative; 
            z-index: 2;
            filter: drop-shadow(0 5px 15px rgba(0,0,0,0.2));
            animation: pulse 2s ease-in-out infinite;
        }
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }
        .header h1 { 
            color: white; 
            font-size: 32px; 
            font-weight: 700; 
            margin-bottom: 10px; 
            position: relative; 
            z-index: 2;
            text-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }
        .header p { 
            color: rgba(255,255,255,0.95); 
            font-size: 18px; 
            font-weight: 500; 
            position: relative; 
            z-index: 2;
        }
        .content { 
            padding: 50px 40px; 
            background: rgba(255, 255, 255, 0.98);
        }
        .alert-card {
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.05), rgba(220, 38, 38, 0.02));
            border: 1px solid rgba(239, 68, 68, 0.2);
            border-radius: 20px;
            padding: 30px;
            margin: 30px 0;
            border-left: 4px solid #ef4444;
            position: relative;
        }
        .alert-card::before {
            content: '⚠️';
            position: absolute;
            top: -15px;
            left: 30px;
            background: white;
            padding: 5px 10px;
            border-radius: 50%;
            font-size: 20px;
        }
        .reset-text { 
            font-size: 18px; 
            color: #1a1a1a; 
            line-height: 1.7; 
            margin-bottom: 30px; 
        }
        .reset-button-container {
            text-align: center;
            margin: 40px 0;
            position: relative;
        }
        .reset-btn { 
            display: inline-block; 
            background: linear-gradient(45deg, #f59e0b, #d97706); 
            color: white; 
            padding: 20px 50px; 
            border-radius: 50px; 
            text-decoration: none; 
            font-weight: 700; 
            font-size: 18px; 
            box-shadow: 0 8px 25px rgba(245, 158, 11, 0.4);
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
            position: relative;
            overflow: hidden;
        }
        .reset-btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            transition: left 0.6s;
        }
        .reset-btn:hover::before {
            left: 100%;
        }
        .security-features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 40px 0;
        }
        .security-feature {
            background: rgba(245, 158, 11, 0.05);
            border: 1px solid rgba(245, 158, 11, 0.1);
            border-radius: 15px;
            padding: 25px;
            text-align: center;
            transition: all 0.3s ease;
        }
        .security-feature:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(245, 158, 11, 0.15);
        }
        .security-feature-icon {
            font-size: 32px;
            margin-bottom: 15px;
            display: block;
        }
        .security-feature-title {
            font-size: 16px;
            font-weight: 600;
            color: #d97706;
            margin-bottom: 8px;
        }
        .security-feature-desc {
            font-size: 14px;
            color: #92400e;
            line-height: 1.5;
        }
        .countdown-timer {
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(220, 38, 38, 0.05));
            border: 2px solid rgba(239, 68, 68, 0.2);
            border-radius: 20px;
            padding: 25px;
            text-align: center;
            margin: 30px 0;
            position: relative;
        }
        .countdown-timer::before {
            content: '⏰';
            position: absolute;
            top: -15px;
            left: 50%;
            transform: translateX(-50%);
            background: white;
            padding: 5px 10px;
            border-radius: 50%;
            font-size: 24px;
        }
        .timer-text {
            font-size: 18px;
            font-weight: 600;
            color: #dc2626;
            margin-bottom: 10px;
        }
        .timer-desc {
            font-size: 14px;
            color: #991b1b;
        }
        .help-section {
            background: rgba(34, 197, 94, 0.05);
            border: 1px solid rgba(34, 197, 94, 0.2);
            border-radius: 20px;
            padding: 30px;
            margin: 30px 0;
            text-align: center;
        }
        .help-section h3 {
            color: #16a34a;
            font-size: 20px;
            margin-bottom: 15px;
        }
        .help-section p {
            color: #166534;
            font-size: 14px;
            line-height: 1.6;
            margin-bottom: 15px;
        }
        .help-link {
            color: #22c55e;
            text-decoration: none;
            font-weight: 600;
            font-size: 14px;
        }
        .footer { 
            background: rgba(26, 26, 26, 0.95); 
            padding: 40px; 
            text-align: center; 
            color: rgba(255, 255, 255, 0.8); 
            position: relative;
        }
        .footer::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, #f59e0b, #d97706);
        }
        .footer-brand {
            font-size: 20px;
            font-weight: 700;
            color: white;
            margin-bottom: 10px;
        }
        .footer-contact {
            font-size: 14px;
            margin: 10px 0;
        }
        .footer-copyright {
            font-size: 12px;
            margin-top: 20px;
            opacity: 0.7;
        }
        @media (max-width: 600px) {
            .content { padding: 30px 25px; }
            .header { padding: 40px 25px; }
            .security-features { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="email-container">
        <div class="header">
            <div class="security-icon">🔐</div>
            <h1>Password Reset Request</h1>
            <p>Secure Your InterviewAce Account</p>
        </div>
        
        <div class="content">
            <div class="alert-card">
                <div class="reset-text">
                    <p><strong>Security Alert! 🚨</strong></p>
                    <p>We received a request to reset your <strong>InterviewAce</strong> account password. If this was you, click the secure button below to create a new password.</p>
                </div>
            </div>
            
            <div class="reset-button-container">
                <a href="{{ .ConfirmationURL }}" class="reset-btn">
                    🔑 Reset My Password Securely
                </a>
            </div>
            
            <div class="countdown-timer">
                <div class="timer-text">This link expires in 1 hour</div>
                <div class="timer-desc">For your security, this reset link will automatically expire</div>
            </div>
            
            <div class="security-features">
                <div class="security-feature">
                    <span class="security-feature-icon">🛡️</span>
                    <div class="security-feature-title">Bank-Level Security</div>
                    <div class="security-feature-desc">Your account remains protected until you create a new password</div>
                </div>
                <div class="security-feature">
                    <span class="security-feature-icon">⏱️</span>
                    <div class="security-feature-title">Time-Limited Access</div>
                    <div class="security-feature-desc">Reset link expires automatically for maximum security</div>
                </div>
                <div class="security-feature">
                    <span class="security-feature-icon">🔒</span>
                    <div class="security-feature-title">Encrypted Connection</div>
                    <div class="security-feature-desc">All password reset processes use secure encryption</div>
                </div>
            </div>
            
            <div class="help-section">
                <h3>🤔 Didn't request this reset?</h3>
                <p>If you didn't request a password reset, you can safely ignore this email. Your account security remains intact.</p>
                <p>However, if you're concerned about unauthorized access, please contact our security team immediately.</p>
                <a href="mailto:security@mockinterviewer.com" class="help-link">📧 Contact Security Team</a>
            </div>
            
            <div style="background: rgba(107, 114, 128, 0.05); padding: 20px; border-radius: 10px; margin: 30px 0; font-size: 12px; color: #6b7280; line-height: 1.5;">
                <strong>Troubleshooting:</strong> If the button doesn't work, copy and paste this URL into your browser:<br>
                <span style="word-break: break-all; color: #f59e0b; font-family: monospace;">{{ .ConfirmationURL }}</span>
            </div>
        </div>
        
        <div class="footer">
            <div class="footer-brand">InterviewAce Security</div>
            <div class="footer-contact">📧 security@mockinterviewer.com | 📞 +91-98765-43210</div>
            <div class="footer-copyright">© 2025 InterviewAce. All rights reserved.</div>
        </div>
    </div>
</body>
</html>
```

---

## 🎨 **Template Features:**

### **Verification Email:**
- ✅ **Website Theme Colors** - Green gradients matching your site
- ✅ **Glass Morphism Effects** - Backdrop blur and transparency
- ✅ **Animated Elements** - Rotating backgrounds, hover effects
- ✅ **Statistics Section** - Success metrics like your homepage
- ✅ **Feature Cards** - Grid layout matching your design
- ✅ **Professional Typography** - Inter font family
- ✅ **Mobile Responsive** - Adapts to all screen sizes

### **Password Reset Email:**
- ✅ **Security-Focused Design** - Orange/amber theme for urgency
- ✅ **Advanced Animations** - Pulsing security icon, hover effects
- ✅ **Security Features Grid** - Highlighting protection measures
- ✅ **Countdown Timer** - Visual expiration warning
- ✅ **Help Section** - Clear instructions for users
- ✅ **Professional Layout** - Consistent with your brand

## 🔧 **Implementation:**
1. Copy the HTML templates above
2. Paste into Supabase Dashboard → Authentication → Email Templates
3. Test with signup and password reset flows

These templates now perfectly match your website's modern design with glass morphism, gradients, and professional styling!