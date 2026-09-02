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

    async function sendToChatwoot(content, messageType) {
        const config = window.NICOLABS_CONFIG || {};
        const CHATWOOT_PUBLIC_URL = config.CHATWOOT_PUBLIC_URL || 'https://chatwoot.nico-family.com/public/api/v1/inboxes/wGkSDZbWsvuQ7eKaZuo6KqCt';
        const IDENTITY_SECRET = config.CHATWOOT_IDENTITY_SECRET || 'Foa8NVwLajDeVeFtFUnd739p';

        // Prefix bot messages so they are distinguishable in Chatwoot
        const finalContent = messageType === 'outgoing' ? `[Asistente]: ${content}` : content;

        // ── Helper: compute HMAC-SHA256 using the browser Web Crypto API ──────
        async function computeHmac(message, secret) {
            const enc = new TextEncoder();
            const key = await window.crypto.subtle.importKey(
                'raw', enc.encode(secret),
                { name: 'HMAC', hash: 'SHA-256' },
                false, ['sign']
            );
            const sig = await window.crypto.subtle.sign('HMAC', key, enc.encode(message));
            return Array.from(new Uint8Array(sig)).map(b => b.toString(16).padStart(2, '0')).join('');
        }

        try {
            // ── PASO 1: Obtener o crear contacto ─────────────────────────────
            let contactSourceId = sessionStorage.getItem('nicolabs_chatwoot_api_contact_source_id');

            if (!contactSourceId) {
                // Compute identity hash required by Chatwoot identity validation
                const identifierHash = await computeHmac(SESSION_ID, IDENTITY_SECRET);

                const contactRes = await fetch(`${CHATWOOT_PUBLIC_URL}/contacts`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        identifier: SESSION_ID,
                        identifier_hash: identifierHash,
                        name: 'Visitante Web'
                    })
                });

                if (contactRes.ok) {
                    const contactData = await contactRes.json();
                    contactSourceId = contactData.source_id;
                    sessionStorage.setItem('nicolabs_chatwoot_api_contact_source_id', contactSourceId);
                } else {
                    const errText = await contactRes.text();
                    throw new Error('[Chatwoot] Error al crear contacto: ' + contactRes.status + ' ' + errText);
                }
            }

            if (!contactSourceId) throw new Error('[Chatwoot] No se pudo obtener/crear contacto');

            // ── PASO 2: Obtener o crear conversación ─────────────────────────
            let conversationId = sessionStorage.getItem('nicolabs_chatwoot_api_conversation_id');

            if (!conversationId) {
                const convRes = await fetch(`${CHATWOOT_PUBLIC_URL}/contacts/${contactSourceId}/conversations`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' }
                });
                if (convRes.ok) {
                    const convData = await convRes.json();
                    conversationId = convData.id;
                    sessionStorage.setItem('nicolabs_chatwoot_api_conversation_id', conversationId);
                } else {
                    const errText = await convRes.text();
                    throw new Error('[Chatwoot] Error al crear conversación: ' + convRes.status + ' ' + errText);
                }
            }

            if (!conversationId) throw new Error('[Chatwoot] No se pudo obtener/crear conversación');

            // ── PASO 3: Enviar mensaje ────────────────────────────────────────
            const msgRes = await fetch(`${CHATWOOT_PUBLIC_URL}/contacts/${contactSourceId}/conversations/${conversationId}/messages`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ content: finalContent })
            });
            if (!msgRes.ok) {
                const errText = await msgRes.text();
                throw new Error('[Chatwoot] Error enviando mensaje: ' + msgRes.status + ' ' + errText);
            }

        } catch (error) {
            console.error('Error in sendToChatwoot:', error);
        }
    }

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
        sessionStorage.removeItem('nicolabs_chatwoot_api_contact_source_id');
        sessionStorage.removeItem('nicolabs_chatwoot_api_conversation_id');
        // Regenerate session ID for a fresh conversation
        localStorage.setItem('nicolabs_session_id', 'session-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9));
        SESSION_ID = localStorage.getItem('nicolabs_session_id');

        // Reset UI to welcome message
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

    let pollingIntervalId = null;

    async function fetchMessagesFromChatwoot() {
        const contactSourceId = sessionStorage.getItem('nicolabs_chatwoot_api_contact_source_id');
        const conversationId = sessionStorage.getItem('nicolabs_chatwoot_api_conversation_id');
        if (!contactSourceId || !conversationId) return;

        const config = window.NICOLABS_CONFIG || {};
        const CHATWOOT_PUBLIC_URL = config.CHATWOOT_PUBLIC_URL || 'https://chatwoot.nico-family.com/public/api/v1/inboxes/wGkSDZbWsvuQ7eKaZuo6KqCt';

        try {
            const res = await fetch(`${CHATWOOT_PUBLIC_URL}/contacts/${contactSourceId}/conversations/${conversationId}/messages`);
            if (res.ok) {
                const messages = await res.json();
                if (Array.isArray(messages)) {
                    const history = getHistory();
                    let updated = false;

                    // Sort messages chronologically to make sure we parse them in order
                    const sortedMessages = messages.sort((a, b) => a.created_at - b.created_at);

                    sortedMessages.forEach(msg => {
                        // Only care about messages from agents/bot (message_type === 1 or message_type === 'outgoing')
                        const isBot = msg.message_type === 1 || msg.message_type === 'outgoing';
                        if (isBot) {
                            // Check if this message text is already in our history
                            const alreadyExists = history.some(h => h.text === msg.content && h.sender === 'bot');
                            if (!alreadyExists) {
                                // Remove any active typing indicators before adding the new message
                                document.querySelectorAll('.message.bot.typing').forEach(el => el.remove());
                                
                                addMessage(msg.content, 'bot');
                                updated = true;
                            }
                        }
                    });

                    // Stop polling once we successfully receive at least one new response from the bot
                    if (updated) {
                        stopPolling();
                    }
                }
            }
        } catch (err) {
            console.error('Error polling Chatwoot messages:', err);
        }
    }

    function startPolling() {
        if (pollingIntervalId) return;
        fetchMessagesFromChatwoot();
        pollingIntervalId = setInterval(fetchMessagesFromChatwoot, 4000);
    }

    function stopPolling() {
        if (pollingIntervalId) {
            clearInterval(pollingIntervalId);
            pollingIntervalId = null;
        }
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
            stopPolling();
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
        addTypingIndicator();

        // Enviar solo el mensaje del cliente a Chatwoot y empezar a escuchar la respuesta
        sendToChatwoot(text, 'incoming');
        startPolling();
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

    // ── Marquee Spotlight Engine ────────────────────────────────────────────
    (function initMarqueeSpotlight() {
        const container = document.querySelector('.marquee-container');
        const track     = document.querySelector('.marquee-track');
        const items     = Array.from(document.querySelectorAll('.client-logo-item'));

        if (!container || !track || !items.length) return;

        let hoveredItem  = null;
        let rafId        = null;

        // ── Hover: pause animation & spotlight the hovered item ──
        items.forEach(item => {
            item.addEventListener('mouseenter', () => {
                hoveredItem = item;
                track.style.animationPlayState = 'paused';

                // Clear auto-spotlight classes, apply hover class
                items.forEach(i => i.classList.remove('spotlight-active', 'spotlight-near', 'spotlight-hovered'));
                item.classList.add('spotlight-hovered');
            });

            item.addEventListener('mouseleave', () => {
                hoveredItem = null;
                item.classList.remove('spotlight-hovered');
                track.style.animationPlayState = 'running';
            });
        });

        // ── Auto-spotlight: Fixed Stage Lighting Zones ──
        function tick() {
            if (!hoveredItem) {
                const containerRect = container.getBoundingClientRect();
                const cWidth = containerRect.width;

                items.forEach(item => {
                    const r = item.getBoundingClientRect();
                    // Skip if out of viewport
                    if (r.right < containerRect.left || r.left > containerRect.right) {
                        item.classList.remove('spotlight-active', 'spotlight-near');
                        return;
                    }

                    // Calculate center of item as ratio 0.0 -> 1.0 within container
                    const itemCenterX = (r.left + r.width / 2) - containerRect.left;
                    const ratio = itemCenterX / cWidth;

                    item.classList.remove('spotlight-active', 'spotlight-near');

                    // 1) CENTER STAGE ZONE (42% - 58%): Prominent Zoom 1.38x + Cyan Ring + Color
                    if (ratio >= 0.42 && ratio <= 0.58) {
                        item.classList.add('spotlight-active');
                    }
                    // 2) LEFT STAGE LIGHT (20% - 31%): Luminous Color Reveal, NO Zoom
                    else if (ratio >= 0.20 && ratio <= 0.31) {
                        item.classList.add('spotlight-near');
                    }
                    // 3) RIGHT STAGE LIGHT (69% - 80%): Luminous Color Reveal, NO Zoom
                    else if (ratio >= 0.69 && ratio <= 0.80) {
                        item.classList.add('spotlight-near');
                    }
                });
            }

            rafId = requestAnimationFrame(tick);
        }

        rafId = requestAnimationFrame(tick);
    })();
    // ── End Marquee Spotlight Engine ────────────────────────────────────────

});


