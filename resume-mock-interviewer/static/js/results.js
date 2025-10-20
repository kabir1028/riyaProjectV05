// Results page JavaScript

let performanceChart;

document.addEventListener('DOMContentLoaded', function() {
    loadResults();
    createParticles();
});

function createParticles() {
    const particles = document.createElement('div');
    particles.className = 'particles';
    particles.id = 'particles';
    document.body.appendChild(particles);
    
    for (let i = 0; i < 30; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.top = Math.random() * 100 + '%';
        particle.style.width = Math.random() * 3 + 1 + 'px';
        particle.style.height = particle.style.width;
        particle.style.animationDelay = Math.random() * 6 + 's';
        particle.style.animationDuration = (Math.random() * 4 + 4) + 's';
        particles.appendChild(particle);
    }
}

function loadResults() {
    try {
        // Check if we have a result ID from URL
        const resultId = window.resultId;
        
        if (resultId) {
            // Load specific result by ID
            loadResultById(resultId);
            return;
        }
        
        const resultsData = sessionStorage.getItem('interviewResults');
        const answersData = sessionStorage.getItem('interviewAnswers');
        const questionsData = sessionStorage.getItem('interviewQuestions');
        
        console.log('Loading results:', { resultsData, answersData, questionsData });
        
        if (!resultsData) {
            console.log('No results data found, redirecting to start interview');
            window.location.href = '/start-interview';
            return;
        }
        
        const results = JSON.parse(resultsData);
        const answers = answersData ? JSON.parse(answersData) : [];
        const questions = questionsData ? JSON.parse(questionsData) : [];
        
        // Animate score counter
        animateScore(results.score || 0);
        
        // Update progress ring
        updateProgressRing(results.score || 0);
        
        // Display feedback
        document.getElementById('feedbackText').textContent = results.feedback || 'No feedback available.';
        
        // Update performance stats
        updatePerformanceStats(results, answers);
        
        // Create performance chart
        createPerformanceChart(results, answers);
        
        // Display Q&A review
        displayQAReview(questions, answers);
        
        // Display companies
        displayCompanies(results.companies || []);
        
        // Update improvement suggestions
        updateImprovementSuggestions(results.score);
        
    } catch (error) {
        console.error('Results loading error:', error);
        Toast.error('Failed to load results');
        window.location.href = '/start-interview';
    }
}

