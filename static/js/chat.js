// Fan Chat Assistant Interaction

const BOT_RESPONSES = {
    'hello': "Hello! Welcome to the FIFA World Cup 2026 Stadium Helper. How can I assist you today? (Ask me about gates, parking, restrooms, or transit)",
    'gate': "Gate C currently has the shortest queue (under 2 minutes). We recommend arriving through Gate C if possible.",
    'restroom': "The nearest restrooms are located next to North Concourse (Gate A) and West Concourse (Gate C). Check the glowing signs!",
    'food': "North Food Court wait time is about 5 minutes. The West Food Court is currently empty and offers the fastest service!",
    'parking': "Parking Lot West has the most open spaces. Parking Lot East is currently at 94% capacity.",
    'metro': "The Metro Transit station is located north of Gate A. Trains arrive every 4 minutes. Just follow the blue neon pathway.",
    'emergency': "If you require urgent assistance, press the EMERGENCY HELP button on your screen or locate a volunteer immediately.",
    'lost': "Lost & Found is situated next to the guest relations desk near the VIP Entrance.",
    'default': "I can help you navigate the stadium! Ask me about: 'gate queues', 'metro transit', 'nearest restrooms', 'fastest food courts', or 'lost and found'."
};

function initChatAssistant() {
    const chatInput = document.getElementById('chat-input-text');
    const chatSend = document.getElementById('chat-send-btn');
    const msgContainer = document.getElementById('chat-messages');
    const voiceBtn = document.getElementById('chat-voice-btn');
    const speakBtn = document.getElementById('btn-speak-announcement');

    if (!chatInput || !chatSend || !msgContainer) return;

    // Send click
    chatSend.addEventListener('click', () => {
        handleUserMessage(chatInput, msgContainer);
    });

    // Enter key press
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleUserMessage(chatInput, msgContainer);
        }
    });

    // Voice Typing (Microphone Input)
    if (voiceBtn) {
        voiceBtn.addEventListener('click', () => {
            startVoiceRecognition(voiceBtn, chatInput);
        });
    }

    // Voice Read Aloud (Public Announcement Player)
    if (speakBtn) {
        speakBtn.addEventListener('click', () => {
            const announcementText = document.getElementById('gemini-announcement').textContent;
            speakText(announcementText, true); // Force speak ignoring mute setting
        });
    }

    // Narrator Toggle Button
    window.narratorMuted = false;
    const muteBtn = document.getElementById('btn-toggle-mute');
    if (muteBtn) {
        muteBtn.addEventListener('click', () => {
            window.narratorMuted = !window.narratorMuted;
            const icon = document.getElementById('mute-icon');
            const text = document.getElementById('mute-text');
            
            if (window.narratorMuted) {
                if ('speechSynthesis' in window) {
                    window.speechSynthesis.cancel();
                }
                muteBtn.classList.remove('btn-outline-info');
                muteBtn.classList.add('btn-outline-danger');
                icon.className = 'fa-solid fa-volume-xmark';
                text.textContent = 'Narrator OFF';
            } else {
                muteBtn.classList.remove('btn-outline-danger');
                muteBtn.classList.add('btn-outline-info');
                icon.className = 'fa-solid fa-volume-high';
                text.textContent = 'Narrator ON';
                speakText("Narrator active");
            }
        });
    }
}

function handleUserMessage(inputEl, msgContainer) {
    const text = inputEl.value.trim();
    if (!text) return;

    // 1. Render user bubble
    appendBubble(text, 'user', msgContainer);
    inputEl.value = '';

    // 2. Generate bot response (simulated processing lag)
    setTimeout(() => {
        const reply = findBestResponse(text);
        appendBubble(reply, 'bot', msgContainer);
    }, 450);
}

function findBestResponse(text) {
    const query = text.toLowerCase();
    
    if (query.includes('hello') || query.includes('hi')) return BOT_RESPONSES.hello;
    if (query.includes('gate') || query.includes('entrance') || query.includes('entry')) return BOT_RESPONSES.gate;
    if (query.includes('restroom') || query.includes('toilet') || query.includes('bathroom')) return BOT_RESPONSES.restroom;
    if (query.includes('food') || query.includes('eat') || query.includes('hot dog') || query.includes('drink')) return BOT_RESPONSES.food;
    if (query.includes('parking') || query.includes('car')) return BOT_RESPONSES.parking;
    if (query.includes('metro') || query.includes('train') || query.includes('bus') || query.includes('transport')) return BOT_RESPONSES.metro;
    if (query.includes('lost') || query.includes('phone') || query.includes('found')) return BOT_RESPONSES.lost;
    if (query.includes('emergency') || query.includes('police') || query.includes('hurt')) return BOT_RESPONSES.emergency;
    
    return BOT_RESPONSES.default;
}

function appendBubble(text, sender, container) {
    const bubble = document.createElement('div');
    bubble.className = `chat-bubble ${sender}`;
    bubble.textContent = text;
    container.appendChild(bubble);
    
    // Auto scroll bottom
    container.scrollTop = container.scrollHeight;
}

// Speech Recognition (Voice Typing)
function startVoiceRecognition(voiceBtn, chatInput) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
        alert("Speech Recognition is not supported in this browser. Please use Google Chrome or MS Edge.");
        return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onstart = () => {
        voiceBtn.classList.remove('btn-outline-info');
        voiceBtn.classList.add('btn-danger');
        voiceBtn.innerHTML = '<i class="fa-solid fa-microphone-slash"></i>';
        chatInput.placeholder = "Listening...";
    };

    recognition.onend = () => {
        voiceBtn.classList.remove('btn-danger');
        voiceBtn.classList.add('btn-outline-info');
        voiceBtn.innerHTML = '<i class="fa-solid fa-microphone"></i>';
        chatInput.placeholder = "Type or speak question...";
    };

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        chatInput.value = transcript;
        setTimeout(() => {
            document.getElementById('chat-send-btn').click();
        }, 300);
    };

    recognition.onerror = (e) => {
        console.error("Speech Recognition Error", e.error);
    };

    recognition.start();
}

// Speech Synthesis (Text-to-Speech Player)
function speakText(text, force = false) {
    if (window.narratorMuted && !force) return;
    
    if ('speechSynthesis' in window) {
        // Cancel existing plays
        window.speechSynthesis.cancel();
        
        const utterance = new SpeechSynthesisUtterance(text.trim());
        
        // Auto-select lang
        if (text.includes("ATENCIÓN") || text.includes("AVISO") || text.includes("español")) {
            utterance.lang = 'es-ES';
        } else {
            utterance.lang = 'en-US';
        }
        
        utterance.rate = 1.05;
        window.speechSynthesis.speak(utterance);
    } else {
        alert("Text-to-Speech is not supported in this browser.");
    }
}

// Hook
window.initChatAssistant = initChatAssistant;
window.speakText = speakText;
