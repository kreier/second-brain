# frontmatter.md

Single source of truth for note frontmatter. Any agent or script writing to
this vault must validate against this schema before saving a file.

`schema_version: 1`

## Type enum and mutability

| type       | folder                 | mutable | required extra fields          |
|------------|-------------------------|---------|----------------------------------|
| `log`       | `processed/logs/`         | no       | —                                  |
| `fact`      | `processed/topics/`        | no       | —                                  |
| `project`    | `processed/projects/`       | yes      | `status`                            |
| `idea`       | `processed/ideas/`           | yes      | —                                  |
| `travel`     | `processed/travel/`           | yes      | `location`, `dates`                  |

Adding a new `type`: add a row here first, add a matching folder under
`processed/`, add a template under `templates/`, then use it. Never invent a
`type` value on the fly.

## Fields common to all notes

```yaml
---
id: 2026-08-07-hongsa-lignite-drying     # slug, unique, stable, filename minus extension
type: fact                                # one of the enum above
title: Hongsa lignite pre-drying technology
created: 2026-08-07T14:32:00+07:00        # ISO 8601, when the note was written
updated: 2026-08-07T14:32:00+07:00        # bump on every edit (mutable types only)
source: raw/archive/2026-08-07-laos-energy-transcript.md   # where this was derived from, if any
status: processed                          # draft | processed | archived
tags: [energy, laos, engineering]           # free-form, lowercase, kebab-case
related: ["[[Laos Energy Sector]]"]           # wikilinks to related notes
supersedes: null                             # id of note this replaces, if any
superseded_by: null                           # id of note that replaces this, if any
---
```

Notes:

- `id` should match the filename (without `.md`) so links and files never
  drift apart. Prefer `YYYY-MM-DD-slug` for `log`/`fact`/`travel`,
  plain `slug` for `project`/`idea` (they aren't tied to a single date).
- `tags` are for cross-cutting retrieval (topics, keywords, entities). `type`
  is for structural classification. Don't duplicate the type as a tag.
- `related` uses Obsidian wikilink syntax so links survive folder moves.
- `source` is required if the note was derived from something in
  `raw/archive/`. Omit or set `null` for notes written directly (e.g. an
  `idea` you typed straight into the vault).

## Raw material frontmatter (`raw/inbox/`, `raw/archive/`)

Separate, smaller schema — raw files capture objective facts about the
*source*, not editorial decisions about what it means. Do not put `type`,
`tags`, or `related` on raw files: what a piece of raw material becomes
(one note or several, which types) is an extraction decision made during
processing, not something to pre-judge on the source itself.

```yaml
---
captured: 2026-06-18T09:15:00+07:00    # when this material was captured/exported
source_type: llm-conversation           # llm-conversation | voice-transcript | chat-export | email-export | note
platform: Claude                          # e.g. Claude, ChatGPT, Gemini, WhatsApp, voice-memo app
raw_id: 2026-06-18-laos-energy-hongsa-lignite   # matches filename stem; stable reference for `source:` even if renamed
---
```

All four fields are optional but recommended — populate what you know at
capture time. `raw_id` in particular is worth setting even for a quick
voice memo, since it's the anchor processed notes will point back to via
`source:`, and it's easiest to get right before the file is renamed or
moved.

This frontmatter travels with the file from `raw/inbox/` to `raw/archive/`
unchanged — it's part of the immutable provenance record.

## Type-specific fields

### `project`

```yaml
status: active        # active | paused | done
repo: null              # optional link to a GitHub repo, e.g. github.com/kreier/...
```

### `travel`

```yaml
location: Luang Prabang, Laos
dates: 2026-07-10/2026-07-18     # ISO date range
trip_id: 2026-laos                 # groups notes from the same trip
```

### `log`

No extra required fields. One file per day is the convention:
`processed/logs/2026/2026-08-07.md`. Never edit after creation — a
reflection on a past day is a new log entry linking back with a wikilink.

### `fact`

No extra required fields. Keep these atomic — one discrete claim, decision,
or piece of information per note. If you're writing more than a few
paragraphs, it's probably actually an `idea` or `project` note instead.

## Immutability mechanics

For `log` and `fact` notes: never edit the body or frontmatter after
creation, with one exception — `superseded_by` may be added later to point
at a newer note. To correct or update an immutable note, create a new note
and set its `supersedes:` field to the old note's `id`, then add
`superseded_by:` pointing back on the old note.

For `project`, `idea`, `travel`: edit freely. Bump `updated:` on every
change. Rely on git history for the version record — don't create `-v2`
files or duplicate notes for revisions.
