let questions = [];
let currentQuestion = 0;
let answers = [];
let role = '';
let difficulty = '';
let startTime = Date.now();

// Load interview data
document.addEventListener('DOMContentLoaded', async () => {
    role = sessionStorage.getItem('selectedRole');
    difficulty = sessionStorage.getItem('selectedDifficulty');
    
    if (!role || !difficulty) {
        Toast.error('Interview setup incomplete. Redirecting...');
        setTimeout(() => window.location.href = '/start-interview', 2000);
        return;
    }
    
    Toast.info('Loading AI-generated questions...');
    await loadQuestions();
});

async function loadQuestions() {
    try {
        const response = await fetch(`/api/questions?role=${encodeURIComponent(role)}&difficulty=${encodeURIComponent(difficulty)}&use_ai=true`);
        const data = await response.json();
        
        if (data.success) {
            questions = data.questions;
            
            if (data.source === 'ai') {
                Toast.success('AI questions generated successfully!');
            } else {
                Toast.info('Using curated questions');
            }
            
            // Initialize answers array
            answers = questions.map(q => ({
                type: q.type,
                text: '',
                selected: null,
                correct: false
            }));
            
            renderQuestion();
            updateIndicators();
        } else {
            throw new Error('Failed to load questions');
        }
    } catch (error) {
        console.error('Load questions error:', error);
        Toast.error('Failed to load questions. Please try again.');
        setTimeout(() => window.location.href = '/start-interview', 2000);
    }
}

function renderQuestion() {
    const question = questions[currentQuestion];
    const answerSection = document.getElementById('answerSection');
    
    // Update question number and text
    document.getElementById('questionNumber').textContent = `Question ${currentQuestion + 1} of ${questions.length}`;
    document.getElementById('questionText').textContent = question.question;
    
    // Update progress bar
    const progress = ((currentQuestion + 1) / questions.length) * 100;
    document.getElementById('progressFill').style.width = progress + '%';
    document.getElementById('progressText').textContent = Math.round(progress) + '%';
    
    // Render answer input based on type
    if (question.type === 'multiple-choice') {
        answerSection.innerHTML = `
            <div class="options-container" style="margin-top: 2rem; display: flex; flex-direction: column; gap: 1rem;">
                ${question.options.map((option, index) => {
                    const isSelected = answers[currentQuestion].selected === index;
                    return `
                    <div class="option-card" 
                         onclick="selectOption(${index})"
                         style="padding: 1.2rem 1.5rem; 
                                border: 2px solid ${isSelected ? '#22c55e' : '#e5e7eb'}; 
                                border-radius: 10px; 
                                cursor: pointer; 
                                transition: all 0.2s ease; 
                                background: ${isSelected ? '#f0fdf4' : 'white'};
                                display: flex; 
                                align-items: center; 
                                gap: 1rem;">
                        <div class="radio-dot" 
                             style="min-width: 24px; 
                                    height: 24px; 
                                    border-radius: 50%; 
                                    border: 3px solid ${isSelected ? '#22c55e' : '#d1d5db'};
                                    background: white;
                                    display: flex; 
                                    align-items: center; 
                                    justify-content: center; 
                                    transition: all 0.2s;">
                            ${isSelected ? '<div style="width: 12px; height: 12px; border-radius: 50%; background: #22c55e;"></div>' : ''}
                        </div>
                        <div class="option-letter" 
                             style="min-width: 32px; 
                                    height: 32px; 
                                    border-radius: 6px; 
                                    background: ${isSelected ? '#22c55e' : '#f3f4f6'}; 
                                    color: ${isSelected ? 'white' : '#6b7280'}; 
                                    display: flex; 
                                    align-items: center; 
                                    justify-content: center; 
                                    font-weight: 700; 
                                    font-size: 0.95rem; 
                                    transition: all 0.2s;">
                            ${String.fromCharCode(65 + index)}
                        </div>
                        <div class="option-text" 
                             style="flex: 1; 
                                    color: ${isSelected ? '#166534' : '#374151'}; 
                                    font-size: 1rem; 
                                    line-height: 1.5;
                                    font-weight: ${isSelected ? '600' : '400'};">
                            ${option}
                        </div>
                    </div>
                `}).join('')}
            </div>
        `;
    } else {
        answerSection.innerHTML = `
            <div style="margin-top: 2rem; animation: fadeInLeft 0.6s ease-out;">
                <textarea 
                    id="answerText" 
                    placeholder="Write your detailed answer here...\n\n✓ Be specific and provide examples\n✓ Explain your reasoning clearly\n✓ Aim for at least 30 words for better evaluation\n✓ Use proper grammar and structure"
                    style="width: 100%; min-height: 250px; padding: 1.5rem; border: 3px solid #e5e7eb; 
                           border-radius: 12px; background: white; 
                           color: #1a1a1a; font-size: 1.05rem; resize: vertical; font-family: inherit; line-height: 1.8;
                           transition: all 0.3s;"
                    oninput="updateAnswer(this.value)"
                    onfocus="this.style.borderColor='#22c55e'; this.style.boxShadow='0 0 0 3px rgba(34, 197, 94, 0.1)'"
                    onblur="this.style.borderColor='#e5e7eb'; this.style.boxShadow='none'"
                >${answers[currentQuestion].text}</textarea>
                <div style="margin-top: 0.8rem; padding: 1rem; background: #f9fafb; border-radius: 8px; display: flex; justify-content: space-between; align-items: center;">
                    <span id="wordCount" style="font-weight: 600; font-size: 1rem;">0 words</span>
                    <span style="color: #6b7280; font-size: 0.9rem;">💡 Minimum 30 words recommended</span>
                </div>
            </div>
        `;
        
        // Update word count
        updateWordCount();
    }
    
    // Update navigation buttons
    document.getElementById('prevBtn').style.display = currentQuestion > 0 ? 'block' : 'none';
    document.getElementById('nextBtn').textContent = currentQuestion === questions.length - 1 ? 'Submit Interview' : 'Next →';
    
    updateIndicators();
}

