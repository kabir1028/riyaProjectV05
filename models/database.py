import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseManager:
    @staticmethod
    def get_connection():
        return psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432'),
            database=os.getenv('DB_NAME', 'interviewace'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', '3322')
        )
    
    @staticmethod
    def init_db():
        conn = DatabaseManager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id VARCHAR(255) PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255),
                name VARCHAR(255),
                avatar_url TEXT,
                auth_provider VARCHAR(50) DEFAULT 'local',
                oauth_id VARCHAR(255),
                is_guest BOOLEAN DEFAULT FALSE,
                is_verified BOOLEAN DEFAULT FALSE,
                verification_token VARCHAR(255),
                reset_otp VARCHAR(10),
                otp_expiry TIMESTAMP,
                phone VARCHAR(50),
                user_role VARCHAR(255),  
                experience VARCHAR(50),
                location VARCHAR(255),
                bio TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS results (
                id VARCHAR(255) PRIMARY KEY,
                user_id VARCHAR(255) NOT NULL,
                score INTEGER NOT NULL,
                feedback TEXT,
                companies TEXT,
                answers TEXT,
                questions TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        ''')
        
        conn.commit()
        cursor.close()
        conn.close()
        print("PostgreSQL database initialized")
        print("Tables: users (with OAuth support), results")
