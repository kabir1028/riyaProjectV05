import uuid
import secrets
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from models.database import DatabaseManager
from services.email_service import EmailService
import psycopg2

class UserService:
    @staticmethod
    def create_user(email, password, is_guest=False, auth_provider='local', oauth_id=None, name=None, avatar_url=None):
        try:
            conn = DatabaseManager.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT id, email, auth_provider, is_verified, password_hash FROM users WHERE email = %s', (email,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                user_id = existing_user[0]
                existing_provider = existing_user[2]
                is_verified = existing_user[3]
                has_password = existing_user[4] is not None
                
                if auth_provider != 'local':
                    if not has_password:
                        random_password = secrets.token_urlsafe(32)
                        password_hash = generate_password_hash(random_password)
                        cursor.execute('UPDATE users SET password_hash = %s WHERE id = %s', (password_hash, user_id))
                    
                    cursor.execute('UPDATE users SET auth_provider = %s, oauth_id = %s, name = COALESCE(%s, name), avatar_url = COALESCE(%s, avatar_url), is_verified = TRUE WHERE id = %s',
                                 (auth_provider, oauth_id, name, avatar_url, user_id))
                    conn.commit()
                
                cursor.close()
                conn.close()
                return {
                    'success': True,
                    'message': 'Login successful!',
                    'user': {
                        'id': user_id,
                        'email': email,
                        'access_token': f'token_{user_id}_{secrets.token_urlsafe(16)}'
                    }
                }
            
            user_id = str(uuid.uuid4())
            
            if auth_provider != 'local' and not password:
                random_password = secrets.token_urlsafe(32)
                password_hash = generate_password_hash(random_password)
            else:
                password_hash = generate_password_hash(password) if password else None
            
            verification_token = secrets.token_urlsafe(32) if auth_provider == 'local' else None
            is_verified = True if auth_provider != 'local' else False
            
            cursor.execute('''
                INSERT INTO users (id, email, password_hash, is_guest, auth_provider, oauth_id, name, avatar_url, verification_token, is_verified)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (user_id, email, password_hash, is_guest, auth_provider, oauth_id, name, avatar_url, verification_token, is_verified))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            if not is_guest and auth_provider == 'local':
                EmailService.send_verification_email(email, verification_token)
            
            message = 'Account created! Please check your email to verify.' if auth_provider == 'local' else 'Login successful!'
            
            return {
                'success': True,
                'message': message,
                'user': {
                    'id': user_id,
                    'email': email,
                    'access_token': f'token_{user_id}_{secrets.token_urlsafe(16)}'
                }
            }
            
        except psycopg2.IntegrityError:
            return {'success': False, 'message': 'Email already registered'}
        except Exception as e:
            print(f"Create user error: {e}")
            return {'success': False, 'message': 'Failed to create account'}

    @staticmethod
    def authenticate_user(email, password):
        try:
            conn = DatabaseManager.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT id, email, password_hash, auth_provider, is_verified FROM users WHERE email = %s AND is_guest = FALSE', (email,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if user:
                if user[3] != 'local':
                    return {'success': False, 'message': f'Please login with {user[3].title()}'}
                
                if not user[4]:
                    return {'success': False, 'message': 'Account not verified. Please check your email and verify first.'}
                
                if check_password_hash(user[2], password):
                    return {
                        'success': True,
                        'message': 'Login successful!',
                        'user': {
                            'id': user[0],
                            'email': user[1],
                            'access_token': f'token_{user[0]}_{secrets.token_urlsafe(16)}'
                        }
                    }
            return {'success': False, 'message': 'Invalid credentials'}
                
        except Exception as e:
            print(f"Auth error: {e}")
            return {'success': False, 'message': 'Login failed'}

    @staticmethod
    def create_guest_user(user_id):
        try:
            conn = DatabaseManager.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO users (id, email, is_guest, auth_provider)
                VALUES (%s, %s, TRUE, 'guest')
                ON CONFLICT (id) DO NOTHING
            ''', (user_id, f'guest_{user_id}@temp.com'))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return {'success': True, 'user_id': user_id}
            
        except Exception as e:
            print(f"Create guest error: {e}")
            return {'success': False, 'message': 'Failed to create guest'}
    
    @staticmethod
    def verify_email(token):
        try:
            conn = DatabaseManager.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('UPDATE users SET is_verified = TRUE, verification_token = NULL WHERE verification_token = %s', (token,))
            
            if cursor.rowcount > 0:
                conn.commit()
                cursor.close()
                conn.close()
                return {'success': True, 'message': 'Email verified successfully!'}
            else:
                cursor.close()
                conn.close()
                return {'success': False, 'message': 'Invalid or expired token'}
        except Exception as e:
            print(f"Verify email error: {e}")
            return {'success': False, 'message': 'Verification failed'}
    
    @staticmethod
    def request_password_reset(email):
        try:
            conn = DatabaseManager.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT id, is_verified FROM users WHERE email = %s AND is_guest = FALSE', (email,))
            user = cursor.fetchone()
            
            if user:
                if not user[1]:
                    cursor.close()
                    conn.close()
                    return {'success': False, 'message': 'Account not verified. Please check your email and verify first.'}
                
                import random
                otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
                otp_expiry = datetime.now() + timedelta(minutes=10)
                
                cursor.execute('UPDATE users SET reset_otp = %s, otp_expiry = %s WHERE email = %s', (otp, otp_expiry, email))
                conn.commit()
                EmailService.send_password_reset_otp(email, otp)
            
            cursor.close()
            conn.close()
            return {'success': True, 'message': 'If email exists, OTP sent to your email'}
        except Exception as e:
            print(f"Password reset request error: {e}")
            return {'success': False, 'message': 'Failed to process request'}
    
    @staticmethod
    def verify_otp(email, otp):
        try:
            conn = DatabaseManager.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT reset_otp, otp_expiry FROM users WHERE email = %s', (email,))
            user = cursor.fetchone()
            
            if not user or not user[0]:
                cursor.close()
                conn.close()
                return {'success': False, 'message': 'Invalid OTP'}
            
            if datetime.now() > user[1]:
                cursor.close()
                conn.close()
                return {'success': False, 'message': 'OTP expired. Please request a new one'}
            
            if user[0] == otp:
                cursor.execute('UPDATE users SET reset_otp = NULL WHERE email = %s', (email,))
                conn.commit()
                cursor.close()
                conn.close()
                return {'success': True, 'message': 'OTP verified!', 'email': email}
            else:
                cursor.close()
                conn.close()
                return {'success': False, 'message': 'Invalid OTP'}
        except Exception as e:
            print(f"OTP verification error: {e}")
            return {'success': False, 'message': 'Verification failed'}
    
    @staticmethod
    def reset_password(email, new_password):
        try:
            conn = DatabaseManager.get_connection()
            cursor = conn.cursor()
            
            password_hash = generate_password_hash(new_password)
            cursor.execute('UPDATE users SET password_hash = %s, otp_expiry = NULL, auth_provider = %s WHERE email = %s', (password_hash, 'local', email))
            
            if cursor.rowcount > 0:
                conn.commit()
                cursor.close()
                conn.close()
                return {'success': True, 'message': 'Password reset successfully! You can now login with your password.'}
            else:
                cursor.close()
                conn.close()
                return {'success': False, 'message': 'Failed to reset password'}
        except Exception as e:
            print(f"Password reset error: {e}")
            return {'success': False, 'message': 'Reset failed'}
    
    @staticmethod
    def resend_verification(email):
        try:
            conn = DatabaseManager.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT id, is_verified, auth_provider FROM users WHERE email = %s', (email,))
            user = cursor.fetchone()
            
            if not user:
                cursor.close()
                conn.close()
                return {'success': True, 'message': 'If email exists, verification sent'}
            
            if user[2] != 'local':
                cursor.close()
                conn.close()
                return {'success': False, 'message': 'OAuth accounts do not need verification'}
            
            if user[1]:
                cursor.close()
                conn.close()
                return {'success': False, 'message': 'Email already verified'}
            
            verification_token = secrets.token_urlsafe(32)
            cursor.execute('UPDATE users SET verification_token = %s WHERE email = %s', (verification_token, email))
            conn.commit()
            cursor.close()
            conn.close()
            
            EmailService.send_verification_email(email, verification_token)
            return {'success': True, 'message': 'Verification email sent!'}
        except Exception as e:
            print(f"Resend verification error: {e}")
            return {'success': False, 'message': 'Failed to resend verification'}
