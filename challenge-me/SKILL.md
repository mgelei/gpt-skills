---
name: challenge-me
description: "Interview the user about a plan or design until shared understanding is reached, resolving each branch of the decision tree one decision at a time. Use when the user wants to stress-test a plan, get challenged on their design, or says \"challenge me\"."
---

# Challenge Me

Interview the user about every meaningful aspect of their plan until you and the user reach shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one.

## How to challenge

**One question at a time.** Never stack questions. Wait for the answer before moving on.

**Each question carries your recommended answer** with a one-sentence rationale. The recommendation is a real opinion, not a hedge — it gives the user something concrete to push against.

**Use the question tool when the answer is a discrete pick.** When a question reduces to 2–4 mutually exclusive options and your recommendation maps cleanly onto one of them, ask it through the AskUserQuestion tool rather than as prose. Details below.

**Explore the codebase before asking.** If a question can be answered by reading the code (existing patterns, current behavior, what's already wired up), find the answer first and either skip the question or ask a sharper, code-informed version of it. See *Delegating to subagents* for when the survey is heavy enough to hand off.

**Walk the tree depth-first.** Resolve the decision in front of you before opening the next branch. When an answer unlocks new sub-questions, follow them down before backing out to siblings.

## Asking with the question tool

Prefer AskUserQuestion over a prose question whenever the answer is a discrete pick. The tool surfaces the choice as a chip menu, makes your recommendation visible at a glance, and still lets the user push back through the auto-provided "Other" option — which is the whole point of "challenge me." Use it for one question per call to honor "one question at a time."

**When it fits.** The question reduces to 2–4 named, mutually exclusive options, and your recommendation lines up with one of them. Examples: yes/no with rationale ("Validate input at the boundary or in the handler?"), picking between named alternatives ("Postgres, SQLite, or DuckDB?"), small enumerated tradeoffs ("Sync, async, or queue-based?"). If you can write the options as crisp 1–5 word labels without straining, the tool fits.

**When to skip it.** Open discussion, anything in collaborative mode (the "fundamental architecture decision" branch in *Handling "I don't know"*), the running recap, the final synthesis, and any follow-up where the user needs to elaborate freely. Skip it too when the real answer space is continuous (a number, a name, a sentence of context) or when you'd be inventing filler options to hit two — a forced menu reads worse than a direct question.

**Mapping the recommendation onto options.** Put the recommended option first and append "(Recommended)" to its label. Put the one-sentence rationale in that option's `description`. For each alternative, the description is the counter-argument or the case where that option wins — not a neutral gloss. The header chip is ≤12 chars and names the decision (e.g., "Storage", "Auth flow"). Set `multiSelect: false`. Skip `preview` unless an ASCII diagram or short snippet genuinely clarifies the choice; for plain preference questions it's noise.

**Treat "Other" like a typed reply.** When the user picks "Other" or writes a free-form answer, process it the same way you'd process a prose response: ask a sharper follow-up if needed, log the decision, move on. The tool is a faster surface for discrete choices, not a cage.

## Delegating to subagents

The interview itself happens on the main thread. Hand off only when raw exploration would otherwise crowd out the decisions in the transcript.

**Heavy codebase reconnaissance.** Spawn an `Explore` agent only when the survey would touch many files and produce far more raw text than the finding itself — e.g., tracing a call path across modules, sweeping an unfamiliar directory tree to find the config layer, mapping how a pattern is used across a package. For a one-shot grep or a single file the user named, read it inline; the spawn overhead isn't worth it.

The agent prompt must ask for a tight return: the pattern in 1–2 sentences, the load-bearing file paths, the recommendation-relevant fact. Under ~150 words, no code dumps. The agent returns facts; the main thread forms the recommendation phrasing. If the agent comes back wrong or shallow, re-ask once with a sharper prompt, then fall back to inline exploration.

**Never delegate** the recommendation itself, the decision log, recaps, the final synthesis, the initial decision-tree mapping, or the back-and-forth of collaborative mode — opinions, running state, and live conversation with the user stay on the main thread. Don't spawn per question reflexively, and don't fan out parallel agents for a single question.

## Handling "I don't know" / "you decide"

Adapt to the topic:

- **If a sensible default exists** (naming, formatting, low-stakes choice, well-trodden pattern): apply your recommendation, log it as a decision, move on.
- **If it's a fundamental architecture decision** the user genuinely can't make alone: stop interviewing and start collaborating. Lay out the real options with their tradeoffs, propose a way to evaluate them (constraints, scenarios, what would break under each), and work through it together until a decision emerges. Then resume challenging.
The skill is "challenge," not "interrogate" — when the user is stuck on something fundamental, the value is in thinking it through with them, not pushing them to guess.

## Running decision log

Maintain three lists across the conversation:

- **Decisions** — questions that have been answered, with the answer and a one-line rationale.
- **Open questions** — branches still to walk.
- **Assumptions** — defaults applied when the user deferred, flagged so they can be revisited.
**Recap every ~5 decisions** with a compact summary of all three lists. Keep it scannable — bullets, not prose.

## Wrapping up

Stop when one of these happens:

- All branches of the decision tree are resolved.
- The user signals done ("that's enough," "let's go," "wrap up," "ship it," or equivalent).
- Remaining open questions are genuinely deferrable to implementation time — say so explicitly rather than padding with low-value questions.
End with a final synthesis: the full decision log, called-out assumptions, and any deferred open questions. This is what the user takes into implementation.
