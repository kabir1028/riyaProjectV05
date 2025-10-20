#!/usr/bin/env python3
"""
Database inspection tool to check Supabase results table
"""

import os
import requests
from dotenv import load_dotenv
from datetime import datetime
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY')

def check_table_structure():
    """Check if results table exists and its structure"""
    print("🔍 Checking Supabase table structure...")
    
    headers = {
        'apikey': SUPABASE_SERVICE_KEY,
        'Authorization': f'Bearer {SUPABASE_SERVICE_KEY}',
        'Content-Type': 'application/json'
    }
    
    session = create_session_with_retries()
    
    try:
        response = session.get(
            f"{SUPABASE_URL}/rest/v1/results?limit=1",
            headers=headers,
            timeout=30
        )
        
        print(f"Table check response: {response.status_code}")
        if response.status_code == 200:
            print("✅ Results table exists and is accessible")
            return True
        else:
            print(f"❌ Table access failed: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Connection error: {str(e)}")
        print("💡 Check your internet connection and try again.")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False
    finally:
        session.close()

def get_all_results():
    """Get all results from the database"""
    print("\n📊 Fetching all results from database...")
    
    headers = {
        'apikey': SUPABASE_SERVICE_KEY,
        'Authorization': f'Bearer {SUPABASE_SERVICE_KEY}',
        'Content-Type': 'application/json'
    }
    
    session = create_session_with_retries()
    
    try:
        response = session.get(
            f"{SUPABASE_URL}/rest/v1/results",
            headers=headers,
            timeout=30
        )
        
        print(f"Results query response: {response.status_code}")
        
        if response.status_code == 200:
            results = response.json()
            print(f"📈 Found {len(results)} total results in database")
            
            if results:
                print("\n📋 Results summary:")
                for i, result in enumerate(results, 1):
                    created_at = result.get('created_at', 'Unknown')
                    user_id = result.get('user_id', 'No user_id')
                    score = result.get('score', 'No score')
                    result_id = result.get('id', 'No ID')
                    
                    print(f"  {i}. ID: {result_id[:8]}... | Score: {score} | User: {user_id} | Created: {created_at}")
            else:
                print("📭 No results found in database")
            
            return results
        else:
            print(f"❌ Failed to fetch results: {response.text}")
            return []
            
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Connection error: {str(e)}")
        return []
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return []
    finally:
        session.close()

def test_insert():
    """Test inserting a sample record"""
    print("\n🧪 Testing database insert...")
    
    headers = {
        'apikey': SUPABASE_SERVICE_KEY,
        'Authorization': f'Bearer {SUPABASE_SERVICE_KEY}',
        'Content-Type': 'application/json'
    }
    
    test_data = {
        'id': f'test_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
        'score': 85,
        'feedback': 'Test feedback from database checker',
        'companies': '["Test Company 1", "Test Company 2"]',
        'answers': '[{"test": "answer"}]',
        'questions': '[{"test": "question"}]',
        'user_id': 'test_user_123',
        'created_at': datetime.now().isoformat()
    }
    
    session = create_session_with_retries()
    
    try:
        response = session.post(
            f"{SUPABASE_URL}/rest/v1/results",
            json=test_data,
            headers=headers,
            timeout=30
        )
        
        print(f"Test insert response: {response.status_code}")
        
        if response.status_code == 201:
            print("✅ Test insert successful!")
            print(f"Inserted test record with ID: {test_data['id']}")
            return True
        else:
            print(f"❌ Test insert failed: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Connection error during insert: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error during insert: {str(e)}")
        return False
    finally:
        session.close()

def create_session_with_retries():
    """Create a requests session with retry strategy"""
    session = requests.Session()
    
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS", "POST"]
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session

def check_user_results(user_id):
    """Check results for a specific user with retry logic"""
    if not user_id:
        print("\n⚠️  No user_id provided for user-specific check")
        return
    
    print(f"\n👤 Checking results for user: {user_id}")
    
    headers = {
        'apikey': SUPABASE_SERVICE_KEY,
        'Authorization': f'Bearer {SUPABASE_SERVICE_KEY}',
        'Content-Type': 'application/json'
    }
    
    session = create_session_with_retries()
    
    try:
        response = session.get(
            f"{SUPABASE_URL}/rest/v1/results?user_id=eq.{user_id}",
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            user_results = response.json()
            print(f"📊 Found {len(user_results)} results for this user")
            
            for result in user_results:
                print(f"  - Score: {result.get('score')} | Created: {result.get('created_at')}")
        else:
            print(f"❌ Failed to fetch user results: {response.text}")
            
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Connection error: {str(e)}")
        print("💡 This might be a temporary network issue. Try again in a few moments.")
    except requests.exceptions.Timeout:
        print("❌ Request timed out. The server might be slow to respond.")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
    finally:
        session.close()

def main():
    print("🚀 InterviewAce Database Inspector")
    print("=" * 50)
    
    # Check configuration
    if not all([SUPABASE_URL, SUPABASE_KEY, SUPABASE_SERVICE_KEY]):
        print("❌ Missing Supabase configuration in .env file")
        return
    
    print(f"🔗 Supabase URL: {SUPABASE_URL}")
    print(f"🔑 Service Key: {SUPABASE_SERVICE_KEY[:20]}...")
    
    # Run checks
    table_exists = check_table_structure()
    
    if table_exists:
        results = get_all_results()
        test_insert()
        
        # Check for specific user if needed
        user_id = input("\n🔍 Enter user_id to check specific user results (or press Enter to skip): ").strip()
        if user_id:
            check_user_results(user_id)
    
    print("\n✨ Database inspection complete!")

if __name__ == "__main__":
    main()