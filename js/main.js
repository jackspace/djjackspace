// DJ Jackspace Professional Website JavaScript
// Enhanced functionality for the cosmic DJ experience

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all website functionality
    initMobileMenu();
    initSmoothScrolling();
    initContactForm();
    initScrollAnimations();
    initMixcloudUpdater();
    initParallax();
    initLoadingAnimations();
});

// Mobile Menu Functionality
function initMobileMenu() {
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
        
        // Close mobile menu when clicking on a link
        const mobileLinks = mobileMenu.querySelectorAll('a');
        mobileLinks.forEach(link => {
            link.addEventListener('click', function() {
                mobileMenu.classList.add('hidden');
            });
        });
        
        // Close mobile menu when clicking outside
        document.addEventListener('click', function(event) {
            if (!mobileMenuBtn.contains(event.target) && !mobileMenu.contains(event.target)) {
                mobileMenu.classList.add('hidden');
            }
        });
    }
}

// Smooth Scrolling for Navigation Links
function initSmoothScrolling() {
    const navLinks = document.querySelectorAll('a[href^="#"]');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                const offsetTop = targetSection.offsetTop - 80; // Account for fixed nav
                
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Contact Form Handling
function initContactForm() {
    const contactForm = document.getElementById('contact-form');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form data
            const formData = new FormData(contactForm);
            const data = Object.fromEntries(formData);
            
            // Validate form
            if (validateContactForm(data)) {
                handleFormSubmission(data);
            }
        });
    }
}

function validateContactForm(data) {
    const { name, email, message } = data;
    
    if (!name || name.trim().length < 2) {
        showFormMessage('Please enter your name.', 'error');
        return false;
    }
    
    if (!email || !isValidEmail(email)) {
        showFormMessage('Please enter a valid email address.', 'error');
        return false;
    }
    
    if (!message || message.trim().length < 10) {
        showFormMessage('Please enter a message (at least 10 characters).', 'error');
        return false;
    }
    
    return true;
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function handleFormSubmission(data) {
    const submitBtn = document.querySelector('#contact-form button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    
    // Show loading state
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Sending...';
    submitBtn.disabled = true;
    
    // Simulate form submission (replace with actual endpoint)
    setTimeout(() => {
        showFormMessage('Thank you! Your message has been sent. I\'ll get back to you soon!', 'success');
        document.getElementById('contact-form').reset();
        
        // Reset button
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    }, 2000);
}

function showFormMessage(message, type) {
    // Remove existing message
    const existingMessage = document.querySelector('.form-message');
    if (existingMessage) {
        existingMessage.remove();
    }
    
    // Create new message
    const messageDiv = document.createElement('div');
    messageDiv.className = `form-message p-4 rounded-lg mb-4 ${
        type === 'success' ? 'bg-green-900/50 text-green-300 border border-green-500/30' : 
        'bg-red-900/50 text-red-300 border border-red-500/30'
    }`;
    messageDiv.textContent = message;
    
    // Insert message at the top of the form
    const form = document.getElementById('contact-form');
    form.insertBefore(messageDiv, form.firstChild);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        messageDiv.remove();
    }, 5000);
}

// Scroll Animations
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
            }
        });
    }, observerOptions);
    
    // Observe all sections
    const sections = document.querySelectorAll('section');
    sections.forEach(section => {
        observer.observe(section);
    });
    
    // Observe cards and other elements
    const animatedElements = document.querySelectorAll('.event-card, .music-platform-card, .gallery-item, .stat-card');
    animatedElements.forEach(element => {
        observer.observe(element);
    });
}

// Mixcloud Auto-updater (simulated for demo)
function initMixcloudUpdater() {
    // This would normally fetch real data from Mixcloud API
    // For demo purposes, we'll simulate new content loading
    
    const mixcloudContainer = document.getElementById('mixcloud-container');
    if (!mixcloudContainer) return;
    
    // Simulate checking for new mixes every 30 seconds (in production, this would be much less frequent)
    setInterval(() => {
        checkForNewMixes();
    }, 30000);
}

function checkForNewMixes() {
    // Simulate API call to check for new Mixcloud uploads
    // In reality, this would be handled by the backend Python agent
    
    console.log('Checking for new Mixcloud uploads...');
    
    // This is where the Python agent would inject new content
    // For now, we'll just log that the check happened
}

// Parallax Effects
function initParallax() {
    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        const parallax = document.querySelector('.stars');
        const parallax2 = document.querySelector('.stars2');
        const parallax3 = document.querySelector('.stars3');
        
        if (parallax) {
            const speed = scrolled * 0.2;
            parallax.style.transform = `translateY(${speed}px)`;
        }
        
        if (parallax2) {
            const speed = scrolled * 0.1;
            parallax2.style.transform = `translateY(${speed}px)`;
        }
        
        if (parallax3) {
            const speed = scrolled * 0.05;
            parallax3.style.transform = `translateY(${speed}px)`;
        }
    });
}

// Loading Animations
function initLoadingAnimations() {
    // Add loading animations to images
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        img.addEventListener('load', function() {
            this.style.opacity = '0';
            this.style.transition = 'opacity 0.3s ease';
            setTimeout(() => {
                this.style.opacity = '1';
            }, 100);
        });
    });
}

// Navigation Active State
window.addEventListener('scroll', function() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');
    
    let current = '';
    
    sections.forEach(section => {
        const sectionTop = section.offsetTop - 100;
        if (window.pageYOffset >= sectionTop) {
            current = section.getAttribute('id');
        }
    });
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === '#' + current) {
            link.classList.add('active');
        }
    });
});

// Utility Functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Performance optimized scroll handler
const handleScroll = debounce(function() {
    // Add scroll-based functionality here
}, 10);

window.addEventListener('scroll', handleScroll);

// Error Handling
window.addEventListener('error', function(e) {
    console.error('JavaScript error:', e.error);
    // In production, you might want to send this to an error tracking service
});

// Service Worker Registration (for PWA capabilities)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/sw.js')
            .then(function(registration) {
                console.log('ServiceWorker registration successful');
            })
            .catch(function(err) {
                console.log('ServiceWorker registration failed');
            });
    });
}

// Analytics (replace with your actual analytics code)
function trackEvent(eventName, properties = {}) {
    // Google Analytics 4 or other analytics service
    if (typeof gtag !== 'undefined') {
        gtag('event', eventName, properties);
    }
    
    console.log('Event tracked:', eventName, properties);
}

// Track contact form submissions
document.addEventListener('submit', function(e) {
    if (e.target.id === 'contact-form') {
        trackEvent('contact_form_submit', {
            form_name: 'main_contact_form'
        });
    }
});

// Track outbound links
document.addEventListener('click', function(e) {
    const link = e.target.closest('a');
    if (link && link.hostname !== window.location.hostname) {
        trackEvent('outbound_link_click', {
            url: link.href,
            text: link.textContent.trim()
        });
    }
});

// Export functions for use in other scripts if needed
window.DJJackspace = {
    trackEvent,
    showFormMessage,
    checkForNewMixes
};