from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import json
import os
import uuid
import requests
import random

from datetime import datetime, timedelta
from dotenv import load_dotenv
from supabase_client import get_supabase_client

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')
if not app.secret_key:
    raise ValueError('FLASK_SECRET_KEY environment variable is required')

# Get Supabase client
supabase = get_supabase_client()

# In-memory OTP storage (use Redis in production)
otp_storage = {}



@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/interview')
def interview():
    return render_template('interview.html')

@app.route('/start-interview')
def start_interview():
    return render_template('start_interview.html')

@app.route('/results')
@app.route('/results/<result_id>')
def results(result_id=None):
    return render_template('results.html', result_id=result_id)

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/forgot-password')
def forgot_password():
    return render_template('forgot_password.html')

@app.route('/reset-password')
def reset_password():
    return render_template('reset_password.html')

@app.route('/verify-otp')
def verify_otp():
    return render_template('verify_otp.html')

@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Authentication routes
@app.route('/api/auth/signup', methods=['POST'])
def auth_signup():
    try:
        email = request.json.get('email')
        password = request.json.get('password')
        
        if not email or not password:
            return jsonify({'success': False, 'message': 'Email and password required'}), 400
        
        response = supabase.auth_signup(email, password)
        
        if response.status_code == 200:
            return jsonify({
                'success': True,
                'message': 'Account created successfully! Please check your email for verification.',
                'user': response.json()
            })
        else:
            return jsonify({'success': False, 'message': 'Failed to create account'}), 400
            
    except Exception:
        return jsonify({'success': False, 'message': 'Signup failed'}), 400

@app.route('/api/auth/login', methods=['POST'])
def auth_login():
    try:
        email = request.json.get('email')
        password = request.json.get('password')
        
        if not email or not password:
            return jsonify({'success': False, 'message': 'Email and password required'}), 400
        
        response = supabase.auth_login(email, password)
        
        if response.status_code == 200:
            user_data = response.json()
            session['user'] = user_data
            return jsonify({
                'success': True,
                'message': 'Login successful!',
                'user': user_data
            })
        else:
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
            
    except Exception:
        return jsonify({'success': False, 'message': 'Login failed'}), 401

@app.route('/api/auth/logout', methods=['POST'])
def auth_logout():
    try:
        session.clear()
        return jsonify({
            'success': True,
            'message': 'Logged out successfully'
        })
    except Exception:
        return jsonify({
            'success': False,
            'message': 'Logout failed'
        }), 400

@app.route('/auth/callback')
def auth_callback():
    """Handle Supabase auth callback"""
    # Get all URL parameters
    access_token = request.args.get('access_token')
    refresh_token = request.args.get('refresh_token')
    callback_type = request.args.get('type', 'signup')
    
    # Also check for token in URL fragment (common with Supabase)
    if not access_token:
        # Check if we're being redirected from password reset
        token = request.args.get('token')
        reset_type = request.args.get('type')
        
        if token and reset_type == 'recovery':
            # This is a password reset, redirect to reset page with token
            return redirect(f'/reset-password?token={token}&type=recovery')
    
    if access_token:
        # Store token in session
        session['access_token'] = access_token
        
        # Check if this is a password reset
        if callback_type == 'recovery':
            return redirect(f'/reset-password?access_token={access_token}')
        else:
            # Regular signup verification
            return redirect('/?verified=true')
    else:
        return redirect('/?error=verification_failed')

@app.route('/')
def home():
    """Handle home page with potential reset redirect"""
    # Check if this is a password reset redirect
    token = request.args.get('token')
    reset_type = request.args.get('type')
    
    if token and reset_type == 'recovery':
        return redirect(f'/reset-password?token={token}&type=recovery')
    
    return render_template('index.html')

