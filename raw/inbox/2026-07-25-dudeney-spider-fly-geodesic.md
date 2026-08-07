---
captured: 2026-07-25T16:20:00+07:00
source_type: llm-conversation
platform: Claude
raw_id: 2026-07-25-dudeney-spider-fly-geodesic
---

# Raw import: Dudeney spider-and-fly geodesic problem

> Reconstructed summary of a past conversation, imported as example raw
> material for the processing pipeline. Not a verbatim transcript.

- Worked through the classic Dudeney "spider and fly" puzzle: a spider and
  a fly sit at fixed points inside a rectangular room (on opposite walls),
  and the question is the shortest path the spider can crawl along the
  room's surfaces to reach the fly — surprisingly, the shortest path isn't
  always the "obvious" one (e.g. straight across the floor then up a wall);
  depending on room proportions, unfolding a less intuitive combination of
  walls/ceiling gives a shorter path.
- The general method: "unfold" the 3D room into a flat 2D net for each
  candidate combination of surfaces the path could cross, since a straight
  line in the unfolded net corresponds to the shortest path across those
  folded surfaces in 3D. Compare path lengths across all plausible
  unfoldings to find the true minimum.
- Built this out as an HTML/SVG visualization showing the different
  unfolded nets side by side with their straight-line paths drawn in, to
  make the non-obvious solution visually intuitive.
- Open thread: generalizing the same unfolding technique to other
  geodesic-on-a-surface problems (e.g. shortest path across a cube,
  or curved surfaces where true geodesics require calculus of variations
  rather than a flat unfolding).

## Possible follow-ups
- Extract the unfolding method as a general note, separate from this
  specific puzzle instance — it's reusable for other polyhedral
  shortest-path problems.
- Link to the HTML/SVG artifact if it's saved somewhere retrievable.
