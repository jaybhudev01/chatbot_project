        let sessionId = "";
        let userName = "";
        const BASE_URL = window.location.protocol === 'file:' ? 'http://127.0.0.1:8000' : '';
        
        // Element references
        const onboardingModal = document.getElementById('onboardingModal');
        const chatInput = document.getElementById('chatInput');
        const btnSend = document.getElementById('btnSend');
        const btnEndChat = document.getElementById('btnEndChat');
        const inputPanel = document.getElementById('inputPanel');
        const suggestionsContainer = document.getElementById('suggestionsContainer');
        const messageArea = document.getElementById('messageArea');
        const sidebar = document.getElementById('sidebar');
        const sidebarToggle = document.getElementById('sidebarToggle');
        
        // Toggle Sidebar on mobile
        sidebarToggle.addEventListener('click', () => {
            sidebar.classList.toggle('active');
        });
        
        // Close sidebar if clicking outside on mobile
        document.addEventListener('click', (e) => {
            if (window.innerWidth <= 768) {
                if (!sidebar.contains(e.target) && e.target !== sidebarToggle && !sidebarToggle.contains(e.target)) {
                    sidebar.classList.remove('active');
                }
            }
        });

        // Initialize User Onboarding Form
        async function submitOnboarding() {
            const nameField = document.getElementById('userName');
            const emailField = document.getElementById('userEmail');
            const mobileField = document.getElementById('userMobile');
            
            const name = nameField.value.trim();
            const email = emailField.value.trim();
            const mobile = mobileField.value.trim();
            
            // UI Error resets
            document.getElementById('nameError').style.display = 'none';
            document.getElementById('emailError').style.display = 'none';
            document.getElementById('mobileError').style.display = 'none';
            
            let hasError = false;
            
            if (name.length < 1) {
                document.getElementById('nameError').style.display = 'block';
                hasError = true;
            }
            
            const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
            if (!emailRegex.test(email)) {
                document.getElementById('emailError').style.display = 'block';
                hasError = true;
            }
            
            const mobileRegex = /^\+?[0-9]{10,12}$/;
            if (!mobileRegex.test(mobile)) {
                document.getElementById('mobileError').style.display = 'block';
                hasError = true;
            }
            
            if (hasError) return;
            
            // Call Backend /api/start
            const submitBtn = document.getElementById('btnSubmitOnboarding');
            submitBtn.textContent = 'Starting Session...';
            submitBtn.disabled = true;
            
            try {
                const response = await fetch(`${BASE_URL}/api/start`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ name, email, mobile })
                });
                
                const data = await response.json();
                if (!response.ok) {
                    throw new Error(data.detail || 'Could not start session.');
                }
                
                sessionId = data.session_id;
                userName = data.name;
                
                // Hide modal and activate input panel
                onboardingModal.style.opacity = '0';
                setTimeout(() => {
                    onboardingModal.style.display = 'none';
                }, 300);
                
                // Enable Input
                inputPanel.style.opacity = '1';
                inputPanel.style.pointerEvents = 'auto';
                chatInput.disabled = false;
                chatInput.placeholder = `Ask anything, ${userName}...`;
                btnSend.disabled = false;
                btnEndChat.style.display = 'flex';
                suggestionsContainer.style.display = 'flex';
                
                // Print a welcoming bot message
                addMessage(`Welcome, **${userName}**! We are glad to have you. Feel free to ask about our courses, fees, batches, or click on the query chips below.`, 'bot');
                
            } catch (err) {
                alert(`Error: ${err.message}`);
                submitBtn.textContent = 'Start Consultation';
                submitBtn.disabled = false;
            }
        }
        
        // Handle input events
        chatInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
        
        btnSend.addEventListener('click', sendMessage);
        
        // Suggestion Chips Click
        document.querySelectorAll('.suggestion-chip').forEach(chip => {
            chip.addEventListener('click', () => {
                chatInput.value = chip.textContent;
                sendMessage();
            });
        });
        
        // End Chat Handler
        btnEndChat.addEventListener('click', async () => {
            if (!confirm('Are you sure you want to end this chat session? A transcript log will be emailed to theeasylearn@gmail.com and your registered address.')) {
                return;
            }
            
            btnEndChat.textContent = 'Ending...';
            btnEndChat.disabled = true;
            chatInput.disabled = true;
            btnSend.disabled = true;
            
            try {
                const response = await fetch(`${BASE_URL}/api/end`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ session_id: sessionId })
                });
                const data = await response.json();
                
                addMessage('Chat session completed. Thank you!', 'bot');
                suggestionsContainer.style.display = 'none';
                inputPanel.innerHTML = `<div style="text-align:center; width:100%; color:var(--text-muted); font-size:0.9rem;">Chat session finished. Log has been emailed. Refresh page to start a new consultation.</div>`;
                btnEndChat.style.display = 'none';
                
            } catch (err) {
                alert(`Failed to end session: ${err.message}`);
                btnEndChat.textContent = 'End Session';
                btnEndChat.disabled = false;
                chatInput.disabled = false;
                btnSend.disabled = false;
            }
        });
        
        // Send a message
        async function sendMessage() {
            const query = chatInput.value.trim();
            if (!query) return;
            
            chatInput.value = '';
            addMessage(query, 'user');
            
            // Add typing indicator
            const typingIndicator = addTypingIndicator();
            
            try {
                const response = await fetch(`${BASE_URL}/api/chat`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ session_id: sessionId, message: query })
                });
                
                const data = await response.json();
                
                // Remove typing indicator
                typingIndicator.remove();
                
                if (!response.ok) {
                    throw new Error(data.detail || 'Could not process query.');
                }
                
                // Add bot response
                addMessage(data.response, 'bot');
                
            } catch (err) {
                typingIndicator.remove();
                addMessage(`*Error: ${err.message}*`, 'bot');
            }
        }
        
        // UI Helpers
        function addMessage(text, sender) {
            const msgDiv = document.createElement('div');
            msgDiv.className = `message ${sender}`;
            
            const timeLabel = document.createElement('span');
            timeLabel.className = 'timestamp-label';
            const now = new Date();
            timeLabel.textContent = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            
            const contentDiv = document.createElement('div');
            contentDiv.className = 'message-content';
            
            // Render text with rich format parsing (bold, bullets, breaks)
            contentDiv.innerHTML = parseRichFormat(text);
            
            const outerDiv = document.createElement('div');
            outerDiv.style.display = 'flex';
            outerDiv.style.flexDirection = 'column';
            outerDiv.appendChild(contentDiv);
            outerDiv.appendChild(timeLabel);
            
            if (sender === 'bot') {
                const botAvatar = document.createElement('div');
                botAvatar.className = 'avatar';
                botAvatar.textContent = 'S';
                msgDiv.appendChild(botAvatar);
            }
            
            msgDiv.appendChild(outerDiv);
            messageArea.appendChild(msgDiv);
            
            // Auto scroll
            messageArea.scrollTop = messageArea.scrollHeight;
        }
        
        function addTypingIndicator() {
            const msgDiv = document.createElement('div');
            msgDiv.className = 'message bot';
            
            const avatar = document.createElement('div');
            avatar.className = 'avatar';
            avatar.textContent = 'S';
            
            const contentDiv = document.createElement('div');
            contentDiv.className = 'message-content';
            contentDiv.innerHTML = `
                <div class="typing-indicator">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            `;
            
            msgDiv.appendChild(avatar);
            msgDiv.appendChild(contentDiv);
            messageArea.appendChild(msgDiv);
            messageArea.scrollTop = messageArea.scrollHeight;
            
            return msgDiv;
        }
        
        // Parse raw output text (markdown/bullets) into HTML
        function parseRichFormat(text) {
            // Strip agent prefix if present
            if (text.startsWith('Skisha: ')) {
                text = text.substring(8);
            }
            
            // Convert escaping backslashes
            text = text.replace(/\\n/g, '\n');
            
            let html = text;
            
            // Convert bold formatting **text** -> <strong>text</strong>
            html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
            
            // Convert lists/bullet formatting
            // Handle bullet block
            if (html.includes('\n- ') || html.includes('\n* ')) {
                const lines = html.split('\n');
                let inList = false;
                let listHtml = '';
                
                for (let i = 0; i < lines.length; i++) {
                    const line = lines[i].trim();
                    if (line.startsWith('- ') || line.startsWith('* ')) {
                        if (!inList) {
                            listHtml += '<ul>';
                            inList = true;
                        }
                        listHtml += `<li>${line.substring(2)}</li>`;
                    } else {
                        if (inList) {
                            listHtml += '</ul>';
                            inList = false;
                        }
                        listHtml += line + (i < lines.length - 1 ? '<br>' : '');
                    }
                }
                if (inList) {
                    listHtml += '</ul>';
                }
                html = listHtml;
            } else {
                // simple newlines replace
                html = html.replace(/\n/g, '<br>');
            }
            
            return html;
        }
