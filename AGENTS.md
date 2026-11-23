# Mintlify documentation

Every docs change (guides, screenshots, release notes) lands through a ready
pull request, so pending work stays visible on GitHub instead of sitting in a
checkout. A merge to `main` publishes the docs.

Edit in the worktree that `bun run agent:docs worktree [branch]` prints from
the sibling msportal-main checkout; this shared checkout stays on `main` for
reading. The workflow (branch names, when a docs PR merges, release notes,
handoffs) is in that checkout's `docs/agents/git.md` › Mintlify documentation.
For product media and content verification, follow `claude.md` and the app
checkout's `msportal-docs` skill.

## MSP Guides copies

Mintlify opens a page in the first tab that lists it, so a page listed in both
Company Guides and MSP Guides would pull MSP readers into Company Guides. MSP
Guides therefore lists `msp-guides/<path>` for every page Company Guides shares.
Most of those files are generated from `user-guides/<path>` and say so in a
comment under the frontmatter; the rest are hand-maintained MSP versions.

- Edit the `user-guides` page, never a generated copy.
- To share a page with MSP Guides, list its `user-guides/<path>` in both tabs.
- After any change to `user-guides` or `docs.json`, run
  `python3 scripts/sync-msp-guides.py` and commit what it writes. It moves the
  MSP navigation entry, regenerates the copies, points their links at MSP pages,
  and deletes copies that left the navigation. `--check` only reports.
