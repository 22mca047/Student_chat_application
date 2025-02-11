document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('submitButton').addEventListener('click', submitData);
});
function submitData() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const url = 'http://127.0.0.1:2500/checklogin';
    const data = {
        'student_email': email,
        'student_password': password
    };

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
            localStorage.setItem('student_id', data['student_id'])
            localStorage.setItem('token', data['token'])
            window.location.href = "/home";
    })
    .catch(error =>{
        window.location.href = '/';
    })
}


