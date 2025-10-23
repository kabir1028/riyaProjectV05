import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

class AIService:
    """
    AI Service using Groq API (Free, Fast, and Powerful)
    Alternative: Can use Hugging Face, OpenAI, or other providers
    """
    
    GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
    GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'
    MODEL = 'llama-3.1-70b-versatile'  # Fast and free model
    
    @staticmethod
    def generate_interview_questions(role, experience_level, resume_text=None):
        """
        Generate 10 interview questions (3 MCQ + 7 Written) based on role and experience
        """
        
        prompt = f"""You are an expert technical interviewer. Generate exactly 10 interview questions for a {role} position at {experience_level} level.

Requirements:
- First 3 questions: Multiple choice with 4 options each
- Next 7 questions: Open-ended written questions
- Questions should be relevant to {role} and {experience_level} level
- Include practical, technical, and behavioral questions

Return ONLY a valid JSON array with this exact structure:
[
  {{
    "question": "Question text here?",
    "type": "multiple-choice",
    "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
    "correctAnswer": 0
  }},
  {{
    "question": "Question text here?",
    "type": "short-answer"
  }}
]

Generate the questions now:"""

        try:
            response = requests.post(
                AIService.GROQ_API_URL,
                headers={
                    'Authorization': f'Bearer {AIService.GROQ_API_KEY}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': AIService.MODEL,
                    'messages': [
                        {'role': 'system', 'content': 'You are an expert technical interviewer. Always return valid JSON only.'},
                        {'role': 'user', 'content': prompt}
                    ],
                    'temperature': 0.7,
                    'max_tokens': 2000
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                # Extract JSON from response
                content = content.strip()
                if '```json' in content:
                    content = content.split('```json')[1].split('```')[0].strip()
                elif '```' in content:
                    content = content.split('```')[1].split('```')[0].strip()
                
                questions = json.loads(content)
                return questions[:10]  # Ensure only 10 questions
            else:
                print(f"Groq API error: {response.status_code} - {response.text}")
                return AIService._get_fallback_questions(role, experience_level)
                
        except Exception as e:
            print(f"AI question generation error: {e}")
            return AIService._get_fallback_questions(role, experience_level)
    
    @staticmethod
    def evaluate_answer(question, answer, question_type):
        """
        Evaluate a single answer using AI
        Returns score (0-20) and feedback
        """
        
        if question_type == 'multiple-choice':
            # MCQ already evaluated on frontend
            return None
        
        # Pre-validation: Check for gibberish
        if not AIService._is_valid_answer(answer):
            return {
                "score": 0,
                "feedback": "Invalid answer: Please provide a meaningful, well-structured response."
            }
        
        prompt = f"""Evaluate this interview answer STRICTLY on a scale of 0-20 points.

Question: {question}
Answer: {answer}

Evaluation criteria:
- Relevance and accuracy (0-8 points)
- Depth and detail (0-6 points)
- Clarity and structure (0-6 points)

IMPORTANT: Give 0 points if answer is gibberish or doesn't address the question.

Return ONLY a valid JSON object:
{{
  "score": 15,
  "feedback": "Brief feedback here"
}}"""

        try:
            response = requests.post(
                AIService.GROQ_API_URL,
                headers={
                    'Authorization': f'Bearer {AIService.GROQ_API_KEY}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': AIService.MODEL,
                    'messages': [
                        {'role': 'system', 'content': 'You are an expert interviewer. Return valid JSON only.'},
                        {'role': 'user', 'content': prompt}
                    ],
                    'temperature': 0.5,
                    'max_tokens': 200
                },
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                # Extract JSON
                content = content.strip()
                if '```json' in content:
                    content = content.split('```json')[1].split('```')[0].strip()
                elif '```' in content:
                    content = content.split('```')[1].split('```')[0].strip()
                
                evaluation = json.loads(content)
                return evaluation
            else:
                return AIService._fallback_evaluation(answer)
                
        except Exception as e:
            print(f"AI evaluation error: {e}")
            return AIService._fallback_evaluation(answer)
    
    @staticmethod
    def generate_comprehensive_report(answers, questions, role, experience_level):
        """
        Generate comprehensive interview report with AI analysis
        """
        
        # Prepare answers summary
        answers_summary = []
        for i, (q, a) in enumerate(zip(questions, answers)):
            answers_summary.append(f"Q{i+1}: {q['question']}\nA: {a.get('text', a.get('selected', 'No answer'))}")
        
        prompt = f"""Analyze this {role} interview at {experience_level} level and provide a comprehensive report.

Interview Answers:
{chr(10).join(answers_summary[:5])}  

Generate a detailed report with:
1. Overall performance summary (2-3 sentences)
2. Key strengths (3 points)
3. Areas for improvement (3 points)
4. Specific recommendations (3 points)

Return ONLY valid JSON:
{{
  "summary": "Overall performance summary here",
  "strengths": ["Strength 1", "Strength 2", "Strength 3"],
  "improvements": ["Area 1", "Area 2", "Area 3"],
  "recommendations": ["Rec 1", "Rec 2", "Rec 3"]
}}"""

        try:
            response = requests.post(
                AIService.GROQ_API_URL,
                headers={
                    'Authorization': f'Bearer {AIService.GROQ_API_KEY}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': AIService.MODEL,
                    'messages': [
                        {'role': 'system', 'content': 'You are an expert career advisor. Return valid JSON only.'},
                        {'role': 'user', 'content': prompt}
                    ],
                    'temperature': 0.7,
                    'max_tokens': 800
                },
                timeout=20
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                # Extract JSON
                content = content.strip()
                if '```json' in content:
                    content = content.split('```json')[1].split('```')[0].strip()
                elif '```' in content:
                    content = content.split('```')[1].split('```')[0].strip()
                
                report = json.loads(content)
                return report
            else:
                return AIService._fallback_report()
                
        except Exception as e:
            print(f"AI report generation error: {e}")
            return AIService._fallback_report()
    
    @staticmethod
    def _get_fallback_questions(role, experience_level):
        """Fallback questions if AI fails"""
        base_questions = [
            {
                "question": f"What is the most important skill for a {role}?",
                "type": "multiple-choice",
                "options": ["Technical expertise", "Communication", "Problem-solving", "All of the above"],
                "correctAnswer": 3
            },
            {
                "question": f"Which tool is commonly used in {role} roles?",
                "type": "multiple-choice",
                "options": ["Git", "Docker", "VS Code", "All of the above"],
                "correctAnswer": 3
            },
            {
                "question": f"What is the best practice for code quality in {role}?",
                "type": "multiple-choice",
                "options": ["Code reviews", "Testing", "Documentation", "All of the above"],
                "correctAnswer": 3
            },
            {"question": f"Describe your experience with {role} projects.", "type": "short-answer"},
            {"question": "What is your approach to problem-solving?", "type": "short-answer"},
            {"question": "How do you handle tight deadlines?", "type": "short-answer"},
            {"question": "Describe a challenging project you worked on.", "type": "short-answer"},
            {"question": "What are your career goals?", "type": "short-answer"},
            {"question": "How do you stay updated with technology?", "type": "short-answer"},
            {"question": "Why should we hire you?", "type": "short-answer"}
        ]
        return base_questions
    
    @staticmethod
    def _is_valid_answer(answer):
        """Check if answer is valid (not gibberish)"""
        if not answer or len(answer.strip()) < 20:
            return False
        
        words = answer.strip().split()
        if len(words) < 10:
            return False
        
        # Check for gibberish
        single_chars = sum(1 for word in words if len(word) <= 2)
        if single_chars > len(words) * 0.5:
            return False
        
        # Check for repeated patterns
        unique_words = set(words)
        if len(unique_words) < len(words) * 0.3:
            return False
        
        # Check average word length
        avg_word_length = sum(len(word) for word in words) / len(words)
        if avg_word_length < 3:
            return False
        
        return True
    
    @staticmethod
    def _fallback_evaluation(answer):
        """Fallback evaluation if AI fails"""
        if not AIService._is_valid_answer(answer):
            return {"score": 0, "feedback": "Invalid answer: Please provide a meaningful response."}
        
        words = answer.split()
        word_count = len(words)
        has_punctuation = any(c in answer for c in '.!?,;:')
        avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
        
        if word_count >= 50 and has_punctuation and avg_word_length > 4:
            return {"score": 18, "feedback": "Comprehensive answer with good detail"}
        elif word_count >= 30 and has_punctuation:
            return {"score": 14, "feedback": "Good answer with adequate explanation"}
        elif word_count >= 20:
            return {"score": 10, "feedback": "Basic answer, needs more detail"}
        else:
            return {"score": 5, "feedback": "Answer is too brief"}
    
    @staticmethod
    def _fallback_report():
        """Fallback report if AI fails"""
        return {
            "summary": "You demonstrated good understanding of the concepts. Continue practicing to improve your interview skills.",
            "strengths": [
                "Clear communication",
                "Technical knowledge",
                "Problem-solving approach"
            ],
            "improvements": [
                "Provide more detailed examples",
                "Structure answers better",
                "Include specific metrics"
            ],
            "recommendations": [
                "Practice more technical questions",
                "Work on real-world projects",
                "Study system design concepts"
            ]
        }
