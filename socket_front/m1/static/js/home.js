function fetchData() {
    const apiUrl = 'http://127.0.0.1:2500/getall';
    const token = localStorage.getItem('token');
    const student_id = localStorage.getItem('student_id');
    const requestPayload = {
        student_id: student_id
    };

    fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(requestPayload)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('Data:', data);
        console.log('Student ID:', student_id);

        const students = data.student_data;
        const teachers = data.teacher_data;

        $('#student').empty();
        $('#teacher').empty();

        students.forEach(student => {
            $('#student').append(`
                <li class="student-list-item p-2 border-bottom">
                    <a href="http://127.0.0.1:1001/chat/${student.student_id}" class="d-flex justify-content-between">
                        <div class="d-flex flex-row">
                            <div>
                                <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava6-bg.webp"
                                alt="avatar" class="d-flex align-self-center me-3" width="60">
                                <span class="badge bg-success badge-dot"></span>
                            </div>
                            <div class="pt-1">
                                <p class="fw-bold mb-0">${student.student_name}</p>
                                <p class="small text-muted">Email: ${student.student_email}</p>
                            </div>
                        </div>
                        <div class="pt-1">
                            <p class="small text-muted mb-1">Just now</p>
                            <span class="badge bg-danger rounded-pill float-end">STD: ${student.student_std}</span>
                        </div>
                    </a>
                </li>`);
        });

        teachers.forEach(teacher => {
            $('#teacher').append(`
                <li class="p-2 border-bottom">
                    <a href="#!" class="d-flex justify-content-between">
                        <div class="d-flex flex-row">
                            <div>
                                <img
                                    src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava1-bg.webp"
                                    alt="avatar" class="d-flex align-self-center me-3" width="60">
                                <span class="badge bg-success badge-dot"></span>
                            </div>
                            <div class="pt-1">
                                <p class="fw-bold mb-0">${teacher.teacher_name}</p>
                                <p class="small text-muted">Hello, Are you there?</p>
                            </div>
                        </div>
                        <div class="pt-1">
                            <p class="small text-muted mb-1">SUB: ${teacher.teacher_subject}</p>
                            <span class="badge bg-danger rounded-pill float-end">STD: ${teacher.teacher_class}</span>
                        </div>
                    </a>
                </li>`);
        });
    })
    .catch(error => {
        window.location.href = '/';
    });
}

function displayError(message) {
    const container = document.getElementById('response-container');
    container.innerHTML = `<p style="color: red;">Error: ${message}</p>`;
}

$(document).ready(fetchData);


