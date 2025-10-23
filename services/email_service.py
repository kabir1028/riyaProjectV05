import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

class EmailService:
    @staticmethod
    def send_verification_email(to_email, verification_token):
        try:
            smtp_server = os.getenv('SMTP_SERVER')
            smtp_port = int(os.getenv('SMTP_PORT', 587))
            smtp_username = os.getenv('SMTP_USERNAME')
            smtp_password = os.getenv('SMTP_PASSWORD')
            from_email = os.getenv('SMTP_FROM_EMAIL')
            from_name = os.getenv('SMTP_FROM_NAME', 'InterviewAce')
            app_url = os.getenv('APP_URL', 'http://localhost:5000')
            
            verification_link = f"{app_url}/verify-email?token={verification_token}"
            
            msg = MIMEMultipart('alternative')
            msg['Subject'] = 'Verify Your Email - InterviewAce'
            msg['From'] = f"{from_name} <{from_email}>"
            msg['To'] = to_email
            
            html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to InterviewAce</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
</head>
<body style="font-family: 'Inter', 'Segoe UI', sans-serif; background: linear-gradient(135deg, #ffffff 0%, #f0f9f0 50%, #e8f5e8 100%); padding: 40px 20px; margin: 0;">
    <div style="max-width: 650px; margin: 0 auto; background: rgba(255, 255, 255, 0.95); border-radius: 25px; overflow: hidden; box-shadow: 0 25px 50px rgba(34, 197, 94, 0.15); border: 1px solid rgba(34, 197, 94, 0.2);">
        <div style="height: 4px; background: linear-gradient(90deg, #22c55e, #16a34a);"></div>
        <div style="background: linear-gradient(135deg, #22c55e, #16a34a); padding: 50px 40px; text-align: center;">
            <div style="font-size: 48px; margin-bottom: 15px;">🎯</div>
            <h1 style="color: white; font-size: 32px; font-weight: 700; margin: 0 0 10px 0; text-shadow: 0 2px 10px rgba(0,0,0,0.2);">Welcome to InterviewAce!</h1>
            <p style="color: rgba(255,255,255,0.95); font-size: 18px; font-weight: 500; margin: 0;">Your AI-Powered Interview Success Platform</p>
        </div>
        <div style="padding: 50px 40px; background: rgba(255, 255, 255, 0.98);">
            <div style="background: rgba(34, 197, 94, 0.05); border-radius: 20px; padding: 30px; margin: 30px 0; border: 1px solid rgba(34, 197, 94, 0.1); border-top: 3px solid #22c55e;">
                <p style="font-size: 18px; color: #1a1a1a; line-height: 1.7; margin: 0 0 15px 0;"><strong>Congratulations! 🎉</strong></p>
                <p style="font-size: 18px; color: #1a1a1a; line-height: 1.7; margin: 0 0 15px 0;">You've just joined <strong>50,000+ professionals</strong> who are mastering their interview skills with InterviewAce.</p>
                <p style="font-size: 18px; color: #1a1a1a; line-height: 1.7; margin: 0;">To unlock your professional interview preparation journey, please verify your email address:</p>
            </div>
            <div style="text-align: center; margin: 40px 0;">
                <a href="{verification_link}" style="display: inline-block; background: linear-gradient(45deg, #22c55e, #16a34a); color: white; padding: 20px 50px; border-radius: 50px; text-decoration: none; font-weight: 700; font-size: 18px; box-shadow: 0 8px 25px rgba(34, 197, 94, 0.4); text-transform: uppercase; letter-spacing: 1px;">✅ Verify My Professional Account</a>
            </div>
            <div style="background: rgba(245, 158, 11, 0.05); border: 1px solid rgba(245, 158, 11, 0.2); border-radius: 10px; padding: 20px; margin: 30px 0; border-left: 4px solid #f59e0b;">
                <h4 style="color: #d97706; font-size: 16px; margin: 0 0 10px 0;">🛡️ Account Security</h4>
                <p style="color: #92400e; font-size: 14px; line-height: 1.5; margin: 0;">If you didn't create an InterviewAce account, you can safely ignore this email.</p>
            </div>
        </div>
        <div style="background: rgba(26, 26, 26, 0.95); padding: 40px; text-align: center; color: rgba(255, 255, 255, 0.8); border-top: 2px solid #22c55e;">
            <div style="font-size: 20px; font-weight: 700; color: white; margin-bottom: 10px;">InterviewAce</div>
            <div style="font-size: 14px; margin: 10px 0;">📧 info@mockinterviewer.com | 📞 +91-98765-43210</div>
            <div style="font-size: 12px; margin-top: 20px; opacity: 0.7;">© 2025 InterviewAce. All rights reserved.</div>
        </div>
    </div>
</body>
</html>
            """
            
            msg.attach(MIMEText(html, 'html'))
            
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"Email send error: {e}")
            return False
    
    @staticmethod
    def send_password_reset_otp(to_email, otp):
        try:
            smtp_server = os.getenv('SMTP_SERVER')
            smtp_port = int(os.getenv('SMTP_PORT', 587))
            smtp_username = os.getenv('SMTP_USERNAME')
            smtp_password = os.getenv('SMTP_PASSWORD')
            from_email = os.getenv('SMTP_FROM_EMAIL')
            from_name = os.getenv('SMTP_FROM_NAME', 'InterviewAce')
            app_url = os.getenv('APP_URL', 'http://localhost:5000')
            
            # OTP email - no link needed
            
            msg = MIMEMultipart('alternative')
            msg['Subject'] = 'Password Reset OTP - InterviewAce'
            msg['From'] = f"{from_name} <{from_email}>"
            msg['To'] = to_email
            
            html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Password Reset - InterviewAce</title>
</head>
<body style="font-family: Arial, sans-serif; background: #f8f9fa; padding: 20px; margin: 0;">
    <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
        <div style="background: #f59e0b; padding: 30px; text-align: center;">
            <h1 style="color: white; font-size: 24px; margin: 0;">🔐 InterviewAce</h1>
        </div>
        <div style="padding: 30px;">
            <div style="font-size: 16px; color: #333; line-height: 1.6; margin-bottom: 30px;">
                <p>Hello,</p>
                <p>You have requested to reset your InterviewAce account password.</p>
                <p>Your One-Time Password (OTP) is:</p>
            </div>
            <div style="text-align: center; margin: 30px 0;">
                <div style="font-size: 32px; font-weight: bold; color: #f59e0b; background: #f8f9fa; padding: 15px 30px; border-radius: 10px; letter-spacing: 5px; display: inline-block;">{otp}</div>
            </div>
            <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0; font-size: 14px; color: #666;">
                <p style="margin: 0 0 10px 0;"><strong>Important:</strong></p>
                <ul style="margin: 0; padding-left: 20px;">
                    <li>This link will expire in 10 minutes</li>
                    <li>Do not share this link with anyone</li>
                    <li>If you did not request this, please ignore this email</li>
                </ul>
            </div>
            <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0; font-size: 14px; color: #666;">
                <p style="margin: 0;"><strong>Need help?</strong> Contact us at support@mockinterviewer.com</p>
            </div>
        </div>
        <div style="background: #333; padding: 20px; text-align: center; color: white; font-size: 14px;">
            <p style="margin: 0 0 5px 0;">InterviewAce - AI Interview Platform</p>
            <p style="margin: 0;">© 2025 InterviewAce. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
            """
            
            msg.attach(MIMEText(html, 'html'))
            
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"Email send error: {e}")
            return False