function selectOption(index) {
    const question = questions[currentQuestion];
    answers[currentQuestion].selected = index;
    answers[currentQuestion].correct = index === question.correctAnswer;
    
    // Re-render the question to update UI
    renderQuestion();
}

function updateAnswer(text) {
    answers[currentQuestion].text = text;
    updateWordCount();
    updateIndicators();
}

function updateWordCount() {
    const text = answers[currentQuestion].text || '';
    const words = text.trim().split(/\s+/).filter(w => w.length > 0);
    const wordCount = words.length;
    const wordCountEl = document.getElementById('wordCount');
    if (wordCountEl) {
        wordCountEl.textContent = `${wordCount} words`;
        if (wordCount >= 30) {
            wordCountEl.style.color = '#22c55e';
            wordCountEl.innerHTML = `✓ ${wordCount} words <span style="font-size: 0.85rem; color: #16a34a;">(Excellent)</span>`;
        } else if (wordCount >= 20) {
            wordCountEl.style.color = '#f59e0b';
            wordCountEl.innerHTML = `⚠ ${wordCount} words <span style="font-size: 0.85rem; color: #d97706;">(Good, add more)</span>`;
        } else if (wordCount >= 10) {
            wordCountEl.style.color = '#ef4444';
            wordCountEl.innerHTML = `✗ ${wordCount} words <span style="font-size: 0.85rem; color: #dc2626;">(Too short)</span>`;
        } else {
            wordCountEl.style.color = '#ef4444';
            wordCountEl.innerHTML = `✗ ${wordCount} words <span style="font-size: 0.85rem; color: #dc2626;">(Insufficient)</span>`;
        }
    }
}

function updateIndicators() {
    const indicator = document.getElementById('questionIndicator');
    indicator.innerHTML = questions.map((q, index) => {
        const answer = answers[index];
        const isAnswered = answer.type === 'multiple-choice' ? answer.selected !== null : answer.text.trim().length > 0;
        const isCurrent = index === currentQuestion;
        
        return `<div class="indicator-dot ${isAnswered ? 'completed' : ''} ${isCurrent ? 'current' : ''}" 
                     onclick="goToQuestion(${index})"
                     title="Question ${index + 1}"></div>`;
    }).join('');
}

function goToQuestion(index) {
    if (index >= 0 && index < questions.length) {
        currentQuestion = index;
        renderQuestion();
    }
}

// Navigation
document.getElementById('prevBtn').addEventListener('click', () => {
    if (currentQuestion > 0) {
        currentQuestion--;
        renderQuestion();
    }
});

document.getElementById('nextBtn').addEventListener('click', async () => {
    // Validate current answer
    const answer = answers[currentQuestion];
    if (answer.type === 'multiple-choice' && answer.selected === null) {
        Toast.warning('Please select an answer before proceeding');
        return;
    }
    if (answer.type === 'short-answer' && !answer.text.trim()) {
        Toast.warning('Please provide an answer before proceeding');
        return;
    }
    
    if (currentQuestion < questions.length - 1) {
        currentQuestion++;
        renderQuestion();
    } else {
        await submitInterview();
    }
});

async function submitInterview() {
    // Check if all questions are answered
    const unanswered = answers.findIndex((a, i) => {
        if (a.type === 'multiple-choice') return a.selected === null;
        return !a.text.trim();
    });
    
    if (unanswered !== -1) {
        Toast.warning(`Please answer question ${unanswered + 1} before submitting`);
        goToQuestion(unanswered);
        return;
    }
    
    // Show loading
    Toast.info('Evaluating your answers with AI... This may take a moment.');
    document.getElementById('nextBtn').disabled = true;
    document.getElementById('nextBtn').textContent = 'Evaluating...';
    
    try {
        const user = JSON.parse(localStorage.getItem('user') || 'null');
        const userId = user?.id;
        
        if (!userId) {
            Toast.error('User session expired. Please login again.');
            setTimeout(() => window.location.href = '/login', 2000);
            return;
        }
        
        const timeTaken = Math.floor((Date.now() - startTime) / 1000);
        
        const response = await fetch('/api/submit-answers', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                answers: answers,
                questions: questions,
                role: role,
                difficulty: difficulty,
                user_id: userId,
                time_taken: timeTaken,
                use_ai: true
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            Toast.success('Interview completed! Redirecting to results...');
            
            // Store result ID
            sessionStorage.setItem('lastResultId', data.id);
            
            setTimeout(() => {
                window.location.href = `/results/${data.id}`;
            }, 1500);
        } else {
            throw new Error(data.message || 'Submission failed');
        }
    } catch (error) {
        console.error('Submit error:', error);
        Toast.error('Failed to submit interview. Please try again.');
        document.getElementById('nextBtn').disabled = false;
        document.getElementById('nextBtn').textContent = 'Submit Interview';
    }
}

// Prevent accidental page leave
window.addEventListener('beforeunload', (e) => {
    if (currentQuestion < questions.length) {
        e.preventDefault();
        e.returnValue = '';
    }
});
