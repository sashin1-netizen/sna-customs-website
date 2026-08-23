(() => {
  const qsa = (s, c = document) => [...c.querySelectorAll(s)];
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;

  qsa('[data-media-image]').forEach(img => {
    const frame = img.closest('[data-media-frame]');
    const fallbackSrc = img.dataset.fallbackSrc;
    let triedFallback = false;
    const ready = () => frame?.classList.add('media-ready');
    const failed = () => {
      if (!triedFallback && fallbackSrc && img.src !== fallbackSrc) {
        triedFallback = true;
        img.src = fallbackSrc;
        return;
      }
      frame?.classList.add('media-failed');
    };
    if (img.complete && img.naturalWidth > 1) ready();
    img.addEventListener('load', ready);
    img.addEventListener('error', failed);
  });

  if (!reduceMotion && matchMedia('(min-width: 821px)').matches) {
    const parallaxMedia = qsa('[data-parallax]');
    let ticking = false;
    const paintParallax = () => {
      const vh = innerHeight || 1;
      parallaxMedia.forEach(el => {
        const r = el.parentElement.getBoundingClientRect();
        const centre = r.top + r.height / 2;
        const delta = Math.max(-1, Math.min(1, (centre - vh / 2) / vh));
        el.style.setProperty('--parallax-y', `${delta * -28}px`);
      });
      ticking = false;
    };
    addEventListener('scroll', () => {
      if (!ticking) {
        ticking = true;
        requestAnimationFrame(paintParallax);
      }
    }, { passive: true });
    paintParallax();
  }
})();
