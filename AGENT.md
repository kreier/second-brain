# AGENT.md

Instructions for any AI agent (Claude Code, Gemini, or other) operating on
this vault. Read this before touching any file.

## The three-stage flow

1. Material lands in `raw/inbox/` — a transcript, export, or conversation log.
2. You process it: extract structured notes into `processed/`.
3. Once fully extracted, move the source file to `raw/archive/` unchanged.

Never skip step 3. `raw/inbox/` should only ever contain unprocessed material.

## Directory permissions

| Path              | You may...                                      |
|-------------------|--------------------------------------------------|
| `raw/inbox/`       | read, and delete/move (only after processing)    |
| `raw/archive/`      | read only. Never create, edit, or delete here.    |
| `processed/*`        | read always; write depends on `type`, see below   |
| `moc/`                 | read, create, edit (curated index notes)          |
| `templates/`            | read only, unless asked to add a new template      |
| `.agent/changelog.md`     | append only                                        |

## Mutability by type

Every note's `type` frontmatter field determines whether it's immutable or
mutable. This mapping lives in `frontmatter.md` — check it, don't assume.

- **Immutable types** (`log`, `fact`): never edit an existing file. If new
  information corrects or updates one, create a new note and link it via
  `supersedes:` (on the new note) and `superseded_by:` (added to the old
  note's frontmatter — this is the one exception to "never edit," since it's
  a link update, not a content change).
- **Mutable types** (`project`, `idea`, `travel`): edit in place. Update the
  `updated:` field on every edit. Git history is the version record — don't
  create `-v2` files.

## Processing a raw file: step by step

1. Read the file in `raw/inbox/`. If it has frontmatter (`captured`,
   `source_type`, `platform`, `raw_id` — see `frontmatter.md`), use it: set
   the derived notes' `source:` to point at this file's `raw_id`, and let
   `captured` inform the note's `created:` context if the material is being
   processed well after capture. If the raw file has no frontmatter, don't
   block on it — process anyway, and note the gap in `.agent/changelog.md`
   rather than inventing values.
2. Identify discrete atomic ideas, facts, decisions, or events worth keeping.
3. For each one, check whether a related note already exists (search
   `processed/` by title, alias, and tags) before creating a new note —
   prefer linking and extending over duplicating.
4. Create new notes using the matching template in `templates/`, with
   complete frontmatter per `frontmatter.md`. Set `source:` to the inbox
   file's path (it will point to `raw/archive/` after step 6).
5. Link new notes to related existing notes using `[[wikilinks]]`. Add
   entries to a relevant `moc/` note if one exists for the topic/project.
6. Move the source file from `raw/inbox/` to `raw/archive/`, unchanged.
7. Append a line to `.agent/changelog.md` (see format below).
8. Commit with a conventional message, e.g.:
   `process: 2026-08-07-laos-energy-transcript.md -> 3 notes`

## Frontmatter validation

Before writing any note, confirm every required field for its `type` is
present, `type` is a valid enum value, and dates are ISO 8601
(`YYYY-MM-DD` or full timestamp with offset). Do not invent new frontmatter
fields ad hoc — if a new field is genuinely needed, propose it and add it to
`frontmatter.md` first.

## Entity resolution

Before creating a new note for a topic or project, search existing notes for
matching titles, aliases, or close tag overlap. Prefer extending or linking
an existing note over creating a near-duplicate. If genuinely unsure, create
the note but flag it in the changelog for later review rather than silently
merging or silently duplicating.

## Changelog format

Append one line per processing action to `.agent/changelog.md`:

```
- 2026-08-07T14:32:00+07:00 | processed 2026-08-07-laos-energy-transcript.md -> topics/hongsa-lignite-drying.md, topics/hongsa-bot-structure.md | agent: claude-code
```

## Git workflow

Two tiers, depending on how routine the change is.

### Tier 1 — routine processing: commit directly to `main`

Applies when you're following the processing steps above exactly: extracting
notes from a clearly-scoped inbox file, using an existing template, no new
`type`, no ambiguous entity merges. Commit straight to `main`. Keep commits
small — one inbox file (or one clear batch) per commit, not one giant commit
for the whole inbox. Small commits are easier for either of us to revert
individually if one extraction turns out wrong.

Commit message format:

```
process: <inbox-filename> -> <n> notes

- processed/topics/foo.md (new)
- processed/projects/bar.md (updated, linked)

source archived: raw/archive/<inbox-filename>
```

### Tier 2 — structural or judgment-call changes: branch + PR

Applies to anything that isn't purely mechanical:

- proposing a new `type` or any change to `frontmatter.md`
- uncertain entity resolution (unclear whether something duplicates an
  existing note vs. deserves a new one)
- a substantive edit to an existing mutable note that changes its meaning,
  not just appends to it
- bulk operations: re-tagging, migrating a folder, renaming across many files

For these: create a branch named `agent/YYYY-MM-DD-short-description`, make
the change there, and open a PR (`gh pr create`) rather than merging
yourself. Leave it unmerged for review. PR description format:

```markdown
## What
<one-line summary of the proposed change>

## Why
<what triggered this — which inbox file, which ambiguity>

## Open questions
<anything you're unsure about and want a decision on>
```

If a PR is closed without merging, don't re-propose the same change in a
later session unless something material has changed — check open and
recently-closed PRs before proposing a structural change.

### Review queue — for ambiguous-but-not-structural cases

If something is uncertain but doesn't rise to a Tier 2 PR (e.g. "not sure if
this note duplicates an existing one, but not confident enough to merge or
block on it"), commit as Tier 1 and add a line to
`.agent/review-queue.md` instead of opening a PR. Don't leave the queue
entry unresolved silently — it's there for the human to clear, not to be
auto-resolved later without review.

## Hard rules

- Never edit a file under `raw/archive/`.
- Never edit an existing immutable note (`log`, `fact`) — only add
  `superseded_by` links when a new note supersedes it.
- Never delete a processed note. If it's wrong, mark it superseded or, for
  mutable types, correct it in place with a clear commit message.
- Never leave a file in `raw/inbox/` half-processed without noting progress
  in `.agent/changelog.md`.
- This vault is public. Do not add personal, private, or sensitive material
  about identifiable third parties — there is no `people/` category yet by
  design.
