# GPT-5.6 prompting research

Status: decision record for [#26](https://github.com/mgelei/gpt-skills/issues/26), input to [#25](https://github.com/mgelei/gpt-skills/issues/25), and evidence base for the skill audit in [#27](https://github.com/mgelei/gpt-skills/issues/27)

Researched: 2026-07-30

## Decision

Do not rewrite the repository's prompts merely because GPT-5.6 is newer. Preserve the current behavioral contract, evaluate it on GPT-5.6 with the existing reasoning setting, and make only measured, surgical changes.

For new or revised guidance, prefer a compact outcome-first structure: goal, relevant context, success criteria, hard constraints, authority boundaries, tool-routing rules, output contract, stopping conditions, and validation. State each rule once. Remove duplicate process scaffolding and irrelevant tools, but retain safety, business, evidence, permission, and schema constraints. This is the core recommendation in OpenAI's [GPT-5.6 prompting guide](https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6).

## Evidence scope and limits

The comparison below uses current OpenAI documentation as the authority for model behavior and migration guidance. OpenAI's model-specific GPT-5.5 query now resolves to the current GPT-5.6 guide, so there is no stable current copy of the former standalone GPT-5.5 guide to cite. The retained GPT-5.5 baseline therefore comes from OpenAI's current [reasoning guide](https://developers.openai.com/api/docs/guides/reasoning), which still documents GPT-5.5 defaults and pre-5.6 behavior, plus explicit GPT-5.5-to-5.6 comparisons in the [GPT-5.6 model guide](https://developers.openai.com/api/docs/guides/model-guidance?model=gpt-5.6).

Real-user reports are included as operational signals, not as general model guarantees. Their workloads, harnesses, providers, reasoning settings, and sample sizes differ.

## GPT-5.5 to GPT-5.6 comparison

| Topic | GPT-5.5 baseline | GPT-5.6 guidance or change | Repository decision |
| --- | --- | --- | --- |
| Prompt structure | Reasoning-capable GPT-5 models work well with a clear goal, strong constraints, and an explicit output contract without prescribed intermediate reasoning. | The model-specific guide sharpens this into outcome, evidence, completion bar, decision rules, and stop conditions. | **Unchanged, with stronger emphasis.** Keep outcome-first prompts and avoid step-by-step micromanagement unless the steps are contractual. [Sources: reasoning](https://developers.openai.com/api/docs/guides/reasoning), [GPT-5.6 prompting](https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6) |
| Prompt density | Existing prompts should be preserved as the migration baseline and changed only after representative evals expose a failure. | OpenAI now explicitly recommends removing repeated instructions, ineffective examples, irrelevant tools, and redundant tool descriptions. In one internal coding-agent sample, leaner prompts improved scores by about 10-15% while reducing tokens by 41-66% and cost by 33-67%; OpenAI says to treat these figures as directional. | **Strengthened recommendation, not a universal deletion pass.** Trim one category at a time and rerun the same cases. [Source](https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6) |
| Response length | GPT-5.5 is the comparison point for existing output style. | GPT-5.6 tends to be more concise by default. Broad instructions such as "be concise" may now make answers too short; `text.verbosity` should set the request-level default while the prompt names content that must survive compression. | **Changed.** Remove generic brevity instructions when they suppress required content; retain explicit length and completeness contracts. [Source](https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6#personality-collaboration-and-response-length) |
| Tone and collaboration | Tone and task behavior were commonly mixed into general style instructions. | OpenAI recommends short, separate descriptions of personality and collaboration style, with concrete writing choices instead of vague labels such as "friendly." | **Newly explicit.** Prompt-generation guidance should treat tone and collaboration behavior as distinct decisions when either materially affects the result. [Source](https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6#personality-collaboration-and-response-length) |
| Autonomy and approvals | Agentic prompts need tool, completion, and verification rules. | GPT-5.6 is described as more proactive and persistent. OpenAI recommends one compact authority policy that distinguishes read/review work, in-scope implementation, and actions requiring confirmation. Repeating approval warnings can produce unnecessary pauses. | **Strengthened.** State safe local authority and escalation boundaries once; do not scatter overlapping approval rules through the prompt. [Source](https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6#define-autonomy-and-approval-boundaries) |
| Reasoning effort | GPT-5.5 defaults to `medium`; supported effort is model-dependent. | GPT-5.6 also defaults to `medium`, adds `max`, and supports a separate Responses API `pro` mode. OpenAI says to preserve the GPT-5.5 setting, then compare the same setting with one level lower. | **Runtime change, not prompt prose.** Do not tell the model to "think harder" or embed effort/Pro instructions in ordinary prompts. Tune settings in the harness only when requested and supported by evals. [Sources: reasoning](https://developers.openai.com/api/docs/guides/reasoning#reasoning-effort), [GPT-5.6 model guidance](https://developers.openai.com/api/docs/guides/model-guidance?model=gpt-5.6) |
| Multi-turn reasoning state | Models before GPT-5.6 default to reasoning from the current turn; GPT-5.5/5.4 tool-heavy flows should preserve assistant `phase` values when history is replayed. | GPT-5.6 defaults to making available reasoning from earlier turns usable through `all_turns`; stale reasoning can also anchor later work. | **Runtime change with prompt implications.** Keep milestones and current work layer clear, compact after milestones, and use current-turn behavior when assumptions change. Do not duplicate state-management instructions in every task prompt. [Source](https://developers.openai.com/api/docs/guides/reasoning#preserve-reasoning-across-calls) |
| Tool orchestration | Direct tool calls remain appropriate when results require fresh judgment. | Programmatic Tool Calling is new for bounded deterministic reduction; multi-agent is a beta option for separable parallel work. Availability alone is not a reason to use either. | **New capability, unchanged principle.** Expose only relevant tools. Keep approval, citations, semantic judgment, and final validation in direct model control. Treat PTC and multi-agent as harness features outside ordinary reusable prompt text. [Sources: GPT-5.6 model guidance](https://developers.openai.com/api/docs/guides/model-guidance?model=gpt-5.6), [GPT-5.6 prompting](https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6#programmatic-tool-calling) |
| Frontend and visual work | Product context, existing design rules, responsive states, and validation remain necessary. | GPT-5.6 has stronger layout and visual-hierarchy judgment, but OpenAI still says to preserve the design system, name relevant states and constraints, and render before finishing. | **Capability improved; prompting contract remains.** Do not replace specific design constraints with a generic request to make the UI polished. [Source](https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6#frontend-and-visual-tasks) |
| Validation and evidence | Agentic and research prompts should define done and how work is verified. | GPT-5.6 guidance continues to require success criteria, retrieval/citation rules, validation tools, missing-evidence behavior, and an honest fallback. | **Unchanged.** Keep verification and evidence requirements; a shorter prompt is not successful if it weakens the completion contract. [Sources: reasoning](https://developers.openai.com/api/docs/guides/reasoning#advice-on-prompting), [GPT-5.6 prompting](https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6#grounding-citations-and-retrieval-budgets) |

## Practices to change, retain, or avoid

### Change or newly adopt

- Remove duplicated rules, redundant approval language, examples that do not correct measured behavior, and tools unrelated to the task. Do this incrementally against the same eval cases. [OpenAI](https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6#simplify-prompts-first)
- Replace generic brevity commands with a priority order that names required facts, caveats, decisions, and next steps, then identifies what may be omitted. [OpenAI](https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6#personality-collaboration-and-response-length)
- Use decision rules for contextual choices and reserve `ALWAYS`, `NEVER`, `must`, and `only` for real invariants. [OpenAI](https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6#outcome-first-prompts-and-stopping-conditions)
- Separate personality from collaboration behavior when the artifact needs both. Describe concrete writing and initiative choices rather than relying on broad adjectives. [OpenAI](https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6#personality-collaboration-and-response-length)
- For long-running work, state the current layer—research, design, implementation, review, or external coordination—and require sparse milestone updates rather than narration of every call. [OpenAI](https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6#long-running-workflows-and-state)

### Retain

- User-visible outcome, success criteria, hard constraints, required output shape, evidence rules, stop conditions, permission boundaries, and proportionate validation. [OpenAI](https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6#simplify-prompts-first)
- Relevant examples and style rules when they encode a product requirement or correct a measured failure. [OpenAI](https://developers.openai.com/api/docs/guides/model-guidance?model=gpt-5.6#prompting-best-practices)
- Explicit tool prerequisites, fallbacks for partial results, and a check that the final answer—not merely an intermediate tool result—satisfies the contract. [OpenAI](https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6#tool-routing)
- Representative evals before and after each change, with the model setting held stable until prompt effects are understood. [OpenAI](https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6#prompt-migration-workflow)

### Avoid or treat as obsolete scaffolding

- Wholesale prompt rewrites during the model switch; they confound model, prompt, setting, tool, and runtime effects. [OpenAI](https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6#prompt-migration-workflow)
- Repeated process instructions for behavior the model already performs reliably, broad anti-pattern catalogs, and duplicated warnings. [OpenAI](https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6#simplify-prompts-first)
- Prompt text that asks for hidden chain-of-thought, Pro mode, extra reasoning, PTC, or multi-agent execution. These are execution-layer decisions and should be configured and evaluated separately. [OpenAI](https://developers.openai.com/api/docs/guides/model-guidance?model=gpt-5.6)

## Signals from real users

These reports support the official direction but also show why prompt changes must not be blamed for every migration issue.

- Ploy's production migration found that roughly one third of initial raw failures came from an eval harness built around another model's sequential tool style. Prompt wording did not fix GPT-5.6 filling optional tool arguments; a schema-boundary change did. Cache and reasoning-replay behavior also required runtime work. This supports diagnosing prompt, schema, cache, state, and harness failures separately. [Ploy migration report](https://ploy.ai/blog/migrating-a-production-ai-agent-to-gpt-5-6)
- Rudrank Riyam reports that broad, outcome-owned "lanes" work well when "good" and the required evidence are written down, while Max reasoning is costly and the model can still declare readiness before proving the last invariant. This supports outcome ownership plus explicit proof requirements, not unbounded autonomy. [A Sol's Work](https://rudrank.com/a-sols-work-shipping-with-gpt-5-6-sol)
- The oh-my-openagent project shipped a GPT-5.6-specific reviewer prompt that was 36% shorter than its GPT-5.5 prompt while preserving the verdict contract, and paired it with targeted tests and a model-specific fallback rather than changing every GPT-5.5 use. This is a useful implementation example, not a general benchmark. [PR #6010](https://github.com/code-yeongyu/oh-my-openagent/pull/6010)
- Early OpenAI Developer Community reports are mixed on visual verification, scope control, context size, and cost. A recurring suggestion is to maximize context signal-to-noise, start a fresh task for unrelated work, and provide exact screenshots or acceptance criteria instead of asking for an open-ended UX review. Treat this as anecdotal until reproduced locally. [Community thread](https://community.openai.com/t/gpt-5-6-sol-vs-terra-what-are-you-seeing-in-real-development-during-these-first-days/1386726)

## Implications for this repository

The current [`prompt-architect/SKILL.md`](../prompt-architect/SKILL.md) is already substantially aligned with GPT-5.6 guidance:

- it audits outcome, constraints, sources, authority, tools, success, evidence, verification, and stopping conditions;
- it starts generated artifacts with the desired outcome and removes redundant instructions;
- it avoids generic brevity commands and preserves required facts and caveats;
- it keeps reasoning effort, Pro mode, model slugs, and API parameters out of ordinary prompts;
- it requires Codex authority boundaries and proportionate validation; and
- it treats the strict clarification ledger and code-block-only final response as product contracts, which should not be removed merely to shorten the skill.

No immediate rewrite is justified by the research. The likely improvements are narrower and should be gated by eval failures:

1. Distinguish personality from collaboration style in the audit when either is material.
2. For grounded research prompts, make evidence sufficiency, inference labeling, conflict handling, and retrieval stopping rules explicit.
3. For frontend prompts, preserve the existing design system and require rendered inspection of the named states.
4. For API-targeted artifacts, keep prompt text separate from model-family, reasoning, state, caching, PTC, and multi-agent settings; include those settings only when the user asks for an API or harness artifact.

## Follow-ups for #25

1. Build a small regression set before editing skills: at minimum one simple rewrite, one grounded research prompt, one Codex implementation prompt, one persistent-instructions prompt, one frontend task, and one strict structured-output task.
2. Record for each case: contract completeness, unnecessary clarification, unauthorized action, tool-routing quality, validation evidence, output length, prompt tokens, and user corrections required.
3. Run the current skill unchanged on GPT-5.6 first. If a case fails, make the smallest edit tied to that trace and rerun the same set.
4. Keep the stable ledger, acceptance detection, final-output boundary, safety constraints, and no-placeholder rules unless an eval demonstrates a specific defect.
5. Track API migration work—model tiers, reasoning settings, state replay, caching, PTC, multi-agent, and tool schemas—in a separate implementation issue. They are not prompt-only changes.
6. Revisit all GPT-5.6 guidance after OpenAI changes the beta features or publishes stable model snapshots; the current note reflects documentation available on 2026-07-30.

## Existing skill audit for #27

This is a static contract audit against the guidance above. It identifies prompt-level incompatibilities and unjustified migration edits; it does not replace the representative GPT-5.6 evals proposed for #25.

| Skill | Finding | Action |
| --- | --- | --- |
| [`bootstrap-project`](../bootstrap-project/SKILL.md) | Compatible. Its length mainly encodes a consequential interview write gate, evidence boundaries, artifact contracts, and validation. Those constraints should survive prompt compression. It does not request model settings or hidden reasoning, and it keeps current research conditional on need. | No change. Evaluate whether repeated interview-gate wording can be shortened only after a regression case shows equal compliance with fewer tokens. |
| [`challenge-me`](../challenge-me/SKILL.md) | One prompt-level incompatibility. The skill required spawning a subagent for noisy reconnaissance, although multi-agent execution is a runtime choice and may not exist on every supported surface. The useful contract is focused reconnaissance and a compact decision-changing result, not the orchestration mechanism. | Replace the subagent requirement with capability-neutral context-control guidance. Preserve the main-thread ownership, result shape, and non-delegable judgment boundaries. |
| [`close-thread`](../close-thread/SKILL.md) | Compatible. Its repeated-looking cautions apply to distinct destructive or data-loss boundaries across local checkouts, ordinary worktrees, managed worktrees, and archival surfaces. These are safety and permission invariants, not obsolete process scaffolding. | No change. Do not compress the preservation and approval rules without surface-specific loss-prevention evals. |
| [`prompt-architect`](../prompt-architect/SKILL.md) | Compatible. It already produces outcome-first prompts, separates prompt prose from API settings, removes redundancy, defines authority and validation, and preserves its strict ledger and final-output product contracts. | No immediate change. Gate the four narrower opportunities already listed under repository implications—personality versus collaboration, grounded-research evidence rules, frontend rendered-state checks, and API/harness separation—on representative failures. |

Audit conclusion: all four skills can target GPT-5.6 without wholesale rewrites. Only `challenge-me` needs a surgical prompt change. No skill should embed a GPT-5.6 model slug, reasoning level, Pro mode, state-replay policy, PTC requirement, or multi-agent requirement; those remain runtime configuration and evaluation concerns.

## Plugin terms and privacy review

This audit and the `challenge-me` wording change do not add a tool, connector, publisher backend, data flow, telemetry, or new user action. No update is needed to the current [Plugin Terms](https://mate.gelei.dev/plugin-terms/) or [Plugin Privacy Policy](https://mate.gelei.dev/plugin-privacy/). Reassess if later work changes a skill to invoke new external services, collect or transmit data, or materially expands autonomous actions.
