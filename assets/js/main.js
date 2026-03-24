document.addEventListener('DOMContentLoaded', function() {
    // 1. 導覽列滾動變色邏輯
    const header = document.querySelector('.aks-header');
    if(header) {
        window.addEventListener('scroll', function() {
            let currentScroll = window.pageYOffset || document.documentElement.scrollTop;
            if (currentScroll > 50) header.classList.add('is-scrolled');
            else header.classList.remove('is-scrolled');
        }, false);
    }

    // 2. 手機版選單開關邏輯
    const mobileToggle = document.querySelector('.aks-mobile-toggle');
    const mobileMenu = document.querySelector('.aks-mobile-menu');
    const mobileClose = document.querySelector('.aks-mobile-close');
    if(mobileToggle && mobileMenu && mobileClose) {
        mobileToggle.addEventListener('click', () => {
            mobileMenu.classList.add('is-open');
            document.body.style.overflow = 'hidden'; 
        });
        mobileClose.addEventListener('click', () => {
            mobileMenu.classList.remove('is-open');
            document.body.style.overflow = '';
        });
    }

    // 3. 手機版手風琴選單邏輯
    const mobileItems = document.querySelectorAll('.aks-mobile-item.aks-has-sub');
    mobileItems.forEach(item => {
        const link = item.querySelector('.aks-mobile-link');
        link.addEventListener('click', () => {
            const isActive = item.classList.contains('is-active');
            mobileItems.forEach(el => el.classList.remove('is-active'));
            if(!isActive) item.classList.add('is-active');
        });
    });

    // 4. 進場動畫引擎
    const observer = new IntersectionObserver((entries, obs) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) { entry.target.classList.add('is-in'); obs.unobserve(entry.target); }
        });
    }, { root: null, rootMargin: '0px', threshold: 0.15 });
    setTimeout(() => { document.querySelectorAll('.io-reveal').forEach(el => observer.observe(el)); }, 500);
});
