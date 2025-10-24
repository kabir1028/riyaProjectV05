function createStartParticles() {
    const particles = document.getElementById('particles');
    if (!particles) return;
    
    for (let i = 0; i < 40; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.top = Math.random() * 100 + '%';
        particle.style.width = Math.random() * 4 + 2 + 'px';
        particle.style.height = particle.style.width;
        particle.style.animationDelay = Math.random() * 6 + 's';
        particle.style.animationDuration = (Math.random() * 3 + 3) + 's';
        particles.appendChild(particle);
    }
}

function showComingSoon() {
    Toast.info('Voice interview feature is under development. Try our comprehensive text-based interview for now!');
}

document.addEventListener('DOMContentLoaded', createStartParticles);

document.getElementById('interviewSetupForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const resume = document.getElementById('resume').files[0];
    const role = document.getElementById('role').value;
    const difficulty = document.getElementById('difficulty').value;
    
    if (!resume) {
        Toast.error('Please upload your resume to continue with the interview.');
        return;
    }
    
    if (!role || !difficulty) {
        Toast.warning('Please select both job role and experience level.');
        return;
    }
    
    const user = JSON.parse(localStorage.getItem('user') || 'null');
    const isLoggedIn = user && (user.access_token || user.isGuest);
    
    if (isLoggedIn) {
        startInterview(role, difficulty, resume.name);
    } else {
        showLoginGuestModal(role, difficulty, resume.name);
    }
});

function showLoginGuestModal(role, difficulty, resumeName) {
    const modal = document.createElement('div');
    modal.innerHTML = `
        <div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.7); z-index: 1000; display: flex; align-items: center; justify-content: center;">
            <div style="background: white; padding: 2rem; border-radius: 15px; text-align: center; max-width: 450px; margin: 1rem; box-shadow: 0 20px 40px rgba(0,0,0,0.3);">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🎯</div>
                <h3 style="margin-bottom: 1rem; color: #1a1a1a;">Choose Your Interview Experience</h3>
                <p style="color: #6b7280; margin-bottom: 2rem; line-height: 1.5;">Get the most out of your interview practice</p>
                
                <div style="display: flex; flex-direction: column; gap: 1rem; margin-bottom: 2rem;">
                    <div style="border: 2px solid #22c55e; border-radius: 10px; padding: 1.5rem; text-align: left;">
                        <h4 style="color: #22c55e; margin: 0 0 0.5rem 0; font-size: 1.1rem;">🔐 Login/Signup (Recommended)</h4>
                        <ul style="color: #4a5568; font-size: 0.9rem; margin: 0; padding-left: 1.2rem;">
                            <li>Save up to 5 interview results</li>
                            <li>Track your progress over time</li>
                            <li>Access detailed performance analytics</li>
                            <li>Resume from any device</li>
                        </ul>
                    </div>
                    
                    <div style="border: 2px solid #f59e0b; border-radius: 10px; padding: 1.5rem; text-align: left;">
                        <h4 style="color: #f59e0b; margin: 0 0 0.5rem 0; font-size: 1.1rem;">👤 Continue as Guest</h4>
                        <ul style="color: #4a5568; font-size: 0.9rem; margin: 0; padding-left: 1.2rem;">
                            <li>Single interview session only</li>
                            <li>Results lost on page refresh</li>
                            <li>No progress tracking</li>
                            <li>Limited features</li>
                        </ul>
                    </div>
                </div>
                
                <div style="display: flex; gap: 1rem; justify-content: center;">
                    <a href="/login" style="background: #22c55e; color: white; text-decoration: none; padding: 0.75rem 1.5rem; border-radius: 8px; font-weight: 600;">Login</a>
                    <a href="/signup" style="background: #3b82f6; color: white; text-decoration: none; padding: 0.75rem 1.5rem; border-radius: 8px; font-weight: 600;">Signup</a>
                    <button onclick="continueAsGuest('${role}', '${difficulty}', '${resumeName}')" style="background: #f59e0b; color: white; border: none; padding: 0.75rem 1.5rem; border-radius: 8px; cursor: pointer; font-weight: 600;">Guest</button>
                </div>
                
                <button onclick="closeModal(this)" style="position: absolute; top: 10px; right: 15px; background: none; border: none; font-size: 1.5rem; cursor: pointer; color: #6b7280;">×</button>
            </div>
        </div>
    `;
    document.body.appendChild(modal);
}

async function continueAsGuest(role, difficulty, resumeName) {
    const guestId = 'guest_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    
    try {
        await fetch('/api/create-guest', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: guestId })
        });
        
        localStorage.setItem('user', JSON.stringify({
            id: guestId,
            email: 'guest@temp.com',
            isGuest: true
        }));
        
        console.log('Created guest user:', guestId);
        startInterview(role, difficulty, resumeName);
        document.querySelector('[style*="position: fixed"]').remove();
    } catch (error) {
        console.error('Failed to create guest user:', error);
        Toast.error('Failed to create guest session');
    }
}

function closeModal(button) {
    button.closest('[style*="position: fixed"]').remove();
}

function startInterview(role, difficulty, resumeName) {
    Toast.success('Interview setup complete! Redirecting to questions...');
    
    sessionStorage.setItem('selectedRole', role);
    sessionStorage.setItem('selectedDifficulty', difficulty);
    sessionStorage.setItem('resumeName', resumeName);
    
    setTimeout(() => {
        window.location.href = '/interview';
    }, 1500);
}
