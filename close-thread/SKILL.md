---
name: close-thread
description: Safely close or archive the current ChatGPT Work conversation, Codex desktop task, or Codex CLI session. Use when the user asks to close, finish, wrap up, shut down, or archive the current work. Stop only task-owned resources, preserve Git and worktree changes, and use the current surface's supported archival or handoff path without losing work.
---

# Close Thread

Close the current work safely. Treat resource cleanup, workspace preservation, code integration, and archival as separate actions with separate authorization requirements.

A successful close leaves no confirmed task-owned resource running unintentionally, preserves or explicitly accounts for all useful workspace changes, gives the user a concise closeout summary, and archives through the current surface when requested, supported, and safe.

## Workflow

Perform the applicable steps in this order:

1. Stop resources owned by this task.
2. Inspect and preserve workspace changes.
3. Send a closeout summary.
4. Archive through the current surface when requested or clearly implied by the user's request.

Skip steps that do not apply, such as Git inspection in a web-only conversation. Continue in one turn when no user decision is required. If an action could lose work, affect a resource of uncertain ownership, or requires authorization the user has not provided, stop before that action and ask exactly one focused question.

Do not report an action as successful without evidence from the relevant tool, process state, Git output, API result, or supported surface behavior.

## 1. Stop Task-Owned Resources

Stop only resources that this task started or clearly owns.

- Use conversation context and managed tool-session state first to identify terminals, development servers, file or test watchers, browser sessions, background jobs, application servers, and tunnels.
- Interrupt a managed command session gracefully with `Ctrl-C` or the equivalent session input, then confirm that it exited.
- For an unmanaged process, verify ownership using the exact PID, command, repository path, or other task-specific evidence before stopping it. A matching process name or listening port alone is insufficient.
- Leave user-owned and uncertain processes running. Ask before stopping a server or session the user may still need.
- Do not enumerate every system process or port when narrower evidence is available.
- If a graceful interrupt fails, retry once when safe. Otherwise leave the process running and report the failure and identifying evidence.

## 2. Preserve Workspace Changes

If the task has no local workspace or repository, state that in the closeout summary and continue.

For a Git repository, inspect without mutating:

```bash
git rev-parse --show-toplevel
git status --short --branch
git branch --show-current
git worktree list --porcelain
git rev-parse --git-dir
git rev-parse --git-common-dir
```

Use the results together with reliable task or environment context to classify the checkout as:

- a local checkout;
- an ordinary linked worktree; or
- a ChatGPT desktop managed worktree.

Do not infer worktree ownership, management status, or the starting branch from a directory or branch name alone.

Report staged, unstaged, and untracked changes. A request to close or archive does not authorize committing, stashing, discarding, resetting, merging, rebasing, pushing, deleting a worktree, pruning worktrees, or creating a branch.

When the user authorizes a commit, establish the intended branch from explicit user or task context, recorded setup metadata, or unambiguous Git evidence. Do not create a new branch unless the user explicitly requests one. If the intended branch cannot be established safely, ask before committing.

### ChatGPT Desktop Managed Worktrees

Treat a worktree as app-managed only when reliable task context or environment metadata establishes that fact. These worktrees commonly begin on detached `HEAD` and may contain copied local changes from the selected starting state.

- If the user wants to continue in the local checkout, prefer the desktop app's supported **Hand off** flow. Do not imitate Handoff with a manual merge.
- If the user wants to keep working in the managed worktree, do not recommend **Create branch here** by default.
- When the work should ultimately land on the verified starting branch, use **Hand off** first if the detached or app-managed worktree cannot update that branch safely.
- Before archiving, explain that the desktop app may remove a managed worktree after saving a recovery snapshot. Treat the snapshot as recovery only, not as a substitute for the user's intended handoff, commit, push, or delivery path.
- Do not archive while useful work exists only in the managed worktree unless it has been handed off, committed or pushed as authorized, or the user explicitly accepts snapshot-only recovery.
- Do not manually delete or prune a managed worktree as part of closing the task.

If Handoff is required but cannot be invoked from the current task, tell the user the exact supported UI action to take. Pause archival until the user completes it or explicitly chooses another preservation path.

### Ordinary Linked Worktrees

Do not merge merely because the user asked to close or archive. Merge only when the user explicitly requested integration.

For an authorized fast-forward merge:

1. Establish the destination branch from explicit user or task context, recorded setup metadata, or unambiguous Git evidence. Never guess from branch names.
2. Require a clean source worktree unless the user separately authorizes how to preserve its changes.
3. Find the destination checkout with `git worktree list --porcelain` and require it to be clean.
4. Run the merge from the verified destination checkout:

```bash
git -C <destination-worktree> merge --ff-only <source-branch-or-commit>
```

5. Verify the destination status and recent log.

If the fast-forward fails, report the divergence and stop. Do not rebase, squash, force-push, or create a merge commit without separate authorization.

### Local Checkouts

Leave authorized unfinished changes in place and report them. Ask how to preserve or publish them only when the requested cleanup or archival could make them inaccessible.

## 3. Send the Closeout Summary

Before attempting archival, send a concise user-visible summary containing:

- resources stopped, including confirmation evidence, and resources deliberately left running;
- whether a local workspace exists and, when applicable, its Git cleanliness;
- where useful changes remain and how they were preserved;
- any authorized Handoff, branch creation, commit, push, or merge result;
- any blocker and the single next action required from the user.

Do not promise that the summary will remain visible after archival unless the current surface documents that behavior.

If archival cannot proceed safely, end with the focused question required to resolve the blocker. Do not claim that the task is closed.

## 4. Archive Through the Current Surface

Use only an archival capability actually exposed by the current surface.

- In ChatGPT Work or the ChatGPT desktop app, invoke an available task or conversation archive action only after the closeout summary and preservation checks succeed. If no callable archive action is exposed, tell the user to use the task or conversation menu.
- In Codex CLI, tell the user to enter `/archive` after the closeout response. Do not invoke a nested `codex archive` shell command.
- In an app-server integration, use `thread/archive` only when that API is available and the exact current thread ID is already supplied by trusted runtime context.
- Never inspect local session transcripts, archived-session directories, or unrelated conversation history to discover a thread ID.
- Do not substitute deletion for archival. Deletion is permanent and requires a separate explicit request.

If preservation or cleanup remains blocked, state the consequence and ask whether the user wants to archive anyway. Archive only after they explicitly accept that consequence.

Attempt archival once. If the result is missing, ambiguous, or unsuccessful, do not repeatedly retry or claim success. Report the result and the supported manual action, if one is known.

After a confirmed archive action, stop. Do not begin unrelated cleanup or additional work.
