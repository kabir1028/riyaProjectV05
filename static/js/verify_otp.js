document.getElementById('verifyOtpForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const email = document.getElementById('email').value;
    const otp = document.getElementById('otp').value;
    
    if (!email || !otp) {
        Toast.warning('Please fill in all fields.');
        return;
    }
    
    if (otp.length !== 6) {
        Toast.error('OTP must be 6 digits.');
        return;
    }
    
    try {
        const response = await fetch('/api/auth/verify-otp', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, otp })
        });
        
        const data = await response.json();
        
        if (data.success) {
            Toast.success(data.message);
            sessionStorage.setItem('resetEmail', email);
            setTimeout(() => {
                window.location.href = '/reset-password';
            }, 1500);
        } else {
            Toast.error(data.message);
        }
        
    } catch (error) {
        Toast.error('Network error. Please try again.');
    }
});

document.getElementById('otp').addEventListener('input', function(e) {
    e.target.value = e.target.value.replace(/[^0-9]/g, '');
});
