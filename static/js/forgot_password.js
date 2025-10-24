document.getElementById('forgotPasswordForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const email = document.getElementById('email').value;
    
    if (!email) {
        Toast.warning('Please enter your email address.');
        return;
    }
    
    try {
        const response = await fetch('/api/auth/forgot-password', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email })
        });
        
        const data = await response.json();
        
        if (data.success) {
            Toast.success(data.message);
            sessionStorage.setItem('resetEmail', email);
            setTimeout(() => {
                window.location.href = '/verify-otp';
            }, 2000);
        } else {
            Toast.error(data.message);
        }
        
    } catch (error) {
        Toast.error('Network error. Please try again.');
    }
});

document.getElementById('resendVerificationBtn').addEventListener('click', function() {
    document.getElementById('resendEmailModal').style.display = 'flex';
});

document.getElementById('cancelResend').addEventListener('click', function() {
    document.getElementById('resendEmailModal').style.display = 'none';
});

document.getElementById('resendVerificationForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const email = document.getElementById('resendEmail').value;
    
    if (!email) {
        Toast.warning('Please enter your email address.');
        return;
    }
    
    try {
        const response = await fetch('/api/auth/resend-verification', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email })
        });
        
        const data = await response.json();
        
        if (data.success) {
            Toast.success(data.message);
            document.getElementById('resendEmailModal').style.display = 'none';
            document.getElementById('resendEmail').value = '';
        } else {
            Toast.error(data.message);
        }
        
    } catch (error) {
        Toast.error('Network error. Please try again.');
    }
});
