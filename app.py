from flask import Flask, render_template
import os
from config import Config
from models import DatabaseManager
from controllers import auth_bp, interview_bp

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

# Initialize database
DatabaseManager.init_db()

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(interview_bp)

# Page routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/start-interview')
def start_interview():
    return render_template('start_interview_new.html')

@app.route('/interview')
def interview():
    return render_template('interview.html')

@app.route('/results')
@app.route('/results/<result_id>')
def results(result_id=None):
    return render_template('results.html', result_id=result_id)

@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/forgot-password')
def forgot_password_page():
    return render_template('forgot_password.html')

@app.route('/reset-password')
def reset_password_page():
    return render_template('reset_password.html')

@app.route('/verify-email')
def verify_email_page():
    return render_template('verify_email.html')

@app.route('/verify-otp')
def verify_otp_page():
    return render_template('verify_otp.html')

if __name__ == '__main__':
    print(f"Starting InterviewAce Application...")
    print(f"Server URL: http://{Config.HOST}:{Config.PORT}")
    print(f"Database: SQLite")
    print(f"Application ready!")
    
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
