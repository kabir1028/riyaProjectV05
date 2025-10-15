// Interview page JavaScript

let questions = [];
let currentQuestionIndex = 0;
let answers = [];
let selectedRole = '';
let selectedDifficulty = '';

document.addEventListener('DOMContentLoaded', function() {
    // Get selections from sessionStorage
    selectedRole = sessionStorage.getItem('selectedRole') || 'Software Engineer';
    selectedDifficulty = sessionStorage.getItem('selectedDifficulty') || 'Beginner';
    
    loadQuestions();
    
    // Event listeners
    document.getElementById('nextBtn').addEventListener('click', nextQuestion);
    document.getElementById('prevBtn').addEventListener('click', prevQuestion);
});

async function loadQuestions() {
    try {
        const response = await fetch(`/api/questions?role=${encodeURIComponent(selectedRole)}&difficulty=${encodeURIComponent(selectedDifficulty)}`);
        questions = await response.json();
        
        if (questions.length === 0) {
            showError(document.getElementById('questionContainer'), 'No questions available for the selected role and difficulty.');
            return;
        }
        
        displayQuestion();
    } catch (error) {
        console.error('Questions loading error:', error);
        Toast.error('Failed to load questions. Using sample questions...');
        
        // Fallback sample questions
        questions = [
            {
                question: "What is your greatest strength?",
                type: "short-answer"
            },
            {
                question: "Tell me about yourself.",
                type: "short-answer"
            },
            {
                question: "Why do you want this job?",
                type: "short-answer"
            },
            {
                question: "What is object-oriented programming?",
                type: "multiple-choice",
                options: ["A programming paradigm", "A database type", "A web framework", "A testing method"],
                correctAnswer: 0
            },
            {
                question: "Describe your experience with teamwork.",
                type: "short-answer"
            }
        ];
        
        displayQuestion();
    }
}

function updateQuestionIndicators() {
    const indicator = document.getElementById('questionIndicator');
    if (!indicator) return;
    
    indicator.innerHTML = '';
    
    for (let i = 0; i < questions.length; i++) {
        const dot = document.createElement('div');
        dot.className = 'indicator-dot';
        
        if (i < currentQuestionIndex) {
            dot.classList.add('completed');
        } else if (i === currentQuestionIndex) {
            dot.classList.add('current');
        }
        
        dot.addEventListener('click', () => {
            if (i < currentQuestionIndex || (i === currentQuestionIndex + 1 && answers[currentQuestionIndex])) {
                currentQuestionIndex = i;
                displayQuestion();
            }
        });
        
        indicator.appendChild(dot);
    }
}

function displayQuestion() {
    if (currentQuestionIndex >= questions.length) {
        submitAnswers();
        return;
    }
    
    const question = questions[currentQuestionIndex];
    const progress = ((currentQuestionIndex + 1) / questions.length) * 100;
    
    // Update progress bar with animation
    const progressFill = document.getElementById('progressFill');
    progressFill.style.width = progress + '%';
    
    // Update question number with animation
    const questionNumber = document.getElementById('questionNumber');
    questionNumber.style.animation = 'none';
    questionNumber.offsetHeight; // Trigger reflow
    questionNumber.style.animation = 'fadeInLeft 0.6s ease-out';
    questionNumber.textContent = `Question ${currentQuestionIndex + 1} of ${questions.length}`;
    
    // Update question text with animation
    const questionText = document.getElementById('questionText');
    questionText.style.animation = 'none';
    questionText.offsetHeight; // Trigger reflow
    questionText.style.animation = 'fadeInUp 0.6s ease-out 0.2s both';
    questionText.textContent = question.question;
    
    // Create answer section
    const answerSection = document.getElementById('answerSection');
    answerSection.innerHTML = '';
    
    if (question.type === 'multiple-choice') {
        const optionsDiv = document.createElement('div');
        optionsDiv.className = 'options';
        
        question.options.forEach((option, index) => {
            const optionDiv = document.createElement('div');
            optionDiv.className = 'option';
            optionDiv.textContent = option;
            optionDiv.style.setProperty('--delay', (index * 0.1) + 's');
            optionDiv.addEventListener('click', () => selectOption(optionDiv, index));
            
            // Restore selection if exists
            if (answers[currentQuestionIndex] && answers[currentQuestionIndex].selectedOption === index) {
                optionDiv.classList.add('selected');
            }
            
            optionsDiv.appendChild(optionDiv);
        });
        
        answerSection.appendChild(optionsDiv);
    } else {
        const textareaContainer = document.createElement('div');
        textareaContainer.style.position = 'relative';
        
        const textarea = document.createElement('textarea');
        textarea.id = 'shortAnswer';
        textarea.placeholder = 'Type your detailed answer here (minimum 10 words required)...';
        textarea.style.width = '100%';
        textarea.style.minHeight = '150px';
        textarea.style.padding = '20px';
        textarea.style.border = '2px solid rgba(34, 197, 94, 0.3)';
        textarea.style.borderRadius = '15px';
        textarea.style.fontSize = '1rem';
        textarea.style.resize = 'vertical';
        textarea.style.background = 'rgba(255, 255, 255, 0.8)';
        textarea.style.color = '#1a1a1a';
        textarea.style.animation = 'slideInUp 0.6s ease-out 0.4s both';
        
        const wordCounter = document.createElement('div');
        wordCounter.className = 'word-counter insufficient';
        wordCounter.textContent = '0/10 words';
        
        textarea.addEventListener('input', function() {
            const words = this.value.trim().split(/\s+/).filter(word => word.length > 0);
            const wordCount = words.length;
            
            wordCounter.textContent = `${wordCount}/10 words`;
            
            if (wordCount >= 10) {
                wordCounter.className = 'word-counter sufficient';
                textarea.style.borderColor = '#22c55e';
            } else {
                wordCounter.className = 'word-counter insufficient';
                textarea.style.borderColor = '#ef4444';
            }
        });
        
        // Load previous answer if exists
        if (answers[currentQuestionIndex]) {
            textarea.value = answers[currentQuestionIndex].text || '';
            textarea.dispatchEvent(new Event('input'));
        }
        
        textareaContainer.appendChild(textarea);
        textareaContainer.appendChild(wordCounter);
        answerSection.appendChild(textareaContainer);
    }
    
    // Update question indicators
    updateQuestionIndicators();
    
    // Update navigation buttons
    document.getElementById('prevBtn').style.display = currentQuestionIndex > 0 ? 'block' : 'none';
    const nextBtn = document.getElementById('nextBtn');
    
    if (currentQuestionIndex === questions.length - 1) {
        nextBtn.innerHTML = 'Submit Interview <span style="margin-left: 10px;">✓</span>';
        nextBtn.style.background = 'linear-gradient(45deg, #28A745, #20c997)';
    } else {
        nextBtn.innerHTML = 'Next <span style="margin-left: 8px;">→</span>';
        nextBtn.style.background = 'linear-gradient(45deg, #28A745, #20c997)';
    }
}

