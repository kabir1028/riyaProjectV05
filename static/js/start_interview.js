if (typeof Toast === 'undefined') {
    window.Toast = {
        success: (msg) => alert('✓ ' + msg),
        error: (msg) => alert('✗ ' + msg),
        warning: (msg) => alert('⚠ ' + msg),
        info: (msg) => alert('ℹ ' + msg)
    };
}

let uploadedFile = null;

const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('resumeFile');
const resumePreview = document.getElementById('resumePreview');
const startBtn = document.getElementById('startWrittenBtn');

uploadArea.addEventListener('click', () => fileInput.click());

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    const file = e.dataTransfer.files[0];
    handleFile(file);
});

fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    handleFile(file);
});

function handleFile(file) {
    if (!file) return;
    
    const validTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    if (!validTypes.includes(file.type)) {
        if (typeof Toast !== 'undefined') {
            Toast.error('Please upload PDF, DOC, or DOCX file only');
        } else {
            alert('✗ Please upload PDF, DOC, or DOCX file only');
        }
        return;
    }
    
    if (file.size > 102400) {
        if (typeof Toast !== 'undefined') {
            Toast.error('File size must be under 100KB');
        } else {
            alert('✗ File size must be under 100KB');
        }
        return;
    }
    
    uploadedFile = file;
    
    document.getElementById('fileName').textContent = file.name;
    document.getElementById('fileSize').textContent = (file.size / 1024).toFixed(2) + ' KB';
    resumePreview.classList.add('active');
    uploadArea.style.display = 'none';
    document.getElementById('resumeViewer').style.display = 'none';
    
    startBtn.disabled = false;
    document.getElementById('startVoiceBtn').disabled = false;
    
    if (typeof Toast !== 'undefined') {
        Toast.success('Resume uploaded successfully!');
    } else {
        alert('✓ Resume uploaded successfully!');
    }
}

document.getElementById('removeFile').addEventListener('click', () => {
    uploadedFile = null;
    fileInput.value = '';
    resumePreview.classList.remove('active');
    uploadArea.style.display = 'block';
    startBtn.disabled = true;
    document.getElementById('resumeViewer').style.display = 'none';
});

document.getElementById('viewResume').addEventListener('click', () => {
    const viewer = document.getElementById('resumeViewer');
    const viewerContent = document.getElementById('viewerContent');
    
    if (viewer.style.display === 'none') {
        viewer.style.display = 'block';
        
        const fileURL = URL.createObjectURL(uploadedFile);
        
        if (uploadedFile.type === 'application/pdf') {
            viewerContent.innerHTML = `<embed src="${fileURL}" type="application/pdf" />`;
        } else {
            viewerContent.innerHTML = `
                <div style="text-align: center; padding: 2rem; color: #6b7280;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">📄</div>
                    <p><strong>${uploadedFile.name}</strong></p>
                    <p style="font-size: 0.9rem; margin-top: 0.5rem;">Preview available for PDF files only</p>
                    <p style="font-size: 0.85rem; color: #9ca3af;">DOC/DOCX files will be processed during interview</p>
                </div>
            `;
        }
    } else {
        viewer.style.display = 'none';
    }
});

document.getElementById('closeViewer').addEventListener('click', () => {
    document.getElementById('resumeViewer').style.display = 'none';
});

document.getElementById('writtenInterviewForm').addEventListener('submit', (e) => {
    e.preventDefault();
    
    if (!uploadedFile) {
        if (typeof Toast !== 'undefined') {
            Toast.error('Please upload your resume first');
        } else {
            alert('✗ Please upload your resume first');
        }
        return;
    }
    
    const jobRole = document.getElementById('jobRole').value;
    const experienceLevel = document.getElementById('experienceLevel').value;
    
    if (!jobRole || !experienceLevel) {
        if (typeof Toast !== 'undefined') {
            Toast.warning('Please select job role and experience level');
        } else {
            alert('⚠ Please select job role and experience level');
        }
        return;
    }
    
    const user = JSON.parse(localStorage.getItem('user') || 'null');
    const isLoggedIn = user && (user.id || user.isGuest);
    
    if (!isLoggedIn) {
        showLoginModal('written', jobRole, experienceLevel);
        return;
    }
    
    sessionStorage.setItem('selectedRole', jobRole);
    sessionStorage.setItem('selectedDifficulty', experienceLevel);
    sessionStorage.setItem('resumeName', uploadedFile.name);
    
    if (typeof Toast !== 'undefined') {
        Toast.success('Starting interview...');
    }
    
    setTimeout(() => {
        window.location.href = '/interview';
    }, 1000);
});

document.getElementById('voiceInterviewForm').addEventListener('submit', (e) => {
    e.preventDefault();
    
    if (!uploadedFile) {
        if (typeof Toast !== 'undefined') {
            Toast.error('Please upload your resume first');
        } else {
            alert('✗ Please upload your resume first');
        }
        return;
    }
    
    const jobRole = document.getElementById('voiceJobRole').value;
    const experienceLevel = document.getElementById('voiceExperienceLevel').value;
    
    if (!jobRole || !experienceLevel) {
        if (typeof Toast !== 'undefined') {
            Toast.warning('Please select job role and experience level');
        } else {
            alert('⚠ Please select job role and experience level');
        }
        return;
    }
    
    const user = JSON.parse(localStorage.getItem('user') || 'null');
    const isLoggedIn = user && (user.id || user.isGuest);
    
    if (!isLoggedIn) {
        showLoginModal('voice', jobRole, experienceLevel);
        return;
    }
    
    sessionStorage.setItem('selectedRole', jobRole);
    sessionStorage.setItem('selectedDifficulty', experienceLevel);
    sessionStorage.setItem('resumeName', uploadedFile.name);
    
    if (typeof Toast !== 'undefined') {
        Toast.success('Starting voice interview...');
    }
    
    setTimeout(() => {
        window.location.href = '/voice-interview';
    }, 1000);
});

