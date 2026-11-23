# PhD research vault

A personal research system for a PhD in robot learning for manipulation
(VLAs, world models, physics-informed models, generalization). It's an
[Obsidian](https://obsidian.md) vault, fed by Zotero, with Claude Code commands
as preset workflows, and built so that AI-written content can never pass as
checked fact.

```
Zotero (papers, PDFs, citekeys) ──auto-export──▶ zotero/library.bib
                                                    │
Claude Code in this folder:  /read  /verify  /ask  /gaps  /log
                                                    │
Obsidian: papers/ concepts/ questions/ daily/ ◀─────┘  + dashboards/
```

## How trust works

Every statement in a note has a label, shown as a coloured callout:

| Callout | Meaning | Who writes it |
|---|---|---|
| `> [!paper]` green | From the paper, **always with page/section** | Claude or you |
| `> [!ai]` orange | AI summary or interpretation, may be wrong | Claude |
| `> [!idea]` purple | Your own idea | **Only you** |
| `> [!unverified]` red | No checked source yet | Claude or you |

Each note climbs a ladder: **draft** (Claude wrote it) → **verified** (`/verify`
re-checked every claim against the PDF) → **trusted** (you reviewed it and set
`trust: trusted` and `signed_off_on: YYYY-MM-DD` yourself). `/gaps` only uses
trusted notes.

Metadata (titles, authors, years, venues) comes only from Zotero, arXiv or
Semantic Scholar via `scripts/meta.py`, never from the model's memory.
References that can't be resolved are flagged `unresolved`, not guessed.
`scripts/check_vault.py` enforces the rules mechanically (uncited `[!paper]`
lines, trust without sign-off, `/gaps` questions built on untrusted notes).

## Commands

Run `claude` inside this folder, then:

| Command | What it does |
|---|---|
| `/read <citekey or arXiv id> [skim\|deep]` | Reads the PDF, writes `papers/<citekey>.md` with cited claims, a generalization angle, concept links, and the **foundation chain**: the prior works the paper says it builds on, as stub notes to read next |
| `/verify <note>` | Re-reads the PDF and marks every claim ✅ / ⚠️ / ❌ in the note's verification log. Sets `verified` only if all pass |
| `/ask <question>` | Answers only from your vault, with `[[note]]` + page citations, and says what the vault doesn't cover |
| `/gaps [topic]` | Compares claims, benchmarks and assumptions across **trusted** notes and drafts research questions in `questions/`, with real search results for "has this been done?" |
| `/log <text>` / `/log week` | Adds to today's daily note / drafts the weekly review with reading vs target |

## Folders

| Folder | Contents |
|---|---|
| `inbox/` | Quick captures and new PDFs to triage |
| `daily/` | Daily logs (`YYYY-MM-DD.md`) |
| `papers/` | One note per paper, named by its Better BibTeX citekey |
| `concepts/` | Explainers written once and reused, with prerequisites leading to fundamentals |
| `projects/` | Research directions and experiments |
| `questions/` | Research questions and gap reviews |
| `reviews/weekly/` | Weekly reviews |
| `templates/` | Note templates |
| `dashboards/` | Start at `dashboards/Home.md` |
| `zotero/` | `library.bib`, auto-exported by Zotero |
| `scripts/` | `meta.py` (metadata lookup), `check_vault.py` (rule checker) |

## Setup (about 20 minutes)

### 1. Clone the vault
```bash
git clone git@github.com:<you>/<repo>.git ~/phd-vault
```

### 2. Obsidian
1. Install Obsidian and choose **Open folder as vault** → `~/phd-vault`.
2. Settings → Community plugins → turn off Restricted mode → Browse, and install + enable:
   - **Dataview** (required). In its settings, turn on **Enable JavaScript Queries**
     (the weekly progress dashboard uses it).
   - **Obsidian Git** (recommended): auto-commit and pull every few minutes, so
     Claude sessions in the cloud and your laptop stay in sync.
   - **Zotero Integration** (optional): imports your PDF highlights into notes.
     Point it at Better BibTeX, and set its output folder to `inbox/` so
     imported highlights don't overwrite paper notes.
3. Settings → Appearance → CSS snippets: make sure **provenance-callouts** is on
   (it colours the four callouts).
4. Settings → Core plugins: Daily notes and Templates are already configured
   (`daily/`, `templates/`).

### 3. Zotero + Better BibTeX
1. Install [Zotero 7](https://www.zotero.org/download/) and the
   [Better BibTeX](https://retorque.re/zotero-better-bibtex/installation/) plugin.
2. Citekey format (Settings → Better BibTeX → Citation keys): the default
   `auth.lower + year + shorttitle(1,0).lower` gives keys like `chi2023diffusion`.
   Pick one format and don't change it later, since note names depend on it.
3. Right-click your library (or a "PhD" collection) → **Export…** → format
   **Better BibTeX**, tick **Keep updated**, and save to
   `~/phd-vault/zotero/library.bib`. Tick "Export files" off (PDF paths are still
   written to the `file` field).
4. Add papers to Zotero with the browser connector so they come with real
   metadata and PDFs.

### 4. Claude Code
1. Install Claude Code and run `claude` from `~/phd-vault`. It reads `CLAUDE.md`
   and picks up the commands in `.claude/skills/`.
2. Optional: set `S2_API_KEY` (free from Semantic Scholar) for higher rate limits.
3. Try it: add a paper to Zotero, then `/read <its citekey> skim`, then
   `/verify <citekey>`, review the note, and set `trust: trusted` +
   `signed_off_on`.

### Note on PDFs and cloud sessions
PDFs stay in Zotero's storage and are not committed (`*.pdf` is gitignored).
`/read` and `/verify` need the PDF, so run them on your laptop, or drop the PDF
in `inbox/` for a one-off. Cloud sessions can still use `/ask`, `/gaps` and
`/log` on the notes.

## Weekly rhythm (suggested)
- **Daily**: `/log` what you did. Triage `inbox/`.
- **Each read**: `/read` → `/verify` → your review and sign-off → add an `[!idea]`.
- **Weekly**: `/log week`, check `dashboards/Weekly progress.md` (target 3 deep +
  10 skims, edit the numbers there), clear the Trust queue, and run `/gaps` on
  one topic.

## Not set up yet
- **Daily paper brief** (arXiv cs.RO/LG/CV + keywords, conferences, labs,
  citation alerts): sources are still being decided. It'll write into `inbox/`.
