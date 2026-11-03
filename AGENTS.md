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