function selectOption(optionElement, optionIndex) {
    // Remove previous selection with animation
    document.querySelectorAll('.option').forEach(opt => {
        opt.classList.remove('selected');
        opt.style.transform = 'translateX(0) scale(1)';
    });
    
    // Add selection to clicked option with animation
    optionElement.classList.add('selected');
    
    // Store answer
    const question = questions[currentQuestionIndex];
    answers[currentQuestionIndex] = {
        questionId: currentQuestionIndex,
        selectedOption: optionIndex,
        correct: optionIndex === question.correctAnswer,
        type: 'multiple-choice'
    };
    
    // Add haptic feedback (if supported)
    if (navigator.vibrate) {
        navigator.vibrate(50);
    }
}

function nextQuestion() {
    // Save current answer for short-answer questions
    const shortAnswerTextarea = document.getElementById('shortAnswer');
    if (shortAnswerTextarea) {
        answers[currentQuestionIndex] = {
            questionId: currentQuestionIndex,
            text: shortAnswerTextarea.value.trim(),
            type: 'short-answer'
        };
    }
    
    // Check if answer is provided and meets requirements
    if (!answers[currentQuestionIndex]) {
        Toast.warning('Please provide an answer before proceeding.');
        return;
    }
    
    // Check word count for short-answer questions
    if (answers[currentQuestionIndex].type === 'short-answer') {
        const words = (answers[currentQuestionIndex].text || '').trim().split(/\s+/).filter(word => word.length > 0);
        if (words.length < 10) {
            Toast.error('Please provide at least 10 words in your answer.');
            return;
        }
    }
    
    if (currentQuestionIndex === questions.length - 1) {
        submitAnswers();
    } else {
        currentQuestionIndex++;
        displayQuestion();
    }
}

function prevQuestion() {
    if (currentQuestionIndex > 0) {
        currentQuestionIndex--;
        displayQuestion();
    }
}

async function submitAnswers() {
    try {
        const response = await fetch('/api/submit-answers', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                answers: answers,
                role: selectedRole,
                difficulty: selectedDifficulty,
                questions: questions
            })
        });
        
        const result = await response.json();
        
        // Store results and additional data in sessionStorage
        sessionStorage.setItem('interviewResults', JSON.stringify(result));
        sessionStorage.setItem('interviewAnswers', JSON.stringify(answers));
        sessionStorage.setItem('interviewQuestions', JSON.stringify(questions));
        
        console.log('Stored results:', result);
        
        // Redirect to results page with ID
        window.location.href = '/results/' + result.id;
        
    } catch (error) {
        console.error('Submit error:', error);
        Toast.error('Failed to submit answers. Please try again.');
        
        // Calculate actual score based on answers
        let calculatedScore = 0;
        for (const answer of answers) {
            if (answer.type === 'multiple-choice' && answer.correct) {
                calculatedScore += 20;
            } else if (answer.type === 'short-answer' && answer.text) {
                const wordCount = answer.text.trim().split(/\s+/).length;
                if (wordCount >= 20) calculatedScore += 20;
                else if (wordCount >= 10) calculatedScore += 15;
                else if (wordCount >= 5) calculatedScore += 10;
            }
        }
        
        const mockResults = {
            score: Math.min(100, calculatedScore),
            feedback: calculatedScore >= 80 ? 'Excellent performance! You demonstrated strong knowledge and communication skills.' : 
                     calculatedScore >= 60 ? 'Good performance! Continue practicing to improve your interview skills.' :
                     'Keep practicing! Focus on providing more detailed answers and reviewing key concepts.',
            companies: ['Google', 'Microsoft', 'Amazon', 'Meta', 'Apple', 'Netflix', 'Uber', 'Airbnb']
        };
        
        // Generate a temporary ID for fallback results
        const tempId = 'temp_' + Date.now();
        mockResults.id = tempId;
        
        sessionStorage.setItem('interviewResults', JSON.stringify(mockResults));
        sessionStorage.setItem('interviewAnswers', JSON.stringify(answers));
        sessionStorage.setItem('interviewQuestions', JSON.stringify(questions));
        
        console.log('Stored calculated results:', mockResults);
        
        setTimeout(() => {
            window.location.href = '/results/' + tempId;
        }, 1500);
    }
}