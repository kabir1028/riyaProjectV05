from supabase_client import get_supabase_client
import json

def setup_supabase_tables():
    """Create necessary tables in Supabase"""
    supabase = get_supabase_client()
    
    print("Setting up Supabase tables...")
    
    # Note: In Supabase, you typically create tables through the dashboard
    # This script is for reference of the table structure needed
    
    table_sql = """
    -- Create results table
    CREATE TABLE IF NOT EXISTS results (
        id TEXT PRIMARY KEY,
        score INTEGER,
        feedback TEXT,
        companies TEXT,
        answers TEXT,
        questions TEXT,
        user_id UUID REFERENCES auth.users(id),
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    
    -- Enable Row Level Security
    ALTER TABLE results ENABLE ROW LEVEL SECURITY;
    
    -- Create policy for users to see their own results
    CREATE POLICY "Users can view their own results" ON results
        FOR SELECT USING (auth.uid() = user_id);
    
    -- Create policy for users to insert their own results
    CREATE POLICY "Users can insert their own results" ON results
        FOR INSERT WITH CHECK (auth.uid() = user_id);
    """
    
    print("Table structure (to be created in Supabase dashboard):")
    print(table_sql)
    print("\nPlease create this table structure in your Supabase dashboard.")
    print("Go to: https://app.supabase.com -> Your Project -> SQL Editor")
    print("Run the above SQL commands to create the tables.")

if __name__ == "__main__":
    setup_supabase_tables()