let questions = [];
let currentQuestion = 0;
let answers = [];
let role = '';
let difficulty = '';
let mediaRecorder = null;
let audioChunks = [];
let recognition = null;
let startTime = Date.now();

if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = 'en-US';
    
    recognition.onresult = (event) => {
        let transcript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
            transcript += event.results[i][0].transcript;
        }
        document.getElementById('transcriptText').textContent = transcript;
        answers[currentQuestion].text = transcript;
    };
    
    recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        updateStatus('Error: ' + event.error, 'ready');
    };
}

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
            answers = questions.map(q => ({ type: 'voice', text: '', audio: null }));
            
            console.log('Questions loaded:', questions);
            renderQuestion();
            
            setTimeout(() => {
                speakQuestion();
                Toast.success('Question loaded! Listen and click record to answer.');
            }, 500);
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
    if (!questions || questions.length === 0) {
        console.error('No questions available');
        return;
    }
    
    const question = questions[currentQuestion];
    console.log('Rendering question:', question);
    
    const questionText = question.question || question.text || 'Question not available';
    
    document.getElementById('questionNumber').textContent = `Question ${currentQuestion + 1} of ${questions.length}`;
    document.getElementById('questionText').textContent = questionText;
    document.getElementById('transcriptText').textContent = answers[currentQuestion].text || 'Your spoken answer will appear here...';
    
    const progress = ((currentQuestion + 1) / questions.length) * 100;
    document.getElementById('progressFill').style.width = progress + '%';
    document.getElementById('progressText').textContent = Math.round(progress) + '%';
    
    document.getElementById('prevBtn').style.display = currentQuestion > 0 ? 'block' : 'none';
    document.getElementById('nextBtn').textContent = currentQuestion === questions.length - 1 ? 'Submit Interview' : 'Next →';
    document.getElementById('nextBtn').disabled = !answers[currentQuestion].text;
    
    updateStatus('🎤 Ready to record - Click the microphone button', 'ready');
}

function speakQuestion() {
    if ('speechSynthesis' in window) {
        speechSynthesis.cancel();
        
        const question = questions[currentQuestion];
        const questionText = question.question || question.text || '';
        
        if (questionText) {
            const utterance = new SpeechSynthesisUtterance(questionText);
            utterance.rate = 0.85;
            utterance.pitch = 1;
            utterance.volume = 1;
            
            utterance.onstart = () => {
                updateStatus('🔊 AI is speaking the question...', 'processing');
                document.getElementById('pulseRing').style.display = 'block';
            };
            
            utterance.onend = () => {
                updateStatus('🎤 Question complete - Click record to answer', 'ready');
                document.getElementById('pulseRing').style.display = 'none';
            };
            
            speechSynthesis.speak(utterance);
            console.log('Speaking question:', questionText);
        } else {
            console.error('No question text to speak');
        }
    } else {
        console.error('Speech synthesis not supported');
        Toast.warning('Text-to-speech not supported in your browser');
    }
}

function playQuestion() {
    speakQuestion();
}

function startRecording() {
    if (!recognition) {
        Toast.error('Speech recognition not supported in your browser');
        return;
    }
    
    try {
        recognition.start();
        document.getElementById('recordBtn').classList.add('recording');
        document.getElementById('recordBtn').style.display = 'none';
        document.getElementById('stopBtn').style.display = 'block';
        document.getElementById('pulseRing').style.display = 'block';
        updateStatus('🎤 Listening... Speak your answer', 'listening');
    } catch (error) {
        console.error('Recording error:', error);
    }
}

function stopRecording() {
    if (recognition) {
        recognition.stop();
    }
    
    document.getElementById('recordBtn').classList.remove('recording');
    document.getElementById('recordBtn').style.display = 'block';
    document.getElementById('stopBtn').style.display = 'none';
    document.getElementById('pulseRing').style.display = 'none';
    document.getElementById('nextBtn').disabled = false;
    updateStatus('✓ Answer recorded - Click Next to continue', 'ready');
}

function updateStatus(message, type) {
    const indicator = document.getElementById('statusIndicator');
    indicator.textContent = message;
    indicator.className = 'status-indicator status-' + type;
}

function previousQuestion() {
    if (currentQuestion > 0) {
        currentQuestion--;
        renderQuestion();
    }
}

function nextQuestion() {
    const currentAnswer = answers[currentQuestion].text;
    
    if (!currentAnswer || currentAnswer.trim().length < 10) {
        Toast.warning('Please record a proper answer before proceeding (at least 10 words)');
        return;
    }
    
    if (currentQuestion < questions.length - 1) {
        currentQuestion++;
        renderQuestion();
        
        setTimeout(() => {
            speakQuestion();
        }, 500);
    } else {
        submitInterview();
    }
}

async function submitInterview() {
    Toast.info('Evaluating your voice interview... This may take a moment.');
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
        
        const response = await fetch('/api/submit-voice-interview', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                answers: answers,
                questions: questions,
                role: role,
                difficulty: difficulty,
                user_id: userId,
                time_taken: timeTaken,
                interview_type: 'voice'
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            Toast.success('Voice interview completed! Redirecting to results...');
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
