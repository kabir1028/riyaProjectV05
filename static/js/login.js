document.getElementById('loginForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    if (!email || !password) {
        Toast.warning('Please fill in all fields.');
        return;
    }
    
    await Auth.login(email, password);
});

document.getElementById('guestLoginBtn').addEventListener('click', async function() {
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
        console.error('Guest login error:', error);
        Toast.error('Failed to login as guest');
    }
});
