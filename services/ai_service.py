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
        
        prompt = f"""You are a senior technical interviewer at a top tech company. Generate exactly 10 UNIQUE and DIVERSE interview questions for a {role} position at {experience_level} level.

CRITICAL REQUIREMENTS:
- First 3 questions: Multiple choice with 4 options (technical/conceptual)
- Next 7 questions: Open-ended written questions (mix of technical, practical, and scenario-based)
- Each question MUST be DIFFERENT and cover DIFFERENT topics
- Questions MUST be specific to {role} and appropriate for {experience_level} level
- NO generic questions like "tell me about yourself" or "why should we hire you"
- Include: algorithms, system design, coding problems, debugging scenarios, architecture decisions, real-world challenges

For {experience_level} level:
- Beginner: Focus on fundamentals, basic concepts, simple problem-solving
- Intermediate: Focus on practical experience, design patterns, optimization, trade-offs
- Advanced: Focus on system architecture, scalability, complex algorithms, leadership, advanced concepts

For {role}:
- Software Engineer: Data structures, algorithms, system design, coding, debugging, APIs, databases
- AI Scientist: Machine learning algorithms, neural networks, model optimization, research papers, AI ethics
- Data Scientist: Statistics, data analysis, ML models, data pipelines, visualization, business metrics

Return ONLY a valid JSON array:
[
  {{
    "question": "Specific technical question?",
    "type": "multiple-choice",
    "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
    "correctAnswer": 0
  }},
  {{
    "question": "Detailed scenario-based question?",
    "type": "short-answer"
  }}
]

Generate 10 DIVERSE questions now:"""

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
        """Fallback questions if AI fails - role and level specific"""
        
        questions_by_role = {
            'Software Engineer': {
                'Beginner': [
                    {"question": "What is the time complexity of binary search?", "type": "multiple-choice", "options": ["O(n)", "O(log n)", "O(n²)", "O(1)"], "correctAnswer": 1},
                    {"question": "Which data structure uses LIFO principle?", "type": "multiple-choice", "options": ["Queue", "Stack", "Array", "Tree"], "correctAnswer": 1},
                    {"question": "What does REST stand for?", "type": "multiple-choice", "options": ["Representational State Transfer", "Remote State Transfer", "Real State Transfer", "None"], "correctAnswer": 0},
                    {"question": "Explain the difference between GET and POST HTTP methods with examples.", "type": "short-answer"},
                    {"question": "Write a function to reverse a string and explain your approach.", "type": "short-answer"},
                    {"question": "What is the difference between SQL and NoSQL databases? When would you use each?", "type": "short-answer"},
                    {"question": "Explain how you would debug a program that crashes intermittently.", "type": "short-answer"},
                    {"question": "Describe the MVC architecture pattern and its benefits.", "type": "short-answer"},
                    {"question": "How would you optimize a slow database query?", "type": "short-answer"},
                    {"question": "Explain the concept of API rate limiting and why it's important.", "type": "short-answer"}
                ],
                'Intermediate': [
                    {"question": "Which design pattern ensures only one instance exists?", "type": "multiple-choice", "options": ["Factory", "Observer", "Singleton", "Strategy"], "correctAnswer": 2},
                    {"question": "What is the space complexity of merge sort?", "type": "multiple-choice", "options": ["O(1)", "O(log n)", "O(n)", "O(n²)"], "correctAnswer": 2},
                    {"question": "Which is NOT a SOLID principle?", "type": "multiple-choice", "options": ["Single Responsibility", "Open/Closed", "Code Reusability", "Dependency Inversion"], "correctAnswer": 2},
                    {"question": "Design a URL shortener service like bit.ly. Explain your database schema, API endpoints, and how you'd handle collisions.", "type": "short-answer"},
                    {"question": "You have a microservices architecture with 10 services. How would you implement distributed tracing and logging?", "type": "short-answer"},
                    {"question": "Explain the difference between optimistic and pessimistic locking with real-world use cases.", "type": "short-answer"},
                    {"question": "Your API response time increased from 100ms to 2s. Walk through your debugging process.", "type": "short-answer"},
                    {"question": "How would you implement a real-time notification system for 1 million users?", "type": "short-answer"},
                    {"question": "Explain caching strategies (Redis, CDN, browser cache) and when to use each.", "type": "short-answer"},
                    {"question": "Design a rate limiter that can handle 1000 requests per second per user.", "type": "short-answer"}
                ],
                'Advanced': [
                    {"question": "What is the time complexity of Tarjan's algorithm?", "type": "multiple-choice", "options": ["O(V + E)", "O(V²)", "O(V log V)", "O(E log V)"], "correctAnswer": 0},
                    {"question": "Which consensus algorithm is used in blockchain?", "type": "multiple-choice", "options": ["Raft", "Paxos", "Proof of Work", "All of above"], "correctAnswer": 3},
                    {"question": "What does CAP theorem stand for?", "type": "multiple-choice", "options": ["Consistency, Availability, Partition", "Cache, API, Performance", "Code, Architecture, Pattern", "None"], "correctAnswer": 0},
                    {"question": "Design Instagram's architecture to handle 500M daily active users. Include database sharding, CDN, caching, and load balancing strategies.", "type": "short-answer"},
                    {"question": "Explain the CAP theorem with real-world examples. How would you design a system that prioritizes consistency vs availability?", "type": "short-answer"},
                    {"question": "You're leading a team migrating a monolith to microservices. What's your strategy, timeline, and risk mitigation plan?", "type": "short-answer"},
                    {"question": "Design a distributed lock service like Chubby/ZooKeeper. Explain consensus, failure handling, and performance.", "type": "short-answer"},
                    {"question": "How would you implement zero-downtime deployment for a critical payment service?", "type": "short-answer"},
                    {"question": "Explain event sourcing and CQRS patterns. When would you use them and what are the trade-offs?", "type": "short-answer"},
                    {"question": "Design a global CDN system. Explain edge locations, cache invalidation, and routing strategies.", "type": "short-answer"}
                ]
            },
            'AI Scientist': {
                'Beginner': [
                    {"question": "What does CNN stand for?", "type": "multiple-choice", "options": ["Convolutional Neural Network", "Cascading Neural Network", "Circular Neural Network", "None"], "correctAnswer": 0},
                    {"question": "Which activation function is commonly used?", "type": "multiple-choice", "options": ["Sigmoid", "ReLU", "Tanh", "All of above"], "correctAnswer": 1},
                    {"question": "What is overfitting?", "type": "multiple-choice", "options": ["Model too simple", "Model too complex", "Perfect model", "None"], "correctAnswer": 1},
                    {"question": "Explain the difference between supervised and unsupervised learning with 2 examples each.", "type": "short-answer"},
                    {"question": "What is overfitting and how would you prevent it? Provide 3 specific techniques.", "type": "short-answer"},
                    {"question": "Explain backpropagation algorithm in neural networks step by step.", "type": "short-answer"},
                    {"question": "Compare decision trees and random forests. When would you use each?", "type": "short-answer"},
                    {"question": "How would you handle imbalanced datasets in classification problems?", "type": "short-answer"},
                    {"question": "Explain the bias-variance tradeoff with a practical example.", "type": "short-answer"},
                    {"question": "What evaluation metrics would you use for a medical diagnosis model and why?", "type": "short-answer"}
                ],
                'Intermediate': [
                    {"question": "Which optimizer adapts learning rates?", "type": "multiple-choice", "options": ["SGD", "Adam", "Momentum", "None"], "correctAnswer": 1},
                    {"question": "What is the main advantage of LSTM?", "type": "multiple-choice", "options": ["Faster training", "Less parameters", "Long-term memory", "Simpler"], "correctAnswer": 2},
                    {"question": "Which prevents overfitting?", "type": "multiple-choice", "options": ["Dropout", "Batch norm", "Data augmentation", "All of above"], "correctAnswer": 3},
                    {"question": "Design a recommendation system for Netflix. Explain your approach, features, model architecture, and evaluation metrics.", "type": "short-answer"},
                    {"question": "Explain the vanishing gradient problem in RNNs. How do LSTMs and GRUs solve this?", "type": "short-answer"},
                    {"question": "You're building a fraud detection model. Walk through your entire ML pipeline from data collection to deployment.", "type": "short-answer"},
                    {"question": "Compare transfer learning and fine-tuning. When would you use each approach?", "type": "short-answer"},
                    {"question": "How would you deploy a deep learning model to production with 99.9% uptime?", "type": "short-answer"},
                    {"question": "Explain attention mechanism in transformers and why it's revolutionary.", "type": "short-answer"},
                    {"question": "Your model has 95% accuracy but fails in production. What could be wrong and how would you fix it?", "type": "short-answer"}
                ],
                'Advanced': [
                    {"question": "What technique is used in Transformers?", "type": "multiple-choice", "options": ["Learned embeddings", "Sinusoidal encoding", "Random init", "One-hot"], "correctAnswer": 1},
                    {"question": "What is ResNet's main innovation?", "type": "multiple-choice", "options": ["Dropout", "Skip connections", "Attention", "Batch norm"], "correctAnswer": 1},
                    {"question": "Which loss is used for GANs?", "type": "multiple-choice", "options": ["Cross-entropy", "MSE", "Wasserstein", "Hinge"], "correctAnswer": 2},
                    {"question": "Design a large language model training pipeline. Explain distributed training, gradient accumulation, mixed precision, and optimization strategies.", "type": "short-answer"},
                    {"question": "Explain the architecture of GPT and BERT. What are the key differences and when would you use each?", "type": "short-answer"},
                    {"question": "You're training a model with 175B parameters. Explain your infrastructure, parallelization strategy, and cost optimization.", "type": "short-answer"},
                    {"question": "Design a real-time object detection system for autonomous vehicles. Include model architecture, latency requirements, and edge deployment.", "type": "short-answer"},
                    {"question": "Explain neural architecture search (NAS) and its applications. What are the computational challenges?", "type": "short-answer"},
                    {"question": "How would you implement continual learning to prevent catastrophic forgetting?", "type": "short-answer"},
                    {"question": "Design an AI system for medical diagnosis. Address data privacy, model interpretability, and regulatory compliance.", "type": "short-answer"}
                ]
            },
            'Data Scientist': {
                'Beginner': [
                    {"question": "Which measure is most affected by outliers?", "type": "multiple-choice", "options": ["Mean", "Median", "Mode", "Range"], "correctAnswer": 0},
                    {"question": "What does ETL stand for?", "type": "multiple-choice", "options": ["Extract, Transform, Load", "Evaluate, Test, Learn", "Execute, Track, Log", "None"], "correctAnswer": 0},
                    {"question": "Which chart shows correlation?", "type": "multiple-choice", "options": ["Bar chart", "Pie chart", "Scatter plot", "Line chart"], "correctAnswer": 2},
                    {"question": "Explain the difference between correlation and causation with a real-world example.", "type": "short-answer"},
                    {"question": "You have a dataset with missing values. Explain 3 different approaches to handle them.", "type": "short-answer"},
                    {"question": "What is A/B testing? Design an A/B test for a website's checkout button color.", "type": "short-answer"},
                    {"question": "Explain Type I and Type II errors with examples from business context.", "type": "short-answer"},
                    {"question": "How would you detect and handle outliers in a sales dataset?", "type": "short-answer"},
                    {"question": "Explain the difference between supervised and unsupervised learning for business problems.", "type": "short-answer"},
                    {"question": "What metrics would you use to evaluate a customer churn prediction model?", "type": "short-answer"}
                ],
                'Intermediate': [
                    {"question": "Which test compares means of two groups?", "type": "multiple-choice", "options": ["Chi-square", "T-test", "ANOVA", "Correlation"], "correctAnswer": 1},
                    {"question": "What is linear regression's main assumption?", "type": "multiple-choice", "options": ["Non-linear", "Linear relationship", "Categorical only", "No relationship"], "correctAnswer": 1},
                    {"question": "Which metric evaluates regression?", "type": "multiple-choice", "options": ["Accuracy", "Precision", "R-squared", "F1-score"], "correctAnswer": 2},
                    {"question": "Design a customer lifetime value (CLV) prediction model. Explain features, model selection, and business impact.", "type": "short-answer"},
                    {"question": "You're analyzing user behavior data. Walk through your exploratory data analysis process and key insights you'd look for.", "type": "short-answer"},
                    {"question": "Build a dashboard for executives. What metrics would you include and how would you visualize them?", "type": "short-answer"},
                    {"question": "Explain feature engineering for time series data. Provide 5 specific features you'd create.", "type": "short-answer"},
                    {"question": "Your model shows 90% accuracy but business says it's not working. What could be wrong?", "type": "short-answer"},
                    {"question": "Design an experiment to test if a new feature increases user engagement. Include sample size calculation.", "type": "short-answer"},
                    {"question": "How would you build a real-time anomaly detection system for fraud?", "type": "short-answer"}
                ],
                'Advanced': [
                    {"question": "Which method estimates treatment effects?", "type": "multiple-choice", "options": ["Propensity score", "Instrumental variables", "Difference-in-differences", "All of above"], "correctAnswer": 3},
                    {"question": "What is the curse of dimensionality?", "type": "multiple-choice", "options": ["Computational complexity", "High dimensions problem", "Storage issue", "Visualization"], "correctAnswer": 1},
                    {"question": "Which technique detects anomalies?", "type": "multiple-choice", "options": ["Isolation Forest", "One-class SVM", "LOF", "All of above"], "correctAnswer": 3},
                    {"question": "Design a data platform for a company with 100TB daily data. Include architecture, storage, processing, and governance.", "type": "short-answer"},
                    {"question": "Explain causal inference methods. How would you measure the impact of a marketing campaign?", "type": "short-answer"},
                    {"question": "Build a recommendation engine for e-commerce. Explain collaborative filtering, content-based, and hybrid approaches.", "type": "short-answer"},
                    {"question": "Design a real-time data pipeline processing 1M events/second. Include technologies, scaling, and monitoring.", "type": "short-answer"},
                    {"question": "You're leading a data science team of 10. How would you structure projects, ensure quality, and measure impact?", "type": "short-answer"},
                    {"question": "Explain time series forecasting for demand prediction. Include seasonality, trends, and model selection.", "type": "short-answer"},
                    {"question": "Design an ML ops pipeline with automated retraining, monitoring, and rollback capabilities.", "type": "short-answer"}
                ]
            }
        }
        
        return questions_by_role.get(role, {}).get(experience_level, questions_by_role['Software Engineer']['Beginner'])
    
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
