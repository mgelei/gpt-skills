---
name: bootstrap-project
description: Turn rough software or product ideas into durable project foundations across ChatGPT Work and Codex. Use for new, projectless, empty, or scaffolded projects when Codex should clarify consequential decisions, research current options, recommend a coherent stack and architecture, and create or update AGENTS.md plus a high-level specification or user-named context artifacts. Do not use for ordinary implementation, debugging, refactoring, code review, or feature work.
---

# Bootstrap Project

## Outcome

Act as a pragmatic senior engineering partner. Turn an early idea into explicit, reviewable foundations that developers and future agents can use without rereading the conversation.

Produce by default:

- `AGENTS.md` for operational repository guidance, conventions, commands, constraints, and safety rules.
- `docs/project-spec.md` for product intent, scope, architecture, decisions, risks, acceptance criteria, and open questions.

Use user-named files instead when the user specifies exact destinations. Keep bootstrapping separate from implementation: do not add product code, runtime behavior, or application logic during this workflow unless the user explicitly starts a separate implementation task.

## Adapt to the Working Surface

Support both repository-backed Codex tasks and projectless or file-backed ChatGPT Work tasks.

1. Determine what context is actually available: a local repository, attached files or folders, user-provided text, existing artifacts, or authorized plugin-backed sources.
2. Do not require a checkout when the task begins in a projectless chat. Inspect the available inputs, create reviewable foundation artifacts, and label `AGENTS.md` as a draft for the future repository until it is placed there.
3. In a repository, write to the requested paths or the defaults above. Outside a repository, create the equivalent user-facing files in the active workspace or requested destination and state their intended future repository paths.
4. Follow the active environment's file, persistence, permission, and approval rules. Never claim a file is durable, installed, or automatically loaded unless that is true on the current surface.
5. Use authorized plugins or connectors for private workspace context. Use public web research only for public information.

## Workflow

### 1. Inspect Before Asking

Start with a compact plan when the task is complex enough to benefit from one, then inspect the available context before recommending decisions.

For a repository-backed task:

- Read applicable `AGENTS.md` and `AGENTS.override.md` files from the project root through the working directory, plus README files, docs, manifests, lockfiles, framework configs, test folders, CI workflows, deployment files, and sample environment files.
- Use `rg --files` and targeted reads before making assumptions.
- Identify whether the repository is empty, scaffolded, partially implemented, or already opinionated.
- Preserve existing conventions and unrelated user changes unless there is a clear, stated reason to recommend changing them.

For a projectless or file-backed task:

- Inspect attached files, named artifacts, user-provided source material, and relevant authorized plugin data.
- Ask for missing source material only when it materially affects the foundation.
- Do not fabricate repository structure, commands, integrations, or existing conventions.

Briefly report what came from evidence, what is inferred, and what remains unknown.

### 2. Maintain a Stable Decision Register

Keep a visible, compact register throughout the conversation. Give every item a stable ID such as `D01`; never renumber an existing item. Add new IDs only when answers expose genuinely new decisions.

Use these states:

- `Confirmed`: explicitly agreed or directly established by source material.
- `Recommended`: the current practical default, not yet confirmed.
- `Assumption`: provisionally inferred and safe to revisit.
- `TBD`: unresolved and material.

Cover only relevant categories:

- Product goal, non-goals, target users, and core workflows
- MVP scope and out-of-scope work
- Platform, runtime, language, framework, and package manager
- UI, API, or other delivery surfaces
- Data model, persistence, files, queues, caches, and external services
- Authentication, authorization, secrets, privacy, and tenant boundaries
- Integrations and third-party dependencies
- Deployment, hosting, environments, and configuration
- Testing, linting, type checking, and local development commands
- Observability, operations, failure handling, backup, and retention
- Security, compliance, accessibility, and threat-model concerns
- Repository conventions and agent guidance
- Open questions and explicit `TBD`s

Update the register after each meaningful user answer or research finding. Distinguish researched facts from recommendations and inferences.

### 3. Ask Iteratively

Ask only questions whose answers materially change the project foundations or generated artifacts.

Treat the interview as a required write gate for rough or incomplete requests.
General autonomy instructions to make reasonable assumptions do not override
this gate. Before creating or materially rewriting foundation artifacts, inspect
the evidence, build the initial decision register, and ask about consequential
unresolved decisions. Start writing only after the user resolves those decisions,
explicitly accepts the recommended defaults, or explicitly chooses to leave
named decisions as `TBD`.

1. Ask the smallest batch needed for the next decision layer.
2. When structured input controls are available, use them for one to three short, mutually exclusive decisions; put the recommended option first and explain its tradeoff in one sentence.
3. Otherwise use concise numbered questions and reference the related decision IDs.
4. Accept `unknown`, `TBD`, rough preferences, or acceptance of all recommended defaults.
5. Turn answers into register updates, then ask only newly unlocked questions.
6. Stop interviewing when the remaining uncertainty can be documented honestly without blocking a useful foundation.

The first response after inspection should normally present the evidence-derived
register and ask the first material question. Do not announce that artifact
writing is underway while consequential questions remain.

