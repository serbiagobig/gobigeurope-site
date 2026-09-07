(() => {
  const toggle = document.querySelector('.site-mobile-toggle');
  const nav = document.querySelector('.site-mobile-nav');

  if (toggle && nav) {
    const openLabel = toggle.dataset.openLabel || 'Open menu';
    const closeLabel = toggle.dataset.closeLabel || 'Close menu';

    const setOpen = (open) => {
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.setAttribute('aria-label', open ? closeLabel : openLabel);
      nav.classList.toggle('is-open', open);
      document.body.classList.toggle('site-nav-open', open);
    };

    toggle.addEventListener('click', () => {
      setOpen(toggle.getAttribute('aria-expanded') !== 'true');
    });

    nav.addEventListener('click', (event) => {
      const link = event.target.closest('a');
      if (link) setOpen(false);
    });

    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape') setOpen(false);
    });

    window.addEventListener('resize', () => {
      if (window.innerWidth > 850) setOpen(false);
    });
  }

  document.querySelectorAll('[data-site-back="true"]').forEach((link) => {
    link.addEventListener('click', (event) => {
      const ref = document.referrer;
      let internalReferrer = false;
      try {
        internalReferrer = !!ref && new URL(ref).origin === window.location.origin;
      } catch (_) {}

      if (internalReferrer && window.history.length > 1) {
        event.preventDefault();
        window.history.back();
      }
    });
  });

  // AGRO TAG product 05 opens the approved berry-harvesting case page.
  const path = window.location.pathname.toLowerCase();
  if (path.endsWith('/agro-tag.html') || path.endsWith('agro-tag.html')) {
    const cards = Array.from(document.querySelectorAll('.products .product'));
    const berryCard = cards.find((card) => {
      const number = card.querySelector('.product-num');
      return number && number.textContent.trim() === '05';
    });

    if (berryCard) {
      berryCard.setAttribute('role', 'link');
      berryCard.setAttribute('tabindex', '0');
      berryCard.style.cursor = 'pointer';
      const openBerry = () => { window.location.href = 'berry-harvesting.html'; };
      berryCard.addEventListener('click', (event) => {
        if (event.target.closest('a,button,input,select,textarea')) return;
        openBerry();
      });
      berryCard.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' || event.key === ' ') {
          event.preventDefault();
          openBerry();
        }
      });
    }
  }
})();
