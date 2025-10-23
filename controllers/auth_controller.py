from flask import Blueprint, request, jsonify, session, redirect
from services.user_service import UserService
from services.oauth_service import OAuthService
import secrets

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'success': False, 'message': 'Email and password required'}), 400
        
        result = UserService.create_user(email, password)
        
        if result['success']:
            session['user'] = result['user']
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Signup API error: {e}")
        return jsonify({'success': False, 'message': 'Signup failed'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'success': False, 'message': 'Email and password required'}), 400
        
        result = UserService.authenticate_user(email, password)
        
        if result['success']:
            session['user'] = result['user']
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Login API error: {e}")
        return jsonify({'success': False, 'message': 'Login failed'}), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully'})

@auth_bp.route('/verify-email', methods=['POST'])
def verify_email():
    try:
        data = request.get_json()
        token = data.get('token')
        
        if not token:
            return jsonify({'success': False, 'message': 'Token required'}), 400
        
        result = UserService.verify_email(token)
        return jsonify(result)
    except Exception as e:
        print(f"Verify email API error: {e}")
        return jsonify({'success': False, 'message': 'Verification failed'}), 500

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    try:
        data = request.get_json()
        email = data.get('email')
        
        if not email:
            return jsonify({'success': False, 'message': 'Email required'}), 400
        
        result = UserService.request_password_reset(email)
        return jsonify(result)
    except Exception as e:
        print(f"Forgot password API error: {e}")
        return jsonify({'success': False, 'message': 'Request failed'}), 500

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'success': False, 'message': 'Email and password required'}), 400
        
        result = UserService.reset_password(email, password)
        return jsonify(result)
    except Exception as e:
        print(f"Reset password API error: {e}")
        return jsonify({'success': False, 'message': 'Reset failed'}), 500

@auth_bp.route('/google')
def google_login():
    auth_url = OAuthService.get_google_auth_url()
    return redirect(auth_url)

@auth_bp.route('/google/callback')
def google_callback():
    try:
        code = request.args.get('code')
        if not code:
            return redirect('/login?error=oauth_failed')
        
        user_info = OAuthService.get_google_user_info(code)
        if not user_info:
            return redirect('/login?error=oauth_failed')
        
        email = user_info.get('email')
        name = user_info.get('name')
        avatar_url = user_info.get('picture')
        oauth_id = user_info.get('id')
        
        result = UserService.create_user(
            email=email,
            password=None,
            auth_provider='google',
            oauth_id=oauth_id,
            name=name,
            avatar_url=avatar_url
        )
        
        if result['success']:
            session['user'] = result['user']
            session.modified = True
            return redirect('/?oauth_success=true')
        else:
            return redirect('/login?error=oauth_failed')
    except Exception as e:
        print(f"Google callback error: {e}")
        return redirect('/login?error=oauth_failed')

@auth_bp.route('/github')
def github_login():
    auth_url = OAuthService.get_github_auth_url()
    return redirect(auth_url)

@auth_bp.route('/github/callback')
def github_callback():
    try:
        code = request.args.get('code')
        if not code:
            return redirect('/login?error=oauth_failed')
        
        user_info = OAuthService.get_github_user_info(code)
        if not user_info:
            return redirect('/login?error=oauth_failed')
        
        email = user_info.get('email')
        name = user_info.get('name') or user_info.get('login')
        avatar_url = user_info.get('avatar_url')
        oauth_id = str(user_info.get('id'))
        
        result = UserService.create_user(
            email=email,
            password=None,
            auth_provider='github',
            oauth_id=oauth_id,
            name=name,
            avatar_url=avatar_url
        )
        
        if result['success']:
            session['user'] = result['user']
            session.modified = True
            return redirect('/?oauth_success=true')
        else:
            return redirect('/login?error=oauth_failed')
    except Exception as e:
        print(f"GitHub callback error: {e}")
        return redirect('/login?error=oauth_failed')

@auth_bp.route('/resend-verification', methods=['POST'])
def resend_verification():
    try:
        data = request.get_json()
        email = data.get('email')
        
        if not email:
            return jsonify({'success': False, 'message': 'Email required'}), 400
        
        result = UserService.resend_verification(email)
        return jsonify(result)
    except Exception as e:
        print(f"Resend verification API error: {e}")
        return jsonify({'success': False, 'message': 'Request failed'}), 500

@auth_bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    try:
        data = request.get_json()
        email = data.get('email')
        otp = data.get('otp')
        
        if not email or not otp:
            return jsonify({'success': False, 'message': 'Email and OTP required'}), 400
        
        result = UserService.verify_otp(email, otp)
        return jsonify(result)
    except Exception as e:
        print(f"Verify OTP API error: {e}")
        return jsonify({'success': False, 'message': 'Verification failed'}), 500

@auth_bp.route('/current-user', methods=['GET'])
def get_current_user():
    user = session.get('user')
    if user:
        return jsonify({'success': True, 'user': user})
    return jsonify({'success': False, 'user': None})
