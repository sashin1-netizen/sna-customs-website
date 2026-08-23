# Deployment

Production is GitHub Pages from `main` through `.github/workflows/deploy-pages.yml`.

Release sequence:
1. Open PR from a feature/fix branch.
2. Required `Quality gates` must pass.
3. Review responsive screenshots and diff.
4. Squash/merge to `main`.
5. Pages workflow deploys the exact merged commit.
6. Verify production HTTP response and key journeys on mobile and desktop.

Rollback: revert the merge commit or move `main` back through a normal reviewed revert; do not force-push protected history.
