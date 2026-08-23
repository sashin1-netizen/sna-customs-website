(() => {
  const qs = (s, c = document) => c.querySelector(s);
  const qsa = (s, c = document) => [...c.querySelectorAll(s)];
  const header = qs('[data-header]');
  const menuButton = qs('[data-menu-button]');
  const mobileNav = qs('[data-mobile-nav]');
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const track = (event, detail = {}) => {
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({ event, ...detail });
  };

  const closeMenu = () => {
    if (!menuButton || !mobileNav) return;
    menuButton.setAttribute('aria-expanded', 'false');
    mobileNav.hidden = true;
  };
  if (menuButton && mobileNav) {
    menuButton.addEventListener('click', () => {
      const open = menuButton.getAttribute('aria-expanded') === 'true';
      menuButton.setAttribute('aria-expanded', String(!open));
      mobileNav.hidden = open;
    });
    qsa('a', mobileNav).forEach(a => a.addEventListener('click', closeMenu));
    document.addEventListener('keydown', e => { if (e.key === 'Escape') closeMenu(); });
  }

  if (header) {
    let lastY = window.scrollY;
    window.addEventListener('scroll', () => {
      const y = window.scrollY;
      const menuOpen = menuButton?.getAttribute('aria-expanded') === 'true';
      header.classList.toggle('is-hidden', y > lastY && y > 260 && !menuOpen);
      lastY = y;
    }, { passive: true });
  }

  const reveals = qsa('[data-reveal]');
  if (reduceMotion || !('IntersectionObserver' in window)) {
    reveals.forEach(el => el.classList.add('is-visible'));
  } else {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: .12, rootMargin: '0px 0px -5% 0px' });
    reveals.forEach(el => observer.observe(el));
  }

  const dialog = qs('[data-video-dialog]');
  const slot = qs('[data-video-slot]');
  qsa('[data-video], [data-video-id]').forEach(button => {
    button.addEventListener('click', () => {
      if (!dialog || !slot || typeof dialog.showModal !== 'function') return;
      const id = button.dataset.video || button.dataset.videoId;
      if (!id) return;
      slot.innerHTML = `<iframe src="https://www.youtube-nocookie.com/embed/${encodeURIComponent(id)}?autoplay=1&rel=0" title="S&A Customs video feature" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen></iframe>`;
      dialog.showModal();
      track('sna_proof_video_open', { video_id: id });
    });
  });
  qs('[data-video-close]')?.addEventListener('click', () => dialog?.close());
  dialog?.addEventListener('close', () => { if (slot) slot.innerHTML = ''; });
  dialog?.addEventListener('click', e => { if (e.target === dialog) dialog.close(); });

  const form = qs('[data-build-form]');
  if (form) {
    const requestedWork = new URLSearchParams(location.search).get('work');
    const workSelect = form.elements?.work;
    if (requestedWork && workSelect) {
      const option = [...workSelect.options].find(o => o.value.toLowerCase() === requestedWork.toLowerCase() || o.text.toLowerCase() === requestedWork.toLowerCase());
      if (option) workSelect.value = option.value;
    }
    form.addEventListener('submit', e => {
      e.preventDefault();
      if (!form.reportValidity()) return;
      const data = new FormData(form);
      const lines = [
        'Hi S&A Customs, I want to discuss a build.', '',
        `Name: ${data.get('name') || ''}`,
        `WhatsApp: ${data.get('phone') || ''}`,
        `Location: ${data.get('location') || 'Not specified'}`,
        '', 'CAR',
        `Make / model: ${data.get('car') || ''}`,
        `Year: ${data.get('year') || 'Not specified'}`,
        `Current engine: ${data.get('engine') || 'Not specified'}`,
        `Current transmission: ${data.get('transmission') || 'Not specified'}`,
        '', 'PROJECT',
        `Work: ${data.get('work') || ''}`,
        `Ideal timing: ${data.get('timing') || 'Flexible'}`,
        `Budget context: ${data.get('budget') || 'Prefer to discuss after scope'}`,
        '', 'What I want the car to become:', `${data.get('goal') || ''}`
      ];
      track('sna_project_brief_open', { work: String(data.get('work') || ''), timing: String(data.get('timing') || ''), budget: String(data.get('budget') || '') });
      const url = `https://wa.me/27747942955?text=${encodeURIComponent(lines.join('\n'))}`;
      window.open(url, '_blank', 'noopener,noreferrer');
    });
  }

  qsa('a[href*="wa.me"]').forEach(a => a.addEventListener('click', () => track('sna_whatsapp_click', { href: a.href })));
  qsa('a[href^="tel:"]').forEach(a => a.addEventListener('click', () => track('sna_phone_click', { href: a.getAttribute('href') })));
  qsa('a[href*="start-a-build"]').forEach(a => a.addEventListener('click', () => track('sna_start_build_click', { href: a.getAttribute('href') })));
  qsa('[data-year]').forEach(el => { el.textContent = String(new Date().getFullYear()); });
})();
