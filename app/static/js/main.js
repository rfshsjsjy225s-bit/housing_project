/* ==========================================
   مشروع سكن الغرباء الجامعي الخيري
   الملف: app/static/js/main.js
   الوصف: التأثيرات الديناميكية والتفاعلات.
   إعداد: وكالة مسارك كود
   ========================================== */

'use strict';

// ==========================================
// 1. تهيئة عند اكتمال تحميل الصفحة
// ==========================================
document.addEventListener('DOMContentLoaded', function () {

    initNavbarScroll();
    initSmoothScrolling();
    initScrollReveal();
    initMobileMenu();
    initBackToTop();
    initHeroParallax();
    initCounterAnimation();

    console.log('%c 🏛️  سكن الغرباء الجامعي الخيري ', 
                'background: #0A1F44; color: #C9A227; font-size: 16px; font-weight: bold; padding: 8px 16px; border-radius: 6px;');
    console.log('%c ✨  تصميم وتطوير: وكالة مسارك كود ',
                'background: #C9A227; color: #0A1F44; font-size: 14px; font-weight: bold; padding: 6px 12px; border-radius: 6px;');
});


// ==========================================
// 2. تأثير التمرير على شريط التنقل
// ==========================================
function initNavbarScroll() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;

    const handleScroll = () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    };

    // استخدام throttle لأداء أفضل
    let ticking = false;
    window.addEventListener('scroll', () => {
        if (!ticking) {
            window.requestAnimationFrame(() => {
                handleScroll();
                ticking = false;
            });
            ticking = true;
        }
    }, { passive: true });

    // تشغيل عند التحميل الأول
    handleScroll();
}


// ==========================================
// 3. التمرير السلس بين الأقسام
// ==========================================
function initSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#' || targetId === '') return;

            const target = document.querySelector(targetId);
            if (!target) return;

            e.preventDefault();

            const navbarHeight = document.querySelector('.navbar')?.offsetHeight || 80;
            const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - navbarHeight - 20;

            window.scrollTo({
                top: targetPosition,
                behavior: 'smooth'
            });

            // إغلاق القائمة الجوالة إذا كانت مفتوحة
            const navLinks = document.querySelector('.nav-links');
            if (navLinks && navLinks.classList.contains('active')) {
                navLinks.classList.remove('active');
            }
        });
    });
}


// ==========================================
// 4. ظهور العناصر تدريجياً عند التمرير (Scroll Reveal)
// ==========================================
function initScrollReveal() {
    const revealElements = document.querySelectorAll(
        '.card, .step-card, .section-title, .section-subtitle, .feature-card, ' +
        '.activity-card, .supervisor-card, .faq-card, .vision-card, .mission-card, ' +
        '.notification-card, .list-styled li'
    );

    if (!revealElements.length) return;

    // إعداد مبدئي
    revealElements.forEach((el, index) => {
        el.classList.add('reveal');
        el.style.transitionDelay = `${(index % 6) * 0.08}s`;
    });

    // استخدام IntersectionObserver لأداء ممتاز
    if ('IntersectionObserver' in window) {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -80px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('active');
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);

        revealElements.forEach(el => observer.observe(el));
    } else {
        // fallback للمتصفحات القديمة
        revealElements.forEach(el => el.classList.add('active'));
    }
}


// ==========================================
// 5. القائمة الجوالة
// ==========================================
function initMobileMenu() {
    const navbar = document.querySelector('.navbar');
    const navContainer = document.querySelector('.nav-container');
    if (!navbar || !navContainer) return;

    // إنشاء زر القائمة
    const menuToggle = document.createElement('button');
    menuToggle.className = 'menu-toggle';
    menuToggle.setAttribute('aria-label', 'القائمة');
    menuToggle.innerHTML = '<span></span><span></span><span></span>';

    // إدراجه في المكان المناسب للشاشات الصغيرة فقط
    if (window.innerWidth <= 768) {
        navContainer.insertBefore(menuToggle, navContainer.firstChild);
    }

    menuToggle.addEventListener('click', () => {
        const navLinks = document.querySelector('.nav-links');
        if (navLinks) {
            navLinks.classList.toggle('active');
            menuToggle.classList.toggle('active');
        }
    });

    // إغلاق القائمة عند النقر خارجها
    document.addEventListener('click', (e) => {
        const navLinks = document.querySelector('.nav-links');
        if (
            navLinks && 
            navLinks.classList.contains('active') && 
            !navbar.contains(e.target)
        ) {
            navLinks.classList.remove('active');
            menuToggle.classList.remove('active');
        }
    });
}


// ==========================================
// 6. زر العودة للأعلى
// ==========================================
function initBackToTop() {
    // إنشاء الزر
    const backToTop = document.createElement('button');
    backToTop.className = 'back-to-top';
    backToTop.setAttribute('aria-label', 'العودة للأعلى');
    backToTop.innerHTML = '↑';
    document.body.appendChild(backToTop);

    // إظهار/إخفاء الزر عند التمرير
    let ticking = false;
    window.addEventListener('scroll', () => {
        if (!ticking) {
            window.requestAnimationFrame(() => {
                if (window.scrollY > 400) {
                    backToTop.classList.add('visible');
                } else {
                    backToTop.classList.remove('visible');
                }
                ticking = false;
            });
            ticking = true;
        }
    }, { passive: true });

    // التمرير للأعلى عند النقر
    backToTop.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}


// ==========================================
// 7. تأثير Parallax خفيف على Hero Section
// ==========================================
function initHeroParallax() {
    const hero = document.querySelector('.hero-section');
    if (!hero) return;

    // تجاهل على الأجهزة المحمولة لأداء أفضل
    if (window.innerWidth <= 768) return;

    let ticking = false;
    window.addEventListener('scroll', () => {
        if (!ticking) {
            window.requestAnimationFrame(() => {
                const scrolled = window.pageYOffset;
                if (scrolled < window.innerHeight) {
                    hero.style.backgroundPositionY = `${scrolled * 0.4}px`;
                }
                ticking = false;
            });
            ticking = true;
        }
    }, { passive: true });
}


// ==========================================
// 8. تأثير العد التنازلي للأرقام (لإحصائيات مستقبلية)
// ==========================================
function initCounterAnimation() {
    const counters = document.querySelectorAll('[data-counter]');
    if (!counters.length) return;

    const animateCounter = (el) => {
        const target = parseInt(el.getAttribute('data-counter'), 10) || 0;
        const duration = 1800;
        const start = performance.now();
        const startValue = 0;

        const updateCounter = (currentTime) => {
            const elapsed = currentTime - start;
            const progress = Math.min(elapsed / duration, 1);
            // دالة تنعيم (Ease Out)
            const eased = 1 - Math.pow(1 - progress, 3);
            el.textContent = Math.floor(startValue + (target - startValue) * eased);

            if (progress < 1) {
                requestAnimationFrame(updateCounter);
            } else {
                el.textContent = target;
            }
        };

        requestAnimationFrame(updateCounter);
    };

    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateCounter(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        counters.forEach(counter => observer.observe(counter));
    }
}


// ==========================================
// 9. إدارة تغيير حجم النافذة
// ==========================================
let resizeTimer;
window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
        // إزالة القائمة الجوالة عند التكبير
        const navLinks = document.querySelector('.nav-links');
        const menuToggle = document.querySelector('.menu-toggle');
        
        if (window.innerWidth > 768 && navLinks && navLinks.classList.contains('active')) {
            navLinks.classList.remove('active');
            if (menuToggle) menuToggle.classList.remove('active');
        }
    }, 200);
});