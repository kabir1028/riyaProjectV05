document.addEventListener('DOMContentLoaded', function() {
    const user = Auth.getCurrentUser();
    if (!user) {
        window.location.href = '/login';
        return;
    }

    document.getElementById('displayEmail').textContent = user.email;
    document.getElementById('displayName').textContent = user.email.split('@')[0];
    document.getElementById('memberSince').textContent = 'Jan 2025';

    loadProfileData(user.id);

    document.getElementById('profileForm').addEventListener('submit', function(e) {
        e.preventDefault();
        saveProfile();
    });

    updateProfileCompletion();
});

async function loadProfileData(userId) {
    try {
        const historyResponse = await fetch(`/api/profile/history?user_id=${userId}`);
        const historyData = await historyResponse.json();
        if (historyData.success) {
            document.getElementById('totalInterviews').textContent = historyData.total_interviews;
        }
        
        const profileResponse = await fetch('/api/auth/profile');
        const profileData = await profileResponse.json();
        if (profileData.success && profileData.profile) {
            const profile = profileData.profile;
            document.getElementById('fullName').value = profile.name || '';
            document.getElementById('phone').value = profile.phone || '';
            document.getElementById('currentRole').value = profile.user_role || '';
            document.getElementById('experience').value = profile.experience || '';
            document.getElementById('location').value = profile.location || '';
            document.getElementById('bio').value = profile.bio || '';
            
            if (profile.name) {
                document.getElementById('displayName').textContent = profile.name;
            }
            
            updateProfileCompletion();
        }
    } catch (error) {
        console.error('Error loading profile:', error);
    }
}

function updateProfileCompletion() {
    const fields = ['fullName', 'phone', 'currentRole', 'experience', 'location', 'bio'];
    const filled = fields.filter(id => document.getElementById(id).value.trim()).length;
    const percentage = Math.round((filled / fields.length) * 100);
    
    document.getElementById('profileCompletion').textContent = percentage + '% Complete';
    document.getElementById('profileProgress').style.width = percentage + '%';
}

document.querySelectorAll('#profileForm input, #profileForm select, #profileForm textarea').forEach(el => {
    el.addEventListener('input', updateProfileCompletion);
});

async function saveProfile() {
    try {
        const profileData = {
            name: document.getElementById('fullName').value.trim(),
            phone: document.getElementById('phone').value.trim(),
            user_role: document.getElementById('currentRole').value.trim(),
            experience: document.getElementById('experience').value,
            location: document.getElementById('location').value.trim(),
            bio: document.getElementById('bio').value.trim()
        };
        
        const response = await fetch('/api/auth/profile', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(profileData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            Toast.success('Profile updated successfully!');
            if (profileData.name) {
                document.getElementById('displayName').textContent = profileData.name;
            }
        } else {
            Toast.error(data.message || 'Failed to update profile');
        }
    } catch (error) {
        console.error('Error saving profile:', error);
        Toast.error('Failed to update profile');
    }
}

function addSkill() {
    const skillsList = document.getElementById('skillsList');
    const currentSkills = skillsList.querySelectorAll('.skill-tag');
    
    if (currentSkills.length >= 5) {
        Toast.warning('Maximum 5 skills allowed');
        return;
    }
    
    const skill = prompt('Enter skill name:');
    if (skill && skill.trim()) {
        const tag = document.createElement('span');
        tag.className = 'skill-tag';
        tag.style.cssText = 'position: relative; padding-right: 2rem;';
        tag.innerHTML = `
            ${skill.trim()}
            <button onclick="removeSkill(this)" style="position: absolute; right: 0.5rem; top: 50%; transform: translateY(-50%); background: rgba(239, 68, 68, 0.1); color: #ef4444; border: none; width: 20px; height: 20px; border-radius: 50%; cursor: pointer; font-size: 0.75rem; display: flex; align-items: center; justify-content: center;">×</button>
        `;
        skillsList.insertBefore(tag, skillsList.lastElementChild);
    }
}

function removeSkill(btn) {
    btn.parentElement.remove();
}

function changePassword() {
    window.location.href = '/forgot-password';
}
