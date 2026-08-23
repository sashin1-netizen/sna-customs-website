from pathlib import Path
from bs4 import BeautifulSoup
import json, re, sys
root=Path(__file__).resolve().parents[1]
htmls=['index.html','workshop.html','builds/r36-dsg-mk2.html','start-a-build.html','privacy.html','404.html']
errors=[]
for name in htmls:
    path=root/name
    if not path.exists(): errors.append(f'missing {name}'); continue
    soup=BeautifulSoup(path.read_text(encoding='utf-8'),'html.parser')
    if not soup.find('meta',attrs={'name':'viewport'}): errors.append(f'{name}: missing viewport')
    if not soup.title or not soup.title.string.strip(): errors.append(f'{name}: missing title')
    if name not in ('privacy.html','404.html') and len(soup.find_all('h1')) != 1: errors.append(f'{name}: expected exactly one h1')
    for img in soup.find_all('img'):
        if not img.has_attr('alt'): errors.append(f'{name}: image missing alt')
        if not img.get('width') or not img.get('height'): errors.append(f'{name}: image missing intrinsic dimensions')
    for a in soup.find_all('a',href=True):
        href=a['href']
        if href.startswith(('http://','https://','mailto:','tel:','#')): continue
        clean=href.split('#')[0]
        target=(path.parent/clean).resolve()
        if clean and not target.exists(): errors.append(f'{name}: broken local href {href}')
index=(root/'index.html').read_text(encoding='utf-8')
if '<iframe' in index: errors.append('index.html must not eagerly load iframe video')
if 'instagram-media' in index: errors.append('index.html must not eagerly load Instagram embed script')
css=(root/'assets/site.css').read_text(encoding='utf-8')
if 'prefers-reduced-motion' not in css: errors.append('reduced-motion handling missing')
if re.search(r'min-width\s*:\s*[5-9]\d\dpx',css): errors.append('suspicious large fixed min-width')
if errors:
    print('\n'.join('ERROR: '+e for e in errors)); sys.exit(1)
print('Static QA passed')
