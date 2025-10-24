document.addEventListener('DOMContentLoaded', async function() {
    const user = Auth.getCurrentUser();
    if (!user) {
        window.location.href = '/login';
        return;
    }

    try {
        const response = await fetch(`/api/profile/history?user_id=${user.id}`);
        const data = await response.json();

        if (data.success && data.history.length > 0) {
            displayTimeline(data.history);
            updateStats(data.history);
        } else {
            showEmptyState();
        }
    } catch (error) {
        console.error('Error loading history:', error);
        showEmptyState();
    }
});

function updateStats(history) {
    document.getElementById('totalCount').textContent = history.length;
    
    const scores = history.map(h => h.score);
    const avgScore = Math.round(scores.reduce((a, b) => a + b, 0) / scores.length);
    const bestScore = Math.max(...scores);
    
    document.getElementById('avgScore').textContent = avgScore;
    document.getElementById('bestScore').textContent = bestScore;
    
    const improvement = history.length > 1 ? 
        Math.round(((history[0].score - history[history.length - 1].score) / history[history.length - 1].score) * 100) : 0;
    document.getElementById('improvement').textContent = (improvement > 0 ? '+' : '') + improvement + '%';
}

function displayTimeline(history) {
    const container = document.getElementById('timeline');
    container.innerHTML = history.map((item, index) => {
        const date = new Date(item.created_at);
        const dateStr = date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
        const timeStr = date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
        
        const scoreColor = item.score >= 80 ? '#22c55e' : item.score >= 60 ? '#f59e0b' : '#ef4444';
        const scoreEmoji = item.score >= 80 ? '🌟' : item.score >= 60 ? '⭐' : '📌';
        
        const companies = item.companies.slice(0, 4).map(c => {
            const companyName = typeof c === 'object' ? c.name : c;
            return `<span style="background: rgba(34, 197, 94, 0.1); color: #22c55e; padding: 0.4rem 0.8rem; border-radius: 15px; font-size: 0.85rem; font-weight: 500;">${companyName}</span>`;
        }).join(' ');
        
        return `
            <div class="timeline-item">
                <div class="timeline-dot" style="border-color: ${scoreColor}; color: ${scoreColor};">
                    ${scoreEmoji}
                </div>
                <div class="timeline-card" style="border-left-color: ${scoreColor};">
                    <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem; flex-wrap: wrap; gap: 1rem;">
                        <div>
                            <h3 style="font-size: 1.3rem; font-weight: 600; color: #1a1a1a; margin-bottom: 0.5rem;">
                                Interview Session #${history.length - index}
                            </h3>
                            <div style="display: flex; gap: 1rem; color: #6b7280; font-size: 0.9rem;">
                                <span>📅 ${dateStr}</span>
                                <span>🕐 ${timeStr}</span>
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 2.5rem; font-weight: 700; color: ${scoreColor}; line-height: 1;">${item.score}</div>
                            <div style="font-size: 0.85rem; color: #6b7280;">Score</div>
                        </div>
                    </div>
                    
                    <div style="color: #4a5568; margin-bottom: 1.5rem; line-height: 1.6; font-size: 1rem;">
                        ${formatFeedback(item.feedback)}
                    </div>
                    
                    <div style="margin-bottom: 1.5rem;">
                        <div style="font-size: 0.85rem; color: #6b7280; margin-bottom: 0.5rem; font-weight: 500;">Recommended Companies:</div>
                        <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">${companies}</div>
                    </div>
                    
                    <div style="display: flex; gap: 1rem; justify-content: flex-end;">
                        <a href="/results/${item.id}" style="background: ${scoreColor}; color: white; padding: 0.75rem 1.5rem; border-radius: 10px; text-decoration: none; font-weight: 500; display: inline-flex; align-items: center; gap: 0.5rem;">
                            📊 View Detailed Report
                        </a>
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

function formatFeedback(feedback) {
    if (typeof feedback === 'string') {
        try {
            feedback = JSON.parse(feedback);
        } catch (e) {
            return feedback;
        }
    }
    
    if (typeof feedback === 'object' && feedback.summary) {
        return feedback.summary;
    }
    
    return typeof feedback === 'string' ? feedback : 'No feedback available';
}

function showEmptyState() {
    document.getElementById('timeline').innerHTML = `
        <div style="text-align: center; padding: 5rem 2rem; background: rgba(255, 255, 255, 0.95); border-radius: 20px; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);">
            <div style="font-size: 6rem; margin-bottom: 2rem;">📊</div>
            <h3 style="color: #1a1a1a; margin-bottom: 1rem; font-size: 2rem;">Your Journey Starts Here</h3>
            <p style="color: #6b7280; margin-bottom: 3rem; font-size: 1.2rem;">Take your first interview to begin building your success timeline</p>
            <a href="/start-interview" class="btn btn-primary" style="padding: 1.25rem 2.5rem; font-size: 1.2rem; display: inline-flex; align-items: center; gap: 0.75rem;">
                🚀 Start Your First Interview
            </a>
        </div>
    `;
}
