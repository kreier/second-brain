# AGENT.md — Operating Instructions for AI Agents

Instructions for any AI agent (Antigravity, Claude Code, Gemini CLI, or other) operating on this repository. Read this before touching any file.

---

## 1. Roles & Division of Responsibility

To maintain long-term architectural coherence, responsibilities are strictly divided:

- **The User**: Defines goals, hardware constraints, priorities, feature scope, and signs off on phase completions.
- **ChatGPT**: Serves as the conceptual sounding board for exploring designs, drafting ADRs, and breaking complex phases into actionable tasks.
- **The Coding Agent (You)**: Reads the repository documentation, implements scoped tasks, executes tests, updates `docs/STATUS.md`, records journal entries in `docs/journal/`, and preserves architectural constraints.

---

## 2. Before Making Any Code or Documentation Changes

Always follow this sequence before starting work:

1. Read [`README.md`](README.md).
2. Read [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).
3. Read [`docs/STATUS.md`](docs/STATUS.md) to understand current state.
4. Read [`docs/ROADMAP.md`](docs/ROADMAP.md) and the current phase specification in [`docs/phases/`](docs/phases/).
5. Check existing tests and verification commands.

### Golden Rules for the Coding Agent
- **Never redesign the architecture**: Do not change agreed architecture without discussing it first and recording the decision as an Architectural Decision Record in `docs/decisions/`.
- **Code to configuration, optimize for the Reference Profile**:
  - Never hardcode host IPs (`10.5.5.5`), `/mnt/memory`, or serial devices into application code or Dockerfiles. All services must read configuration from `settings.yml` (see [`config/settings.example.yml`](config/settings.example.yml)) and environment variables.
  - When analyzing performance, context windows, tensor offloading, and power control, benchmark against the [Canonical Reference Profile](docs/profiles/reference-vault-penta.md) (TX3 Mini at `10.5.5.2`, USB Memory, and Penta at `10.5.5.5` Quad-GPU Pascal 30GB VRAM).
- **Work in small, testable slices**: Focus strictly on the active task within the current phase.
- **Never commit personal notes to git**: Real personal knowledge lives on the external memory mount (`/mnt/memory`). Only safe synthetic data belongs in `demo/vault/`.
- **Update status after work**: Once tasks or tests are executed, update `docs/STATUS.md` and check off items in the active phase specification.

## 3. Knowledge Vault Ingestion & Note Mutability Rules

When operating on the Obsidian vault notes on the external memory store (or in `demo/vault/`):

> [!NOTE]
> The canonical vault directories (`raw/inbox/`, `raw/archive/`, `processed/`, `moc/`) reside on the external **Memory** storage mount (`/mnt/memory` on the TX3 Mini or the path in `settings.yml`), not in the root git tree. Sample fixtures are provided in `demo/vault/`.

### The Three-Stage Flow
1. Material lands in `raw/inbox/` — transcript, export, email, chat log.
2. Extract atomic, structured notes into `processed/` per [`frontmatter.md`](frontmatter.md).
3. Move the source file to `raw/archive/` unchanged.

### Directory Permissions
| Path | Allowed Actions |
|---|---|
| `raw/inbox/` | Read, and move to archive (only after extraction) |
| `raw/archive/` | **Read only**. Cryptographically permanent. Never edit or delete. |
| `processed/*` | Read always; write depends on `type` (see below) |
| `moc/` | Read, create, edit (curated Maps of Content) |
| `templates/` | Read only, unless asked to add a new note template |
| `.agent/changelog.md` | Append only |

### Mutability by Note Type
Every note's `type` in its YAML frontmatter determines whether it is mutable:
- **Immutable Types (`log`, `fact`)**: Never edit an existing note. If new information updates or corrects an existing note, create a new note and link it via `supersedes:` and `superseded_by:`.
- **Mutable Types (`project`, `idea`, `travel`, `moc`)**: Edit in place. Update `updated:` timestamp on every edit. Git history provides the version record.

### Vault Processing Procedure
1. Read file in `raw/inbox/`. Use `captured`, `source_type`, `platform`, `raw_id` if present.
2. Identify atomic facts, ideas, decisions, or events worth retaining.
3. Check `processed/` (by title, alias, and tags) to link/extend rather than duplicate.
4. Create notes using templates from `templates/` with validated frontmatter per [`frontmatter.md`](frontmatter.md). Set `source:` to `raw_id`.
5. Link related notes with `[[wikilinks]]`. Update relevant `moc/` hub notes.
6. Move source file from `raw/inbox/` to `raw/archive/` unchanged.
7. Append entry to `.agent/changelog.md`.

---

## 4. Git Commit Standards

Keep commits focused and semantic:
- `feat(web): ...`
- `feat(curator): ...`
- `feat(brain): ...`
- `feat(stats): ...`
- `feat(manager): ...`
- `process: <inbox-file> -> <n> notes`
- `docs: ...`
- `test: ...`

When a phase's acceptance criteria are fully met, mark the phase complete in `docs/STATUS.md` and recommend tagging a release (e.g. `v0.1.0` for Phase 1).

---

## 5. Hard Invariants

1. Never edit or delete files under `raw/archive/`.
2. Never delete existing processed notes.
3. Containers must remain stateless; all persistent knowledge must live on `/memory`.
4. The host-level manager must remain outside Docker containers.
5. In vault operation, zero personal data or unvetted external telemetry may be transmitted out of the `10.5.5.0/24` subnet.
