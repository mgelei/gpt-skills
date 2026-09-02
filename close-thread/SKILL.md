---
name: close-thread
description: Safely close or archive the current ChatGPT Work conversation, Codex desktop task, or Codex CLI session. Use when the user asks to close, finish, wrap up, shut down, or archive current work. Stop only task-owned resources, preserve workspace changes, and use the supported handoff or archival path without losing work.
---

# Close Thread

Close the current work without losing user data. Treat resource cleanup, Git mutations, code integration, and archival as separate actions with separate authorization.

Work in this order:

1. Stop task-owned resources.
2. Inspect and preserve workspace changes.
3. Send a closeout summary.
4. Archive when requested or clearly implied, supported, and safe.

Skip irrelevant steps, such as Git inspection in a web-only conversation. Continue in one turn unless an action risks data loss, affects a resource of uncertain ownership, or lacks required authorization. In that case, stop before the action and ask exactly one focused question. Never report success without evidence from the relevant tool, process state, Git output, API result, or supported surface behavior.

## Stop Task-Owned Resources

Use conversation context and managed tool-session state to identify terminals, servers, watchers, browser sessions, background jobs, and tunnels started by this task.

- Interrupt managed sessions gracefully, then confirm they exited. Retry once when safe; otherwise report the failure and leave them running.
- Before stopping an unmanaged process, verify ownership from its exact PID, command, repository path, or similarly task-specific evidence. A process name or port alone is insufficient.
- Leave user-owned or uncertain resources running. Ask before stopping anything the user may still need.
- Prefer narrow ownership checks over enumerating all system processes or ports.

## Preserve Workspace Changes

If there is no local workspace or repository, say so in the closeout summary and continue.

For a Git repository, inspect without mutating:

```bash
git rev-parse --show-toplevel
git status --short --branch
git branch --show-current
git worktree list --porcelain
git rev-parse --git-common-dir
```

Use reliable task or environment context with this output to classify the checkout as local, an ordinary linked worktree, or a ChatGPT desktop managed worktree. Never infer worktree ownership, management, or the starting branch from directory or branch names alone.

Report staged, unstaged, and untracked changes. Closing does not authorize committing, stashing, discarding, resetting, merging, rebasing, pushing, branch creation, or worktree deletion or pruning.

For any linked or app-managed worktree, read [references/worktrees.md](references/worktrees.md) before committing, integrating, handing off, or archiving.

For a local checkout, leave unfinished changes in place and report them. Ask how to preserve or publish them only when cleanup or archival could make them inaccessible.

## Send the Closeout Summary

Before archival, send a concise user-visible summary covering:

- resources stopped, with confirmation, and resources deliberately left running;
- whether a workspace exists and, when applicable, its Git cleanliness;
- where useful changes remain and how they were preserved;
- any authorized Handoff, branch, commit, push, or merge result;
- any blocker and the one next action required from the user.

Do not promise the summary will remain visible after archival unless the surface documents that behavior. If archival is unsafe, end with the focused question needed to resolve the blocker and do not claim the task is closed.

## Archive Through the Current Surface

Use only an archive capability exposed by the current surface:

- In ChatGPT Work or the desktop app, invoke the available task or conversation archive action only after the summary and preservation checks. If no callable action exists, direct the user to the task or conversation menu.
- In Codex CLI, tell the user to enter `/archive` after this response. Do not invoke a nested `codex archive` shell command.
- In an app-server integration, use `thread/archive` only when that API is available and trusted runtime context already supplies the exact current thread ID.

Never inspect session transcripts, archived-session directories, or unrelated conversation history to discover a thread ID. Never substitute deletion for archival; deletion requires a separate explicit request.

If cleanup or preservation remains blocked, state the consequence and ask whether to archive anyway. Proceed only if the user accepts it. Attempt archival once; if the result is missing, ambiguous, or unsuccessful, report it and any known supported manual action without retrying or claiming success.

After confirmed archival, stop.
