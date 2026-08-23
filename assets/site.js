(() => {
  const current = document.currentScript?.src || location.href;
  const load = name => new Promise((resolve, reject) => {
    const script = document.createElement('script');
    script.src = new URL(name, current).href;
    script.defer = true;
    script.onload = resolve;
    script.onerror = reject;
    document.head.appendChild(script);
  });
  load('site-base.js')
    .then(() => load('polish.js'))
    .then(() => load('cinematic.js'))
    .catch(() => {});
})();