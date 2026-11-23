---
name: read
description: Read a paper (citekey, arXiv id or PDF path) and write its vault note with page-cited claims, provenance callouts and a foundation chain back to fundamentals. Use when the owner says /read, "read this paper", or drops a paper to process.
argument-hint: <citekey | arXiv id | PDF path> [skim|deep]
---

# /read: paper → note + foundation chain

Follow CLAUDE.md rules at every step. Depth defaults to `skim` unless the owner says `deep`.

## 1. Resolve the paper (real metadata only)
1. If given a citekey: `python3 scripts/meta.py bib <citekey>`.
2. If given an arXiv id/URL: `python3 scripts/meta.py arxiv <id>`. Then check
   whether it's already in `zotero/library.bib` (search by arXiv id or title).
   If it isn't, tell the owner to add it to Zotero so it gets a citekey, and
   use a provisional file name `<firstauthor><year><firstword>` (lowercase,
   from the API metadata) with `metadata_source: arxiv`.
3. If given a PDF path only: read the first page, take the title from it, then
   `python3 scripts/meta.py title "<title>"` and confirm title and year match.
4. If a note already exists in `papers/`, update it instead of overwriting.
   Keep everything inside `[!idea]` callouts and the `trust` fields untouched.
   If it's a stub, fill it in and set `stub: false`.
5. If nothing resolves: stop and ask. Never write metadata from memory.

## 2. Read the PDF
- Read the actual PDF (path from the `file` field / `pdf`). If you can't open
  it, ask the owner for the PDF. Do not write a paper note from the abstract
  alone; at most write a stub labelled "abstract only".
- **skim**: abstract, intro, figures, method overview, main results table,
  conclusion and limitations.
- **deep**: the whole paper including appendix sections relevant to the method
  and experiments.
- Track page numbers and section numbers as you read. Every `[!paper]` line
  needs one.

## 3. Write `papers/<citekey>.md` from `templates/paper.md`
- Fill frontmatter from step 1 only. `trust: draft`. `status: skimmed` or
  `read-deep`. `date_read:` today's real date.
- `[!paper]` = what the paper says, with location. Copy numbers exactly.
- `[!ai]` = your explanation or interpretation, citing what it's based on.
- Anything you believe but can't locate → `[!unverified]` with the reason.
- Leave `## My notes` as an empty `[!idea]` callout. Never write in it.
- Fill the **Generalization angle**: what kind of generalization the paper
  tests (objects, scenes, embodiments, tasks, physics, language), with where.

## 4. Foundation chain (the "what is this built on" part)
1. Find, **in the paper's own text**, the 3–6 prior works it says it builds on
   (e.g. "we build on", "following", "extends", the method section's
   background). Record where it says so.
2. Optionally cross-check with `python3 scripts/meta.py refs <arxiv|doi>`
   (influential references first). Only list a work as a foundation if the
   paper's text supports it.
3. Resolve each foundation's metadata: library.bib first, else
   `meta.py arxiv/doi/title`. Unresolvable → `[!unverified]` with the exact
   string the paper uses.
4. For each foundation without a note, create a **stub** in `papers/`
   (frontmatter only + one `[!ai]` line on why it matters here, citing this
   paper's location), `stub: true`, `status: to-read`, `trust: draft`.
   If it's not in Zotero, name it provisionally and list it in your reply so
   the owner can add it.
5. Add them to `foundations:` in frontmatter and to the Foundations section.

## 5. Concepts
- For each key concept (2–5), link `[[Concept name]]`. Check `concepts/` first
  (including `aliases`) and reuse.
- If a concept note doesn't exist and the paper explains it, create it from
  `templates/concept.md`: `[!ai]` explanation citing the paper and location,
  `[!paper]` for equations with location, and `prerequisites` that lead one step
  further down towards fundamentals. Keep it short. `trust: draft`.

## 6. Finish
1. Add a line to today's daily note (`daily/YYYY-MM-DD.md`, create from the
   template if needed) under `## Read`: `[[citekey]] (skim|deep): one line`.
2. Run `python3 scripts/check_vault.py --fix` and fix every error.
3. Reply with: the gist (2–3 lines), the foundations found (with which ones
   are new stubs or unresolved), concepts created, papers to add to Zotero,
   and a reminder that the note is `draft` until `/verify` and their sign-off.
