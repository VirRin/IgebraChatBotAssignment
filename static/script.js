document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');

    // Auto-resize textarea
    function autoResize() {
        this.style.height = 'auto';
        this.style.height = `${this.scrollHeight}px`;
    }
    userInput.addEventListener('input', autoResize);

    // Add message to chat
    function addMessage(content, type) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', `${type}-message`);
        
        if (type === 'bot') {
            // Create typing indicator
            messageElement.innerHTML = '<span class="typing-indicator">•••</span>';
            chatMessages.appendChild(messageElement);
            
            // Simulate typing effect
            let typedContent = '';
            let i = 0;
            const typingInterval = setInterval(() => {
                if (i < content.length) {
                    typedContent += content.charAt(i);
                    messageElement.innerHTML = typedContent;
                    i++;
                    chatMessages.scrollTop = chatMessages.scrollHeight;
                } else {
                    clearInterval(typingInterval);
                }
            }, 20);
        } else {
            messageElement.textContent = content;
            chatMessages.appendChild(messageElement);
        }

        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Send message to backend
    async function sendMessage() {
        const query = userInput.value.trim();
        if (!query) return;

        addMessage(query, 'user');
        userInput.value = '';
        userInput.style.height = 'auto';

        try {
            const response = await fetch('/api/chat', {  // Changed to '/api/chat'
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            if (data.error) {
                addMessage(`Error: ${data.error}`, 'bot');
            } else {
                addMessage(data.response, 'bot');
            }
        } catch (error) {
            console.error('Error:', error);
            addMessage(`Sorry, I couldn't process your request. Please try again.`, 'bot');
        }
    }

    // Event listeners
    sendBtn.addEventListener('click', sendMessage);
    
    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
});