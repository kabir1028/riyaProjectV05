#!/usr/bin/env python3
"""
Create the results table in Supabase
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY')

def create_results_table():
    """Create the results table in Supabase"""
    print("🔨 Creating results table in Supabase...")
    
    # SQL to create the table
    sql_query = """
    CREATE TABLE IF NOT EXISTS public.results (
        id TEXT PRIMARY KEY,
        score INTEGER NOT NULL,
        feedback TEXT NOT NULL,
        companies TEXT NOT NULL,
        answers TEXT NOT NULL,
        questions TEXT NOT NULL,
        user_id TEXT,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    
    -- Enable Row Level Security
    ALTER TABLE public.results ENABLE ROW LEVEL SECURITY;
    
    -- Create policy to allow all operations for authenticated users
    CREATE POLICY "Allow all operations for authenticated users" ON public.results
        FOR ALL USING (true);
    
    -- Create policy to allow read access for anonymous users (for demo data)
    CREATE POLICY "Allow read for anonymous users" ON public.results
        FOR SELECT USING (true);
    """
    
    headers = {
        'apikey': SUPABASE_SERVICE_KEY,
        'Authorization': f'Bearer {SUPABASE_SERVICE_KEY}',
        'Content-Type': 'application/json'
    }
    
    # Execute SQL via Supabase REST API
    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/rpc/exec_sql",
        json={'sql': sql_query},
        headers=headers
    )
    
    print(f"Table creation response: {response.status_code}")
    
    if response.status_code in [200, 201]:
        print("✅ Results table created successfully!")
        return True
    else:
        print(f"❌ Failed to create table: {response.text}")
        
        # Try alternative method using direct SQL endpoint
        print("🔄 Trying alternative method...")
        
        response = requests.post(
            f"{SUPABASE_URL}/sql",
            data=sql_query,
            headers={
                'apikey': SUPABASE_SERVICE_KEY,
                'Authorization': f'Bearer {SUPABASE_SERVICE_KEY}',
                'Content-Type': 'application/sql'
            }
        )
        
        print(f"Alternative method response: {response.status_code}")
        
        if response.status_code in [200, 201]:
            print("✅ Results table created successfully!")
            return True
        else:
            print(f"❌ Alternative method also failed: {response.text}")
            return False

def test_table_access():
    """Test if we can access the newly created table"""
    print("\n🧪 Testing table access...")
    
    headers = {
        'apikey': SUPABASE_SERVICE_KEY,
        'Authorization': f'Bearer {SUPABASE_SERVICE_KEY}',
        'Content-Type': 'application/json'
    }
    
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/results?limit=1",
        headers=headers
    )
    
    if response.status_code == 200:
        print("✅ Table is accessible!")
        return True
    else:
        print(f"❌ Table access failed: {response.text}")
        return False

def main():
    print("🚀 Supabase Table Creator")
    print("=" * 40)
    
    if not all([SUPABASE_URL, SUPABASE_SERVICE_KEY]):
        print("❌ Missing Supabase configuration")
        return
    
    print(f"🔗 Supabase URL: {SUPABASE_URL}")
    print(f"🔑 Service Key: {SUPABASE_SERVICE_KEY[:20]}...")
    
    # Create table
    success = create_results_table()
    
    if success:
        # Test access
        test_table_access()
        print("\n✨ Setup complete! You can now save interview results.")
    else:
        print("\n❌ Setup failed. You may need to create the table manually in Supabase dashboard.")
        print("\n📋 Manual SQL to run in Supabase SQL Editor:")
        print("""
CREATE TABLE IF NOT EXISTS public.results (
    id TEXT PRIMARY KEY,
    score INTEGER NOT NULL,
    feedback TEXT NOT NULL,
    companies TEXT NOT NULL,
    answers TEXT NOT NULL,
    questions TEXT NOT NULL,
    user_id TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

ALTER TABLE public.results ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow all operations for authenticated users" ON public.results
    FOR ALL USING (true);

CREATE POLICY "Allow read for anonymous users" ON public.results
    FOR SELECT USING (true);
        """)

if __name__ == "__main__":
    main()