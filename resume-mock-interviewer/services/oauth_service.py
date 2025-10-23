import requests
import os
from dotenv import load_dotenv

load_dotenv()

class OAuthService:
    @staticmethod
    def get_google_auth_url():
        client_id = os.getenv('GOOGLE_CLIENT_ID')
        redirect_uri = os.getenv('GOOGLE_REDIRECT_URI')
        scope = 'openid email profile'
        
        auth_url = (
            f"https://accounts.google.com/o/oauth2/v2/auth?"
            f"client_id={client_id}&"
            f"redirect_uri={redirect_uri}&"
            f"response_type=code&"
            f"scope={scope}&"
            f"access_type=offline&"
            f"prompt=consent"
        )
        return auth_url
    
    @staticmethod
    def get_google_user_info(code):
        try:
            client_id = os.getenv('GOOGLE_CLIENT_ID')
            client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
            redirect_uri = os.getenv('GOOGLE_REDIRECT_URI')
            
            token_url = 'https://oauth2.googleapis.com/token'
            token_data = {
                'code': code,
                'client_id': client_id,
                'client_secret': client_secret,
                'redirect_uri': redirect_uri,
                'grant_type': 'authorization_code'
            }
            
            token_response = requests.post(token_url, data=token_data)
            token_json = token_response.json()
            access_token = token_json.get('access_token')
            
            if not access_token:
                return None
            
            user_info_url = 'https://www.googleapis.com/oauth2/v2/userinfo'
            headers = {'Authorization': f'Bearer {access_token}'}
            user_response = requests.get(user_info_url, headers=headers)
            
            return user_response.json()
        except Exception as e:
            print(f"Google OAuth error: {e}")
            return None
    
    @staticmethod
    def get_github_auth_url():
        client_id = os.getenv('GITHUB_CLIENT_ID')
        redirect_uri = os.getenv('GITHUB_REDIRECT_URI')
        
        auth_url = (
            f"https://github.com/login/oauth/authorize?"
            f"client_id={client_id}&"
            f"redirect_uri={redirect_uri}&"
            f"scope=user:email"
        )
        return auth_url
    
    @staticmethod
    def get_github_user_info(code):
        try:
            client_id = os.getenv('GITHUB_CLIENT_ID')
            client_secret = os.getenv('GITHUB_CLIENT_SECRET')
            
            token_url = 'https://github.com/login/oauth/access_token'
            token_data = {
                'client_id': client_id,
                'client_secret': client_secret,
                'code': code
            }
            headers = {'Accept': 'application/json'}
            
            token_response = requests.post(token_url, data=token_data, headers=headers)
            token_json = token_response.json()
            access_token = token_json.get('access_token')
            
            if not access_token:
                return None
            
            user_url = 'https://api.github.com/user'
            headers = {'Authorization': f'token {access_token}'}
            user_response = requests.get(user_url, headers=headers)
            user_data = user_response.json()
            
            email_url = 'https://api.github.com/user/emails'
            email_response = requests.get(email_url, headers=headers)
            emails = email_response.json()
            
            primary_email = next((e['email'] for e in emails if e['primary']), user_data.get('email'))
            user_data['email'] = primary_email
            
            return user_data
        except Exception as e:
            print(f"GitHub OAuth error: {e}")
            return None
