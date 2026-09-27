---
id: goodharts-vs-campbells-law
type: idea
title: Goodhart's Law vs. Campbell's Law
created: 2026-07-02T11:05:00+07:00
updated: 2026-08-07T19:47:34+07:00
source: raw/archive/2026-07-02-goodharts-vs-campbells-law.md
status: draft
tags: [metrics, systems, incentives, proxy-metrics, mental-models]
related: ["[[2026-07-02-goodharts-law]]", "[[2026-07-02-campbells-law]]"]
supersedes: 2026-07-02-goodharts-vs-campbells-law
---

Both laws describe what happens when a quantitative measure becomes an optimization target, but they frame the failure differently.

- **Goodhart's Law (Statistical / Information-Theoretic)**: The proxy metric loses its correlation with the underlying objective once it is directly targeted. The failure is epistemic — the number stops meaning what it meant.
- **Campbell's Law (Behavioral / Institutional)**: The metric creates corrupting incentive pressure on the people and processes within the system. The failure is social — actors game the measure at the expense of the real goal.

The distinction matters for diagnosis: Goodhart points at the model (the metric is the wrong thing to optimize), Campbell points at the incentive structure (the right metric breaks under pressure regardless).

## Worked examples

| Example | Better framing | Why |
|---|---|---|
| Teaching to the test | Campbell | Teachers and schools face institutional pressure; the underlying educational process is corrupted by human actors |
| Lines-of-code KPI | Goodhart | The proxy simply stops tracking output quality once targeted; no active corruption needed |
| AI reward hacking | Goodhart | Optimizer finds a local maximum in the reward surface that diverges from intent — purely mechanical, no human behavior involved |

## Open threads

- How do these two laws apply to AI training at the institutional level (labs, evals, benchmarks) rather than just the algorithmic level? Benchmark saturation (e.g. MMLU, HumanEval) looks like Campbell's — the benchmark survives but the signal corrupts as the industry targets it.
- Look into the **Lucas critique** (macroeconomics, 1976) as a third member of this family: structural relationships in econometric models break down once agents anticipate and adapt to policy rules. Possibly worth a separate fact note.
- Other candidates: Cobra effect, Perverse incentive (Wikipedia), Teach to the test literature.
