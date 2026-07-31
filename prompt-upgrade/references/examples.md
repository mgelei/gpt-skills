# Prompt upgrade examples

Use these examples to calibrate scope and output separation. Do not copy their subject matter into unrelated upgrades.

## Simple prompt

### Source

```text
Summarize the attached report. Be concise, but don't miss anything important.
```

Available intent: the summary is for a decision-maker who needs the report's conclusions, evidence, caveats, and next steps.

### Result

## Audit findings

| Classification | Finding | Why it matters | Proposed change |
| --- | --- | --- | --- |
| Change | “Be concise” conflicts with “don't miss anything important.” | GPT-5.6 is concise by default, so a generic brevity instruction can suppress required content. | Name the content that must survive compression and the detail that may be omitted. |
| Change | The output contract is implicit. | A completion bar makes the result easier to verify without prescribing hidden reasoning. | Require a decision-oriented summary with conclusions, evidence, caveats, and next steps. |
| Preserve | The task is intentionally narrow. | Extra persona, process, or tool instructions would add noise without protecting behavior. | Keep the upgraded prompt compact. |

## Ambiguities and tradeoffs

- No length limit was provided. Preserve flexibility rather than inventing a word count.

## Upgraded prompt

```text
Summarize the attached report for a decision-maker.

Include:
- the main conclusions;
- the evidence, facts, or metrics that materially support them;
- important caveats, uncertainties, or limitations; and
- decisions or next steps identified in the report.

Prioritize decision-relevant information. Omit background detail that does not affect the conclusions, caveats, or next steps. Do not introduce facts that are not in the report.
```

## Complex prompt

### Source

```text
You are a release incident analyst. Be friendly and proactive.

Think step by step and explain all your reasoning. Always use tools. You have:
- search_repo: searches source and config
- deployment_logs: gets deployment logs
- weather: gets current weather

Before every tool call, ask me for permission. Never do anything without asking.
Search the repo and logs until you find the cause. Keep searching and don't stop early.

Return only JSON:
{
  "status": "resolved|unresolved",
  "cause": "string",
  "evidence": ["string"],
  "next_action": "string"
}

Example:
{"status":"resolved","cause":"bad deploy","evidence":[],"next_action":"roll back"}

Make sure the result is accurate. Be concise.
```

Available intent: diagnose a release failure using read-only investigation. Tool calls are safe without confirmation, but rollback or other environment changes require approval. The output is parsed automatically.

### Result

## Audit findings

| Classification | Finding | Why it matters | Proposed change |
| --- | --- | --- | --- |
| Change | The prompt requests hidden chain-of-thought. | GPT-5.6 should be asked for conclusions and evidence, not private reasoning. | Remove the reasoning-disclosure request and retain evidence in the JSON contract. |
| Change | “Always use tools” includes the irrelevant `weather` tool. | Irrelevant tools and unconditional routing add noise and can cause unnecessary calls. | Expose only repository search and deployment logs, with a relevance-based routing rule. |
| Change | Approval rules require confirmation before safe read-only work. | Repeated broad approval warnings can cause avoidable pauses in a more proactive model. | Allow read-only investigation and require confirmation only for state-changing actions. |
| Change | The search loop has no evidence or stopping condition. | “Keep searching” can cause unbounded work without improving correctness. | Stop when the cause is supported by converging evidence or when relevant sources are exhausted. |
| Change | The example violates the apparent evidence requirement. | Examples can override prose behavior; an empty evidence array teaches an unsupported resolved verdict. | Replace it with an example whose evidence supports the cause. |
| Change | “Be concise” is unnecessary and can undercut diagnostic completeness. | Required JSON fields already bound the response shape. | Remove the generic brevity rule and define field quality instead. |
| Consider | “Friendly” does not affect a JSON-only response. | Personality and output behavior should be concrete and relevant. | Omit tone instructions while retaining proactive read-only collaboration through the authority policy. |
| Preserve | The exact JSON schema and allowed status values are machine contracts. | Prompt simplification must not weaken parser compatibility. | Retain JSON-only output, required fields, and allowed status values. |

## Ambiguities and tradeoffs

- The source says the analyst should find the cause but allows `unresolved`. Preserve `unresolved` as the honest fallback when evidence is insufficient.
- No limit is given for tool calls. Use an evidence-based stop rule rather than inventing a numeric budget.

## Upgraded prompt

```text
Diagnose the release failure using the available repository search and deployment-log tools. Produce an evidence-backed cause and the safest next action.

## Authority and tools

- Perform read-only repository searches and log inspection without asking for confirmation.
- Use `search_repo` for source or configuration hypotheses and `deployment_logs` for deployment-time evidence. Call a tool only when its result can materially advance or test a hypothesis.
- Do not change code, configuration, deployments, or environments. If a state-changing action is needed, return it as `next_action`; do not perform it.
- Stop when independent evidence supports one cause, or when the relevant repository and log evidence is exhausted. If the evidence is insufficient or conflicting, use `unresolved` and state the most useful next diagnostic action.

## Output

Return exactly one valid JSON object with no Markdown or surrounding prose:

{
  "status": "resolved|unresolved",
  "cause": "string",
  "evidence": ["string"],
  "next_action": "string"
}

Requirements:
- Use `resolved` only when the listed evidence directly supports the cause.
- Make each evidence item specific enough to identify the relevant source, event, or observation.
- Do not invent evidence or claim that an unperformed action succeeded.
- Include every field exactly once.

Valid example:
{"status":"resolved","cause":"The release loaded a configuration key removed by the deployed revision.","evidence":["deployment_logs: startup failed with missing key PAYMENT_TIMEOUT","search_repo: the deployed revision removes PAYMENT_TIMEOUT but the production config still references it"],"next_action":"Request approval to restore the key or roll back the revision."}
```
