# S&A Customs Website

Standalone client website for **S&A Customs**, Reservoir Hills, Durban, South Africa.

## Current build

This repository now contains the active client-facing GitHub Pages build, not the earlier single-file prototype.

The site currently includes:

- Cinematic R36-led hero treatment using real S&A-related media
- Documented 10.7 @ 209 km/h R36 performance proof
- Build archive presentation
- Integrated Auto Rush / customer video coverage
- Workshop capability sections
- Mobile-first responsive behaviour
- Scroll-reveal interaction system
- Separate production CSS and JavaScript assets
- WhatsApp-led enquiry flow
- Independent GitHub Pages deployment

## Structure

```text
.
├── index.html
├── assets/
│   ├── site.css
│   └── site.js
├── .github/
│   └── workflows/
│       └── deploy-pages.yml
├── .nojekyll
└── README.md
```

## Creative direction

South African automotive culture meets modern editorial and motorsport presentation.

The visual system prioritises S&A's actual builds, documented performance, workshop disciplines and third-party automotive coverage instead of generic mechanic-site conventions.

## Content rules

- Real S&A media first
- No fabricated awards or specifications
- Third-party media used as supporting proof
- Placeholder imagery must never be presented as an S&A-owned build
- Mobile presentation is treated as primary because discovery is expected to come heavily from social and WhatsApp

## Business information

S&A Customs  
19 Pridley Road  
Reservoir Hills, Durban, South Africa  
info@snacustoms.co.za

## Deployment

GitHub Pages deploys from `main` through `.github/workflows/deploy-pages.yml`.
