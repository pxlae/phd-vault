---
name: log
description: Record what the owner did today in the daily note, or with "week" draft the weekly review with reading progress vs the 3 deep + 10 skims target. Use when the owner says /log, "log this", or asks for the weekly review.
argument-hint: [what you did | week]
---

# /log: daily log and weekly review

## `/log <text>` (default)
1. Get today's real date (`date +%F`). Open `daily/YYYY-MM-DD.md`, creating it
   from `templates/daily.md` if missing.
2. Put the owner's text under the right heading (`Did`, `Read`, `Thoughts and
   questions`, `Next`). Keep their wording; you may tidy it into bullets.
   Their thoughts go in the `[!idea]` callout as they wrote them.
3. If they mention a paper, link it by citekey if a note exists. If they say
   they read it, ask whether it was a skim or deep read (unless clear) and
   update that note's `status` and `date_read`.
4. If the text is empty, show today's log and what's still unchecked under `Next`.

## `/log week`
1. Work out the ISO week (`date +%G-W%V`) and its Monday–Sunday dates.
2. Create `reviews/weekly/YYYY-Www.md` from `templates/weekly-review.md`
   (fill `week`, `start`, `end`).
3. Count papers in `papers/` with `date_read` in the week: `read-deep` → deep,
   `skimmed` → skims. Fill `deep_reads` and `skims` and compare to the target
   (3 deep, 10 skims). Count from frontmatter, not from memory.
4. Summarize the week's daily notes into `[!ai]` bullets under a "Week in
   brief" heading, linking the daily notes. Leave `What I learned` as an empty
   `[!idea]` for the owner.
5. List notes waiting for `/verify` or sign-off, and open questions in
   `questions/` with status `open`.
6. Reply with the counts vs target and the top 3 suggested next reads
   (from the `to-read` queue, foundations first).
