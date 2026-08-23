from __future__ import annotations

from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote
import sys

ROOT = Path(__file__).resolve().parents[1]
IGNORE_DIRS = {'.git', '.github'}


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links: list[str] = []
        self.ids: list[str] = []
        self.blank_targets_without_rel: list[str] = []
        self.iframes: list[dict[str, str]] = []
        self.has_title = False
        self.has_description = False
        self.has_canonical = False
        self.has_main = False
        self.has_viewport = False
        self.has_skip_link = False
        self.html_lang = ''
        self.h1_count = 0
        self._in_title = False
        self._title_text: list[str] = []

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if tag == 'html':
            self.html_lang = data.get('lang', '').strip()
        if data.get('id'):
            self.ids.append(data['id'])
        if tag == 'a' and data.get('href'):
            href = data['href']
            self.links.append(href)
            classes = set(data.get('class', '').split())
            if 'skip-link' in classes:
                self.has_skip_link = True
            if data.get('target') == '_blank':
                rel = set(data.get('rel', '').split())
                if not {'noopener', 'noreferrer'}.issubset(rel):
                    self.blank_targets_without_rel.append(href)
        if tag in {'img', 'script', 'source', 'link'}:
            for key in ('src', 'href'):
                if data.get(key):
                    self.links.append(data[key])
        if tag == 'iframe':
            self.iframes.append(data)
        if tag == 'title':
            self._in_title = True
        elif tag == 'meta' and data.get('name', '').lower() == 'description' and data.get('content', '').strip():
            self.has_description = True
        elif tag == 'meta' and data.get('name', '').lower() == 'viewport' and data.get('content', '').strip():
            self.has_viewport = True
        elif tag == 'link' and data.get('rel') == 'canonical' and data.get('href'):
            self.has_canonical = True
        elif tag == 'main':
            self.has_main = True
        elif tag == 'h1':
            self.h1_count += 1

    def handle_endtag(self, tag):
        if tag == 'title':
            self._in_title = False
            self.has_title = bool(''.join(self._title_text).strip())

    def handle_data(self, data):
        if self._in_title:
            self._title_text.append(data)


def internal_target(page: Path, href: str) -> Path | None:
    href = href.strip()
    if not href or href.startswith(('#', 'mailto:', 'tel:', 'javascript:', 'data:')):
        return None
    parsed = urlparse(href)
    if parsed.scheme or parsed.netloc:
        return None
    path = unquote(parsed.path)
    if not path:
        return None
    target = (page.parent / path).resolve()
    try:
        target.relative_to(ROOT)
    except ValueError:
        return None
    if target.is_dir():
        target = target / 'index.html'
    return target


def main() -> int:
    errors: list[str] = []
    pages = sorted(p for p in ROOT.rglob('*.html') if not any(part in IGNORE_DIRS for part in p.parts))
    if not pages:
        errors.append('No HTML pages found')

    for page in pages:
        text = page.read_text(encoding='utf-8')
        parser = PageParser()
        parser.feed(text)
        rel = page.relative_to(ROOT)

        if not parser.html_lang:
            errors.append(f'{rel}: missing html lang attribute')
        if not parser.has_viewport:
            errors.append(f'{rel}: missing viewport meta')
        if not parser.has_main:
            errors.append(f'{rel}: missing <main> landmark')
        if not parser.has_skip_link and rel.name != '404.html':
            errors.append(f'{rel}: missing skip link')

        if rel.name != '404.html':
            if not parser.has_title:
                errors.append(f'{rel}: missing non-empty <title>')
            if not parser.has_description:
                errors.append(f'{rel}: missing meta description')
            if not parser.has_canonical:
                errors.append(f'{rel}: missing canonical link')
            if parser.h1_count != 1:
                errors.append(f'{rel}: expected exactly one h1, found {parser.h1_count}')

        duplicates = [item for item, count in Counter(parser.ids).items() if count > 1]
        if duplicates:
            errors.append(f'{rel}: duplicate ids: {duplicates}')

        for href in parser.blank_targets_without_rel:
            errors.append(f'{rel}: target=_blank missing noopener+noreferrer: {href}')

        for iframe in parser.iframes:
            src = iframe.get('src', '')
            if not iframe.get('title', '').strip():
                errors.append(f'{rel}: iframe missing title: {src}')
            if iframe.get('loading') != 'lazy':
                errors.append(f'{rel}: iframe should lazy-load: {src}')

        for href in parser.links:
            target = internal_target(page, href)
            if target is not None and not target.exists():
                errors.append(f'{rel}: broken internal reference {href!r} -> {target.relative_to(ROOT)}')

    index = (ROOT / 'index.html').read_text(encoding='utf-8')
    required_markers = (
        'hero-desktop-hq.mp4',
        'hero-mobile-hq.mp4',
        'start-a-build.html',
        'application/ld+json',
        'C-q4s1PIGtU',
        'VcQQTlrHLhE',
        'instagram.com/embed.js',
        'instagram.com/reel/DWMsagJCOXC/',
        'signal-wall.css',
    )
    for required in required_markers:
        if required not in index:
            errors.append(f'index.html: required production marker missing: {required}')
    if 'hero-desktop-lite.mp4' in index or 'hero-mobile-lite.mp4' in index:
        errors.append('index.html: lite hero video is still referenced in production markup')

    site_css = (ROOT / 'assets/site.css').read_text(encoding='utf-8')
    if 'release-hardening.css' not in site_css:
        errors.append('assets/site.css: release-hardening.css is not loaded')

    site_js = (ROOT / 'assets/site.js').read_text(encoding='utf-8')
    if "'assets/hero-" in site_js or '"assets/hero-' in site_js:
        errors.append('assets/site.js: hero path regression can create /assets/assets URLs')
    if "load('./site-base.js" not in site_js:
        errors.append('assets/site.js: base runtime is not loaded relative to the script asset')

    build_page = (ROOT / 'builds/r36-dsg-mk2.html').read_text(encoding='utf-8')
    if 'youtube-nocookie.com/embed/C-q4s1PIGtU' not in build_page:
        errors.append('R36 build page: inline Auto Rush player missing')

    sitemap = (ROOT / 'sitemap.xml').read_text(encoding='utf-8')
    for route in (
        'services/complete-custom-builds.html',
        'services/engine-dsg-swaps.html',
        'services/custom-wiring.html',
        'services/restoration-panel-paint.html',
        'services/performance-development.html',
    ):
        if route not in sitemap:
            errors.append(f'sitemap.xml: missing {route}')

    for name in ('assets/hero-desktop-hq.mp4', 'assets/hero-mobile-hq.mp4'):
        path = ROOT / name
        if not path.exists() or path.stat().st_size <= 1_000_000:
            errors.append(f'{name}: missing or unexpectedly small production video')

    if errors:
        print('SITE VALIDATION FAILED')
        for error in errors:
            print(f' - {error}')
        return 1

    print(f'SITE VALIDATION PASSED: {len(pages)} HTML pages checked')
    return 0


if __name__ == '__main__':
    sys.exit(main())
