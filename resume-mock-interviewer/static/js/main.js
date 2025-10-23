// Main JavaScript file for common functionality

// Smooth scrolling for anchor links
document.addEventListener('DOMContentLoaded', function() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

// Form validation helper
function validateForm(formId) {
    const form = document.getElementById(formId);
    const inputs = form.querySelectorAll('input[required], select[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.style.borderColor = '#dc3545';
            isValid = false;
        } else {
            input.style.borderColor = '#28a745';
        }
    });
    
    return isValid;
}

// Show loading spinner
function showLoading(element) {
    element.innerHTML = '<div style="text-align: center; padding: 2rem;">Loading...</div>';
}

// Show error message
function showError(element, message) {
    element.innerHTML = `<div style="color: #dc3545; text-align: center; padding: 2rem;">${message}</div>`;
}

// Check for OAuth success on page load
document.addEventListener('DOMContentLoaded', async function() {
    const urlParams = new URLSearchParams(window.location.search);
    
    if (urlParams.get('oauth_success') === 'true') {
        try {
            const response = await fetch('/api/auth/current-user');
            const data = await response.json();
            
            if (data.success && data.user) {
                localStorage.setItem('user', JSON.stringify(data.user));
                if (typeof Toast !== 'undefined') {
                    Toast.success('Login successful!');
                }
            }
        } catch (error) {
            console.error('Error fetching user:', error);
        }
        
        window.history.replaceState({}, document.title, window.location.pathname);
        
        if (typeof updateNavigation === 'function') {
            updateNavigation();
        }
    }
    
    if (urlParams.get('error') === 'oauth_failed') {
        if (typeof Toast !== 'undefined') {
            Toast.error('OAuth login failed. Please try again.');
        }
        window.history.replaceState({}, document.title, window.location.pathname);
    }
});

// Update navigation based on login status
function updateNavigation() {
    const user = Auth.getCurrentUser();
    const navMenu = document.querySelector('.nav-menu');
    
    if (user && user.email && navMenu) {
        const loginItem = navMenu.querySelector('a[href="/login"]');
        const signupBtn = navMenu.querySelector('a[href="/signup"]');
        
        if (loginItem) {
            loginItem.innerHTML = `
                <span class="nav-icon">👤</span>
                <span class="nav-text">Profile</span>
            `;
            loginItem.href = '/profile';
        }
        
        if (signupBtn) {
            signupBtn.textContent = 'Logout';
            signupBtn.href = '#';
            signupBtn.addEventListener('click', (e) => {
                e.preventDefault();
                Auth.logout();
            });
        }
    }
}