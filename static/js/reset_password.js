document.addEventListener('DOMContentLoaded', function() {
    const resetEmail = sessionStorage.getItem('resetEmail');
    
    if (!resetEmail) {
        Toast.error('Please verify OTP first.');
        setTimeout(() => {
            window.location.href = '/forgot-password';
        }, 3000);
        return;
    }
    
    window.resetEmail = resetEmail;
    
    document.getElementById('resetPasswordForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirmPassword').value;
        
        if (!password || !confirmPassword) {
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
        
        try {
            const response = await fetch('/api/auth/reset-password', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 
                    email: window.resetEmail,
                    password: password 
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                Toast.success(data.message);
                sessionStorage.removeItem('resetEmail');
                setTimeout(() => {
                    window.location.href = '/login';
                }, 2000);
            } else {
                Toast.error(data.message);
            }
            
        } catch (error) {
            Toast.error('Network error. Please try again.');
        }
    });
});
