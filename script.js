document.addEventListener('DOMContentLoaded', () => {
    // Custom Cursor
    const cursorDot = document.querySelector('.cursor-dot');
    const cursorOutline = document.querySelector('.cursor-outline');

    window.addEventListener('mousemove', (e) => {
        const posX = e.clientX;
        const posY = e.clientY;

        cursorDot.style.left = `${posX}px`;
        cursorDot.style.top = `${posY}px`;

        cursorOutline.animate({
            left: `${posX}px`,
            top: `${posY}px`
        }, { duration: 500, fill: "forwards" });
    });

    // Mobile Navigation
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    hamburger.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        hamburger.classList.toggle('toggle');
    });

    // Smooth Scroll
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Glassmorphism Navbar Effect on Scroll
    window.addEventListener('scroll', () => {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 50) {
            navbar.style.background = 'rgba(23, 52, 54, 0.8)';
            navbar.style.boxShadow = '0 2px 20px rgba(0,0,0,0.3)';
        } else {
            navbar.style.background = 'rgba(23, 52, 54, 0.4)';
            navbar.style.boxShadow = 'none';
        }
    });

    // Form Submission
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const submitBtn = contactForm.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerText;
            submitBtn.innerText = 'Enviando...';
            submitBtn.disabled = true;

            const formData = new FormData(contactForm);
            const data = Object.fromEntries(formData.entries());

            try {
                // Using the test webhook as per plan
                const response = await fetch('https://n8n.nico-family.com/webhook-test/8fb105dc-8c1b-47c7-bc88-0f0f9a214b9e', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data),
                });

                if (response.ok) {
                    alert('¡Mensaje enviado con éxito! Nos pondremos en contacto pronto.');
                    contactForm.reset();
                } else {
                    throw new Error('Error en el envío');
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Hubo un error al enviar el mensaje. Por favor intenta nuevamente.');
            } finally {
                submitBtn.innerText = originalText;
                submitBtn.disabled = false;
            }
        });
    }

    // Chatbot Widget
    const chatbotContainer = document.getElementById('chatbot-container');

    // Inject Chatbot HTML
    chatbotContainer.innerHTML = `
        <div class="chat-widget" id="chat-widget">
            <div class="chat-header">
                <div class="chat-title">
                     <i class="fas fa-robot"></i> Nico Labs AI
                </div>
                <button class="chat-close" id="chat-close"><i class="fas fa-times"></i></button>
            </div>
            <div class="chat-messages" id="chat-messages">
                <div class="message bot">
                    Hola, soy el asistente virtual de Nico Labs. ¿En qué puedo ayudarte hoy?
                </div>
            </div>
            <div class="chat-input-area">
                <input type="text" id="chat-input" placeholder="Escribe tu mensaje...">
                <button id="chat-send"><i class="fas fa-paper-plane"></i></button>
            </div>
        </div>
        <button class="chat-toggle" id="chat-toggle">
            <i class="fas fa-comment-dots"></i>
        </button>
    `;

    const chatToggle = document.getElementById('chat-toggle');
    const chatWidget = document.getElementById('chat-widget');
    const chatClose = document.getElementById('chat-close');
    const chatInput = document.getElementById('chat-input');
    const chatSend = document.getElementById('chat-send');
    const chatMessages = document.getElementById('chat-messages');

    // Generate or retrieve a unique session ID for this conversation
    // sessionStorage resets when the tab is closed (new session = fresh memory)
    if (!sessionStorage.getItem('nicolabs_session_id')) {
        sessionStorage.setItem('nicolabs_session_id', 'session-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9));
    }
    const SESSION_ID = sessionStorage.getItem('nicolabs_session_id');

    // Toggle Chat
    function toggleChat() {
        chatWidget.classList.toggle('active');
        if (chatWidget.classList.contains('active')) {
            chatInput.focus();
        }
    }

    chatToggle.addEventListener('click', toggleChat);
    chatClose.addEventListener('click', toggleChat);

    // Send Message Logic
    async function sendMessage() {
        const text = chatInput.value.trim();
        if (!text) return;

        // Add User Message
        addMessage(text, 'user');
        chatInput.value = '';

        // Show typing indicator
        const typingId = addTypingIndicator();

        try {
            const response = await fetch('https://n8n.nico-family.com/webhook/f535820b-22eb-438f-930f-d0f8fe2f3a12/chat', {
                method: 'POST',
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    chatInput: text,
                    sessionId: SESSION_ID
                })
            });

            // Remove typing indicator
            removeMessage(typingId);

            // Always read as text first
            const rawText = await response.text();
            console.log('n8n raw response [status=' + response.status + ']:', rawText);

            if (!response.ok) {
                addMessage('⚠️ Error ' + response.status + ': ' + rawText, 'bot');
                return;
            }

            let botReply = '';

            if (rawText) {
                try {
                    // Try parsing as standard JSON first
                    const parsed = JSON.parse(rawText);
                    if (Array.isArray(parsed)) {
                        botReply = parsed[0]?.output || parsed[0]?.text || parsed[0]?.message || rawText;
                    } else {
                        botReply = parsed.output || parsed.text || parsed.message || rawText;
                    }
                } catch (jsonErr) {
                    // It failed standard JSON parse, it might be NDJSON (streaming format)
                    // The AI Agent returns lines like: {"type":"item","content":"..."}
                    const lines = rawText.split('\n').filter(line => line.trim() !== '');
                    let combinedText = '';
                    let isNdjson = false;

                    for (const line of lines) {
                        try {
                            const parsedLine = JSON.parse(line);
                            if (parsedLine.type === 'item' && parsedLine.content) {
                                combinedText += parsedLine.content;
                                isNdjson = true;
                            }
                        } catch (e) {
                            // ignore lines that aren't valid JSON
                        }
                    }

                    if (isNdjson && combinedText) {
                        botReply = combinedText;
                    } else {
                        // Not JSON, not NDJSON, just plain text
                        botReply = rawText;
                    }
                }
            } else {
                botReply = '(n8n devolvió una respuesta vacía — verifica que el Agente AI esté conectado al Chat Trigger)';
            }

            addMessage(botReply, 'bot');

        } catch (error) {
            removeMessage(typingId);
            console.error('Chat fetch error:', error.name, error.message, error);
            // Show REAL error to help diagnose (CORS, network, etc.)
            addMessage('⚠️ Error técnico: ' + error.name + ' — ' + error.message, 'bot');
        }

    }

    chatSend.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

    function addMessage(text, sender) {
        const div = document.createElement('div');
        const id = 'msg-' + Date.now();
        div.id = id;
        div.classList.add('message', sender);
        div.textContent = text;
        chatMessages.appendChild(div);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return id;
    }

    function removeMessage(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }

    function addTypingIndicator() {
        const div = document.createElement('div');
        const id = 'typing-' + Date.now();
        div.id = id;
        div.classList.add('message', 'bot', 'typing');
        div.innerHTML = '<span></span><span></span><span></span>';
        chatMessages.appendChild(div);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return id;
    }

    // Generic Modal Handler
    function setupModal(triggerId, modalId) {
        const trigger = document.getElementById(triggerId);
        const modal = document.getElementById(modalId);
        if (!trigger || !modal) return;

        const closeBtn = modal.querySelector('.modal-close');
        const overlay = modal.querySelector('.modal-overlay');

        function openModal() {
            modal.style.display = 'flex';
            setTimeout(() => {
                modal.classList.add('active');
                document.body.style.overflow = 'hidden';
            }, 10);
        }

        function closeModal() {
            modal.classList.remove('active');
            setTimeout(() => {
                modal.style.display = 'none';
                document.body.style.overflow = '';
            }, 400);
        }

        trigger.addEventListener('click', openModal);
        closeBtn.addEventListener('click', closeModal);
        overlay.addEventListener('click', closeModal);

        window.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && modal.classList.contains('active')) {
                closeModal();
            }
        });
    }

    setupModal('project-gym', 'project-modal');
    setupModal('project-pro', 'pro-modal');
    setupModal('project-conty', 'conty-modal');
    setupModal('project-comunicados', 'comunicados-modal');
    setupModal('project-redes', 'redes-modal');
    setupModal('project-chatbot', 'chatbot-modal');
    setupModal('project-web', 'web-modal');
    setupModal('open-privacy', 'privacy-modal');
    setupModal('nav-privacy', 'privacy-modal');
    setupModal('footer-privacy', 'privacy-modal');

    // Scroll Reveal Animations
    const revealElements = document.querySelectorAll('.reveal-left, .reveal-bottom, .reveal-right');

    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('reveal-visible');
                // Optional: stop observing once revealed
                // revealObserver.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.15 // Trigger when 15% of the element is visible
    });

    revealElements.forEach(el => revealObserver.observe(el));

    // Hero Entry Animation Trigger
    const heroSection = document.getElementById('hero');
    if (heroSection) {
        setTimeout(() => {
            heroSection.classList.add('hero-active');
        }, 100);
    }

});
