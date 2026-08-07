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

1. Read the file in `raw/inbox/`.
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