@app.route('/api/auth/forgot-password', methods=['POST'])
def forgot_password_api():
    try:
        email = request.json.get('email')
        if not email:
            return jsonify({'success': False, 'message': 'Email required'}), 400
        
        # Generate 6-digit OTP
        otp = str(random.randint(100000, 999999))
        
        # Store OTP with expiration (10 minutes)
        otp_storage[email] = {
            'otp': otp,
            'expires': datetime.now() + timedelta(minutes=10)
        }
        
        # Try to send email, fallback to showing OTP
        email_sent = send_otp_email(email, otp)
        
        if email_sent:
            return jsonify({'success': True, 'message': 'OTP sent to your email. Please check your inbox.'})
        else:
            # Fallback for development
            print(f"OTP for {email}: {otp}")
            return jsonify({'success': False, 'message': 'Failed to send OTP. Please try again.'}), 500
    except:
        return jsonify({'success': False, 'message': 'Failed to send OTP'}), 400

@app.route('/api/auth/resend-verification', methods=['POST'])
def resend_verification():
    try:
        email = request.json.get('email')
        
        response = supabase.auth_resend_verification(email)
        
        return jsonify({
            'success': True,
            'message': 'Verification email sent! Check your inbox.'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Failed to send verification email. Please try again.'
        }), 400

@app.route('/api/auth/verify-otp', methods=['POST'])
def verify_otp_api():
    try:
        email = request.json.get('email')
        otp = request.json.get('otp')
        
        if not email or not otp:
            return jsonify({'success': False, 'message': 'Email and OTP required'}), 400
        
        # Check if OTP exists and is valid
        if email in otp_storage:
            stored_data = otp_storage[email]
            if datetime.now() > stored_data['expires']:
                del otp_storage[email]
                return jsonify({'success': False, 'message': 'OTP expired'}), 400
            
            if stored_data['otp'] == otp:
                # OTP is valid, mark as verified
                otp_storage[email]['verified'] = True
                return jsonify({'success': True, 'message': 'OTP verified successfully'})
        
        return jsonify({'success': False, 'message': 'Invalid OTP'}), 400
    except:
        return jsonify({'success': False, 'message': 'Verification failed'}), 400

@app.route('/api/auth/reset-password', methods=['POST'])
def reset_password_api():
    try:
        email = request.json.get('email')
        password = request.json.get('password')
        
        if not email or not password:
            return jsonify({'success': False, 'message': 'Email and password required'}), 400
        
        # Check if OTP was verified
        if email not in otp_storage or not otp_storage[email].get('verified'):
            return jsonify({'success': False, 'message': 'Please verify OTP first'}), 400
        
        # Use admin API to update password
        headers = {
            'apikey': os.getenv('SUPABASE_SERVICE_KEY'),
            'Authorization': f'Bearer {os.getenv("SUPABASE_SERVICE_KEY")}',
            'Content-Type': 'application/json'
        }
        
        # Get user by email first
        users_response = requests.get(
            f"{os.getenv('SUPABASE_URL')}/auth/v1/admin/users",
            headers=headers
        )
        
        print(f"Users API response: {users_response.status_code}")
        
        if users_response.status_code == 200:
            users_data = users_response.json()
            users = users_data.get('users', [])
            user = next((u for u in users if u.get('email') == email), None)
            
            print(f"Found user: {user is not None}")
            
            if user:
                user_id = user['id']
                print(f"Updating password for user ID: {user_id}")
                
                # Update password using admin API
                update_response = requests.put(
                    f"{os.getenv('SUPABASE_URL')}/auth/v1/admin/users/{user_id}",
                    json={'password': password},
                    headers=headers
                )
                
                print(f"Update response: {update_response.status_code}, {update_response.text}")
                
                if update_response.status_code == 200:
                    # Clear OTP data
                    del otp_storage[email]
                    return jsonify({'success': True, 'message': 'Password updated successfully!'})
                else:
                    return jsonify({'success': False, 'message': f'Update failed: {update_response.text}'}), 400
            else:
                return jsonify({'success': False, 'message': 'User not found'}), 404
        else:
            return jsonify({'success': False, 'message': f'Failed to get users: {users_response.text}'}), 400
    except:
        return jsonify({'success': False, 'message': 'Reset failed'}), 400

