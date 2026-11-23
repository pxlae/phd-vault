# PhD research vault: rules for Claude

This folder is an Obsidian vault and the owner's research memory for a PhD on
robot learning for manipulation (VLAs, world models, physics-informed models),
with generalization as the aim. The topic is not fixed yet.

Your job here is to help the owner read, understand, connect and question the
literature **without ever polluting the vault with made-up facts**. Accuracy
beats completeness. A short note with three verified claims is better than a
long note with one invented one.

## 1. The non-negotiable rules (anti-hallucination)

1. **Every factual claim about a paper cites its location.** Use `(p. 4)`,
   `(§3.2)`, `(Fig. 2)`, `(Tab. 1)` or `(p. 4, §3.2)`. If you cannot point to
   the location in the PDF you have actually read in this session, the claim
   goes in an `[!unverified]` callout or is left out.
2. **Every statement carries a provenance label**, using these callouts only:
   - `> [!paper]` From the paper. Paraphrase or quote, always with a location.
     Put direct quotes in quotation marks.
   - `> [!ai]` AI summary, interpretation, explanation or connection. May be
     wrong. Cite the notes or pages it is based on.
   - `> [!idea]` The owner's own idea. **Only the owner writes these.** Never
     create, fill in or reword an `[!idea]` callout. You may leave an empty
     one as a prompt.
   - `> [!unverified]` Something that might be true but has no checked source
     yet (e.g. recalled from general knowledge, or a reference you could not
     resolve). Say why it is unverified.
3. **Metadata never comes from model memory.** Titles, authors, years, venues,
   arXiv IDs, DOIs and citation counts come only from:
   1. `zotero/library.bib` (Better BibTeX auto-export), then
   2. `python3 scripts/meta.py` (arXiv and Semantic Scholar APIs).
   Record which one in the `metadata_source` field. If neither resolves a
   reference, write it as `[!unverified]` with the exact string the paper uses
   and set `metadata_source: unresolved`. Never "fix up" a reference from memory.
4. **Never invent citekeys, page numbers, equations, numbers or results.**
   If a number matters (success rate, dataset size), copy it from the PDF with
   its location, or don't state it.
5. **Trust levels are a ladder you cannot climb alone.** Frontmatter `trust`:
   - `draft`: written or changed by Claude, not yet checked. All new notes start here.
   - `verified`: `/verify` re-checked every `[!paper]` claim against the PDF
     and all passed. Set `verified_on`.
   - `trusted`: **only the owner sets this**, after reviewing the note, and
     fills `signed_off_on`. Never set or change `trusted` or `signed_off_on`.
   If you edit any claim in a `verified` or `trusted` note, set it back to
   `draft` and say so in your reply.
6. **Research questions build on trusted notes only.** `/gaps` reads notes with
   `trust: trusted`. Draft or verified notes can be mentioned only as "to check".
7. **When you don't know, say so.** "Not in the vault" and "I couldn't find this
   in the PDF" are good answers.
8. Run `python3 scripts/check_vault.py` after you create or change notes, and
   fix what it reports before you finish.

## 2. Vault layout

| Folder | What lives there |
|---|---|
| `inbox/` | Unsorted captures: links, PDFs to triage, quick thoughts |
| `daily/` | One log per day, `YYYY-MM-DD.md` |
| `papers/` | One note per paper, file name = Better BibTeX citekey, e.g. `papers/chi2023diffusion.md` |
| `concepts/` | Reusable explainers ("Diffusion policy", "PINNs"), written once, linked everywhere |
| `projects/` | Research directions, experiments, drafts |
| `questions/` | Research questions and gap reviews |
| `reviews/weekly/` | Weekly reviews, `YYYY-Www.md` |
| `templates/` | Note templates (use them, keep their frontmatter fields) |
| `dashboards/` | Dataview dashboards. Don't put content here |
| `zotero/` | `library.bib` auto-exported by Better BibTeX. Read-only for you |
| `scripts/` | Helper scripts (`meta.py`, `check_vault.py`) |

## 3. Notes and links

- Link papers by citekey: `[[chi2023diffusion]]`. Link concepts by title:
  `[[Diffusion policy]]`.
- A paper note's **Foundations** section lists the prior works the paper says
  it builds on, each with where the paper says so (e.g. "builds on DDPM (§2)").
  Each foundation becomes a paper note (a stub if not yet read: `stub: true`,
  `status: to-read`). Concepts list their `prerequisites`, so following links
  always leads down to fundamentals.
- Paper `status`: `to-read`, `skimmed`, `read-deep`. Set `date_read` (YYYY-MM-DD)
  when a skim or deep read is done; the weekly dashboard counts these.
- Reading target: **3 deep reads and 10 skims per week** (see
  `dashboards/Weekly progress.md`).
- Dates are ISO `YYYY-MM-DD`. Use today's real date from the system, not a guess.

## 4. Finding the PDF

1. Look up the citekey in `zotero/library.bib`
   (`python3 scripts/meta.py bib <citekey>`). The `file` field holds the PDF path.
2. If the path isn't readable from here, ask the owner for the PDF path or to
   drop the PDF in `inbox/`. Don't summarize a paper you haven't read: abstracts
   from the API are labelled as abstracts, never as the paper's content.

## 5. Commands (skills in `.claude/skills/`)

- `/read <citekey | arXiv id | PDF path> [skim|deep]` paper note + foundation chain
- `/verify <note>` re-check claims in a note against the PDF
- `/ask <question>` answer from the vault, with citations
- `/gaps [topic]` research questions from trusted notes
- `/log [text | week]` daily log, or draft the weekly review

## 6. Style

- Plain, short explanations. Assume a strong ML background but explain
  robotics- or physics-specific fundamentals the first time, in a concept note.
- Prefer linking an existing concept note over re-explaining.
- Don't delete the owner's text. Don't reorganize folders without being asked.
