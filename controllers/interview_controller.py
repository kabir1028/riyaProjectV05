from flask import Blueprint, request, jsonify
import json
from services.user_service import UserService
from services.interview_service import InterviewService
from services.ai_service import AIService

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
    use_ai = request.args.get('use_ai', 'true').lower() == 'true'
    
    try:
        if use_ai:
            # Generate questions using AI
            questions = AIService.generate_interview_questions(role, difficulty)
            return jsonify({'success': True, 'questions': questions, 'source': 'ai'})
        else:
            # Use static questions from JSON
            with open('data/questions.json', 'r') as f:
                data = json.load(f)
            questions = data.get(role, {}).get(difficulty, [])
            return jsonify({'success': True, 'questions': questions[:10], 'source': 'static'})
    except Exception as e:
        print(f"Get questions error: {e}")
        return jsonify({'success': False, 'error': 'Failed to load questions'}), 500

@interview_bp.route('/submit-answers', methods=['POST'])
def submit_answers():
    try:
        data = request.get_json()
        answers = data.get('answers', [])
        role = data.get('role', 'Software Engineer')
        difficulty = data.get('difficulty', 'Beginner')
        questions = data.get('questions', [])
        user_id = data.get('user_id')
        use_ai = data.get('use_ai', True)
        
        if not user_id:
            return jsonify({'success': False, 'message': 'User ID required'}), 400
        
        # Calculate score with AI evaluation
        total_score = 0
        evaluated_answers = []
        
        for i, answer in enumerate(answers):
            question = questions[i]
            
            if answer.get('type') == 'multiple-choice':
                # MCQ scoring
                if answer.get('correct', False):
                    score = 20
                    feedback = "Correct answer"
                else:
                    score = 0
                    feedback = "Incorrect answer"
            else:
                # AI evaluation for written answers
                if use_ai and answer.get('text', '').strip():
                    evaluation = AIService.evaluate_answer(
                        question.get('question', ''),
                        answer.get('text', ''),
                        'short-answer'
                    )
                    score = evaluation.get('score', 10)
                    feedback = evaluation.get('feedback', 'Answer evaluated')
                else:
                    # Fallback scoring with validation
                    evaluation = AIService._fallback_evaluation(answer.get('text', ''))
                    score = evaluation.get('score', 0)
                    feedback = evaluation.get('feedback', 'Answer evaluated')
            
            total_score += score
            evaluated_answers.append({
                **answer,
                'score': score,
                'feedback': feedback
            })
        
        # Normalize score to 100
        final_score = min(100, int((total_score / 200) * 100))
        
        # Generate comprehensive report with AI
        if use_ai:
            report = AIService.generate_comprehensive_report(answers, questions, role, difficulty)
        else:
            report = AIService._fallback_report()
        
        # Get company recommendations
        companies = InterviewService.get_companies(final_score, role)
        
        # Prepare detailed feedback
        detailed_feedback = {
            'summary': report.get('summary', ''),
            'strengths': report.get('strengths', []),
            'improvements': report.get('improvements', []),
            'recommendations': report.get('recommendations', [])
        }
        
        # Save result
        result = InterviewService.save_result(
            user_id, 
            final_score, 
            json.dumps(detailed_feedback), 
            companies, 
            evaluated_answers, 
            questions
        )
        
        if result:
            result['detailed_feedback'] = detailed_feedback
            result['evaluated_answers'] = evaluated_answers
            return jsonify({'success': True, **result})
        else:
            return jsonify({'success': False, 'message': 'Failed to save result'}), 500
        
    except Exception as e:
        print(f"Submit answers error: {e}")
        import traceback
        traceback.print_exc()
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

@interview_bp.route('/submit-voice-interview', methods=['POST'])
def submit_voice_interview():
    try:
        data = request.get_json()
        answers = data.get('answers', [])
        role = data.get('role', 'Software Engineer')
        difficulty = data.get('difficulty', 'Beginner')
        questions = data.get('questions', [])
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({'success': False, 'message': 'User ID required'}), 400
        
        # Evaluate voice answers using AI
        total_score = 0
        evaluated_answers = []
        
        for i, answer in enumerate(answers):
            question = questions[i]
            
            if answer.get('text', '').strip():
                # AI evaluation for voice answers
                evaluation = AIService.evaluate_answer(
                    question.get('question', ''),
                    answer.get('text', ''),
                    'voice'
                )
                score = evaluation.get('score', 10)
                feedback = evaluation.get('feedback', 'Answer evaluated')
            else:
                score = 0
                feedback = 'No answer provided'
            
            total_score += score
            evaluated_answers.append({
                **answer,
                'score': score,
                'feedback': feedback
            })
        
        # Normalize score to 100
        final_score = min(100, int((total_score / 200) * 100))
        
        # Generate comprehensive report
        report = AIService.generate_comprehensive_report(answers, questions, role, difficulty)
        
        # Get company recommendations
        companies = InterviewService.get_companies(final_score, role)
        
        # Prepare detailed feedback
        detailed_feedback = {
            'summary': report.get('summary', ''),
            'strengths': report.get('strengths', []),
            'improvements': report.get('improvements', []),
            'recommendations': report.get('recommendations', [])
        }
        
        # Save result
        result = InterviewService.save_result(
            user_id, 
            final_score, 
            json.dumps(detailed_feedback), 
            companies, 
            evaluated_answers, 
            questions
        )
        
        if result:
            result['detailed_feedback'] = detailed_feedback
            result['evaluated_answers'] = evaluated_answers
            return jsonify({'success': True, **result})
        else:
            return jsonify({'success': False, 'message': 'Failed to save result'}), 500
        
    except Exception as e:
        print(f"Submit voice interview error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': 'Failed to submit interview'}), 500

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
