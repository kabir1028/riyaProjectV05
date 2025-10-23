// Authentication JavaScript

class Auth {
    static async signup(email, password) {
        try {
            const response = await fetch('/api/auth/signup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            });
            
            const data = await response.json();
            
            if (data.success) {
                Toast.success(data.message);
                setTimeout(() => {
                    window.location.href = '/login';
                }, 2000);
            } else {
                Toast.error(data.message);
            }
            
            return data;
        } catch (error) {
            Toast.error('Network error. Please try again.');
            return { success: false, message: error.message };
        }
    }
    
    static async login(email, password) {
        try {
            const response = await fetch('/api/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            });
            
            const data = await response.json();
            
            if (data.success) {
                Toast.success(data.message);
                localStorage.setItem('user', JSON.stringify(data.user));
                setTimeout(() => {
                    window.location.href = '/';
                }, 1500);
            } else {
                Toast.error(data.message);
            }
            
            return data;
        } catch (error) {
            Toast.error('Network error. Please try again.');
            return { success: false, message: error.message };
        }
    }
    
    static async logout() {
        try {
            const response = await fetch('/api/auth/logout', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                localStorage.removeItem('user');
                Toast.success(data.message);
                setTimeout(() => {
                    window.location.href = '/';
                }, 1500);
            }
            
            return data;
        } catch (error) {
            Toast.error('Network error. Please try again.');
            return { success: false, message: error.message };
        }
    }
    
    static getCurrentUser() {
        try {
            const user = localStorage.getItem('user');
            return user ? JSON.parse(user) : null;
        } catch (error) {
            console.error('Error parsing user data:', error);
            localStorage.removeItem('user');
            return null;
        }
    }
    
    static isLoggedIn() {
        return this.getCurrentUser() !== null;
    }
}

// Update navigation based on auth state
document.addEventListener('DOMContentLoaded', function() {
    updateNavigation();
});

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
            signupBtn.addEventListener('click', (e) => {
                e.preventDefault();
                Auth.logout();
            });
        }
    }
}