import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Supabase configuration
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

class SupabaseClient:
    def __init__(self):
        self.url = SUPABASE_URL
        self.key = SUPABASE_KEY
        self.headers = {
            'apikey': self.key,
            'Authorization': f'Bearer {self.key}',
            'Content-Type': 'application/json'
        }
    
    def insert(self, table, data):
        """Insert data into table"""
        response = requests.post(
            f"{self.url}/rest/v1/{table}",
            json=data,
            headers=self.headers
        )
        return response
    
    def select(self, table, filters=None):
        """Select data from table"""
        url = f"{self.url}/rest/v1/{table}"
        if filters:
            params = []
            for key, value in filters.items():
                params.append(f"{key}=eq.{value}")
            url += "?" + "&".join(params)
        
        response = requests.get(url, headers=self.headers)
        return response
    
    def auth_signup(self, email, password):
        """Sign up user"""
        response = requests.post(
            f"{self.url}/auth/v1/signup",
            json={"email": email, "password": password},
            headers=self.headers
        )
        return response
    
    def auth_login(self, email, password):
        """Login user"""
        response = requests.post(
            f"{self.url}/auth/v1/token?grant_type=password",
            json={"email": email, "password": password},
            headers=self.headers
        )
        return response
    
    def send_otp_email(self, email, otp):
        """Send OTP via Supabase email with custom template"""
        response = requests.post(
            f"{self.url}/auth/v1/recover",
            json={
                "email": email,
                "options": {
                    "data": {
                        "otp": otp,
                        "action_type": "password_reset_otp"
                    }
                }
            },
            headers=self.headers
        )
        return response
    
    def auth_resend_verification(self, email):
        """Resend verification email"""
        response = requests.post(
            f"{self.url}/auth/v1/resend",
            json={"email": email, "type": "signup"},
            headers=self.headers
        )
        return response
    
    def auth_update_password(self, access_token, new_password):
        """Update user password"""
        headers = self.headers.copy()
        headers['Authorization'] = f'Bearer {access_token}'
        
        response = requests.put(
            f"{self.url}/auth/v1/user",
            json={"password": new_password},
            headers=headers
        )
        return response
    
    def auth_update_password_with_token(self, token, new_password):
        """Update password using reset token"""
        # First verify the token to get session
        verify_response = requests.post(
            f"{self.url}/auth/v1/verify",
            json={
                "token": token,
                "type": "recovery"
            },
            headers=self.headers
        )
        
        if verify_response.status_code == 200:
            # Get access token from verification
            verify_data = verify_response.json()
            access_token = verify_data.get('access_token')
            
            if access_token:
                # Update password with access token
                update_headers = self.headers.copy()
                update_headers['Authorization'] = f'Bearer {access_token}'
                
                response = requests.put(
                    f"{self.url}/auth/v1/user",
                    json={"password": new_password},
                    headers=update_headers
                )
                return response
        
        return verify_response

def get_supabase_client():
    """Get Supabase client instance"""
    return SupabaseClient()