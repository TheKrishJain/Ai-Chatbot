document.getElementById('chatbot-button').addEventListener('click', () => {
    const overlay = document.getElementById('chatbot-overlay');
    overlay.style.display = overlay.style.display === 'none' || overlay.style.display === '' ? 'flex' : 'none';
});

document.getElementById('send-button').addEventListener('click', () => {
    sendMessage();
});

document.getElementById('chat-input').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

function sendMessage() {
    const input = document.getElementById('chat-input').value;
    if (!input.trim()) return;

    const chatLog = document.getElementById('chat-log');
    chatLog.innerHTML += `<p>You: ${input}</p>`;
    document.getElementById('chat-input').value = '';

    fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: input })
    })
    .then(response => response.json())
    .then(data => {
        chatLog.innerHTML += `<p>Bot: ${data.reply}</p>`;
        chatLog.scrollTop = chatLog.scrollHeight; // Scroll to the bottom
    });
}

document.addEventListener('click', (e) => {
    if (overlay.style.display === 'flex') {
        overlay.style.display = 'none';
    }
});