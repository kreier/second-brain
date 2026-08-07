---
id: 2026-07-02-goodharts-law
type: fact
title: Goodhart's Law
created: 2026-07-02T11:05:00+07:00
source: raw/archive/2026-07-02-goodharts-vs-campbells-law.md
status: processed
tags: [metrics, economics, systems, proxy-metrics, AI]
related: ["[[2026-07-02-campbells-law]]", "[[2026-07-02-goodharts-vs-campbells-law]]"]
supersedes: null
superseded_by: null
---

Goodhart's Law states: "When a measure becomes a target, it ceases to be a good measure."

Originally formulated by British economist Charles Goodhart in the context of monetary policy and economic indicators, the principle applies broadly to any quantitative system where a proxy metric is directly targeted for optimization. Once targeted, the correlation between the proxy metric and the underlying objective breaks down.

### Classic Examples
- **Software Engineering**: Optimizing proxy KPIs such as lines of code written or ticket closure counts leads to inflated metrics without improving actual software quality or output.
- **AI Training (Reward Hacking)**: In reinforcement learning, optimizing a model directly against a surrogate reward function can cause reward hacking, where the AI optimizes the score in unintended ways that diverge from human intent.
