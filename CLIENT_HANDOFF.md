# S&A Customs — Client Handoff

## Release objective

Present S&A Customs as a distinctive Durban custom automotive workshop, prove real capability with verified project evidence, and convert serious visitors into structured WhatsApp project enquiries.

## Implemented

- Dark motorsport/editorial design system with carbon, graphite, race-ivory and heat-orange palette.
- Responsive HQ burnout-video hero using dedicated desktop and mobile files with a resilient poster fallback.
- Documented R36 DSG Mk2 proof: 10.7 @ 209 km/h.
- Visible S&A Signal media wall with two inline YouTube players and the verified S&A Instagram track-proof reel.
- Direct YouTube/Instagram fallbacks if an external embed is blocked by a browser or privacy setting.
- Dedicated R36 build story with an inline Auto Rush player rather than a static thumbnail pretending to be video.
- Complete custom-build positioning built around whole-car integration.
- Dedicated service-intent landing pages for complete custom builds, engine + DSG swaps, custom wiring, restoration / panel + paint and performance development.
- Workshop page routes visitors into those service pages.
- Structured Start Your Build intake that opens a preformatted WhatsApp brief for user review.
- Service pages pre-select the relevant work type in the project brief.
- WhatsApp handoff falls back to same-tab navigation if a browser blocks the new window.
- Project-intake progress indicator responds to the active stage.
- Conversion-event hooks for project brief, WhatsApp, phone and proof-video interactions (`dataLayer`).
- Local business structured data on the homepage.
- Canonical URLs, descriptions, robots.txt and expanded sitemap.
- Privacy page and branded 404 page.
- Mobile touch-target, safe-area, reduced-motion and media-fallback hardening.
- GitHub Pages deployment now validates the exact release before upload. Failed validation blocks deployment.
- Static release validator covers internal links, page essentials, duplicate IDs, external-link safety, iframe accessibility/lazy loading, service sitemap routes, social/video markers, correct hero runtime paths and production HQ media sizes.

## Root-cause fixes completed

- Fixed the runtime bug that could resolve hero media to `/assets/assets/...` and leave the hero using a fallback or stale visual.
- Removed the runtime source rewrite; production HTML now owns the correct responsive HQ video sources.
- Expanded Instagram CSP permissions and retained the official Instagram embed script.
- Added direct social/video fallbacks so external embed restrictions do not leave empty sections.
- Replaced stale `client-1`/older asset references across the core journey with the final `ready-1` release key.
- Brought Workshop, Start Your Build, all service pages, the R36 build page, Privacy and 404 into the same release system.

## Verified client facts used on the site

- S&A Customs location: 19 Pridley Road, Reservoir Hills, Durban.
- Contact: +27 74 794 2955 and +27 69 401 9364.
- Instagram: @snacustoms_za.
- Workshop capabilities currently represented: complete custom builds, engine + DSG swaps, custom wiring, panel + paint, restoration / OEM+, performance development.
- R36 DSG Mk2 documented personal best: 10.7 @ 209 km/h.
- Golf 1 project travelled from the Eastern Cape to Durban for the work.

## Not fabricated / intentionally not claimed

The site does not invent awards, staff qualifications, years in business, customer-review scores, dyno figures, warranties, turnaround times or performance claims beyond evidence already available to the project. TikTok is not embedded because a verified S&A TikTok account/post has not yet been supplied.

## Client inputs still needed before custom-domain launch

These are not blockers for the GitHub Pages client preview, but should be supplied before the final commercial-domain launch if required:

1. Final custom domain and DNS access.
2. Preferred analytics platform and measurement ID (event hooks are already present).
3. Verified Google Business Profile URL, if available.
4. Approved customer testimonials/reviews, with permission to publish.
5. Additional original build photos/videos for richer project case studies.
6. Confirmed trading hours, if they should appear in structured data and contact sections.
7. Confirmation of the preferred public email address and whether both phone numbers should remain primary.
8. Verified TikTok URL/posts if S&A wants TikTok represented in the live feed.

## Client review checklist

- Homepage clearly communicates what S&A does within the first screen.
- HQ hero media loads, with a poster fallback when video cannot autoplay.
- YouTube players render in the S&A Signal section and on the R36 build page; direct links remain available if embedding is blocked.
- Instagram reel renders where supported; direct verified reel/profile links remain available if Instagram blocks embedding.
- All published proof is accurate.
- Service descriptions match the workshop's actual scope.
- Every major service route reaches a relevant project brief.
- WhatsApp and telephone contact details are correct.
- Mobile navigation, forms and CTAs are usable.
- No client-owned media is being presented without permission.

## Release state

`main` and the `gh-pages` fallback branch are kept on the same release commit. The GitHub Pages workflow validates the site before deploying the artifact. The remaining external verification for a client presentation is the completed GitHub Pages run plus a final live-browser smoke test on the actual Pages URL.
