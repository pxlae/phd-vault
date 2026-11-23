---
name: gaps
description: Propose candidate research questions by comparing claims, assumptions and evaluations across TRUSTED notes only. Use when the owner says /gaps or asks for research gaps, open problems or a gap review.
argument-hint: [topic or concept, optional]
---

# /gaps: research questions from trusted notes

The point is good, *novel* questions grounded in evidence the owner has
checked. Inputs are limited to notes with `trust: trusted`.

1. Collect `papers/` and `concepts/` notes with `trust: trusted` (filter by the
   topic if given: linked concepts, tags, foundations). List the draft/verified
   notes on the topic separately as "not used: needs sign-off".
   If fewer than 3 trusted notes match, stop: say so, list which notes would
   need sign-off, and don't speculate.
2. Build a comparison from those notes only (cite note + location for each cell):
   - claims and results; tasks / robots / benchmarks; what generalization is
     tested (objects, scenes, embodiments, tasks, physics, language);
     assumptions (state, sensing, sim vs real, data scale); stated limitations.
3. Look for:
   - **Contradictions**: papers that disagree, or results that don't fit together.
   - **Missing evaluations**: an axis of generalization nobody tests; a
     benchmark gap; no real-robot or no out-of-distribution test.
   - **Untested assumptions**: shared assumptions no paper varies.
   - **Transplants**: a method from one note that addresses a limitation stated in another.
   - **Stated future work** that later notes don't address.
4. Write 3–7 candidate questions. For each, create `questions/<short-title>.md`
   from `templates/question.md` with `origin: gaps-review`, `status: open`,
   `created:` today, `based_on:` the trusted notes used. The question itself
   and its rationale go in `[!ai]` callouts with citations. Fill **What would
   count as an answer** concretely (an experiment, a dataset, an analysis).
5. **Novelty is not established by you.** In each question's "Risks" section,
   write `[!unverified]` search queries, and run
   `python3 scripts/meta.py search "<query>" 10` for each. Report real hits
   that may already answer it (titles from the API only). Never claim "no one
   has done this".
6. Also write a summary note `questions/gap-review-YYYY-MM-DD.md` linking the
   questions and the comparison table.
7. Run `python3 scripts/check_vault.py` (it rejects gaps-review questions based
   on untrusted notes). Reply with the questions, one line each, ranked by how
   well supported they are, and remind the owner to add their own `[!idea]` take.
