# gpt-skills
Collection of useful and semi-useful Skills for ChatGPT and Codex

| Skill | Description |
| --- | --- |
| [`bootstrap-project`](bootstrap-project/) | Turns rough software or product ideas into durable project foundations. It clarifies consequential decisions and creates repository guidance and a high-level project specification. |
| [`challenge-me`](challenge-me/) | Stress-tests a plan or design through a depth-first interview. It resolves material decisions one at a time and produces a concrete decision record. |
| [`close-thread`](close-thread/) | Closes a ChatGPT Work or Codex task safely. It cleans up task-owned resources, preserves repository changes, summarizes the work, and archives the task when appropriate. |
| [`prompt-architect`](prompt-architect/) | Turns rough prompt ideas into complete, production-ready prompts. It uses an iterative clarification workflow and a stable numbered decision ledger. |

## Prompt Architect plugin

Build the Prompt Architect-only local plugin package and the skill bundle used by the OpenAI plugin submission portal:

```sh
python3 .plugin/package_plugin.py --version 1.0.0
```

This creates:

- `dist/plugin/prompt-architect-1.0.0.zip` for local plugin testing.
- `dist/portal/prompt-architect.zip` for the portal's Skills upload.

The repository also includes the [directory listing copy and review fixtures](.plugin/submission/prompt-architect.md), including the required five positive and three negative tests.
