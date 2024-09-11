function openChatbot() {
    const chatbotWindow = window.open('/chatbot', 'Chatbot', 'width=400,height=600');
    chatbotWindow.focus();
}

function sendText() {
    const userInput = document.getElementById('chatInput').value;
    fetch('/chatbot', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `user_input=${userInput}`,
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('chatOutput').innerText = data.response;
    });
}

function startVoiceRecognition() {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.onstart = function () {
        console.log('Voice recognition started. Speak now.');
    };
    recognition.onspeechend = function () {
        recognition.stop();
    };
    recognition.onresult = function (event) {
        const userInput = event.results[0][0].transcript;
        document.getElementById('chatInput').value = userInput;
        sendText();
    };
    recognition.start();
}
    