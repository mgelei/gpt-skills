# GPT-6 Astra Prompt Guidance

All skills in this repository run on GPT-6 Astra. The `prompt-*` skills also generate prompts for Astra, so review both the skill instructions and the prompts they produce.

## Astra-specific guidance

Based on OpenAI's [GPT-6 Astra prompting best practices](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6-astra#prompting-best-practices), reviewed September 5, 2026 for [issue #39](https://github.com/mgelei/gpt-skills/issues/39):

- **Keep authorized work moving.** Astra can ask for clarification prematurely. Infer intent from the conversation, honor prior answers and authorization, and continue work that does not depend on a missing answer. When approval is needed, first complete authorized preparation so the user can review a concrete result. Preserve actual approval boundaries and intentional interview workflows.
- **Resolve instruction conflicts.** Astra follows skill and repository instructions closely. Make user precedence over skill guidance explicit where conflicts are likely; avoid skill rules that veto the user's chosen workflow. A rule that causes a pause or divergence should be identifiable and explained.
- **Specify relevant output style.** Astra can produce more formatting and detail than needed. For ordinary prose, prefer plain language, the main point early, and connected paragraphs; use lists when they help. Preserve requested schemas, tables, headings, examples, and exact-output contracts.
- **Calibrate delegation to the workflow.** When collaboration tools exist and independent work benefits from delegation, specify the trigger and useful handoff. Do not add delegation requirements to trivial tasks or prompts for environments without those tools.
- **Calibrate verification to risk.** For coding work, complete required checks and choose tests that can detect meaningful failures. Avoid redundant tests that merely mirror a reversible, low-impact edit. Stop after appropriate checks pass unless changes, failures, or unresolved concerns justify more testing.

These are conditional controls, not a block to paste into every prompt. OpenAI does not prescribe a universal skill template, prompt length, or number of subagents.

## General prompt design

The following are repository design principles, rather than additional Astra-specific claims:

- Preserve the user's objective, priorities, constraints, meaningful subgoals, and action boundaries. Do not invent requirements, facts, tool capabilities, or authorization.
- State the deliverable and useful success criteria directly. Include enough context and evidence requirements to complete the task; distinguish source material from instructions.
- Keep each rule in one place. Retain procedural detail when it protects an output contract, fragile operation, or known failure mode; otherwise prefer outcomes and decision criteria.
- Ask only questions that affect the result and cannot be resolved from available context. Respect a requested interview, and state material assumptions when proceeding.
- Report observed results honestly. Distinguish attempted, partial, and verified work; never invent tool results or claim tests ran when they did not.

## Audit outcome

The September 2026 audit used a Sol research memo followed by Astra audits and edits:

| Skill | Decision |
| --- | --- |
| `prompt-architect` | Target Astra, resolve user/skill priority, and apply relevant autonomy, style, delegation, and verification controls to generated prompts. Preserve its decision ledger and finalization contract. |
| `prompt-upgrade` | Target Astra and audit generated prompts for the same conditional controls while preserving intent and required output. |
| `bootstrap-project` | Remove the skill-level veto of user autonomy; reuse prior decisions and authorization without presenting unconfirmed choices as settled. |
| `challenge-me` | No change: the depth-first interview is the requested product behavior. |
| `close-thread` | No change: ownership checks, bounded retries, preservation, and archival gates protect against concrete data-loss risks. |

Validation includes structural skill checks, packaging, and static scenario review. These checks do not demonstrate model-level quality or token savings. Future behavioral comparisons should exercise routine ambiguity, genuinely missing decisions, prior authorization, exact output formats, and tool failures; for prompt generators, also run the resulting prompts on representative downstream tasks.

The published [Plugin Terms](https://mate.gelei.dev/plugin-terms/) and [Plugin Privacy Policy](https://mate.gelei.dev/plugin-privacy/) were checked. No update is needed for these instruction changes: they add no services, publisher-side data handling, or action permissions.
