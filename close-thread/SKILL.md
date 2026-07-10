---
name: close-thread
description: Close a ChatGPT Work or Codex task, chat, thread, or CLI session safely. Use when the user asks to close, finish, wrap up, shut down, or archive the current work. Clean up only resources owned by the task, preserve Git and worktree changes, use the surface's supported handoff or archival path, and avoid losing work when archiving a Codex-managed worktree.
---

# Close Thread

Close the current work safely across ChatGPT Work, Codex in the ChatGPT desktop app, and Codex CLI. Treat cleanup, moving code, and archiving as separate decisions.

## Workflow

1. Stop resources owned by this task.
2. Inspect and preserve workspace changes.
3. Send a closeout summary.
4. Archive through the current surface when available and safe.

Complete the applicable steps in one turn. Skip irrelevant steps, such as Git checks in a web-only Work chat. If a step exposes possible data loss or requires a choice the user has not made, stop before the risky action and ask one focused question.

## 1. Stop Task-Owned Resources

Stop only resources that this task started or clearly owns.

- Use conversation and tool-session state first to identify terminals, dev servers, file or test watchers, browser sessions, background jobs, app servers, and tunnels.
- Interrupt managed command sessions gracefully with `Ctrl-C` or the equivalent session input, then confirm termination.
- For an unmanaged process, inspect the exact PID, repository path, command, or known port before stopping it. A matching process name or listening port alone is insufficient proof of ownership.
- Leave user-owned and uncertain processes running. Ask before stopping a server the user may still need.
- Do not enumerate every system process or port when narrower evidence is available.

## 2. Preserve Workspace Changes

If the task has no local workspace or repository, report that and continue.

For a Git repository, inspect without mutating:

```bash
git rev-parse --show-toplevel
git status --short --branch
git branch --show-current
git worktree list --porcelain
git rev-parse --git-dir
git rev-parse --git-common-dir
```

Classify the checkout as Local, an ordinary linked worktree, or a ChatGPT desktop managed worktree. Do not infer ownership or the starting branch from a directory or branch name alone.

Report staged, unstaged, and untracked changes. Closing does not by itself authorize committing, stashing, discarding, resetting, merging, rebasing, pushing, deleting a worktree, or creating a branch.

### ChatGPT Desktop Managed Worktrees

Treat a worktree created for a desktop Codex task as app-managed when task context or reliable environment metadata establishes that fact. These worktrees normally begin on detached `HEAD` and may include a copy of local uncommitted changes from the selected starting branch.

- If the user wants to continue in the local checkout, prefer the desktop app's **Hand off** flow. It moves the task and Git state safely. Do not imitate Handoff with a manual merge.
- If the user wants to keep working in the worktree, recommend **Create branch here** before committing, pushing, or opening a pull request.
- Before archiving, explain that the desktop app may automatically remove a managed worktree after saving a recovery snapshot. Treat that snapshot as recovery, not as a substitute for the user's intended delivery path.
- Do not archive while useful work exists only in the managed worktree unless it has been handed off, committed or pushed as authorized, or the user explicitly chooses archival with snapshot-only recovery.
- Do not delete or prune a managed worktree manually as part of closing the task.

If Handoff is not callable from the current task, tell the user exactly which UI action is needed and pause archival until they complete it or choose another preservation path.

### Ordinary Linked Worktrees

Do not merge merely because the user said "close" or "archive." Merge only when the user explicitly asked to integrate the work.

For an authorized fast-forward merge:

1. Establish the destination branch from explicit user or task context, recorded setup metadata, or unambiguous Git evidence. Never guess from branch names.
2. Require a clean source worktree unless the user separately authorizes how to preserve its changes.
3. Find the destination checkout with `git worktree list --porcelain` and require it to be clean.
4. Run the merge from the destination checkout:

```bash
git -C <destination-worktree> merge --ff-only <source-branch-or-commit>
```

5. Verify the destination status and recent log.

If fast-forwarding fails, report the divergence. Do not rebase, squash, force-push, or create a merge commit without separate authorization.

### Local Checkouts

Leave authorized, unfinished local changes in place and report them. Ask how to preserve or publish them only when the requested archival or cleanup could make them inaccessible.

## 3. Send The Closeout Summary

Before any archive action, send a concise summary containing:

- resources stopped and resources deliberately left running;
- workspace and Git cleanliness;
- where useful changes remain and how they were preserved;
- any Handoff, branch creation, commit, push, or merge result;
- blockers and the one next action required from the user, if any.

Do not promise that the summary will remain visible after an archive action unless the surface documents that behavior.

## 4. Archive Through The Current Surface

Use only an archive capability actually exposed by the current surface.

- In ChatGPT Work or the ChatGPT desktop app, call an available task or chat archive action only after the closeout summary and preservation checks. If no callable archive action is exposed, tell the user to use the task or chat menu; do not invent a tool name or emit a raw control directive.
- In Codex CLI, explain that the user can enter `/archive` after this turn. Do not try to archive the active CLI session by invoking a nested `codex archive` shell command.
- In an app-server integration, use `thread/archive` only when that API is available and the exact current thread ID is already supplied by trusted runtime context.
- Never inspect local session transcripts, archived-session directories, or unrelated conversation history to discover a thread ID.
- Do not substitute deletion for archival. Deletion is permanent and requires an explicit, separate request.

If preservation or cleanup remains blocked, ask whether to archive anyway and state the consequence. Otherwise, archive once and stop.
