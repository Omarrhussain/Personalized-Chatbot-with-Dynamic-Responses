const chatForm = document.getElementById('chatForm');
const userInput = document.getElementById('userInput');
const chatContainer = document.getElementById('chatContainer');
const newChatBtn = document.getElementById('newChatBtn');

let isFirstMessage = true;

function scrollToBottom() {
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function removeWelcomeMessage() {
    const welcomeMsg = document.querySelector('.welcome-container');
    if (welcomeMsg) {
        welcomeMsg.style.opacity = '0';
        setTimeout(() => welcomeMsg.remove(), 300);
    }
}

function appendUserMessage(content) {
    if (isFirstMessage) {
        removeWelcomeMessage();
        isFirstMessage = false;
    }

    const wrapper = document.createElement('div');
    wrapper.className = 'message-wrapper user';
    
    wrapper.innerHTML = `
        <div class="message">
            <div class="message-content">
                <p>${content}</p>
            </div>
        </div>
    `;
    
    chatContainer.appendChild(wrapper);
    scrollToBottom();
}

function appendBotMessage(content, sources = 0) {
    const wrapper = document.createElement('div');
    wrapper.className = 'message-wrapper bot';
    
    let metaHTML = '';
    if (sources > 0) {
        metaHTML = `
            <div class="message-meta">
                <svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>
                Grounded on ${sources} source${sources > 1 ? 's' : ''}
            </div>
        `;
    }

    // Basic markdown parsing for bold text and newlines
    const formattedContent = content
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/\n/g, '<br>');

    wrapper.innerHTML = `
        <div class="message">
            <div class="avatar bot-avatar">✨</div>
            <div class="message-content">
                <p>${formattedContent}</p>
                ${metaHTML}
            </div>
        </div>
    `;
    
    chatContainer.appendChild(wrapper);
    scrollToBottom();
}

function showTyping() {
    const wrapper = document.createElement('div');
    wrapper.className = 'message-wrapper bot typing-indicator-wrapper';
    wrapper.id = 'typingIndicator';
    
    wrapper.innerHTML = `
        <div class="message">
            <div class="avatar bot-avatar">✨</div>
            <div class="message-content">
                <div class="typing-dots">
                    <div></div><div></div><div></div>
                </div>
            </div>
        </div>
    `;
    
    chatContainer.appendChild(wrapper);
    scrollToBottom();
}

function hideTyping() {
    const indicator = document.getElementById('typingIndicator');
    if (indicator) {
        indicator.remove();
    }
}

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const message = userInput.value.trim();
    if (!message) return;
    
    appendUserMessage(message);
    userInput.value = '';
    
    showTyping();
    
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message, use_history: true })
        });
        
        const data = await response.json();
        hideTyping();
        
        if (data.success) {
            appendBotMessage(data.answer, data.sources_count);
        } else {
            appendBotMessage(`Error: ${data.answer}`);
        }
    } catch (error) {
        hideTyping();
        appendBotMessage(`Connection Error: ${error.message}`);
    }
});

newChatBtn.addEventListener('click', async () => {
    try {
        await fetch('/conversation/clear', { method: 'DELETE' });
        chatContainer.innerHTML = `
            <div class="welcome-container">
                <div class="sparkle-icon">✨</div>
                <h1>Hello, I'm your AI</h1>
                <p>Powered by Advanced RAG & Multi-Agent Systems. How can I help you today?</p>
            </div>
        `;
        isFirstMessage = true;
    } catch (error) {
        console.error("Failed to clear history", error);
    }
});
