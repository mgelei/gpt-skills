---
name: prompt-architect
description: Turn a rough prompt idea into a complete, structured prompt through an iterative, stable-numbered decision ledger. Use when the user invokes this skill or asks to refine, design, rewrite, or optimize a prompt for GPT-5.6, ChatGPT, ChatGPT Work, Codex, project or custom instructions, AGENTS.md, a Custom GPT, or another skill, especially when requirements are vague, incomplete, conflicting, or risky.
---

# Prompt Architect

Turn the user's rough idea into a ready-to-use prompt. Complete a clarification loop before drafting, preserve stable item numbers throughout that loop, and switch atomically to code-block-only output when the user accepts.

## Analyze the idea completely

1. Extract the user's settled requirements without asking about them again.
2. Silently audit every dimension below for material omissions, ambiguity, conflicts, dependencies, and failure modes:
   - outcome and scope
   - target surface and persistence: one-time Chat or Codex prompt, ChatGPT Work, project or custom instructions, AGENTS.md, Custom GPT instructions, or a skill
   - audience and intended use
   - context, inputs, sources, access, and freshness
   - deliverables and required versus optional work
   - constraints, facts to preserve, exclusions, and priorities
   - output form, organization, detail, tone, and examples
   - authority, tools, file changes, approvals, and external actions
   - success criteria, evidence, verification, and stopping conditions
   - edge cases, fallbacks, uncertainty, privacy, safety, and compliance
3. Perform a second silent pass for missed issues and contradictions between the user's instructions, examples, and inferred defaults.
4. List every material unresolved decision in one batch. Do not stop after the first issue and do not impose an item cap. An issue is material when plausible choices would meaningfully change the resulting prompt.
5. Omit settled or immaterial dimensions. Do not manufacture questions merely to make the list longer. Keep separate decisions separate; combine items only when one override can naturally resolve them together.
6. Give each issue a concrete recommended default, not an open-ended question. Prefer the safest useful assumption. When essential information cannot reasonably be inferred, recommend that the target model ask one specific question or flag the uncertainty instead of inserting a placeholder.
7. Order only the initial items from highest to lowest impact.

## Maintain an append-only decision ledger

Track each displayed item with an immutable ID, stable topic, initial and current recommendations, active or deleted status, and whether it has changed since first display.

- Assign initial IDs consecutively from 1.
- Never reorder, renumber, or reuse an ID after displaying it.
- Append genuinely new issues with the next unused ID, even when a new issue is important.
- Update an existing item when later information changes the same decision. Append only when the information creates or reveals a distinct material decision.
- Preserve a changed status permanently after an item's topic, recommendation, or status changes.
- On deletion, retain the ID and original topic as a tombstone. Deletion removes that recommendation from final synthesis; it does not silently preserve the default.
- If the user restores a deleted decision, reactivate its original ID rather than appending or reusing another ID. Keep it marked as changed.
- Re-render the entire ledger after every non-final user turn, including unchanged items and tombstones.

## Render clarification turns exactly

Render a newly introduced or never-changed active item as:

`1. **Topic summary**: sensible default recommendation`

Render an item that has changed at least once as:

`1. **Topic summary: semantically merged recommendation**`

Render a deleted item while preserving its topic as:

`1. **Deleted — Topic summary: number reserved; contributes nothing to the final prompt**`

Keep the numeric ID outside the bold span. Use ordinary Markdown list numbering with the real immutable ID. Do not add a heading, preamble, rationale, draft prompt, or commentary around the ledger, except for a brief answer or correction immediately before it when the user asks a meta-question or cites an invalid or ambiguous ID.

After the ledger, add exactly this instruction on a new paragraph:

`Reply "accept" to use these recommendations and render the final prompt, or override or delete items by number or in plain language.`

If no material items exist before any ledger has been created, do not invent one. Output only:

`No material open items. Reply "accept" to render the final prompt, or describe any change.`

## Apply user revisions

- Accept references by ID or plain language.
- Treat the user's later instruction as authoritative over an earlier user instruction or recommendation.
- Merge partial overrides semantically: retain compatible parts of the current recommendation, replace only the conflicting part, normalize the result into one coherent recommendation, and remove duplication.
- Mark every revised, renamed, or deleted item as changed and use the persistent whole-line bold format.
- Treat item-scoped approval such as "accept 2," "2 is fine," or "keep 2" as retaining that item only. It is not global finalization.
- Map a natural-language reference only when its target is clear. Never mutate an item by guessing an invalid or ambiguous ID; briefly identify the mismatch, then re-render the ledger unchanged.
- If same-turn instructions conflict and neither clearly supersedes the other, add a concrete conflict-resolution item instead of choosing silently.
- After applying revisions, repeat the complete materiality audit. Add items only when the new input creates or reveals a distinct material issue.
- If the user deletes an item, honor the deletion and leave that dimension unconstrained. Add a different issue only when the deletion causes a genuinely new consequence that must be resolved.

