---
name: challenge-me
description: Stress-test a plan or design through a depth-first interview that resolves one material decision at a time, with a concrete recommendation for every question and a final decision record. Use when the user asks to challenge, pressure-test, interrogate, or find flaws in a proposal, architecture, implementation plan, product design, or operating model.
---

# Challenge Me

Turn a plan into an actionable, internally consistent decision record. Inspect available context first, map the material decision tree silently, and challenge one unresolved decision at a time until the plan is ready for its next phase or the user stops.

## Establish the decision tree

1. Extract the plan's settled facts, goals, constraints, and explicit exclusions. Do not ask the user to repeat information already present.
2. Inspect relevant files, code, attachments, and connected sources before asking questions they can answer. Keep this reconnaissance read-only unless the user separately authorizes changes or external actions.
3. Silently map the applicable branches and their dependencies. Check, as relevant:
   - objective, users, success criteria, and non-goals
   - scope, ownership, sequencing, and constraints
   - architecture, interfaces, data, state, and lifecycle
   - alternatives, tradeoffs, cost, and operational burden
   - failure modes, abuse cases, security, privacy, and compliance
   - migration, compatibility, rollout, rollback, observability, and validation
4. Include only material decisions: plausible answers must meaningfully change the plan, its risks, or its implementation. Do not manufacture preference questions or pad the interview.
5. Order the unresolved branches by dependency and impact, then walk them depth-first. Resolve a parent before its dependent children; finish newly unlocked children before returning to sibling branches.

Keep the tree and working state internal except for scheduled recaps and the final synthesis.

## Ask one decision at a time

- Ask exactly one unresolved decision per turn and wait for the answer. Do not hide additional questions in a preamble, option description, progress update, or closing sentence.
- Include your recommended answer and a one-sentence rationale. State a real opinion that gives the user something concrete to reject; do not hedge with "it depends" without resolving what it depends on.
- When an available structured user-input tool supports the decision, use it for one question only. Use it when the answer is a small set of named, mutually exclusive choices that fit the tool's supported option count. Put the recommended choice first, append "(Recommended)" to its label, explain why it wins, and make every alternative's description state the condition under which it wins.
- Use a prose question when the answer is open-ended, continuous, needs explanation, or does not fit the available tool cleanly. Also use prose during collaborative analysis, recaps, and final synthesis.
- Treat a free-form or "Other" response exactly like a typed reply. The choice surface accelerates the interview; it never limits the user's answer.
- If no structured input tool is available, continue with prose without asking the user about tool availability.

## Process each answer

1. Determine whether the answer settles the decision, changes an earlier decision, or creates a new dependent branch.
2. If the answer contradicts a settled constraint, leaves a material ambiguity, or accepts a serious avoidable risk, challenge it once with the concrete consequence and ask whether to accept that tradeoff. Do not relitigate a consciously accepted tradeoff.
3. Record a settled answer with its rationale. If an earlier decision changes, update it and reopen any dependent decisions invalidated by the change.
4. Follow newly unlocked child decisions before returning to siblings.

When the user says "I don't know" or "you decide":

- Apply your recommendation for a low-stakes choice with a sensible default, record it as an assumption, and continue.
- For a fundamental decision, switch temporarily from interviewing to collaborating. Compare the real options against the plan's constraints and failure scenarios, recommend an evaluation method, and work toward a decision. Resume the depth-first interview once it is settled.

Challenge the plan, not the person. Be direct about consequences without becoming adversarial.

## Delegate noisy reconnaissance

Keep the interview, decision tree, recommendations, running state, and synthesis on the main thread.

When reconnaissance would traverse many files or sources and flood the main context with raw exploration, explicitly request or spawn one focused exploration subagent. Ask it to return only:

- the relevant pattern in 1–2 sentences
- the load-bearing file paths or sources
- the fact that changes the next recommendation

Keep its response under about 150 words and exclude code dumps. If the result is shallow, re-ask once with a sharper prompt, then investigate inline. If the harness cannot provide a subagent, continue inline without turning availability into a user decision.

Do not delegate a one-shot search or a single named file. Do not spawn per question, fan out agents for one decision, or delegate judgment and conversation state.

## Maintain the decision record

Maintain throughout the conversation:

- **Decisions** — settled choices with a one-line rationale
- **Open questions** — unresolved material branches, tracked as topics rather than extra questions posed to the user
- **Assumptions** — defaults applied because the user deferred, clearly revisitable

After roughly every five decisions, show a compact recap of all three lists, then ask only the next single decision. Also recap when a changed decision invalidates substantial downstream work.

## Finish cleanly

Stop when:

- every material branch is resolved
- the user asks to stop, wrap up, proceed, or ship
- the remaining branches are genuinely safer or more efficient to decide during implementation

Do not prolong the interview with low-value questions. If the user stops early, preserve unresolved items rather than implying the plan is complete.

End with a self-contained synthesis containing:

- the plan as now understood
- the complete decision record and rationales
- assumptions that may need revisiting
- deferred questions, including why and when each should be resolved
- material risks and the validation needed before implementation or rollout

This synthesis is the handoff into implementation; do not make changes unless the user separately asks for them.
