# Architecture

## Decision

The site remains static by design. The current requirements are content, media, qualified enquiry routing, SEO and responsive presentation — not application state. Avoiding an unnecessary framework reduces client JavaScript and operational complexity.

## Layers

- HTML: semantic content and page information architecture
- CSS: tokens, layout, responsive art direction and motion
- JavaScript: progressive enhancement only
- Playwright: cross-browser journey and overflow checks
- GitHub Actions: repeatable quality and deployment gates

## Performance decisions

- No eager YouTube player; poster first, click to load privacy-enhanced player
- No Instagram embed script; public project links instead
- Intrinsic image dimensions to reduce layout shift
- No webfont request in the critical path
- Reduced-motion fallback
