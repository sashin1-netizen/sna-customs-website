(() => {
  const current = document.currentScript?.src || location.href;
  const load = name => new Promise((resolve, reject) => {
    const script = document.createElement('script');
    script.src = new URL(name, current).href;
    script.onload = resolve;
    script.onerror = reject;
    document.body.appendChild(script);
  });

  load('site-base.js')
    .catch(() => null)
    .then(() => load('polish.js').catch(() => null));
})();
