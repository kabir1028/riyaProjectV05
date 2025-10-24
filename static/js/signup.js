document.getElementById('signupForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    
    if (!email || !password || !confirmPassword) {
        Toast.warning('Please fill in all fields.');
        return;
    }
    
    if (password !== confirmPassword) {
        Toast.error('Passwords do not match.');
        return;
    }
    
    if (password.length < 6) {
        Toast.error('Password must be at least 6 characters long.');
        return;
    }
    
    await Auth.signup(email, password);
});

document.getElementById('guestSignupBtn').addEventListener('click', async function() {
    try {
        const guestId = 'guest_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        
        const response = await fetch('/api/create-guest', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: guestId })
        });
        
        if (response.ok) {
            localStorage.setItem('user', JSON.stringify({
                id: guestId,
                email: 'guest@temp.com',
                isGuest: true
            }));
            
            Toast.success('Logged in as guest');
            setTimeout(() => {
                window.location.href = '/start-interview';
            }, 1000);
        } else {
            Toast.error('Failed to create guest session');
        }
    } catch (error) {
        console.error('Guest signup error:', error);
        Toast.error('Failed to continue as guest');
    }
});
