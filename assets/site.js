(() => {
  const currentScriptUrl = new URL(document.currentScript?.src || location.href);
  const assetUrl = name => new URL(name, currentScriptUrl).href;
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)');

  const load = name => new Promise((resolve, reject) => {
    const script = document.createElement('script');
    script.src = assetUrl(name);
    script.defer = true;
    script.onload = resolve;
    script.onerror = reject;
    document.body.appendChild(script);
  });

  const installHeroResilience = () => {
    const video = document.querySelector('.hero-burnout-video');
    if (!video) return;

    const root = document.documentElement;
    const markFailed = () => root.classList.add('hero-video-failed');
    const markReady = () => {
      root.classList.remove('hero-video-failed');
      root.classList.add('hero-video-ready');
    };

    video.muted = true;
    video.playsInline = true;
    video.addEventListener('loadeddata', markReady, { once: true });
    video.addEventListener('error', markFailed);
    video.querySelectorAll('source').forEach(source => source.addEventListener('error', () => {
      if (video.networkState === HTMLMediaElement.NETWORK_NO_SOURCE) markFailed();
    }));

    const applyMotionPreference = () => {
      if (reduceMotion.matches) {
        root.classList.add('hero-motion-reduced');
        video.pause();
      } else {
        root.classList.remove('hero-motion-reduced');
        video.play().catch(() => {
          /* Autoplay can be blocked; the poster remains the visual fallback. */
        });
      }
    };

    applyMotionPreference();
    reduceMotion.addEventListener?.('change', applyMotionPreference);
    document.addEventListener('visibilitychange', () => {
      if (!document.hidden && !reduceMotion.matches) video.play().catch(() => {});
    });
  };

  const boot = () => {
    installHeroResilience();
    load('./site-base.js?v=ready-1')
      .catch(() => null)
      .then(() => load('./polish.js?v=ready-1').catch(() => null));
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot, { once: true });
  } else {
    boot();
  }
})();
