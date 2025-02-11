var friend_i = document.getElementById("friend_id").value;
var student_id = localStorage.getItem('student_id')
var token = localStorage.getItem("token");

var socket = io.connect('http://127.0.0.1:2500/chat', {
    query: {
        "friend_id": friend_i,
        "student_id": student_id
    },
    secure: true,
    transport: ['websocket', 'polling'],
    reconnection: true,
    heartbeatTimeout: 300000
});

socket.on('connect', function () {
    sessionStorage.setItem('socket_id', socket.id);
    console.log('Connected to Socket.IO server');
    var socketId = sessionStorage.getItem('socket_id');
    socket.emit('handlesocket', { socket_id: socketId, 'friend_id': friend_i, 'student_id':student_id });
});

function sendButton() {
    var msg = document.getElementById('msg').value;
    var friend_id = document.getElementById("friend_id").value;
    console.log(friend_id)
    socket_id = sessionStorage.getItem('socket_id')
    socket.emit('message', { 'friend_id': friend_id, 'msg': msg, 'socket_id':socket_id, 'student_id':student_id });
    document.getElementById('msg').value = '';
}

socket.on('message', function (data) {
    console.log("Received Message:", data);
    if (student_id === data.student_id) {
        $('#log').append(`
            <div class="d-flex flex-row justify-content-end">
                <div>
                    <p class="small p-2 me-3 mb-1 text-white rounded-3 bg-primary">${data.msg}</p>
                    <p class="small me-3 mb-3 rounded-3 text-muted">${data.time}</p>
                </div>
                <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava1-bg.webp"
                    alt="avatar 1" style="width: 45px; height: 100%;">
            </div>`);
    } else {
        $('#log').append(`
            <div class="d-flex flex-row justify-content-start">
                <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava6-bg.webp"
                    alt="avatar 3" style="width: 40px; height: 100%;">
                <div>
                    <p class="small p-2 ms-3 mb-1 rounded-3 bg-body-tertiary">${data.msg}</p>
                    <p class="small ms-3 mb-3 rounded-3 text-muted float-end">${data.time}</p>
                </div>
            </div>`);
    }
});

socket.on('history', function (response) {
    console.log(response);

    if (response && Array.isArray(response.response)) {
        const data = response.response;

        for (let i = 0; i < data.length; i++) {
            const item = data[i];
            const time = item.Time || item.time;

            if (item.sender_id === student_id) {
                $('#log').append(`
                    <div class="d-flex flex-row justify-content-end">
                        <div>
                            <p class="small p-2 me-3 mb-1 text-white rounded-3 bg-primary">${item.msg}</p>
                            <p class="small me-3 mb-3 rounded-3 text-muted">${time}</p>
                        </div>
                        <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava1-bg.webp"
                            alt="avatar 1" style="width: 45px; height: 100%;">
                    </div>`);
            } else {
                $('#log').append(`
                    <div class="d-flex flex-row justify-content-start">
                        <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava6-bg.webp"
                            alt="avatar 3" style="width: 40px; height: 100%;">
                        <div>
                            <p class="small p-2 ms-3 mb-1 rounded-3 bg-body-tertiary">${item.msg}</p>
                            <p class="small ms-3 mb-3 rounded-3 text-muted float-end">${time}</p>
                        </div>
                    </div>`);
            }
        }
    } else {
        console.error('Expected response to be an object with a response array:', response);
    }
});


function fetchData(){
    fetch('http://127.0.0.1:2500/fsData',{
        method : 'POST',
        headers : {
            'content-type': 'application/json',
            'Authorization' : `Bearer ${token}`
        },
        body: JSON.stringify({
            'student_id': student_id,
            'friend_id' : friend_i
        })
    })
    .then(response => {
        if(!response.ok){
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log("data :", data)
        $('#f_name').append(`<h3 style="padding-left: 10px;">${data.friend_detail.student_name}</h3>`)
    })
    .catch(error => {
        window.location.href='/';
    })
}
$(document).ready(fetchData);