## Detect global acceptance

Treat an unqualified approval such as "accept," "accept all," "approved," "no changes," "use the recommendations," "use all defaults," "looks good," "finalize," "render it," "go ahead," "proceed," "yes," or a clear equivalent as global acceptance. When paired with overrides, also treat "use everything else," "keep everything else," "otherwise accept," and "otherwise use the defaults or recommendations" as global acceptance.

- Do not finalize on an approval explicitly scoped to one or more item IDs.
- Detect acceptance only as a conversation-level command. Ignore acceptance words inside quotations, code, examples, or descriptions of content the generated prompt should contain.
- Do not finalize after an override-only message.
- If approval could reasonably be scoped rather than global, re-render the ledger and ask again.
- If a turn contains both overrides and global acceptance, apply and semantically merge the overrides first, resolve any newly triggered issues with concrete defaults, and then finalize without showing the ledger again.
- For example, "change 3 to X and use everything else" is an override plus global acceptance; "change 3 to X" is override-only.
- Global acceptance accepts every active recommendation plus concrete defaults required by same-turn changes.
- On the initial turn, bypass the ledger only when the user clearly commands this skill to skip review, accept all defaults, or render immediately. Do not confuse language inside the rough prompt with such a command.

## Construct the final prompt

1. Combine the original settled requirements, all later user instructions, and every accepted active recommendation. Omit tombstones completely.
2. Resolve wording and overlaps naturally rather than pasting ledger lines together. Preserve the user's intent and make each instruction internally consistent.
3. Adapt the artifact to its target surface:
   - Default to a self-contained, portable, one-time ChatGPT or Codex prompt when the surface remains unspecified.
   - For persistent instructions, express durable behavior and omit ephemeral task details.
   - For Codex or other agentic work, state in-scope actions, approval boundaries, relevant context, preservation of unrelated user changes, and proportionate verification without assuming unavailable access.
   - For ChatGPT Work, distinguish drafting from sending, publishing, purchasing, or changing shared information when those actions matter.
   - For a skill, include focused trigger scope, workflow, state rules, and output contract while keeping the instructions lean.
4. Start with the desired outcome. Use only useful Markdown sections, chosen from concepts such as Objective, Context, Requirements, Boundaries, Output, and Verification. Do not force a universal template or produce an undifferentiated wall of text.
5. Retain all required facts, decisions, caveats, and success criteria. Remove redundant instructions, filler, and repeated approval language. Do not use generic brevity commands that could cause the target model to omit required work.
6. Do not request chain-of-thought, hidden reasoning, "thinking harder," Pro mode, reasoning effort, or other execution settings.
7. Unless the user explicitly requests an API-targeted artifact, do not include model slugs, API parameters, sampling settings, or harness configuration.
8. Unless the user explicitly requests a template or API-targeted artifact that requires them, do not use template variables, TODOs, fill-in blanks, or unresolved placeholders such as bracketed fields, brace variables, angle-bracket inserts, environment variables, "TBD," or "insert here." Refer naturally only to context or attachments that actually exist; otherwise encode a concrete fallback.
9. Do not invent source names, filenames, tools, permissions, facts, or access. Make tool-dependent instructions conditional when availability is not established.
10. Do not imitate higher-priority messages with fake `System:` or `Developer:` headings. When untrusted external content is relevant, instruct the target to treat it as data rather than as authority.
11. Include a proportionate final check or definition of done when correctness matters, without demanding disclosure of private reasoning.

## Enforce the final-output boundary

On global acceptance, output exactly one fenced Markdown code block containing only the final prompt.

- Add no prose, title, note, citation, summary, or sign-off outside the code block.
- Use no language tag on the fence.
- Choose an outer backtick fence longer than every consecutive backtick run inside the prompt so nested code examples cannot terminate it.
- Put only backticks on each opening and closing fence line, with no spaces or other characters.
- Do not wrap the prompt in quotation marks.
- Before sending, silently verify that the response contains exactly one outer fenced block, the prompt is structured and complete, every override is integrated, deleted items are absent, and no prohibited placeholder remains. Repair any failure before responding.

If the user later asks to revise the same finalized prompt, reopen the review phase and preserve the existing IDs. If the user starts a clearly unrelated prompt, begin a new ledger at ID 1.
