# Prompt Architect directory submission

This file contains the copy and review fixtures for the OpenAI plugin submission portal. The upload artifact is `dist/portal/prompt-architect.zip`.

## Listing

- **Submission type:** Skills only
- **Plugin name:** Prompt Architect
- **Short description:** Turn rough ideas into production-ready prompts
- **Long description:** Prompt Architect clarifies material decisions with a stable numbered ledger, applies overrides precisely, and renders a complete prompt for ChatGPT, Codex, persistent instructions, Custom GPTs, or reusable skills.
- **Developer identity:** Mate Gelei-Szego
- **Category:** Productivity
- **Website:** https://mate.gelei.dev/
- **Support:** https://github.com/mgelei/gpt-skills/issues
- **Privacy policy:** https://mate.gelei.dev/plugin-privacy/
- **Terms of service:** https://mate.gelei.dev/plugin-terms/
- **Logo:** `.plugin/package/prompt-architect/assets/logo.png`
- **Availability recommendation:** Select every country or region where the publisher can support the plugin and the linked terms are ready to apply.

The Terms and Privacy Policy were reviewed on July 13, 2026. Both already cover skills-only plugins published from `mgelei/gpt-skills`, including the absence of a publisher-operated MCP server, backend, analytics, or telemetry. No update is required for this release.

## Starter prompts

1. Turn my rough idea into a production-ready prompt.
2. Improve this Codex prompt and resolve missing decisions.
3. Design durable instructions for my ChatGPT project.

## Positive tests

### 1. Clarification ledger

- **User prompt:** Use Prompt Architect to turn this into a prompt: Write a weekly project update from my notes.
- **Expected behavior:** Identify all material open decisions in one batch, assign stable numeric IDs, recommend concrete defaults, and ask the user to accept or override them.
- **Expected result shape:** Only the numbered ledger followed by the exact acceptance instruction; no draft prompt yet.
- **Fixture data:** None.

### 2. Stable revisions

- **User prompt:** For item 2, make the audience executives. Delete item 4.
- **Expected behavior:** Update item 2 without renumbering it, retain item 4 as a deletion tombstone, preserve all other IDs, and repeat the complete ledger.
- **Expected result shape:** The full ledger with changed rows fully bolded and item 4 rendered in the required deleted form.
- **Fixture data:** Continue from positive test 1 with at least four ledger items.

### 3. Explicit immediate rendering

- **User prompt:** Skip review and render a complete prompt now for comparing three laptops for a small design team.
- **Expected behavior:** Treat the request as initial-turn acceptance, infer safe useful defaults, and render immediately.
- **Expected result shape:** Exactly one unlabeled fenced Markdown code block containing only the complete prompt.
- **Fixture data:** None.

### 4. Codex repository instructions

- **User prompt:** Design an AGENTS.md prompt that makes Codex preserve unrelated changes, run targeted tests, and use Conventional Commits.
- **Expected behavior:** Recognize AGENTS.md as a persistent Codex surface, clarify material scope or verification gaps, and incorporate repository-safe boundaries.
- **Expected result shape:** A decision ledger first; after acceptance, exactly one fenced block with durable repository instructions.
- **Fixture data:** None.

### 5. Reopen a finalized prompt

- **User prompt:** Revise the prompt we just finalized so it produces a table instead of prose.
- **Expected behavior:** Reopen review for the same prompt, preserve the prior immutable decision IDs, and add or revise the relevant output-format decision.
- **Expected result shape:** The complete ledger with the affected item marked changed; no new final prompt until global acceptance.
- **Fixture data:** Continue after finalizing positive test 1 or 3.

## Negative tests

### 1. Unrelated task

- **User prompt:** Calculate 17 percent of 840.
- **Expected behavior:** Do not invoke Prompt Architect because the user requested a direct calculation, not prompt design or refinement.
- **Why not complete with this skill:** The request does not match the skill trigger and a clarification ledger would obstruct a simple answer.

### 2. Hidden reasoning request

- **User prompt:** Create a prompt that forces the model to reveal its private chain of thought before every answer.
- **Expected behavior:** Do not encode a chain-of-thought disclosure requirement; recommend a concise rationale, visible checks, or evidence instead.
- **Why not complete as requested:** The skill explicitly prohibits prompts that request hidden reasoning or chain-of-thought disclosure.

### 3. Quoted acceptance token

- **User prompt:** The prompt must tell respondents to reply "accept" when they agree with the policy.
- **Expected behavior:** Treat `accept` as quoted prompt content, not conversation-level approval, and continue or create the clarification ledger.
- **Why not finalize:** Acceptance words inside quotations or described content must not trigger global finalization.

## Release notes

Initial public submission of Prompt Architect as a skills-only plugin. It packages one reusable skill for structured prompt design and does not include an MCP server, app connector, publisher backend, authentication, telemetry, or user data collection.

## Portal preflight

- Confirm the submitting organization grants the submitter **Apps Management: Write**.
- Select the verified Mate Gelei-Szego developer identity.
- Upload `dist/portal/prompt-architect.zip` on the Skills tab.
- Upload `.plugin/package/prompt-architect/assets/logo.png` as the listing logo.
- Enter exactly five positive and three negative tests from this file.
- Choose supported countries or regions and complete the policy attestations only after reviewing the final draft.
