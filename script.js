document.addEventListener('DOMContentLoaded', () => {

    // ── Notification Modal + Confetti ──────────────────────────────────
    const notifOverlay = document.getElementById('form-notification-overlay');
    const notifIcon = document.getElementById('notif-icon');
    const notifTitle = document.getElementById('notif-title');
    const notifSubtitle = document.getElementById('notif-subtitle');
    const notifCloseBtn = document.getElementById('notif-close-btn');

    let confettiFrame = null;

    function launchConfetti() {
        const canvas = document.getElementById('confetti-canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        const colors = ['#00f2ff', '#ffffff', 'rgba(0,242,255,0.7)', '#73f7ff', '#e2e8f0', '#00bcd4'];
        const particles = Array.from({ length: 160 }, () => ({
            x: Math.random() * canvas.width,
            y: Math.random() * -canvas.height * 0.5 - 20,
            w: Math.random() * 10 + 5,
            h: Math.random() * 5 + 2,
            color: colors[Math.floor(Math.random() * colors.length)],
            rotation: Math.random() * 360,
            speed: Math.random() * 3.5 + 1.5,
            swing: Math.random() * 3 - 1.5,
            swingSpeed: Math.random() * 0.04 + 0.01,
            opacity: Math.random() * 0.5 + 0.5
        }));

        let tick = 0;
        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            tick++;
            let stillVisible = false;
            particles.forEach(p => {
                p.y += p.speed;
                p.x += Math.sin(tick * p.swingSpeed) * p.swing;
                p.rotation += 4;
                if (p.y < canvas.height + 20) stillVisible = true;
                ctx.save();
                ctx.globalAlpha = p.opacity;
                ctx.translate(p.x + p.w / 2, p.y + p.h / 2);
                ctx.rotate((p.rotation * Math.PI) / 180);
                ctx.fillStyle = p.color;
                ctx.fillRect(-p.w / 2, -p.h / 2, p.w, p.h);
                ctx.restore();
            });
            if (stillVisible) {
                confettiFrame = requestAnimationFrame(draw);
            } else {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
            }
        }
        draw();
    }

    function stopConfetti() {
        if (confettiFrame) cancelAnimationFrame(confettiFrame);
        const canvas = document.getElementById('confetti-canvas');
        if (canvas) canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);
    }

    function showNotification(type, title, subtitle) {
        // type: 'success' | 'error'
        notifIcon.textContent = type === 'success' ? '🚀' : '⚠️';
        notifTitle.textContent = title;
        notifSubtitle.innerHTML = subtitle;
        notifOverlay.classList.add('active');
        if (type === 'success') launchConfetti();
    }

    function closeNotification() {
        notifOverlay.classList.remove('active');
        stopConfetti();
    }

    if (notifCloseBtn) notifCloseBtn.addEventListener('click', closeNotification);
    if (notifOverlay) notifOverlay.addEventListener('click', (e) => {
        if (e.target === notifOverlay) closeNotification();
    });
    // ── End Notification ────────────────────────────────────────────────

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
                // Using the production webhook for leads
                const response = await fetch('https://n8n.nico-family.com/webhook/a1e59b22-4770-43dc-b4bd-42186903cfd4', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data),
                });

                if (response.ok) {
                    contactForm.reset();
                    showNotification(
                        'success',
                        '¡Solicitud Enviada!',
                        'Tu mensaje llegó con éxito.<br>El equipo de <strong>Nico Labs</strong> va a contactarte muy pronto.'
                    );
                } else {
                    throw new Error('Error en el envío (HTTP ' + response.status + ')');
                }
            } catch (error) {
                console.error('Form fetch error:', error.name, error.message, error);
                showNotification(
                    'error',
                    'Error al Enviar',
                    error.name + ' — ' + error.message + '<br><br>Verificá que el workflow de n8n esté <strong>activado</strong>.'
                );
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

    // Intro animation for the toggle
    chatToggle.style.opacity = '0';
    chatToggle.style.transform = 'scale(0) rotate(-45deg)';
    setTimeout(() => {
        chatToggle.style.transition = 'all 0.6s cubic-bezier(0.34, 1.56, 0.64, 1)';
        chatToggle.style.opacity = '1';
        chatToggle.style.transform = 'scale(1) rotate(0deg)';
    }, 2000);

    // Generate or retrieve a unique session ID for this conversation
    // sessionStorage resets when the tab is closed (new session = fresh memory)
    if (!sessionStorage.getItem('nicolabs_session_id')) {
        sessionStorage.setItem('nicolabs_session_id', 'session-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9));
    }
    const SESSION_ID = sessionStorage.getItem('nicolabs_session_id');

    let originalScrollY = 0;

    // Toggle Chat
    function toggleChat() {
        const isActive = chatWidget.classList.contains('active');

        if (!isActive) {
            // Opening chat
            chatWidget.classList.add('active');
            chatbotContainer.classList.add('chat-active');
            // Push state for Android back button to handle the close action
            history.pushState({ chatOpen: true }, '');

            setTimeout(() => {
                chatInput.focus();
            }, 50);
        } else {
            // Closing chat via button
            closeChatUI();
            // If we are closing via the button, we should theoretically pop the state so we don't trap the user
            if (history.state && history.state.chatOpen) {
                history.back(); // This will trigger popstate, but we are already closing UI, so we handle it gracefully below
            }
        }
    }

    // Helper to actually visually close the chat
    function closeChatUI() {
        chatWidget.classList.remove('active');
        chatbotContainer.classList.remove('chat-active');
    }

    // Android/Browser Back Button Support
    window.addEventListener('popstate', (e) => {
        // If state is null or doesn't have chatOpen, we should close the chat if it's open
        // (This happens when the user presses back while the chat is open)
        if (chatWidget.classList.contains('active')) {
            closeChatUI();
        }
    });

    // Note: Manual chat height adjustment via resize listeners was removed 
    // in favor of pure CSS 100dvh for reliable mobile rendering without shifting.

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
                    sessionId: SESSION_ID,
                    cliente: 'NICOLABS',
                    fuente: 'WEB'
                })
            });

            // Always read as text first (keep typing indicator visible until body is ready)
            const rawText = await response.text();

            // Remove typing indicator only after the full response body is received
            removeMessage(typingId);
            console.log('n8n raw response [status=' + response.status + ']:', rawText);

            if (!response.ok) {
                showNotification(
                    'error',
                    'Error de Conexión',
                    'El chat no pudo comunicarse con el servidor (HTTP ' + response.status + ').<br>Verificá que n8n esté activo.'
                );
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
                showNotification(
                    'error',
                    'Sin Respuesta',
                    ' El agente no devolvió ninguna respuesta.<br>Verificá que el flujo en <strong>n8n</strong> esté correctamente configurado.'
                );
                return;
            }

            // Helper: strip all "Calling <tool> with input: {...}" traces from n8n
            function stripToolTraces(text) {
                // Remove each "Calling <toolname> with input: { ... }" block.
                // Uses [^{}]* to avoid issues with accented chars inside JSON values.
                return text.replace(/Calling\s+[\w-]+\s+with\s+input:\s*\{[^{}]*\}/g, '').trim();
            }

            addMessage(stripToolTraces(botReply), 'bot');

        } catch (error) {
            removeMessage(typingId);
            console.error('Chat fetch error:', error.name, error.message, error);
            showNotification(
                'error',
                'Error de Sistema',
                'Hubo un problema técnico al enviar el mensaje:<br><strong>' + error.name + '</strong>: ' + error.message
            );
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
