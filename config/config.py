import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    HOST = os.getenv('FLASK_HOST', 'localhost')
    PORT = int(os.getenv('FLASK_PORT', 5000))
    DATABASE_PATH = 'interviewace.db'
