const urlParams = new URLSearchParams(window.location.search);
const token = urlParams.get('token');

async function verifyEmail() {
    const btn = document.querySelector('.verify-btn');
    const spinner = document.getElementById('spinner');
    const resultMsg = document.getElementById('result-message');

    btn.disabled = true;
    btn.style.display = 'none';
    spinner.style.display = 'block';

    try {
        const response = await fetch('/api/auth/verify-email', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ token })
        });

        const data = await response.json();

        if (data.success) {
            resultMsg.innerHTML = '<span style="color: #22c55e;">✅ ' + data.message + '</span>';
            
            if (data.user) {
                localStorage.setItem('user', JSON.stringify(data.user));
            }

            setTimeout(() => {
                window.location.href = '/start-interview';
            }, 2000);
        } else {
            resultMsg.innerHTML = '<span style="color: #ef4444;">❌ ' + data.message + '</span>';
            btn.style.display = 'inline-block';
            btn.disabled = false;
        }
    } catch (error) {
        resultMsg.innerHTML = '<span style="color: #ef4444;">❌ Verification failed. Please try again.</span>';
        btn.style.display = 'inline-block';
        btn.disabled = false;
    } finally {
        spinner.style.display = 'none';
    }
}
