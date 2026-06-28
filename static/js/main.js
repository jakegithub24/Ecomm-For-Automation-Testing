/* ═══════════════════════════════════════════════
   TECHPRICE — Main JavaScript
   Frosted Liquid Glass Interactions
   ═══════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {
    initMobileMenu();
    initFilters();
    initSearch();
    initSmoothScroll();
    initNavScroll();
});



/* ─── Mobile Menu ─── */
function initMobileMenu() {
    const btn = document.querySelector('.mobile-menu-btn');
    const menu = document.querySelector('.mobile-menu');
    if (!btn || !menu) return;

    btn.addEventListener('click', () => {
        menu.classList.toggle('open');
        const icon = btn.querySelector('i');
        if (menu.classList.contains('open')) {
            icon.classList.remove('fa-bars-staggered');
            icon.classList.add('fa-xmark');
        } else {
            icon.classList.remove('fa-xmark');
            icon.classList.add('fa-bars-staggered');
        }
    });

    // Close on link click
    menu.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            menu.classList.remove('open');
            btn.querySelector('i').classList.remove('fa-xmark');
            btn.querySelector('i').classList.add('fa-bars-staggered');
        });
    });

    // Close on outside click
    document.addEventListener('click', (e) => {
        if (!menu.contains(e.target) && !btn.contains(e.target)) {
            menu.classList.remove('open');
            btn.querySelector('i').classList.remove('fa-xmark');
            btn.querySelector('i').classList.add('fa-bars-staggered');
        }
    });
}

/* ─── Product Filters ─── */
function initFilters() {
    const filterBtns = document.querySelectorAll('.filter-btn');
    const cards = document.querySelectorAll('.product-card');
    const emptyState = document.getElementById('empty-state');
    const countEl = document.getElementById('product-count');

    if (!filterBtns.length) return;

    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Update active state
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const filter = btn.dataset.filter;
            let visibleCount = 0;

            cards.forEach(card => {
                const state = card.dataset.state;
                const shouldShow = filter === 'all' || state === filter;

                if (shouldShow) {
                    card.style.display = '';
                    card.style.opacity = '0';
                    card.style.transform = 'translateY(20px)';
                    setTimeout(() => {
                        card.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
                        card.style.opacity = '1';
                        card.style.transform = 'translateY(0)';
                    }, visibleCount * 50);
                    visibleCount++;
                } else {
                    card.style.opacity = '0';
                    card.style.transform = 'translateY(20px)';
                    setTimeout(() => {
                        card.style.display = 'none';
                    }, 300);
                }
            });

            // Show/hide empty state
            if (visibleCount === 0) {
                emptyState.style.display = 'block';
            } else {
                emptyState.style.display = 'none';
            }

            if (countEl) {
                countEl.textContent = visibleCount + ' items';
            }
        });
    });
}

/* ─── Search ─── */
function initSearch() {
    const searchInput = document.getElementById('search-input');
    const adminSearch = document.getElementById('admin-search');

    if (searchInput) {
        searchInput.addEventListener('input', debounce((e) => {
            const query = e.target.value.toLowerCase().trim();
            filterBySearch(query, '.product-card', ['data-name', 'data-brand']);
        }, 300));
    }

    if (adminSearch) {
        adminSearch.addEventListener('input', debounce((e) => {
            const query = e.target.value.toLowerCase().trim();
            const rows = document.querySelectorAll('#admin-table-body tr');
            rows.forEach(row => {
                const name = row.querySelector('.td-name')?.textContent.toLowerCase() || '';
                const brand = row.children[1]?.textContent.toLowerCase() || '';
                const category = row.querySelector('.td-category')?.textContent.toLowerCase() || '';
                const match = name.includes(query) || brand.includes(query) || category.includes(query);
                row.style.display = match ? '' : 'none';
            });
        }, 300));
    }
}

function filterBySearch(query, selector, attrs) {
    const items = document.querySelectorAll(selector);
    const emptyState = document.getElementById('empty-state');
    let visibleCount = 0;

    items.forEach(item => {
        let match = false;
        if (!query) {
            match = true;
        } else {
            attrs.forEach(attr => {
                const val = (item.getAttribute(attr) || '').toLowerCase();
                if (val.includes(query)) match = true;
            });
            // Also check text content
            if (item.textContent.toLowerCase().includes(query)) match = true;
        }

        item.style.display = match ? '' : 'none';
        if (match) visibleCount++;
    });

    if (emptyState) {
        emptyState.style.display = visibleCount === 0 ? 'block' : 'none';
    }

    const countEl = document.getElementById('product-count');
    if (countEl) {
        countEl.textContent = visibleCount + ' items';
    }
}

function debounce(fn, delay) {
    let timeout;
    return (...args) => {
        clearTimeout(timeout);
        timeout = setTimeout(() => fn(...args), delay);
    };
}

/* ─── Smooth Scroll ─── */
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });
}

/* ─── Nav Scroll Effect ─── */
function initNavScroll() {
    const nav = document.querySelector('.glass-nav');
    if (!nav) return;

    let lastScroll = 0;
    window.addEventListener('scroll', () => {
        const currentScroll = window.scrollY;

        if (currentScroll > 50) {
            nav.style.padding = '10px 24px';
        } else {
            nav.style.padding = '16px 24px';
        }

        lastScroll = currentScroll;
    });
}

/* ─── Toast Helper ─── */
window.showToast = function(title, message, type = 'info') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const icons = {
        success: 'fa-circle-check',
        error: 'fa-circle-xmark',
        info: 'fa-circle-info'
    };

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <div class="toast-icon"><i class="fa-solid ${icons[type]}"></i></div>
        <div class="toast-content">
            <span class="toast-title">${title}</span>
            <span class="toast-message">${message}</span>
        </div>
    `;

    container.appendChild(toast);

    setTimeout(() => {
        toast.classList.add('removing');
        setTimeout(() => toast.remove(), 300);
    }, 4000);
};

/* ─── Scroll Reveal ─── */
function initScrollReveal() {
    const reveals = document.querySelectorAll('.reveal');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.1 });

    reveals.forEach(el => observer.observe(el));
}

// Initialize scroll reveal after page load
setTimeout(initScrollReveal, 100);