function loadResultById(resultId) {
    fetch(`/api/get-result/${resultId}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            
            // Use the loaded data
            animateScore(data.score);
            updateProgressRing(data.score);
            document.getElementById('feedbackText').textContent = data.feedback;
            updatePerformanceStats(data, data.answers);
            createPerformanceChart(data, data.answers);
            displayQAReview(data.questions, data.answers);
            displayCompanies(data.companies);
            updateImprovementSuggestions(data.score);
        })
        .catch(error => {
            console.error('Error loading result:', error);
            Toast.error('Failed to load result');
            window.location.href = '/start-interview';
        });
}

function animateScore(targetScore) {
    const scoreElement = document.getElementById('scoreNumber');
    scoreElement.textContent = targetScore;
    updateScoreInsights(targetScore);
}

function updateScoreInsights(score) {
    // Update grade
    const grade = score >= 90 ? 'A+ Excellent' : score >= 80 ? 'A Good' : score >= 70 ? 'B+ Average' : score >= 60 ? 'B Below Average' : 'C Needs Improvement';
    document.getElementById('scoreGrade').textContent = grade;
    
    // Update insights
    const accuracy = Math.round((score / 100) * 100) + '%';
    const ranking = score >= 90 ? 'Top 5%' : score >= 80 ? 'Top 15%' : score >= 70 ? 'Top 30%' : score >= 60 ? 'Top 50%' : 'Bottom 50%';
    
    document.getElementById('accuracyInsight').textContent = accuracy;
    document.getElementById('rankingInsight').textContent = ranking;
    
    // Update breakdown scores with animation
    const technical = Math.max(0, score + Math.random() * 20 - 10);
    const communication = Math.max(0, score + Math.random() * 15 - 7);
    const problemSolving = Math.max(0, score + Math.random() * 25 - 12);
    
    setTimeout(() => {
        document.getElementById('technicalFill').style.width = Math.min(100, technical) + '%';
        document.getElementById('communicationFill').style.width = Math.min(100, communication) + '%';
        document.getElementById('problemSolvingFill').style.width = Math.min(100, problemSolving) + '%';
        
        document.getElementById('technicalScore').textContent = Math.round(technical) + '%';
        document.getElementById('communicationScore').textContent = Math.round(communication) + '%';
        document.getElementById('problemSolvingScore').textContent = Math.round(problemSolving) + '%';
    }, 1000);
    
    // Update quick tips
    updateQuickTips(score);
}

function updateQuickTips(score) {
    const tipsContainer = document.getElementById('quickTips');
    let tips = [];
    
    if (score < 60) {
        tips = [
            'Focus on fundamental concepts - spend 30 min daily on basics',
            'Practice explaining technical terms in simple language',
            'Use the STAR method for behavioral questions'
        ];
    } else if (score < 80) {
        tips = [
            'Add specific examples and metrics to your answers',
            'Practice system design and architecture questions',
            'Work on confident delivery and body language'
        ];
    } else {
        tips = [
            'Perfect! Focus on company-specific preparation',
            'Practice leadership and strategic thinking scenarios',
            'Prepare thoughtful questions for the interviewer'
        ];
    }
    
    tipsContainer.innerHTML = '';
    tips.forEach((tip, index) => {
        const tipElement = document.createElement('div');
        tipElement.className = 'tip-item';
        tipElement.textContent = tip;
        tipElement.style.animationDelay = (index * 0.2) + 's';
        tipElement.style.animation = 'fadeInUp 0.6s ease-out both';
        tipsContainer.appendChild(tipElement);
    });
}

function updateProgressRing(score) {
    const circle = document.getElementById('progressCircle');
    const progressText = document.getElementById('progressText');
    
    if (circle) {
        circle.style.setProperty('--progress', score);
        progressText.textContent = score + '%';
        
        // Animate the ring
        setTimeout(() => {
            circle.style.strokeDashoffset = `calc(565.48 - (565.48 * ${score}) / 100)`;
        }, 500);
    }
}

function updatePerformanceStats(results, answers) {
    const correctAnswers = answers.filter(a => a.correct || (a.type === 'short-answer' && a.text && a.text.trim().length > 10)).length;
    const accuracy = Math.round((correctAnswers / answers.length) * 100);
    
    document.getElementById('correctAnswers').textContent = correctAnswers;
    document.getElementById('accuracy').textContent = accuracy + '%';
    document.getElementById('timeSpent').textContent = '15m';
    
    // Add new stats
    const skillLevel = results.score >= 80 ? 'Expert' : results.score >= 60 ? 'Intermediate' : 'Beginner';
    const marketReady = results.score >= 70 ? 'Yes' : 'Partial';
    
    document.getElementById('skillLevel').textContent = skillLevel;
    document.getElementById('marketReady').textContent = marketReady;
    
    // Update comparison chart
    document.getElementById('yourScore').textContent = results.score + '%';
    document.getElementById('yourScoreFill').style.width = results.score + '%';
    
    // Animate comparison bars
    setTimeout(() => {
        document.getElementById('yourScoreFill').style.transition = 'width 2s ease-out';
    }, 500);
}

function createPerformanceChart(results, answers) {
    const ctx = document.getElementById('performanceChart');
    if (!ctx) return;
    
    const correctCount = answers.filter(a => a.correct || (a.type === 'short-answer' && a.text && a.text.trim().length > 10)).length;
    const incorrectCount = answers.length - correctCount;
    
    performanceChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Correct', 'Incorrect', 'Partial'],
            datasets: [{
                data: [correctCount, incorrectCount, Math.floor(answers.length * 0.1)],
                backgroundColor: [
                    'rgba(40, 167, 69, 0.8)',
                    'rgba(220, 53, 69, 0.8)',
                    'rgba(255, 193, 7, 0.8)'
                ],
                borderColor: [
                    'rgba(40, 167, 69, 1)',
                    'rgba(220, 53, 69, 1)',
                    'rgba(255, 193, 7, 1)'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: 'rgba(255, 255, 255, 0.8)',
                        font: {
                            size: 14
                        }
                    }
                }
            },
            animation: {
                animateRotate: true,
                duration: 2000
            }
        }
    });
}

function displayQAReview(questions, answers) {
    const qaReview = document.getElementById('qaReview');
    if (!qaReview || !questions.length) return;
    
    // Update summary counts
    let correctCount = 0, partialCount = 0, incorrectCount = 0;
    
    qaReview.innerHTML = '';
    
    questions.forEach((question, index) => {
        const answer = answers[index] || {};
        const qaItem = document.createElement('div');
        qaItem.className = 'qa-item';
        qaItem.style.animationDelay = (index * 0.1) + 's';
        
        let statusClass = 'partial';
        let statusText = 'Partial';
        let explanation = '';
        
        if (question.type === 'multiple-choice') {
            if (answer.correct) {
                statusClass = 'correct';
                statusText = 'Excellent';
                correctCount++;
                explanation = 'Perfect! You demonstrated strong understanding of this concept.';
            } else if (answer.selectedOption !== undefined) {
                statusClass = 'incorrect';
                statusText = 'Needs Review';
                incorrectCount++;
                explanation = 'Consider reviewing this topic. The correct answer provides better insight into the concept.';
            }
        } else {
            const wordCount = answer.text ? answer.text.trim().split(/\s+/).length : 0;
            if (wordCount >= 20) {
                statusClass = 'correct';
                statusText = 'Comprehensive';
                correctCount++;
                explanation = 'Excellent detailed response! You provided thorough analysis and examples.';
            } else if (wordCount >= 10) {
                statusClass = 'partial';
                statusText = 'Good Effort';
                partialCount++;
                explanation = 'Good start! Consider adding more specific examples and detailed explanations.';
            } else {
                statusClass = 'incorrect';
                statusText = 'Insufficient';
                incorrectCount++;
                explanation = 'This answer needs significant improvement. Provide more detailed, specific responses.';
            }
        }
        
        qaItem.innerHTML = `
            <div class="qa-question">Q${index + 1}: ${question.question}</div>
            <div class="qa-status ${statusClass}">${statusText}</div>
            
            ${answer.selectedOption !== undefined ? `
                <div class="qa-your-answer">
                    ${question.options[answer.selectedOption]}
                </div>
            ` : ''}
            
            ${answer.text ? `
                <div class="qa-your-answer">
                    ${answer.text}
                </div>
            ` : ''}
            
            ${question.type === 'multiple-choice' ? `
                <div class="qa-correct-answer">
                    ${question.options[question.correctAnswer]}
                </div>
            ` : `
                <div class="qa-correct-answer">
                    <strong>Ideal Response Should Include:</strong> Specific examples, technical details, measurable outcomes, and clear reasoning. Aim for 20-50 words with concrete examples.
                </div>
            `}
            
            <div class="qa-explanation">
                <strong>Assessment:</strong> ${explanation}
            </div>
        `;
        
        qaReview.appendChild(qaItem);
    });
    
    // Update summary counts
    document.getElementById('correctCount').textContent = correctCount;
    document.getElementById('partialCount').textContent = partialCount;
    document.getElementById('incorrectCount').textContent = incorrectCount;
}

function displayCompanies(companies) {
    const companiesList = document.getElementById('companiesList');
    companiesList.innerHTML = '';
    
    if (companies.length > 0) {
        companies.forEach((company, index) => {
            const companyDiv = document.createElement('div');
            companyDiv.className = 'company-item';
            companyDiv.textContent = company;
            companyDiv.style.animationDelay = (index * 0.1) + 's';
            companiesList.appendChild(companyDiv);
        });
    } else {
        companiesList.innerHTML = '<p style="color: rgba(255, 255, 255, 0.7);">No company recommendations available.</p>';
    }
}

function updateImprovementSuggestions(score) {
    const improvementsList = document.getElementById('improvementsList');
    const strengthsList = document.getElementById('strengthsList');
    
    improvementsList.innerHTML = '';
    strengthsList.innerHTML = '';
    
    let improvements = [];
    let strengths = [];
    
    if (score < 40) {
        strengths = [
            'Completed the full interview process',
            'Showed willingness to learn and improve',
            'Demonstrated basic understanding of concepts'
        ];
        improvements = [
            'Focus on fundamental concepts and terminology',
            'Practice technical questions daily (30-45 minutes)',
            'Study industry-standard best practices',
            'Improve answer structure and clarity',
            'Build stronger foundational knowledge'
        ];
    } else if (score < 70) {
        strengths = [
            'Good grasp of basic concepts',
            'Adequate problem-solving approach',
            'Shows potential for growth'
        ];
        improvements = [
            'Deepen technical knowledge in specialized areas',
            'Practice explaining complex concepts simply',
            'Work on providing specific examples',
            'Improve time management in responses',
            'Study advanced industry patterns'
        ];
    } else if (score < 90) {
        strengths = [
            'Strong technical foundation',
            'Good communication skills',
            'Well-structured responses',
            'Shows leadership potential'
        ];
        improvements = [
            'Polish presentation and delivery style',
            'Practice handling ambiguous scenarios',
            'Develop more compelling examples',
            'Enhance strategic thinking approach',
            'Focus on industry-specific expertise'
        ];
    } else {
        strengths = [
            'Exceptional technical knowledge',
            'Outstanding communication skills',
            'Strategic thinking ability',
            'Leadership qualities evident',
            'Market-ready professional'
        ];
        improvements = [
            'Maintain current skill level through practice',
            'Consider mentoring and knowledge sharing',
            'Stay current with emerging technologies',
            'Prepare for executive-level discussions',
            'Focus on company-specific preparation'
        ];
    }
    
    strengths.forEach((strength, index) => {
        const li = document.createElement('li');
        li.textContent = strength;
        li.style.animationDelay = (index * 0.1) + 's';
        li.style.animation = 'fadeInLeft 0.6s ease-out both';
        strengthsList.appendChild(li);
    });
    
    improvements.forEach((improvement, index) => {
        const li = document.createElement('li');
        li.textContent = improvement;
        li.style.animationDelay = (index * 0.1) + 's';
        li.style.animation = 'fadeInLeft 0.6s ease-out both';
        improvementsList.appendChild(li);
    });
}