import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

load_dotenv()

def create_database():
    # Connect to PostgreSQL server (not to a specific database)
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', '5432'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', '3322')
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    
    # Create database if it doesn't exist
    cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (os.getenv('DB_NAME', 'interview_db'),))
    exists = cursor.fetchone()
    if not exists:
        cursor.execute(f"CREATE DATABASE {os.getenv('DB_NAME', 'interview_db')}")
        print(f"Database '{os.getenv('DB_NAME', 'interview_db')}' created successfully!")
    else:
        print(f"Database '{os.getenv('DB_NAME', 'interview_db')}' already exists.")
    
    conn.close()

def create_tables():
    # Connect to the specific database
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', '5432'),
        database=os.getenv('DB_NAME', 'interview_db'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', '3322')
    )
    cursor = conn.cursor()
    
    # Create results table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id TEXT PRIMARY KEY,
            score INTEGER,
            feedback TEXT,
            companies TEXT,
            answers TEXT,
            questions TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Tables created successfully!")

if __name__ == "__main__":
    try:
        create_database()
        create_tables()
        print("Database setup completed!")
    except Exception as e:
        print(f"Error: {e}")