from flask import Blueprint, request, jsonify
import json
from services.user_service import UserService
from services.interview_service import InterviewService

interview_bp = Blueprint('interview', __name__, url_prefix='/api')

@interview_bp.route('/create-guest', methods=['POST'])
def create_guest():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({'success': False, 'message': 'User ID required'}), 400
        
        result = UserService.create_guest_user(user_id)
        return jsonify(result)
        
    except Exception as e:
        print(f"Create guest API error: {e}")
        return jsonify({'success': False, 'message': 'Failed to create guest'}), 500

@interview_bp.route('/questions')
def get_questions():
    role = request.args.get('role', 'Software Engineer')
    difficulty = request.args.get('difficulty', 'Beginner')
    
    try:
        with open('data/questions.json', 'r') as f:
            data = json.load(f)
        questions = data.get(role, {}).get(difficulty, [])
        return jsonify(questions)
    except Exception as e:
        print(f"Get questions error: {e}")
        return jsonify({'error': 'Failed to load questions'}), 500

@interview_bp.route('/submit-answers', methods=['POST'])
def submit_answers():
    try:
        data = request.get_json()
        answers = data.get('answers', [])
        role = data.get('role', 'Software Engineer')
        questions = data.get('questions', [])
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({'success': False, 'message': 'User ID required'}), 400
        
        score = InterviewService.calculate_score(answers)
        feedback = InterviewService.generate_feedback(score, role)
        companies = InterviewService.get_companies(score, role)
        
        result = InterviewService.save_result(user_id, score, feedback, companies, answers, questions)
        
        if result:
            return jsonify(result)
        else:
            return jsonify({'success': False, 'message': 'Failed to save result'}), 500
        
    except Exception as e:
        print(f"Submit answers error: {e}")
        return jsonify({'success': False, 'message': 'Failed to submit answers'}), 500

@interview_bp.route('/get-result/<result_id>')
def get_result(result_id):
    try:
        result = InterviewService.get_result_by_id(result_id)
        
        if result:
            return jsonify(result)
        else:
            return jsonify({'error': 'Result not found'}), 404
        
    except Exception as e:
        print(f"Get result error: {e}")
        return jsonify({'error': 'Failed to get result'}), 500

@interview_bp.route('/profile/history')
def get_history():
    try:
        user_id = request.args.get('user_id')
        
        if not user_id:
            return jsonify({'success': False, 'message': 'User ID required'}), 400
        
        results = InterviewService.get_user_results(user_id, 5)
        
        return jsonify({
            'success': True,
            'history': results,
            'total_interviews': len(results)
        })
        
    except Exception as e:
        print(f"Get history error: {e}")
        return jsonify({'success': False, 'message': 'Failed to get history'}), 500
