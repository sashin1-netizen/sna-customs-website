(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const hero = document.querySelector('.hero');
  if (!hero) return;

  hero.classList.add('hero-cinematic');
  hero.setAttribute('data-hero','');

  const media = hero.querySelector('.hero-media');
  const bg = media?.querySelector('img');
  if (bg) bg.classList.add('hero-bg');

  const layer = document.createElement('div');
  layer.innerHTML = `
    <div class="hero-vignette" aria-hidden="true"></div>
    <div class="hero-speedlines" aria-hidden="true"></div>
    <div class="hero-orbit hero-orbit-a" aria-hidden="true"></div>
    <div class="hero-orbit hero-orbit-b" aria-hidden="true"></div>
    <div class="hero-car-stage" aria-hidden="true" data-car-stage>
      <div class="hero-car-frame">
        <img src="https://img.youtube.com/vi/C-q4s1PIGtU/maxresdefault.jpg" alt="" width="1280" height="720" decoding="async">
        <div class="hero-car-glint"></div>
        <div class="hero-car-scan"></div>
      </div>
      <div class="hero-hud"><span>R36 / DSG / MK2</span><b>10.7</b><em>@ 209 KM/H</em></div>
    </div>`;
  while (layer.firstElementChild) hero.insertBefore(layer.firstElementChild, hero.querySelector('.hero-overlay'));

  const title = hero.querySelector('h1');
  title?.classList.add('hero-title');
  title?.querySelectorAll(':scope > span, :scope > em, :scope > strong').forEach(el => el.setAttribute('data-hero-line',''));
  hero.querySelector('.hero-proof')?.classList.add('hero-proof-glass');

  const rail = document.createElement('div');
  rail.className = 'hero-motion-rail';
  rail.setAttribute('aria-hidden','true');
  rail.innerHTML = '<span></span><b>Scroll to enter the workshop</b><i></i>';
  hero.appendChild(rail);

  const glow = document.createElement('div');
  glow.className = 'cursor-glow';
  glow.setAttribute('aria-hidden','true');
  document.body.appendChild(glow);

  document.querySelectorAll('.manifesto,.project-journal,.workshop-preview,.culture-band,.start-preview').forEach(s => s.setAttribute('data-section-motion',''));

  const root = document.documentElement;
  if (!reduce) {
    let tx = 0, ty = 0, cx = 0, cy = 0, raf = 0;
    const render = () => {
      cx += (tx - cx) * .075;
      cy += (ty - cy) * .075;
      root.style.setProperty('--hero-x', `${cx}px`);
      root.style.setProperty('--hero-y', `${cy}px`);
      if (Math.abs(tx-cx) > .05 || Math.abs(ty-cy) > .05) raf = requestAnimationFrame(render);
      else raf = 0;
    };
    hero.addEventListener('pointermove', e => {
      const r = hero.getBoundingClientRect();
      tx = ((e.clientX-r.left)/r.width-.5)*34;
      ty = ((e.clientY-r.top)/r.height-.5)*24;
      if (!raf) raf = requestAnimationFrame(render);
    }, {passive:true});
    hero.addEventListener('pointerleave', () => {
      tx = 0; ty = 0;
      if (!raf) raf = requestAnimationFrame(render);
    });
    const syncScroll = () => {
      const p = Math.max(0, Math.min(1, scrollY / Math.max(hero.offsetHeight,1)));
      root.style.setProperty('--scroll-p', p.toFixed(3));
    };
    addEventListener('scroll', syncScroll, {passive:true});
    syncScroll();

    if (matchMedia('(pointer:fine)').matches) {
      addEventListener('pointermove', e => {
        glow.style.transform = `translate(${e.clientX-208}px,${e.clientY-208}px)`;
      }, {passive:true});
    }
  }

  const sections = document.querySelectorAll('[data-section-motion]');
  if ('IntersectionObserver' in window && !reduce) {
    const io = new IntersectionObserver(entries => entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-motion-visible');
        io.unobserve(entry.target);
      }
    }), {threshold:.16});
    sections.forEach(s => io.observe(s));
  } else {
    sections.forEach(s => s.classList.add('is-motion-visible'));
  }
})();