document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const tab = btn.dataset.tab;
        
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        document.getElementById(tab + 'Tab').classList.add('active');
    });
});

function showLoginModal(type, role, level) {
    const modal = document.createElement('div');
    modal.id = 'loginModal';
    modal.innerHTML = `
        <div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.7); z-index: 10000; display: flex; align-items: center; justify-content: center; animation: fadeIn 0.3s;">
            <div style="background: white; padding: 2.5rem; border-radius: 20px; max-width: 480px; width: 90%; box-shadow: 0 20px 60px rgba(0,0,0,0.3); position: relative; animation: slideUp 0.3s;">
                <button onclick="closeLoginModal()" style="position: absolute; top: 1rem; right: 1rem; background: none; border: none; font-size: 1.8rem; cursor: pointer; color: #6b7280; line-height: 1;">&times;</button>
                
                <div style="text-align: center; margin-bottom: 2rem;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">🎯</div>
                    <h2 style="font-size: 1.8rem; color: #1a1a1a; margin-bottom: 0.5rem;">Ready to Start?</h2>
                    <p style="color: #6b7280; font-size: 0.95rem;">Login or continue as guest to begin your interview</p>
                </div>
                
                <div style="display: flex; flex-direction: column; gap: 1rem;">
                    <a href="/login" style="display: flex; align-items: center; justify-content: center; gap: 0.75rem; padding: 1rem; background: linear-gradient(135deg, #22c55e, #16a34a); color: white; text-decoration: none; border-radius: 12px; font-weight: 600; transition: transform 0.2s;" onmouseover="this.style.transform='translateY(-2px)'" onmouseout="this.style.transform='translateY(0)'">
                        <span style="font-size: 1.2rem;">📧</span>
                        <span>Login with Email</span>
                    </a>
                    
                    <a href="/api/auth/google" style="display: flex; align-items: center; justify-content: center; gap: 0.75rem; padding: 1rem; background: white; color: #1a1a1a; text-decoration: none; border-radius: 12px; font-weight: 600; border: 2px solid #e5e7eb; transition: all 0.2s;" onmouseover="this.style.borderColor='#22c55e'; this.style.transform='translateY(-2px)'" onmouseout="this.style.borderColor='#e5e7eb'; this.style.transform='translateY(0)'">
                        <span style="font-size: 1.2rem;">🔵</span>
                        <span>Continue with Google</span>
                    </a>
                    
                    <a href="/api/auth/github" style="display: flex; align-items: center; justify-content: center; gap: 0.75rem; padding: 1rem; background: #24292e; color: white; text-decoration: none; border-radius: 12px; font-weight: 600; transition: transform 0.2s;" onmouseover="this.style.transform='translateY(-2px)'" onmouseout="this.style.transform='translateY(0)'">
                        <span style="font-size: 1.2rem;">⚫</span>
                        <span>Continue with GitHub</span>
                    </a>
                    
                    <button onclick="continueAsGuest('${type}', '${role}', '${level}')" style="display: flex; align-items: center; justify-content: center; gap: 0.75rem; padding: 1rem; background: #f59e0b; color: white; border: none; border-radius: 12px; font-weight: 600; cursor: pointer; transition: transform 0.2s;" onmouseover="this.style.transform='translateY(-2px)'" onmouseout="this.style.transform='translateY(0)'">
                        <span style="font-size: 1.2rem;">👤</span>
                        <span>Continue as Guest</span>
                    </button>
                </div>
                
                <div style="text-align: center; margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px solid #e5e7eb;">
                    <p style="color: #6b7280; font-size: 0.85rem; margin-bottom: 0.75rem;">Don't have an account?</p>
                    <a href="/signup" style="color: #22c55e; font-weight: 600; text-decoration: none; font-size: 0.95rem;">Sign up for free →</a>
                </div>
            </div>
        </div>
    `;
    document.body.appendChild(modal);
}

function closeLoginModal() {
    const modal = document.getElementById('loginModal');
    if (modal) {
        modal.remove();
    }
}

async function continueAsGuest(type, role, level) {
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
        
        sessionStorage.setItem('selectedRole', role);
        sessionStorage.setItem('selectedDifficulty', level);
        sessionStorage.setItem('resumeName', uploadedFile.name);
        
        closeLoginModal();
        
        if (typeof Toast !== 'undefined') {
            Toast.success('Starting interview as guest...');
        }
        
        setTimeout(() => {
            window.location.href = type === 'voice' ? '/voice-interview' : '/interview';
        }, 1000);
    } catch (error) {
        console.error('Guest creation error:', error);
        if (typeof Toast !== 'undefined') {
            Toast.error('Failed to create guest session');
        }
    }
}

function showComingSoon() {
    if (typeof Toast !== 'undefined') {
        Toast.info('Feature coming soon!');
    } else {
        alert('ℹ Feature coming soon!');
    }
}
