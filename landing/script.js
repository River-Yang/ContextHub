// DOM Ready
document.addEventListener('DOMContentLoaded', function() {
    initNavigation();
    initTerminalAnimation();
    initScrollEffects();
    initButtonActions();
});

// Navigation functionality
function initNavigation() {
    const navLinks = document.querySelectorAll('.nav-link[href^="#"]');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Add scroll spy for nav
    window.addEventListener('scroll', updateActiveNavLink);
}

function updateActiveNavLink() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link[href^="#"]');
    
    let currentSection = '';
    
    sections.forEach(section => {
        const sectionTop = section.offsetTop - 100;
        const sectionHeight = section.offsetHeight;
        
        if (window.scrollY >= sectionTop && window.scrollY < sectionTop + sectionHeight) {
            currentSection = section.getAttribute('id');
        }
    });
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${currentSection}`) {
            link.classList.add('active');
        }
    });
}

// Terminal animation
function initTerminalAnimation() {
    const terminal = document.querySelector('.terminal-body');
    if (!terminal) return;
    
    const lines = terminal.querySelectorAll('.terminal-line');
    
    // Hide all lines initially
    lines.forEach((line, index) => {
        if (index > 0) {
            line.style.opacity = '0';
            line.style.transform = 'translateY(10px)';
        }
    });
    
    // Animate lines in sequence
    function animateTerminal() {
        lines.forEach((line, index) => {
            setTimeout(() => {
                line.style.transition = 'all 0.5s ease';
                line.style.opacity = '1';
                line.style.transform = 'translateY(0)';
            }, index * 800);
        });
    }
    
    // Start animation when terminal comes into view
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                setTimeout(animateTerminal, 500);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });
    
    observer.observe(terminal);
}

// Scroll effects
function initScrollEffects() {
    // Parallax effect for hero background
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const hero = document.querySelector('.hero');
        
        if (hero) {
            hero.style.transform = `translateY(${scrolled * 0.2}px)`;
        }
    });
    
    // Fade in animations for cards
    const cards = document.querySelectorAll('.feature-card, .value-item');
    
    const cardObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1 });
    
    cards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'all 0.6s ease';
        cardObserver.observe(card);
    });
}

// Button actions
function initButtonActions() {
    // Primary CTA buttons
    const ctaButtons = document.querySelectorAll('.btn-primary');
    ctaButtons.forEach(btn => {
        if (btn.textContent.includes('立即体验') || btn.textContent.includes('开始使用')) {
            btn.addEventListener('click', function() {
                // Simulate loading state
                const originalText = this.innerHTML;
                this.innerHTML = '<svg class="btn-icon animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>启动中...';
                this.disabled = true;
                
                setTimeout(() => {
                    // Redirect to main app
                    window.location.href = '../frontend/index.html';
                }, 1500);
            });
        }
    });
    
    // Documentation and GitHub buttons
    const docButtons = document.querySelectorAll('.btn-secondary');
    docButtons.forEach(btn => {
        if (btn.textContent.includes('查看文档')) {
            btn.addEventListener('click', function() {
                // Scroll to demo section or open external docs
                const demoSection = document.querySelector('.demo');
                if (demoSection) {
                    demoSection.scrollIntoView({ behavior: 'smooth' });
                }
            });
        }
        
        if (btn.textContent.includes('GitHub')) {
            btn.addEventListener('click', function() {
                window.open('https://github.com/your-username/ContextHub', '_blank');
            });
        }
    });
    
    // Navigation link handlers
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        if (link.textContent.includes('文档')) {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const demoSection = document.querySelector('.demo');
                if (demoSection) {
                    demoSection.scrollIntoView({ behavior: 'smooth' });
                }
            });
        }
        
        if (link.textContent.includes('GitHub')) {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                window.open('https://github.com/your-username/ContextHub', '_blank');
            });
        }
    });
    
    // Demo code tabs
    const codeTabs = document.querySelectorAll('.code-tab');
    codeTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            // Remove active class from all tabs
            codeTabs.forEach(t => t.classList.remove('active'));
            // Add active class to clicked tab
            this.classList.add('active');
            
            // Switch code content (simplified for demo)
            const codeContent = document.querySelector('.code-content');
            if (this.textContent.includes('analysis.json')) {
                codeContent.textContent = `{
  "analysis_results": {
    "file_type": "python",
    "complexity_score": 0.75,
    "key_functions": [
      "main_handler",
      "process_data",
      "validate_input"
    ],
    "dependencies": [
      "flask",
      "requests",
      "json"
    ],
    "suggestions": [
      "添加错误处理",
      "优化数据库查询",
      "增加单元测试"
    ]
  }
}`;
            } else {
                codeContent.textContent = `{
  "version": "1.0",
  "metadata": {
    "name": "项目分析",
    "task_type": "code_project",
    "analysis_model": "Moonshot Kimi"
  },
  "instructions": {
    "system": "你是专门分析代码项目的AI助手",
    "context": "这是一个Python Web应用..."
  },
  "assets": {
    "state_chain": [
      {
        "type": "analysis",
        "content": "详细的代码分析结果...",
        "metadata": {
          "complexity": "medium",
          "key_points": ["RESTful API", "数据库集成"]
        }
      }
    ]
  }
}`;
            }
        });
    });
}

// Add typing animation to hero subtitle
function initTypingAnimation() {
    const subtitle = document.querySelector('.hero-subtitle');
    if (!subtitle) return;
    
    const text = subtitle.textContent;
    subtitle.textContent = '';
    
    let index = 0;
    function typeNext() {
        if (index < text.length) {
            subtitle.textContent += text.charAt(index);
            index++;
            setTimeout(typeNext, 50);
        }
    }
    
    setTimeout(typeNext, 1000);
}

// Add particle effect to hero background
function initParticleEffect() {
    const hero = document.querySelector('.hero');
    if (!hero) return;
    
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    
    canvas.style.position = 'absolute';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.pointerEvents = 'none';
    canvas.style.zIndex = '1';
    
    hero.appendChild(canvas);
    
    function resizeCanvas() {
        canvas.width = hero.offsetWidth;
        canvas.height = hero.offsetHeight;
    }
    
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();
    
    const particles = [];
    const particleCount = 50;
    
    for (let i = 0; i < particleCount; i++) {
        particles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            vx: (Math.random() - 0.5) * 0.5,
            vy: (Math.random() - 0.5) * 0.5,
            size: Math.random() * 2 + 1,
            opacity: Math.random() * 0.5 + 0.1
        });
    }
    
    function animateParticles() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        particles.forEach(particle => {
            particle.x += particle.vx;
            particle.y += particle.vy;
            
            if (particle.x < 0 || particle.x > canvas.width) particle.vx *= -1;
            if (particle.y < 0 || particle.y > canvas.height) particle.vy *= -1;
            
            ctx.beginPath();
            ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(102, 126, 234, ${particle.opacity})`;
            ctx.fill();
        });
        
        requestAnimationFrame(animateParticles);
    }
    
    animateParticles();
}

