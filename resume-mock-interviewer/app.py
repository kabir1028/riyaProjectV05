from flask import Flask, render_template, request, jsonify
import json
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import uuid
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Database configuration
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', '5432'),
        database=os.getenv('DB_NAME', 'interview_db'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', '3322')
    )

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
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

init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/interview')
def interview():
    return render_template('interview.html')

@app.route('/start-interview')
def start_interview():
    return render_template('start_interview.html')

@app.route('/results')
@app.route('/results/<result_id>')
def results(result_id=None):
    return render_template('results.html', result_id=result_id)

@app.route('/api/get-result/<result_id>')
def get_result(result_id):
    conn = get_db_connection()
    cursor = conn.cursor(RealDictCursor)
    cursor.execute('SELECT * FROM results WHERE id = %s', (result_id,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return jsonify({
            'id': result['id'],
            'score': result['score'],
            'feedback': result['feedback'],
            'companies': json.loads(result['companies']),
            'answers': json.loads(result['answers']),
            'questions': json.loads(result['questions'])
        })
    else:
        # Return demo data if no result found
        return jsonify({
            'id': 'demo',
            'score': 75,
            'feedback': 'This is a demo result. Take an interview to see your actual performance.',
            'companies': ['Google', 'Microsoft', 'Amazon', 'Meta', 'Apple', 'Netflix', 'Uber', 'Airbnb'],
            'answers': [
                {'questionId': 0, 'text': 'Demo answer for behavioral question', 'type': 'short-answer'},
                {'questionId': 1, 'selectedOption': 0, 'correct': True, 'type': 'multiple-choice'}
            ],
            'questions': [
                {'question': 'Tell me about yourself', 'type': 'short-answer'},
                {'question': 'What is your greatest strength?', 'type': 'multiple-choice', 'options': ['Leadership', 'Technical Skills', 'Communication', 'Problem Solving'], 'correctAnswer': 0}
            ]
        })

@app.route('/api/questions')
def get_questions():
    role = request.args.get('role', 'Software Engineer')
    difficulty = request.args.get('difficulty', 'Beginner')
    
    with open('data/questions.json', 'r') as f:
        data = json.load(f)
    
    questions = data.get(role, {}).get(difficulty, [])
    return jsonify(questions)

@app.route('/api/submit-answers', methods=['POST'])
def submit_answers():
    answers = request.json.get('answers', [])
    role = request.json.get('role', 'Software Engineer')
    questions = request.json.get('questions', [])
    
    score = calculate_score(answers)
    feedback = generate_feedback(score, role)
    companies = get_companies(score, role)
    
    # Store in database
    result_id = str(uuid.uuid4())
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO results (id, score, feedback, companies, answers, questions)
        VALUES (%s, %s, %s, %s, %s, %s)
    ''', (result_id, score, feedback, json.dumps(companies), json.dumps(answers), json.dumps(questions)))
    conn.commit()
    conn.close()
    
    return jsonify({
        'id': result_id,
        'score': score,
        'feedback': feedback,
        'companies': companies
    })

def calculate_score(answers):
    if not answers:
        return 0
    
    score = 0
    for answer in answers:
        if answer.get('type') == 'multiple-choice':
            if answer.get('correct', False):
                score += 20  # 20 points for correct multiple choice
        elif answer.get('type') == 'short-answer':
            text = answer.get('text', '').strip()
            word_count = len(text.split()) if text else 0
            if word_count >= 20:
                score += 20  # 20 points for comprehensive answer
            elif word_count >= 10:
                score += 15  # 15 points for adequate answer
            elif word_count >= 5:
                score += 10  # 10 points for basic answer
    
    return min(100, score)

def generate_feedback(score, role):
    if score >= 80:
        return f"Excellent performance! You're well-prepared for {role} positions."
    elif score >= 60:
        return f"Good job! With some practice, you'll excel in {role} interviews."
    else:
        return f"Keep practicing! Focus on {role} fundamentals and technical skills."

def get_companies(score, role):
    companies = {
        'Software Engineer': ['Google', 'Microsoft', 'Amazon', 'Meta', 'Apple', 'Netflix', 'Uber', 'Airbnb'],
        'AI Scientist': ['OpenAI', 'DeepMind', 'NVIDIA', 'Tesla', 'IBM', 'Google AI', 'Microsoft Research', 'Amazon AI'],
        'Data Scientist': ['Netflix', 'Uber', 'Airbnb', 'Spotify', 'LinkedIn', 'Meta', 'Google', 'Amazon']
    }
    
    # Always return 8 companies for better grid display
    return companies.get(role, companies['Software Engineer'])[:8]

if __name__ == '__main__':
    init_db()
    app.run(
        port=int(os.getenv('FLASK_PORT', 5000)),
        debug=os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    )