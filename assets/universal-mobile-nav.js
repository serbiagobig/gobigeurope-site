(() => {
  const toggle = document.querySelector('.site-mobile-toggle');
  const nav = document.querySelector('.site-mobile-nav');
  if (!toggle || !nav) return;

  const setOpen = (open) => {
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
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
})();