@app.route('/api/profile/history')
def get_profile_history():
    """Get user's last 3 interview results"""
    try:
        user_id = session.get('user', {}).get('id')
        if not user_id:
            return jsonify({'error': 'User not authenticated'}), 401
        
        # Get last 5 results for user
        response = supabase.select('results', {'user_id': user_id})
        
        if response.status_code == 200:
            results = response.json()
            # Sort by created_at and get last 5
            sorted_results = sorted(results, key=lambda x: x['created_at'], reverse=True)[:5]
            
            history = []
            for result in sorted_results:
                history.append({
                    'id': result['id'],
                    'score': result['score'],
                    'feedback': result['feedback'],
                    'created_at': result['created_at'],
                    'companies': json.loads(result['companies'])[:3]  # Show only 3 companies
                })
            
            return jsonify({
                'success': True,
                'history': history,
                'total_interviews': len(results)
            })
        else:
            return jsonify({
                'success': True,
                'history': [],
                'total_interviews': 0
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/get-result/<result_id>')
def get_result(result_id):
    try:
        response = supabase.select('results', {'id': result_id})
        
        if response.status_code == 200 and response.json():
            result = response.json()[0]
            return jsonify({
                'id': result['id'],
                'score': result['score'],
                'feedback': result['feedback'],
                'companies': json.loads(result['companies']),
                'answers': json.loads(result['answers']),
                'questions': json.loads(result['questions'])
            })
        else:
            # Return demo data if no result found
            return jsonify({
                'id': 'demo',
                'score': 75,
                'feedback': 'This is a demo result. Take an interview to see your actual performance.',
                'companies': ['Google', 'Microsoft', 'Amazon', 'Meta', 'Apple', 'Netflix', 'Uber', 'Airbnb'],
                'answers': [
                    {'questionId': 0, 'text': 'Demo answer for behavioral question', 'type': 'short-answer'},
                    {'questionId': 1, 'selectedOption': 0, 'correct': True, 'type': 'multiple-choice'}
                ],
                'questions': [
                    {'question': 'Tell me about yourself', 'type': 'short-answer'},
                    {'question': 'What is your greatest strength?', 'type': 'multiple-choice', 'options': ['Leadership', 'Technical Skills', 'Communication', 'Problem Solving'], 'correctAnswer': 0}
                ]
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/questions')
def get_questions():
    role = request.args.get('role', 'Software Engineer')
    difficulty = request.args.get('difficulty', 'Beginner')
    
    try:
        with open('data/questions.json', 'r') as f:
            data = json.load(f)
        questions = data.get(role, {}).get(difficulty, [])
        return jsonify(questions)
    except FileNotFoundError:
        return jsonify({'error': 'Questions file not found'}), 404
    except json.JSONDecodeError:
        return jsonify({'error': 'Invalid questions file format'}), 500
    except Exception:
        return jsonify({'error': 'Failed to load questions'}), 500

@app.route('/api/submit-answers', methods=['POST'])
def submit_answers():
    try:
        answers = request.json.get('answers', [])
        role = request.json.get('role', 'Software Engineer')
        questions = request.json.get('questions', [])
        
        score = calculate_score(answers)
        feedback = generate_feedback(score, role)
        companies = get_companies(score, role)
        
        # Store in Supabase
        result_id = str(uuid.uuid4())
        
        data = {
            'id': result_id,
            'score': score,
            'feedback': feedback,
            'companies': json.dumps(companies),
            'answers': json.dumps(answers),
            'questions': json.dumps(questions),
            'user_id': session.get('user', {}).get('id') if 'user' in session else None
        }
        
        response = supabase.insert('results', data)
        
        return jsonify({
            'id': result_id,
            'score': score,
            'feedback': feedback,
            'companies': companies
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def calculate_score(answers):
    if not answers:
        return 0
    
    score = 0
    for answer in answers:
        if answer.get('type') == 'multiple-choice':
            if answer.get('correct', False):
                score += 20  # 20 points for correct multiple choice
        elif answer.get('type') == 'short-answer':
            text = answer.get('text', '').strip()
            word_count = len(text.split()) if text else 0
            if word_count >= 20:
                score += 20  # 20 points for comprehensive answer
            elif word_count >= 10:
                score += 15  # 15 points for adequate answer
            elif word_count >= 5:
                score += 10  # 10 points for basic answer
    
    return min(100, score)

def generate_feedback(score, role):
    if score >= 80:
        return f"Excellent performance! You're well-prepared for {role} positions."
    elif score >= 60:
        return f"Good job! With some practice, you'll excel in {role} interviews."
    else:
        return f"Keep practicing! Focus on {role} fundamentals and technical skills."



def send_otp_email(email, otp):
    """Send OTP via email - configure SMTP in .env"""
    try:
        import smtplib
        from email.mime.text import MIMEText
        
        smtp_server = os.getenv('SMTP_SERVER')
        smtp_port = int(os.getenv('SMTP_PORT', '587'))
        smtp_username = os.getenv('SMTP_USERNAME')
        smtp_password = os.getenv('SMTP_PASSWORD')
        
        if not all([smtp_server, smtp_username, smtp_password]):
            return False
        
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <body style="font-family: Arial, sans-serif; background: #f8f9fa; padding: 20px; margin: 0;">
            <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                <div style="background: #f59e0b; padding: 30px; text-align: center;">
                    <h1 style="color: white; font-size: 24px; margin: 0;">🔐 InterviewAce</h1>
                </div>
                <div style="padding: 30px;">
                    <p>Hello,</p>
                    <p>You have requested to reset your InterviewAce account password.</p>
                    <p>Your One-Time Password (OTP) is:</p>
                    <div style="text-align: center; margin: 30px 0;">
                        <span style="font-size: 32px; font-weight: bold; color: #f59e0b; background: #f8f9fa; padding: 15px 30px; border-radius: 10px; letter-spacing: 5px;">{otp}</span>
                    </div>
                    <p><strong>Important:</strong></p>
                    <ul>
                        <li>This OTP will expire in 10 minutes</li>
                        <li>Do not share this OTP with anyone</li>
                        <li>If you did not request this, please ignore this email</li>
                    </ul>
                </div>
                <div style="background: #333; padding: 20px; text-align: center; color: white; font-size: 14px;">
                    <p>InterviewAce - AI Interview Platform</p>
                    <p>© 2025 InterviewAce. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        msg = MIMEText(html_body, 'html')
        msg['Subject'] = 'Your InterviewAce Password Reset OTP'
        msg['From'] = smtp_username
        msg['To'] = email
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
        
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False

def get_companies(score, role):
    companies = {
        'Software Engineer': ['Google', 'Microsoft', 'Amazon', 'Meta', 'Apple', 'Netflix', 'Uber', 'Airbnb'],
        'AI Scientist': ['OpenAI', 'DeepMind', 'NVIDIA', 'Tesla', 'IBM', 'Google AI', 'Microsoft Research', 'Amazon AI'],
        'Data Scientist': ['Netflix', 'Uber', 'Airbnb', 'Spotify', 'LinkedIn', 'Meta', 'Google', 'Amazon']
    }
    
    # Always return 8 companies for better grid display
    return companies.get(role, companies['Software Engineer'])[:8]

if __name__ == '__main__':
    host = os.getenv('FLASK_HOST', 'localhost')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"\n🚀 Starting InterviewAce Application...")
    print(f"📍 Server URL: http://{host}:{port}")
    print(f"🔧 Debug Mode: {'ON' if debug else 'OFF'}")
    print(f"💾 Database: Supabase")
    print(f"\n✨ Application ready! Open your browser and visit the URL above.\n")
    
    app.run(
        host=host,
        port=port,
        debug=debug
    )