// Forgot Password form event listener
if(document.getElementById('forgotPasswordForm')) {
    document.getElementById('forgotPasswordForm').addEventListener('submit', function(e) {
        e.preventDefault();
        const email = document.getElementById('email').value;
        const csrf_token = document.querySelector('[name="csrf_token"]').value;

        if (email) {
            fetch('/forgot_password', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    email: email,
                    csrf_token: csrf_token
                })
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
            })
            .catch(error => console.error(error));
        } else {
            document.getElementById('errorMessage').textContent = "אנא הכנס אימייל תקין.";
        }
    });
}

// Reset Password form event listener
if(document.getElementById('resetPasswordForm')) {
    document.getElementById('resetPasswordForm').addEventListener('submit', function(e) {
        e.preventDefault();
        const new_password = document.querySelector('[name="new_password"]').value;
        const token = document.querySelector('[name="token"]').value;
        const csrf_token = document.querySelector('[name="csrf_token"]').value;
        
        if (new_password) {
            fetch('/forgot_password?token=' + token, {  // token sent as query param for clarity
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    new_password: new_password,
                    token: token,
                    csrf_token: csrf_token
                })
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
            })
            .catch(error => console.error(error));
        } else {
            document.getElementById('errorMessage').textContent = "אנא הכנס סיסמה חדשה.";
        }
    });
}
