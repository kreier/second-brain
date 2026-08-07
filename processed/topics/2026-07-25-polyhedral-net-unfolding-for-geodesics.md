---
id: 2026-07-25-polyhedral-net-unfolding-for-geodesics
type: fact
title: Polyhedral Net Unfolding for Geodesics
created: 2026-07-25T16:20:00+07:00
source: raw/archive/2026-07-25-dudeney-spider-fly-geodesic.md
status: processed
tags: [geometry, mathematics, algorithms, geodesics]
related: ["[[2026-07-25-dudeneys-spider-and-fly-puzzle]]"]
supersedes: null
superseded_by: null
---

Net unfolding is a general technique for computing shortest surface paths (geodesics) on 3D polyhedral surfaces without smooth calculus.

### Technique
1. **Develop Flat Nets**: Unfold the 3D faces of the polyhedron into candidate 2D planar developments (nets) representing different sequences of adjacent face traversals.
2. **Straight-Line Geodesics**: On a flat Euclidean 2D net, the shortest path between any two points is a straight line segment.
3. **Compare Candidates**: Calculate Euclidean distances of straight-line paths across all plausible net unfoldings to identify the global minimum surface path.
