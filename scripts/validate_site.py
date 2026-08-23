from __future__ import annotations

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
        self.has_title = False
        self.has_description = False
        self.has_canonical = False
        self.has_main = False
        self.h1_count = 0
        self._in_title = False
        self._title_text = []

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if tag == 'a' and data.get('href'):
            self.links.append(data['href'])
        if tag in {'img', 'script', 'source', 'link'}:
            for key in ('src', 'href'):
                if data.get(key):
                    self.links.append(data[key])
        if tag == 'title':
            self._in_title = True
        elif tag == 'meta' and data.get('name', '').lower() == 'description' and data.get('content', '').strip():
            self.has_description = True
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

        if rel.name != '404.html':
            if not parser.has_title:
                errors.append(f'{rel}: missing non-empty <title>')
            if not parser.has_description:
                errors.append(f'{rel}: missing meta description')
            if not parser.has_canonical:
                errors.append(f'{rel}: missing canonical link')
        if not parser.has_main:
            errors.append(f'{rel}: missing <main> landmark')
        if rel.name != '404.html' and parser.h1_count != 1:
            errors.append(f'{rel}: expected exactly one h1, found {parser.h1_count}')

        for href in parser.links:
            target = internal_target(page, href)
            if target is not None and not target.exists():
                errors.append(f'{rel}: broken internal reference {href!r} -> {target.relative_to(ROOT)}')

    index = (ROOT / 'index.html').read_text(encoding='utf-8')
    for required in ('hero-desktop-hq.mp4', 'hero-mobile-hq.mp4', 'start-a-build.html', 'application/ld+json'):
        if required not in index:
            errors.append(f'index.html: required production marker missing: {required}')
    if 'hero-desktop-lite.mp4' in index or 'hero-mobile-lite.mp4' in index:
        errors.append('index.html: lite hero video is still referenced in production markup')

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

    if errors:
        print('SITE VALIDATION FAILED')
        for error in errors:
            print(f' - {error}')
        return 1

    print(f'SITE VALIDATION PASSED: {len(pages)} HTML pages checked')
    return 0


if __name__ == '__main__':
    sys.exit(main())
