Read `AGENTS.md` before editing or running git commands; it owns this repository's workflow.

- Make assumptions - always ask for clarification

## Product screenshots, GIFs and test account

For product media, use the matching msportal-main checkout's
`docs/testing/shared-test-account.md` and `scripts/media-capture/README.md`. Those
files own the shared account, Demo authorization, capture recipes and export
workflow; read them before opening the app. Use `performance-tests@msportal.ai`
with the existing ignored `PERF_*` configuration. MSPortal Demo is the default,
with read and write testing authorized. Digacore remains read-only. Use standalone
Playwright; Codex's built-in/in-app browser is prohibited for MSPortal.

Show MSP-facing workflows for the buyers first; end-client AI flows are secondary.
Run captures from the app checkout, review the stills and complete GIF loop, then
use `media:export` for this repository. Keep credentials, raw recordings and
unreviewed demo data out of public assets.
