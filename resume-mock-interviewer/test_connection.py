import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def test_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', '3322')
        )
        print("Connection successful!")
        conn.close()
    except psycopg2.OperationalError as e:
        print(f"Connection failed: {e}")
        print("\nTroubleshooting steps:")
        print("1. Check if PostgreSQL service is running")
        print("2. Verify the password in .env file")
        print("3. Try connecting with pgAdmin or another tool first")

if __name__ == "__main__":
    test_connection()