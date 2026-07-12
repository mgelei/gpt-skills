# gpt-skills
Collection of useful and semi-useful Skills for ChatGPT and Codex

| Skill | Description |
| --- | --- |
| [`bootstrap-project`](bootstrap-project/) | Turns rough software or product ideas into durable project foundations. It clarifies consequential decisions and creates repository guidance and a high-level project specification. |
| [`challenge-me`](challenge-me/) | Stress-tests a plan or design through a depth-first interview. It resolves material decisions one at a time and produces a concrete decision record. |
| [`close-thread`](close-thread/) | Closes a ChatGPT Work or Codex task safely. It cleans up task-owned resources, preserves repository changes, summarizes the work, and archives the task when appropriate. |
| [`prompt-architect`](prompt-architect/) | Turns rough prompt ideas into complete, production-ready prompts. It uses an iterative clarification workflow and a stable numbered decision ledger. |

## Store package

Publishing a GitHub Release with a strict semver tag such as `v1.0.1` runs the
[`Package ChatGPT plugin`](.github/workflows/package-plugin.yml) workflow. The
workflow packages all four skills with the store manifest and logo, injects
`1.0.1` as the manifest version, and attaches
`prompt-architect-friends-1.0.1.zip` to the release.

Build the same ZIP locally with:

```sh
python3 .plugin/package_plugin.py --version 1.0.1
```
