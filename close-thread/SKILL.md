---
name: close-thread
description: End-of-thread cleanup workflow for Codex. Use when the user asks to close, finish, shut down, wrap up, or archive a Codex thread, especially after implementation work in a temporary worktree. The skill frees pending resources such as dev servers, verifies git cleanliness, fast-forward merges a clean worktree back to its starting branch when applicable, and archives the thread.
---

# Close Thread

Use this skill at the end of a Codex thread to leave the workspace and thread state clean.

## Workflow

1. Identify and stop pending resources.
2. Resolve git and worktree state.
3. Archive the thread.

Prefer completing all three steps in one turn. If a step is blocked, report the blocker clearly and do not perform later destructive or ambiguous actions.

## 1. Stop Pending Resources

Find resources started during the conversation and stop only those resources.

- Check active tool sessions, terminals, app servers, file watchers, test watchers, browser sessions, background jobs, and tunnels mentioned in the thread.
- For command sessions you started, stop them gracefully first with `Ctrl-C` or the equivalent session input. Confirm the prompt returns.
- If a process was started outside a managed session, inspect it narrowly before killing it. Prefer commands that target the current repo path or known port rather than broad process name matches.
- Do not stop user-owned processes unless the thread context makes ownership clear or the user explicitly approves.
- If a dev server must remain running for the user, ask before stopping it.

Useful checks:

```bash
git status --short --branch
git worktree list --porcelain
lsof -nP -iTCP -sTCP:LISTEN
```

Use `lsof` output carefully: a listening port alone does not prove the process belongs to this thread.

## 2. Resolve Git and Worktree State

First, inspect the current repository:

```bash
git rev-parse --show-toplevel
git status --short --branch
git worktree list --porcelain
git branch --show-current
```

If there are uncommitted changes, stop and report them. Do not stash, discard, commit, or merge unless the user explicitly asks.

If the current checkout is not a linked worktree, report that there is no worktree merge to perform and continue to archive after resource cleanup.

Treat the checkout as a linked worktree when its git directory is under the common repository's worktree metadata, for example:

```bash
git rev-parse --git-dir
git rev-parse --git-common-dir
```

### Determine The Starting Branch

Merge back only to the branch the worktree was started from.

Use, in order:

1. Explicit user or thread context naming the starting branch.
2. Worktree setup metadata from the current environment, if present.
3. Git evidence that is unambiguous, such as branch reflog entries, upstream configuration, or a known base branch recorded when the worktree was created.

Do not guess from branch names alone. If the starting branch cannot be determined confidently, stop and report what evidence is missing.

### Fast-Forward Merge

When the current worktree is clean and the starting branch is known:

1. Find an existing checkout of the starting branch with `git worktree list --porcelain`.
2. If it exists, verify that checkout is clean, then run the merge from that checkout:

```bash
git -C <starting-branch-worktree> status --short --branch
git -C <starting-branch-worktree> merge --ff-only <current-worktree-branch-or-commit>
```

If the starting-branch checkout has uncommitted changes, stop and report them. Do not merge into a dirty destination worktree unless the user explicitly approves.

3. If the starting branch is not checked out anywhere, use a safe temporary checkout or switch only after confirming it will not disturb unrelated user work.
4. If `merge --ff-only` fails, stop and report the non-fast-forward condition. Do not rebase, squash, force push, or create a merge commit.

After the merge, verify:

```bash
git -C <starting-branch-worktree> status --short --branch
git -C <starting-branch-worktree> log --oneline --decorate -5
```

Do not delete the worktree unless the user explicitly requested removal.

## 3. Archive The Thread

Use the Codex thread archival tool instead of emitting raw directives.

If the thread archival tool is not already available, search for `set_thread_archived` with tool discovery and call it after resource and git handling are complete.

Archive only after reporting or resolving blockers from the previous steps. If cleanup or merge is blocked, summarize the blocker and ask whether to archive anyway.

## Final Response

Before archiving, send a concise closeout summary:

- Resources stopped or left running.
- Git cleanliness result.
- Worktree merge result, including source and destination branch when a merge occurred.
- Any blockers or follow-up actions.

Then archive the thread with the available thread archival tool.
