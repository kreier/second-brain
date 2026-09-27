# Phase 6 — Public GitHub Demonstration

**Status:** Scheduled  
**Target Environment:** GitHub Pages (`kreier.github.io/second-brain`)  
**Prerequisites:** [Phase 1](phase-01-foundation.md), [Phase 4](phase-04-statistics.md)

---

## 1. Objective
Create a public, interactive web demonstration deployed to GitHub Pages. Because the real Second Brain operates in an airgapped private vault with personal data, this public demo runs purely client-side using safe, synthetic demo datasets to showcase the UI, funnel statistics, knowledge navigation, and architecture without exposing any private information.

---

## 2. Deliverables
- [ ] Safe synthetic demo fixture dataset (mock sources, sample atomized notes, mock funnels).
- [ ] Client-side demo mode toggle in the React application (intercepting API calls with mock fixtures).
- [ ] GitHub Actions workflow to build and deploy the React demo to GitHub Pages on tag/release.
- [ ] Interactive walkthrough banner explaining the architecture and airgapped design.

---

## 3. Acceptance Criteria
```text
[ ] GitHub Pages deployment builds successfully via GitHub Actions
[ ] Navigating the live GitHub Pages URL loads all 5 views cleanly without runtime errors
[ ] Zero private or real personal data is bundled into the demo distribution
[ ] Interactive UI allows visitors to test search, view the growth funnel, and inspect mock pipeline runs
```
