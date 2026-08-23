# S&A Customs Website

Production-oriented website for **S&A Customs**, Reservoir Hills, Durban.

## Product goal

Turn social/media interest into qualified build enquiries while proving the workshop through documented work rather than generic claims.

## Architecture

A deliberately lightweight static architecture: semantic HTML, a responsive design system, and progressive JavaScript for navigation, reveal motion, on-demand video and the WhatsApp project brief. No framework is used because the current product has no authentication, database or application-state requirement.

## Routes

- `/` — brand, proof, projects and conversion
- `/builds/r36-dsg-mk2.html` — flagship build story
- `/workshop.html` — workshop capability narrative
- `/start-a-build.html` — qualified project brief → WhatsApp
- `/privacy.html` — privacy note
- `/404.html` — custom error route

## Quality contract

- Brand-specific automotive art direction
- Verified/documented project references only
- No stock image presented as S&A work
- Mobile-first composition and no horizontal overflow
- Keyboard focus and reduced-motion support
- YouTube loads only after explicit interaction
- Structured SEO metadata and sitemap
- Cross-browser Playwright checks
- Exact production deployment through GitHub Pages

## Local QA

```bash
python -m pip install -r requirements-dev.txt
python scripts/qa.py
python -m playwright install chromium firefox webkit
python -m http.server 4173
# in another terminal
python tests/site_test.py
```

## Public proof references

- Auto Rush R36 DSG Mk2 feature: https://www.youtube.com/watch?v=C-q4s1PIGtU
- Golf 1 customer rebuild: https://www.youtube.com/watch?v=ew-j-CzPm-Y
- R36 10.7 run: https://www.instagram.com/reel/DWMsagJCOXC/
- MK5 R32 project: https://www.instagram.com/p/DVqogUFCJ6g/
- BMW E30 325i project: https://www.instagram.com/p/DT1KjwSiKHM/
- Instagram: https://www.instagram.com/snacustoms_za/
