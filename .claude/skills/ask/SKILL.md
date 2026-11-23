---
name: ask
description: Answer a research question using only what is in the vault, citing notes and page locations, and saying clearly what is not covered. Use when the owner says /ask or asks a question about their literature.
argument-hint: <question>
---

# /ask: answer from the vault

1. Search the vault (`papers/`, `concepts/`, `questions/`, `projects/`,
   `daily/`) with grep/glob for the question's key terms, synonyms and linked
   concepts. Follow links one or two hops (concepts → papers, foundations).
2. Read the relevant notes. Note each one's `trust` level.
3. Answer using only those notes. Structure:
   - **Answer**: short, direct. Each claim ends with its source, e.g.
     `([[chi2023diffusion]], §4.1)`. Carry over the page/section from the
     note; don't invent a location the note doesn't have.
   - **Confidence**: say which sources are `trusted`, `verified` or `draft`.
     Flag any answer resting on draft notes.
   - **Not in the vault**: what the question needs that the vault doesn't
     cover. You may suggest what to read, but label suggestions from your own
     knowledge as `[!unverified]` and offer to resolve them with
     `python3 scripts/meta.py search "<query>"` (real results only).
   - **Disagreements**: if notes conflict, show both sides with sources.
4. Answer in chat by default. If the owner asks to save it, write it to
   `questions/` from `templates/question.md` with `origin: own`, using
   `[!ai]` callouts.
5. Don't change any notes while answering.
