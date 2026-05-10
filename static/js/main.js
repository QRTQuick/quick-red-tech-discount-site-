/* ===================================
   QUICK RED TECH - MAIN JAVASCRIPT
   Animations, Interactions & Form Handling
   =================================== */

document.addEventListener('DOMContentLoaded', function() {
    
    // Loading Animation
    setTimeout(() => {
        const loader = document.getElementById('loader');
        if (loader) {
            loader.style.display = 'none';
        }
    }, 3000);
    
    // Navbar Scroll Effect
    const navbar = document.getElementById('navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 100) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
    
    // Mobile Menu Toggle
    const hamburger = document.getElementById('hamburger');
    const navMenu = document.getElementById('nav-menu');
    
    if (hamburger && navMenu) {
        hamburger.addEventListener('click', () => {
            navMenu.classList.toggle('active');
            hamburger.classList.toggle('active');
        });
        
        // Close menu when clicking on a link
        document.querySelectorAll('.nav-menu a').forEach(link => {
            link.addEventListener('click', () => {
                navMenu.classList.remove('active');
                hamburger.classList.remove('active');
            });
        });
    }
    
    // Smooth Scroll for Anchor Links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const offsetTop = target.offsetTop - 80;
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Reveal Animations on Scroll
    const revealElements = document.querySelectorAll('.reveal');
    
    const revealOnScroll = () => {
        revealElements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;
            
            if (elementTop < windowHeight - 100) {
                element.classList.add('active');
            }
        });
    };
    
    window.addEventListener('scroll', revealOnScroll);
    revealOnScroll(); // Initial check
    
    // Counter Animation
    const statNumbers = document.querySelectorAll('.stat-number');
    
    const animateCounter = (element) => {
        const target = parseInt(element.getAttribute('data-count'));
        const duration = 2000;
        const step = target / (duration / 16);
        let current = 0;
        
        const updateCounter = () => {
            current += step;
            if (current < target) {
                element.textContent = Math.floor(current);
                requestAnimationFrame(updateCounter);
            } else {
                element.textContent = target;
                if (element.nextElementSibling && element.nextElementSibling.textContent.includes('%')) {
                    element.textContent = target + '%';
                } else if (element.nextElementSibling && element.nextElementSibling.textContent.includes('Hour')) {
                    element.textContent = target + '/7';
                }
            }
        };
        
        updateCounter();
    };
    
    // Trigger counter animation when visible
    const observerOptions = {
        threshold: 0.5
    };
    
    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                counterObserver.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    statNumbers.forEach(stat => {
        counterObserver.observe(stat);
    });
    
    // FAQ Accordion
    const faqItems = document.querySelectorAll('.faq-item');
    
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        question.addEventListener('click', () => {
            const isActive = item.classList.contains('active');
            
            // Close all other items
            faqItems.forEach(otherItem => {
                otherItem.classList.remove('active');
            });
            
            // Toggle current item
            if (!isActive) {
                item.classList.add('active');
            }
        });
    });
    
    // Countdown Timer
    const countdownDate = new Date();
    countdownDate.setDate(countdownDate.getDate() + 7); // 7 days from now
    
    const updateCountdown = () => {
        const now = new Date().getTime();
        const distance = countdownDate - now;
        
        if (distance > 0) {
            const days = Math.floor(distance / (1000 * 60 * 60 * 24));
            const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((distance % (1000 * 60)) / 1000);
            
            const daysEl = document.getElementById('days');
            const hoursEl = document.getElementById('hours');
            const minutesEl = document.getElementById('minutes');
            const secondsEl = document.getElementById('seconds');
            
            if (daysEl) daysEl.textContent = String(days).padStart(2, '0');
            if (hoursEl) hoursEl.textContent = String(hours).padStart(2, '0');
            if (minutesEl) minutesEl.textContent = String(minutes).padStart(2, '0');
            if (secondsEl) secondsEl.textContent = String(seconds).padStart(2, '0');
        }
    };
    
    updateCountdown();
    setInterval(updateCountdown, 1000);
    
    // Form Submission Handler
    const requestForm = document.getElementById('requestForm');
    const formSuccess = document.getElementById('formSuccess');
    
    if (requestForm) {
        requestForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            
            // Disable button and show loading state
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Submitting...';
            
            const formData = new FormData(this);
            
            try {
                const response = await fetch('/submit-request', {
                    method: 'POST',
                    body: formData
                });
                
                const result = await response.json();
                
                if (result.success) {
                    // Hide form and show success message
                    requestForm.style.display = 'none';
                    formSuccess.style.display = 'block';
                    
                    // Scroll to success message
                    formSuccess.scrollIntoView({ behavior: 'smooth', block: 'center' });
                } else {
                    alert(result.message || 'An error occurred. Please try again.');
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalText;
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred. Please try again later.');
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalText;
            }
        });
    }
    
    // Back to Top Button
    const backToTop = document.getElementById('backToTop');
    
    if (backToTop) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 500) {
                backToTop.classList.add('visible');
            } else {
                backToTop.classList.remove('visible');
            }
        });
        
        backToTop.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
    
    // Particle Effect (Simple Implementation)
    const particlesContainer = document.getElementById('particles');
    
    if (particlesContainer) {
        const createParticle = () => {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.cssText = `
                position: absolute;
                width: ${Math.random() * 5 + 2}px;
                height: ${Math.random() * 5 + 2}px;
                background: rgba(255, 0, 0, ${Math.random() * 0.5 + 0.2});
                border-radius: 50%;
                left: ${Math.random() * 100}%;
                top: ${Math.random() * 100}%;
                animation: particleFloat ${Math.random() * 10 + 10}s linear infinite;
                pointer-events: none;
            `;
            
            particlesContainer.appendChild(particle);
            
            // Remove particle after animation
            setTimeout(() => {
                particle.remove();
            }, 20000);
        };
        
        // Create initial particles
        for (let i = 0; i < 30; i++) {
            createParticle();
        }
        
        // Continuously create new particles
        setInterval(createParticle, 1000);
    }
    
    // Add particle animation styles
    const style = document.createElement('style');
    style.textContent = `
        @keyframes particleFloat {
            0% {
                transform: translateY(0) translateX(0);
                opacity: 0;
            }
            10% {
                opacity: 1;
            }
            90% {
                opacity: 1;
            }
            100% {
                transform: translateY(-100vh) translateX(${Math.random() * 100 - 50}px);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
    
    // Testimonial Slider (Auto Rotate)
    const testimonialCards = document.querySelectorAll('.testimonial-card');
    
    if (testimonialCards.length > 0) {
        let currentTestimonial = 0;
        
        setInterval(() => {
            testimonialCards.forEach((card, index) => {
                if (index === currentTestimonial) {
                    card.style.opacity = '1';
                    card.style.transform = 'scale(1)';
                } else {
                    card.style.opacity = '0.7';
                    card.style.transform = 'scale(0.95)';
                }
            });
            
            currentTestimonial = (currentTestimonial + 1) % testimonialCards.length;
        }, 5000);
    }
    
    // Hover Effect for Service Cards
    const serviceCards = document.querySelectorAll('.service-card');
    
    serviceCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            serviceCards.forEach(c => {
                if (c !== card) {
                    c.style.opacity = '0.7';
                }
            });
        });
        
        card.addEventListener('mouseleave', function() {
            serviceCards.forEach(c => {
                c.style.opacity = '1';
            });
        });
    });
    
    // Console Branding
    console.log('%c QUICK RED TECH ', 'background: #ff0000; color: #fff; font-size: 20px; padding: 10px;');
    console.log('%c Premium Web Development Services ', 'color: #ff0000; font-size: 14px;');
    console.log('%c Visit: www.quickredtech.websitediscount.vercel.app ', 'color: #b3b3b3; font-size: 12px;');
    
});

// Preload Critical Resources
if ('loading' in HTMLImageElement.prototype) {
    const images = document.querySelectorAll('img[loading="lazy"]');
    images.forEach(img => {
        img.src = img.dataset.src;
    });
} else {
    // Fallback for browsers that don't support lazy loading
    const script = document.createElement('script');
    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/lazysizes/5.3.2/lazysizes.min.js';
    document.body.appendChild(script);
}
