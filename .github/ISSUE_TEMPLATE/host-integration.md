---
name: Host integration issue
about: A host (Claude, Codex, Kiro, Cursor) didn't discover or run Kedu correctly
title: "[host] "
labels: ["host-integration", "developer-preview"]
---

**Host**
Which agent and surface:
- [ ] Claude Code (CLI / desktop)
- [ ] Codex (CLI / desktop)
- [ ] Kiro (CLI / IDE)
- [ ] Cursor (CLI / desktop)
- Host version:

**What happened**
e.g. the agent didn't find Kedu, didn't read `.kedu/STATE.md`, answered from the summary
instead of searching, or couldn't run `kedu log`/`kedu search`.

**How you invoked it**
The prompt or command you used (`/kedu …`, `$kedu …`, or natural language).

**Expected vs actual**
- Expected:
- Actual:

**Setup**
- Output of `kedu init --host <host>` (or how you wired it):
- Does `kedu search --scope current_project --query "…"` work directly in a terminal?
- `kedu --version`:

**Anything else**
Transcript snippet, screenshots, or the generated host files (`.kiro/…`, `.claude/…`, etc.).
