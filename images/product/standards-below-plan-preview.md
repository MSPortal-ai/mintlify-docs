# Below plan preview provenance and release follow-up

App PR: https://github.com/MSPortal-ai/msportal-main/pull/2967
App branch: `t3/standards-below-plan-status`.
Source: supplied `screenshots/standards-below-plan-*.png` from that app checkout.
All six PNGs visually reviewed for content, legibility and privacy; synthetic companies only.
These are fixture-backed branch previews. The app implementation agent reports a clean 14-test desktop/phone fixture pass. This docs change does not rerun that pass or claim database persistence.
Pending, not deployed: `20261118215353_standards_below_plan.sql`.

## Stable replacement assets

- `standards-below-plan-menu-desktop.png` (2880 × 1920): `user-guides/msp-tools/update-standard-deployments.mdx`.
- `standards-below-plan-menu-mobile.png` (780 × 1688): `user-guides/msp-tools/update-standard-deployments.mdx`.
- `standards-below-plan-saved-desktop.png` (2880 × 1920): `user-guides/msp-tools/read-standards-matrix.mdx`.
- `standards-below-plan-saved-mobile.png` (780 × 1688): `user-guides/msp-tools/read-standards-matrix.mdx`.
- `standards-below-plan-customer-success-desktop.png` (2880 × 1920): `user-guides/msp-tools/read-client-health-details.mdx`.
- `standards-below-plan-customer-success-mobile.png` (780 × 1688): `user-guides/msp-tools/read-client-health-details.mdx`.

## After authorized release and migration rollout

- Verify a real MSPortal Demo company and site can save Below plan and retain it after reload; verify bulk scope, required-gap counts and Customer Success badge.
- Verify linked Planner Not Started reconciliation preserves the assessment, and another Standards status clears it. Check RPC authorization and tenant/company isolation in the app verification follow-up.
- Replace these six assets at the same paths with reviewed production Demo captures of the menu, saved matrix and Customer Success list at desktop and phone sizes; update dimensions if needed.
- Remove Below plan preview notices/captions from the nine changed guides only after those checks, and record the production capture provenance here.
