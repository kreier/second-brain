![GitHub License](https://img.shields.io/github/license/kreier/second-brain)
![GitHub Release](https://img.shields.io/github/v/release/kreier/second-brain)

# Second Brain

A personal knowledge vault: Obsidian-compatible markdown notes, structured
for both human browsing and processing by AI agents (Claude Code, Gemini,
and similar).

## How it works

New material — audio transcripts, conversation exports, notes — lands in
`raw/inbox/`. An agent or I extract the useful content into structured notes
in `processed/`, then the original source moves to `raw/archive/`.

```
raw/inbox/      new, unprocessed material
raw/archive/    processed sources, kept verbatim as provenance (immutable)
processed/      derived notes, organized by type (see below)
moc/            maps of content — curated hub/index notes
templates/      note templates per type
.agent/         agent activity log
```

## Note types and mutability

Every note has a `type` in its frontmatter, which determines both where it
lives and whether it's ever edited after creation:

| type       | folder                    | mutable? |
|------------|----------------------------|----------|
| `log`       | `processed/logs/`            | no — append-only diary entries |
| `fact`      | `processed/topics/`           | no — atomic extracted notes |
| `project`    | `processed/projects/`          | yes — living document, evolves |
| `idea`       | `processed/ideas/`              | yes — blog-style, reiterated over time |
| `travel`     | `processed/travel/`              | yes, while ongoing |

Immutable notes are never edited after creation — corrections or updates
become new notes linked via `supersedes` / `superseded_by` frontmatter.
Mutable notes are edited in place; git history is the version record.

`raw/archive/` is always immutable — it's the permanent, verbatim source of
truth behind every derived note.

See [`frontmatter.md`](frontmatter.md) for the full schema, and
[`AGENT.md`](AGENT.md) for the rules any agent operating on this vault
should follow.

## Status

Early stage — structure and conventions are still settling. No `people/`
category yet by design, since this vault is public.

## License

Content and code in this repository are licensed under Apache 2.0 — see
[LICENSE](LICENSE).
