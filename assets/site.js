(() => {
  const current = document.currentScript?.src || location.href;
  const load = name => new Promise((resolve, reject) => {
    const script = document.createElement('script');
    script.src = new URL(name, current).href;
    script.onload = resolve;
    script.onerror = reject;
    document.body.appendChild(script);
  });

  const installHQHero = () => {
    const video = document.querySelector('.hero-burnout-video');
    if (!video) return;
    const mobile = matchMedia('(max-width: 820px)').matches;
    const src = mobile ? 'assets/hero-mobile-hq.mp4?v=hq-20260823' : 'assets/hero-desktop-hq.mp4?v=hq-20260823';
    video.querySelectorAll('source').forEach(source => source.remove());
    video.src = src;
    video.preload = 'auto';
    video.muted = true;
    video.playsInline = true;
    video.load();
    video.play().catch(() => {});
    document.documentElement.classList.add('hero-hq-active');
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', installHQHero, { once: true });
  } else {
    installHQHero();
  }

  load('site-base.js?v=hq-20260823')
    .catch(() => null)
    .then(() => load('polish.js?v=hq-20260823').catch(() => null));
})();
