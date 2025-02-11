// Function to check if a token is present in localStorage
function checkToken() {
    const token = localStorage.getItem('token');
    if (!token) {
        window.location.href = '/';
    }
}

function sendButton() {
    const msg = document.getElementById("msg").value;
    if (!msg.trim()) {
        return;
    }

    const url = "http://127.0.0.1:2500/bot";
    const data = {
        'msg': msg
    };

    updateChatLog(msg, '');

    showTypingIndicator(true);

    fetch(url, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP Error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(respo => {
        setTimeout(() => {
            showTypingIndicator(false);
            updateChatLog('', respo.response);
            document.getElementById('msg').value = '';
        }, 1000);
    })
    .catch(error => {
        console.error('Error:', error);
        window.location.href = '/';
    });
}

function updateChatLog(userMessage, botResponse) {
    const log = document.getElementById('log');

    if (userMessage) {
        const userMessageHTML = `
            <div class="d-flex flex-row justify-content-end mb-4 pt-1">
                <div>
                    <p class="small p-2 me-3 mb-1 text-white rounded-3 bg-primary">${userMessage}</p>
                </div>
                <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava3-bg.webp" alt="avatar 1" style="width: 45px; height: 100%;">
            </div>
        `;
        log.insertAdjacentHTML('beforeend', userMessageHTML);
    }

    if (botResponse) {
        const botResponseHTML = `
            <div class="d-flex flex-row justify-content-start mb-4">
                <img src="https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava3-bg.webp" alt="avatar 1" style="width: 45px; height: 100%;">
                <div>
                    <p class="small p-2 ms-3 mb-1 rounded-3 bg-body-tertiary">${botResponse}</p>
                </div>
            </div>
        `;
        log.insertAdjacentHTML('beforeend', botResponseHTML);
    }

    log.scrollTop = log.scrollHeight;
}

function showTypingIndicator(isTyping) {
    const typingIndicator = document.getElementById('typingIndicator');
    typingIndicator.style.display = isTyping ? 'block' : 'none';
}

document.getElementById('sendButton').addEventListener('click', sendButton);

window.onload = checkToken;
