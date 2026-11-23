---
name: verify
description: Re-check every claim in a paper or concept note against the source PDF and record pass/fail with locations. Use when the owner says /verify or asks to fact-check a note.
argument-hint: <note name or path>
---

# /verify: check a note against its source

You are an independent checker. Assume the note may be wrong. Don't trust your
memory of the paper or of writing the note: re-read the PDF now.

1. Open the note. For a paper note, find the PDF via
   `python3 scripts/meta.py bib <citekey>`. For a concept note, verify each
   cited claim against the cited paper notes' PDFs.
2. Re-check the metadata: re-run `meta.py` (bib, else arxiv/doi) and compare
   title, authors, year, venue. Report any mismatch.
3. For **every** `[!paper]` line and every factual sentence in `[!ai]`
   callouts that cites a location:
   - Go to that page/section. Does the source say it? Is the number exact?
     Is the location right?
   - Verdict: ✅ supported, ⚠️ supported but wrong location / imprecise
     (give the fix), ❌ not supported / contradicted.
4. Check the Foundations: does the paper's text at the given location really
   say it builds on each listed work?
5. Write the results into `## Verification log` at the end of the note:
   ```
   ### YYYY-MM-DD /verify
   - ✅ (p. 4) "..." 
   - ⚠️ (§3.2 → §3.3) "..." 
   - ❌ (Tab. 2) "...": the table reports 63%, not 68%.
   Metadata: ✅ matches zotero
   ```
6. Fix ⚠️ items in place (location only). Do **not** silently fix ❌ items:
   move each ❌ claim into an `[!unverified]` callout with the reason, or
   correct it with the right citation and say so in the log.
7. If every check is ✅ (after ⚠️ fixes), set `trust: verified` and
   `verified_on:` today. Otherwise keep `trust: draft`.
   **Never set `trusted` or `signed_off_on`.** That's the owner's step.
8. Run `python3 scripts/check_vault.py --fix`.
9. Reply with the counts (✅/⚠️/❌), the ❌ items in one line each, and, if
   verified, a reminder: "Review it and set `trust: trusted` +
   `signed_off_on` when you're happy."