// Add smooth scroll for anchor links
function smoothScrollToAnchor() {
    const anchors = document.querySelectorAll('a[href^="#"]');
    
    anchors.forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Add loading animation
function showLoadingAnimation() {
    const loading = document.createElement('div');
    loading.className = 'loading-overlay';
    loading.innerHTML = `
        <div class="loading-spinner">
            <div class="spinner"></div>
            <p>加载中...</p>
        </div>
    `;
    
    document.body.appendChild(loading);
    
    setTimeout(() => {
        loading.style.opacity = '0';
        setTimeout(() => {
            document.body.removeChild(loading);
        }, 300);
    }, 1000);
}

// CSS for loading animation
const style = document.createElement('style');
style.textContent = `
    .loading-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: var(--bg-primary);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
        transition: opacity 0.3s ease;
    }
    
    .loading-spinner {
        text-align: center;
        color: var(--text-primary);
    }
    
    .spinner {
        width: 40px;
        height: 40px;
        border: 3px solid var(--border-color);
        border-top: 3px solid var(--primary-gradient);
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 0 auto 1rem;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .animate-spin {
        animation: spin 1s linear infinite;
    }
    
    .nav-link.active {
        color: var(--text-primary);
        position: relative;
    }
    
    .nav-link.active::after {
        content: '';
        position: absolute;
        bottom: -4px;
        left: 0;
        width: 100%;
        height: 2px;
        background: var(--primary-gradient);
        border-radius: 1px;
    }
`;

document.head.appendChild(style);

// Initialize everything when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    initNavigation();
    initTerminalAnimation();
    initScrollEffects();
    initButtonActions();
    smoothScrollToAnchor();
    
    // Optional: uncomment to enable particle effect
    // initParticleEffect();
}); 