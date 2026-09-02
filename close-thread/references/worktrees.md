# Worktree Preservation

Read this reference before committing, integrating, handing off, or archiving from an ordinary linked worktree or ChatGPT desktop managed worktree.

Establish the intended or destination branch only from explicit user or task context, recorded setup metadata, or unambiguous Git evidence. Ask if it cannot be established safely. Never create a branch unless the user explicitly requests one.

## ChatGPT Desktop Managed Worktrees

Treat a worktree as app-managed only when reliable task context or environment metadata establishes it. These worktrees commonly start on detached `HEAD` and may contain copied local changes.

- To continue in the local checkout, prefer the desktop app's **Hand off** flow; do not imitate it with a manual merge.
- Do not recommend **Create branch here** by default. If work belongs on the verified starting branch but the managed worktree cannot safely update it, use **Hand off** first.
- Before archival, explain that the app may remove the managed worktree after saving a recovery snapshot. A snapshot is recovery, not a substitute for the intended handoff, commit, push, or delivery.
- Do not archive while useful work exists only in the managed worktree unless it was handed off, committed or pushed as authorized, or the user explicitly accepts snapshot-only recovery.
- Never manually delete or prune an app-managed worktree while closing.

If Handoff is required but unavailable, give the exact supported UI action and pause archival until the user completes it or chooses another preservation path.

## Ordinary Linked Worktrees

Do not merge unless the user explicitly requested integration. For an authorized fast-forward merge:

1. Verify the destination branch and find its checkout with `git worktree list --porcelain`.
2. Require clean source and destination worktrees unless the user separately authorizes how to preserve source changes.
3. Run from the destination checkout:

   ```bash
   git -C <destination-worktree> merge --ff-only <source-branch-or-commit>
   ```

4. Verify the destination status and recent log.

If fast-forwarding fails, report the divergence and stop. Do not rebase, squash, force-push, or create a merge commit without separate authorization.
