from pathlib import Path
import os, json
from playwright.sync_api import sync_playwright

BASE = os.environ.get('BASE_URL', 'http://127.0.0.1:4173')
VIEWPORTS = [
    ('mobile-320', 320, 740), ('mobile-360', 360, 800), ('mobile-390', 390, 844),
    ('mobile-430', 430, 932), ('tablet-768', 768, 1024), ('desktop-1024', 1024, 800),
    ('desktop-1440', 1440, 900), ('wide-1920', 1920, 1080),
]
ROUTES = ['/', '/workshop.html', '/builds/r36-dsg-mk2.html', '/start-a-build.html']
OUT = Path('test-results')
OUT.mkdir(exist_ok=True)

def overflow_diagnostics(page):
    return page.evaluate("""
    () => {
      const vw = document.documentElement.clientWidth;
      const items = [...document.querySelectorAll('body *')].map((el, index) => {
        const r = el.getBoundingClientRect();
        const cs = getComputedStyle(el);
        return {
          index,
          tag: el.tagName,
          id: el.id || '',
          cls: typeof el.className === 'string' ? el.className : '',
          left: Math.round(r.left * 10) / 10,
          right: Math.round(r.right * 10) / 10,
          width: Math.round(r.width * 10) / 10,
          scrollWidth: el.scrollWidth,
          position: cs.position,
          overflowX: cs.overflowX,
          transform: cs.transform,
          text: (el.textContent || '').trim().replace(/\\s+/g, ' ').slice(0, 80)
        };
      }).filter(x => x.right > vw + 1 || x.left < -1 || x.width > vw + 1 || x.scrollWidth > vw + 1);
      return {
        viewport: vw,
        documentScrollWidth: document.documentElement.scrollWidth,
        bodyScrollWidth: document.body.scrollWidth,
        offenders: items.sort((a,b) => Math.max(b.width,b.scrollWidth) - Math.max(a.width,a.scrollWidth)).slice(0, 30)
      };
    }
    """)

with sync_playwright() as p:
    for browser_name, browser_type in [('chromium', p.chromium), ('firefox', p.firefox), ('webkit', p.webkit)]:
        browser = browser_type.launch(headless=True)
        widths = VIEWPORTS if browser_name == 'chromium' else [('desktop-1440', 1440, 900), ('mobile-390', 390, 844)]
        for label, width, height in widths:
            page = browser.new_page(viewport={'width': width, 'height': height})
            errors = []
            page.on('pageerror', lambda exc, bucket=errors: bucket.append(str(exc)))
            for route in ROUTES:
                page.goto(BASE + route, wait_until='domcontentloaded')
                page.evaluate("document.querySelectorAll('[data-reveal]').forEach(el => el.classList.add('is-visible'))")
                metrics = page.evaluate('({sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth})')
                if metrics['sw'] > metrics['cw'] + 1:
                    diag = overflow_diagnostics(page)
                    print(f'OVERFLOW_DIAGNOSTICS {browser_name} {label} {route}:')
                    print(json.dumps(diag, indent=2))
                    page.screenshot(path=str(OUT / f'overflow-{browser_name}-{label}-{route.strip("/").replace("/","-") or "home"}.png'), full_page=True)
                    raise AssertionError(f'{browser_name} {label} {route}: horizontal overflow {metrics}')
                assert not errors, f'{browser_name} {label} {route}: page errors {errors}'
                assert page.locator('h1').count() == 1, f'{browser_name} {label} {route}: expected one H1'
                if route == '/' and browser_name == 'chromium':
                    page.screenshot(path=str(OUT / f'home-{label}.png'), full_page=True)
            page.close()
        browser.close()

    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 390, 'height': 844})
    page.goto(BASE + '/start-a-build.html')
    page.fill('[name=name]', 'Test User')
    page.fill('[name=phone]', '0712345678')
    page.fill('[name=car]', 'Golf Mk2')
    page.select_option('[name=work]', label='Engine / DSG swap')
    page.fill('[name=goal]', 'R36 DSG build')
    page.evaluate("window.__opened=''; window.open=(url)=>{window.__opened=url; return null}")
    page.click('button[type=submit]')
    opened = page.evaluate('window.__opened')
    assert 'wa.me/27747942955' in opened
    browser.close()

print('Cross-browser responsive QA passed')