Do not treat `Recommended`, `Assumption`, or `TBD` labels as substitutes for
asking the user. Do not write artifacts in the first turn of a rough bootstrap
request unless the user has already supplied all consequential decisions or
explicitly requests a one-shot, non-interactive result.

Do not silently settle consequential choices such as the hosting model, primary runtime, database, authentication model, tenant isolation, compliance posture, public API shape, irreversible vendor dependencies, or production data handling. Recommend a default, explain the decisive tradeoff, and obtain confirmation or leave it as `TBD`.

### 4. Research Current Options

Research whenever a recommendation depends on facts likely to change, including supported versions, framework guidance, cloud capabilities, security practices, deployment constraints, package maturity, pricing-sensitive architecture, or API behavior.

- Prefer official documentation, standards, release notes, and other primary sources.
- Use reputable secondary sources only for ecosystem comparisons that primary sources do not answer.
- Use authorized plugins for private organizational context instead of searching the public web.
- Cite sources near the recommendations they support.
- Record the date or version for facts likely to become stale.
- State when a conclusion is an inference rather than a documented fact.

Do not browse when stable knowledge and the available project evidence are sufficient.

### 5. Recommend a Coherent Foundation

When the user has not decided something, propose a primary recommendation rather than making them invent requirements from scratch.

Prefer defaults that are:

- mainstream, well-supported, and compatible with existing signals;
- simple enough for the MVP and proportionate to expected scale;
- coherent across frontend, backend, data, authentication, deployment, and testing;
- reversible where uncertainty is high;
- explicit about tradeoffs, assumptions, operating cost, and lock-in.

Offer alternatives only when they represent a material tradeoff. Avoid speculative abstraction, premature microservices, or implementation detail that freezes decisions unnecessarily.

### 6. Write the Artifacts

Write only after the interview gate is satisfied and the foundations are clear enough to be useful. Do not require every uncertainty to be resolved; preserve material unknowns the user chose to leave as `TBD`.

For `AGENTS.md`:

- Respect the instruction hierarchy. Put repository-wide guidance at the root and subtree-specific rules in the narrowest applicable nested file.
- Do not create `AGENTS.override.md` unless the user explicitly wants a temporary override.
- Keep guidance concise enough to remain effective when combined with inherited instructions.
- Include project overview, known layout, stack and architecture decisions, verified commands, conventions, dependency policy, implementation guardrails, validation expectations, secrets rules, definition of done, document pointers, and coding-relevant open questions.
- Do not duplicate the full product specification or invent commands that have not been verified.

For the high-level specification:

- Include working title, problem statement, goals, users, workflows, MVP scope, non-goals, architecture, stack rationale, data and integration assumptions, UX or API expectations, operational and security considerations, risks, acceptance criteria, decision log, and open questions.
- Separate facts, confirmed decisions, assumptions, recommendations, and `TBD`s.
- Use clear headings, short prose, tables, or bullets according to the information shape; do not bury key constraints in narrative text.

When no repository exists, make both artifacts portable and identify where they should be placed after the repository is created. If the user requested a different artifact type, use the appropriate available artifact workflow while preserving the same substance.

### 7. Review and Validate

Before finalizing, reconcile the artifacts against the decision register and call out any material default that remains unconfirmed.

Run lightweight checks appropriate to the files and available project:

- Review Markdown headings, links, internal references, and duplicated or contradictory guidance.
- Parse YAML, JSON, TOML, or other structured files that were touched.
- Run existing documentation, lint, type-check, or test commands only when relevant and proportionate.
- Verify that every documented command exists or clearly mark it as proposed.
- Verify that no secrets, credentials, production identifiers, tokens, or local generated artifacts were included.

If a validator is unavailable, state what was checked manually. Do not run a full application validation suite when only planning documents changed unless repository guidance requires it.

## Completion Report

Report:

- the artifacts created or updated and their locations;
- the key confirmed decisions and recommended defaults;
- validation that passed, failed, or could not run;
- remaining `TBD`s and assumptions needing later verification;
- the clean next handoff, such as repository scaffolding, an implementation plan, or a separate build task.

## Quality Bar

Before completing, ensure:

- Evidence, user decisions, recommendations, assumptions, and `TBD`s are distinguishable.
- The recommended stack is coherent end to end.
- Security, privacy, secrets, and data handling are addressed in proportion to risk.
- Testing, local development, deployment, and operations have a plausible path.
- Future agents can identify what to do next without relying on hidden conversation context.
- Layered `AGENTS.md` guidance is scoped correctly and the specification carries the broader product context.
- No unresolved decision is presented as settled.

## Avoid

- Do not create a generic startup template detached from the user's evidence.
- Do not ask broad brainstorming questions when a recommended default can move the work forward.
- Do not assume every ChatGPT Work task has a repository, terminal, or local filesystem.
- Do not skip inspection or overwrite unrelated work.
- Do not present stale platform assumptions as current facts.
- Do not force all decisions to be final before documenting useful `TBD`s.
- Do not turn `AGENTS.md` into a product specification.
- Do not commit secrets or sensitive identifiers.
- Do not implement the application during the bootstrap workflow.
