import uuid
import json
from models.database import DatabaseManager

class InterviewService:
    @staticmethod
    def save_result(user_id, score, feedback, companies, answers, questions):
        try:
            conn = DatabaseManager.get_connection()
            cursor = conn.cursor()
            
            result_id = str(uuid.uuid4())
            
            cursor.execute('''
                INSERT INTO results (id, user_id, score, feedback, companies, answers, questions)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (
                result_id, user_id, score, feedback,
                json.dumps(companies), json.dumps(answers), json.dumps(questions)
            ))
            
            conn.commit()
            
            cursor.execute('''
                DELETE FROM results 
                WHERE user_id = %s AND id NOT IN (
                    SELECT id FROM results 
                    WHERE user_id = %s 
                    ORDER BY created_at DESC 
                    LIMIT 5
                )
            ''', (user_id, user_id))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return {
                'id': result_id,
                'score': score,
                'feedback': feedback,
                'companies': companies,
                'answers': answers,
                'questions': questions
            }
            
        except Exception as e:
            print(f"Save result error: {e}")
            return None

    @staticmethod
    def get_user_results(user_id, limit=5):
        try:
            conn = DatabaseManager.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, score, feedback, companies, created_at
                FROM results 
                WHERE user_id = %s
                ORDER BY created_at DESC
                LIMIT %s
            ''', (user_id, limit))
            
            results = []
            for row in cursor.fetchall():
                results.append({
                    'id': row[0],
                    'score': row[1],
                    'feedback': row[2],
                    'companies': json.loads(row[3])[:3],
                    'created_at': str(row[4])
                })
            
            cursor.close()
            conn.close()
            return results
            
        except Exception as e:
            print(f"Get results error: {e}")
            return []

    @staticmethod
    def get_result_by_id(result_id):
        try:
            conn = DatabaseManager.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, score, feedback, companies, answers, questions, created_at
                FROM results 
                WHERE id = %s
            ''', (result_id,))
            
            row = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if row:
                return {
                    'id': row[0],
                    'score': row[1],
                    'feedback': row[2],
                    'companies': json.loads(row[3]),
                    'answers': json.loads(row[4]),
                    'questions': json.loads(row[5]),
                    'created_at': str(row[6])
                }
            return None
            
        except Exception as e:
            print(f"Get result by ID error: {e}")
            return None

    @staticmethod
    def calculate_score(answers):
        if not answers:
            return 0
        
        score = 0
        for answer in answers:
            if answer.get('type') == 'multiple-choice':
                if answer.get('correct', False):
                    score += 20
            elif answer.get('type') == 'short-answer':
                text = answer.get('text', '').strip()
                word_count = len(text.split()) if text else 0
                if word_count >= 20:
                    score += 20
                elif word_count >= 10:
                    score += 15
                elif word_count >= 5:
                    score += 10
        
        return min(100, score)

    @staticmethod
    def generate_feedback(score, role):
        if score >= 80:
            return f"Excellent performance! You're well-prepared for {role} positions."
        elif score >= 60:
            return f"Good job! With some practice, you'll excel in {role} interviews."
        else:
            return f"Keep practicing! Focus on {role} fundamentals and technical skills."

    @staticmethod
    def get_companies(score, role):
        companies = {
            'Software Engineer': ['Google', 'Microsoft', 'Amazon', 'Meta', 'Apple', 'Netflix', 'Uber', 'Airbnb'],
            'AI Scientist': ['OpenAI', 'DeepMind', 'NVIDIA', 'Tesla', 'IBM', 'Google AI', 'Microsoft Research', 'Amazon AI'],
            'Data Scientist': ['Netflix', 'Uber', 'Airbnb', 'Spotify', 'LinkedIn', 'Meta', 'Google', 'Amazon']
        }
        return companies.get(role, companies['Software Engineer'])[:8]
