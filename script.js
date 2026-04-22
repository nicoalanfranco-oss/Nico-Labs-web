document.addEventListener('DOMContentLoaded', () => {

    // ── Translation Logic ──────────────────────────────────────────────
    const langBtns = document.querySelectorAll('.lang-btn');
    let currentLang = localStorage.getItem('nicolabs_lang') || 'es';

    function setLanguage(lang) {
        if (!translations[lang]) return;
        currentLang = lang;
        localStorage.setItem('nicolabs_lang', lang);
        
        // Update active class on buttons
        langBtns.forEach(btn => {
            btn.classList.toggle('active', btn.getAttribute('data-lang') === lang);
        });

        // Translate text content
        document.querySelectorAll("[data-i18n]").forEach(el => {
            const key = el.getAttribute("data-i18n");
            if (translations[lang] && translations[lang][key]) {
                el.innerHTML = translations[lang][key];
            }
        });

        // Translate placeholders
        document.querySelectorAll("[data-i18n-placeholder]").forEach(el => {
            const key = el.getAttribute("data-i18n-placeholder");
            if (translations[lang] && translations[lang][key]) {
                el.placeholder = translations[lang][key];
            }
        });
        
        // Update HTML lang attribute
        document.documentElement.lang = lang;

        // Update Chatbot if it exists
        if (typeof updateChatbotStrings === 'function') {
            updateChatbotStrings(lang);
        }
    }

    langBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            setLanguage(btn.getAttribute('data-lang'));
        });
    });

    // Initial translation call
    setLanguage(currentLang);
    // ── End Translation Logic ──────────────────────────────────────────


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
                        translations[currentLang]['notif-title'],
                        translations[currentLang]['notif-desc']
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

    function updateChatbotStrings(lang) {
        const tooltipGreeting = document.querySelector('.tooltip-greeting');
        const tooltipContent = document.querySelector('.tooltip-content');
        const chatInput = document.getElementById('chat-input');
        const chatTitle = document.querySelector('.chat-title');
        const welcomeMsg = document.querySelector('.message.bot');

        if (translations[lang]) {
            if (tooltipGreeting) tooltipGreeting.innerText = translations[lang]['chat-greeting'];
            if (tooltipContent) {
                tooltipContent.innerHTML = `<span class="tooltip-greeting">${translations[lang]['chat-greeting']}</span> ${translations[lang]['chat-message']}`;
            }
            if (chatInput) chatInput.placeholder = translations[lang]['chat-input'];
            if (chatTitle) chatTitle.innerHTML = `<i class="fas fa-robot"></i> ${translations[lang]['chat-title']}`;
            // If the welcome message is still the default one, update it
            if (welcomeMsg && (welcomeMsg.innerText.includes('Hola') || welcomeMsg.innerText.includes('Hello') || welcomeMsg.innerText.includes('Olá'))) {
                welcomeMsg.innerText = translations[lang]['chat-welcome'];
            }
        }
    }

    // Chatbot Widget
    const chatbotContainer = document.getElementById('chatbot-container');

    // Inject Chatbot HTML
    chatbotContainer.innerHTML = `
        <div class="chat-tooltip" id="chat-tooltip">
            <div class="tooltip-content">
                <span class="tooltip-greeting">¡Hola! 👋</span>
                Soy <strong>Nicolich</strong>, tu asistente virtual. ¿En qué puedo ayudarte?
            </div>
        </div>
        <div class="chat-widget" id="chat-widget">
            <div class="chat-header">
                <div class="chat-title">
                     <i class="fas fa-robot"></i> Nico Labs AI
                </div>
                <div class="chat-header-actions">
                    <button class="chat-action-btn" id="chat-clear" title="Limpiar conversación"><i class="fas fa-trash-alt"></i></button>
                    <button class="chat-close" id="chat-close"><i class="fas fa-times"></i></button>
                </div>
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

    // Initialize chatbot strings after injection
    updateChatbotStrings(currentLang);


    const chatToggle = document.getElementById('chat-toggle');
    const chatWidget = document.getElementById('chat-widget');
    const chatClose = document.getElementById('chat-close');
    const chatInput = document.getElementById('chat-input');
    const chatSend = document.getElementById('chat-send');
    const chatMessages = document.getElementById('chat-messages');
    const chatTooltip = document.getElementById('chat-tooltip');

    // Intro animation for the toggle
    chatToggle.style.opacity = '0';
    chatToggle.style.transform = 'scale(0) rotate(-45deg)';
    setTimeout(() => {
        chatToggle.style.transition = 'all 0.6s cubic-bezier(0.34, 1.56, 0.64, 1)';
        chatToggle.style.opacity = '1';
        chatToggle.style.transform = 'scale(1) rotate(0deg)';
    }, 2000);

    // Generate or retrieve a unique session ID for this conversation
    // localStorage persists even when the tab/browser is closed (persistent memory)
    if (!localStorage.getItem('nicolabs_session_id')) {
        localStorage.setItem('nicolabs_session_id', 'session-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9));
    }
    let SESSION_ID = localStorage.getItem('nicolabs_session_id');
    console.log('Chat Session ID:', SESSION_ID);

    // Persistence: History Logic
    function getHistory() {
        return JSON.parse(localStorage.getItem('nicolabs_chat_history') || '[]');
    }

    function saveMessageToLocal(text, sender) {
        const history = getHistory();
        history.push({ text, sender, timestamp: Date.now() });
        localStorage.setItem('nicolabs_chat_history', JSON.stringify(history));
    }


    function clearChatHistory() {
        localStorage.removeItem('nicolabs_chat_history');
        localStorage.removeItem('nicolabs_session_id');
        // Regenerate session ID
        localStorage.setItem('nicolabs_session_id', 'session-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9));
        SESSION_ID = localStorage.getItem('nicolabs_session_id');
        
        // Clear UI
        chatMessages.innerHTML = `
            <div class="message bot">
                Hola, soy el asistente virtual de Nico Labs. ¿En qué puedo ayudarte hoy?
            </div>
        `;
        showNotification('success', 'Conversación Reiniciada', 'Se ha generado una nueva sesión de chat.');
    }

    function loadChatHistory() {
        const history = getHistory();
        if (history.length > 0) {
            // Clear initial message if there's history
            chatMessages.innerHTML = '';
            history.forEach(msg => {
                const div = document.createElement('div');
                div.classList.add('message', msg.sender);
                if (msg.sender === 'bot') {
                    div.innerHTML = formatMarkdown(msg.text);
                } else {
                    div.textContent = msg.text;
                }
                chatMessages.appendChild(div);
            });
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }

    let originalScrollY = 0;

    // Tooltip Logic
    let tooltipTimeout;
    function showChatTooltip(text, duration = 8000) {
        if (chatWidget.classList.contains('active')) return;
        
        if (text) {
            chatTooltip.querySelector('.tooltip-content').innerHTML = text;
        }
        
        chatTooltip.classList.add('active');
        
        clearTimeout(tooltipTimeout);
        tooltipTimeout = setTimeout(() => {
            hideChatTooltip();
        }, duration);
    }

    function hideChatTooltip() {
        chatTooltip.classList.remove('active');
    }

    // Initial greeting after page load
    setTimeout(() => {
        showChatTooltip();
    }, 4500);

    // Scroll Trigger: Show tooltip when reaching contact section
    const contactSection = document.getElementById('contact');
    if (contactSection) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    // Show a specific message for contact
                    showChatTooltip('<span class="tooltip-greeting">¿Dudas sobre tu proyecto?</span>¡Estoy aquí para asesorarte en tiempo real! 🚀');
                    // Stop observing once triggered to avoid being annoying
                    observer.unobserve(contactSection);
                }
            });
        }, { threshold: 0.3 });
        observer.observe(contactSection);
    }

    // Toggle Chat
    function toggleChat() {
        hideChatTooltip();
        chatWidget.classList.toggle('active');
        if (chatWidget.classList.contains('active')) {
            if (window.innerWidth <= 768) {
                // Lock the body layout viewport completely to prevent OS keyboard scrolling push
                originalScrollY = window.scrollY;
                document.body.style.position = 'fixed';
                document.body.style.top = `-${originalScrollY}px`;
                document.body.style.width = '100%';

                // Set initial perfect height (no autofocus to prevent keyboard shift on mobile)
                setTimeout(() => {
                    adjustChatHeight();
                }, 50);
            } else {
                // Focus only on desktop
                chatInput.focus();
            }
        } else {
            if (window.innerWidth <= 768) {
                // Restore body layout viewport
                document.body.style.position = '';
                document.body.style.top = '';
                document.body.style.width = '';
                window.scrollTo(0, originalScrollY);
                chatWidget.style.height = '';
            }
        }
    }

    // Dynamically adjust chatbot height to match visual viewport (keyboard area)
    function adjustChatHeight() {
        if (window.innerWidth <= 768 && chatWidget.classList.contains('active')) {
            let vh = window.innerHeight;
            if (window.visualViewport) {
                vh = window.visualViewport.height;
            }
            chatWidget.style.height = `${vh}px`;
            chatWidget.style.bottom = 'auto'; // Prevent bottom constraint from stretching it
            chatMessages.scrollTop = chatMessages.scrollHeight;

            // Fix iOS Safari scrolling glitch inside the chat
            window.scrollTo(0, 0);
        }
    }

    if (window.visualViewport) {
        window.visualViewport.addEventListener('resize', () => {
            adjustChatHeight();
            // Ensure keyboard doesn't hide the focused input
            if (document.activeElement === chatInput) {
                setTimeout(() => chatInput.scrollIntoView({ behavior: 'smooth', block: 'center' }), 100);
            }
        });
        window.visualViewport.addEventListener('scroll', () => {
            // Block iOS Safari from scrolling the underlying page when keyboard is up
            if (chatWidget.classList.contains('active')) {
                window.scrollTo(0, 0);
            }
        });
    }
    window.addEventListener('resize', adjustChatHeight);

    chatToggle.addEventListener('click', toggleChat);
    chatClose.addEventListener('click', toggleChat);
    const chatClear = document.getElementById('chat-clear');
    if (chatClear) chatClear.addEventListener('click', clearChatHistory);

    // Initial Load
    loadChatHistory();

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
                    cliente: 'nicolabs',
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

            // Helper: deeply extract the text content from potentially nested JSON responses.
            // n8n agent can return: [{"output": "{\"output\": \"...\"}" }] (double-nested)
            function extractBotText(raw) {
                let value = raw;
                // Keep unwrapping as long as it looks like a JSON string
                for (let i = 0; i < 3; i++) {
                    if (typeof value !== 'string') break;
                    const trimmed = value.trim();
                    if (!trimmed.startsWith('{') && !trimmed.startsWith('[')) break;
                    try {
                        const parsed = JSON.parse(trimmed);
                        const candidate = Array.isArray(parsed)
                            ? (parsed[0]?.output ?? parsed[0]?.text ?? parsed[0]?.message)
                            : (parsed.output ?? parsed.text ?? parsed.message);
                        if (candidate === undefined || candidate === null) break;
                        value = candidate;
                    } catch (e) {
                        break;
                    }
                }
                return String(value);
            }

            if (rawText) {
                try {
                    botReply = extractBotText(rawText);
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

    // Convert a subset of Markdown to safe HTML for bot messages.
    function formatMarkdown(text) {
        // Escape raw HTML to prevent injection
        let html = text
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;');

        // Bold: **text** → <strong>text</strong>
        html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');

        // Italic: *text* → <em>text</em>
        html = html.replace(/(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)/g, '<em>$1</em>');

        // Wrap double-newline separated blocks in <p> tags
        const paragraphs = html.split(/\n{2,}/);
        html = paragraphs
            .map(p => p.trim())
            .filter(p => p.length > 0)
            .map(p => `<p>${p.replace(/\n/g, '<br>')}</p>`)
            .join('');

        return html;
    }

    function addMessage(text, sender) {
        const div = document.createElement('div');
        const id = 'msg-' + Date.now();
        div.id = id;
        div.classList.add('message', sender);
        if (sender === 'bot') {
            div.innerHTML = formatMarkdown(text);
        } else {
            div.textContent = text;
        }
        chatMessages.appendChild(div);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        // Save to local storage
        saveMessageToLocal(text, sender);
        
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


