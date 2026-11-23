#!/usr/bin/env python3
"""Check the vault's anti-hallucination rules. Run after any note changes.

  python3 scripts/check_vault.py          # report problems (exit 1 if errors)
  python3 scripts/check_vault.py --fix    # also sync the `has-unverified` tag

Checks:
  - every line in a [!paper] callout cites a location (p. / § / Sec. / Fig. / Tab. / Eq. / Alg. / App.)
  - paper notes: file name = citekey, valid status / trust / metadata_source, date_read when read
  - trust ladder: verified needs verified_on, trusted needs signed_off_on
  - gaps-review questions are based only on trusted notes
  - links to paper-like notes ([[name2023word]]) that don't exist
Standard library only.
"""
import re
import sys
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent
CHECK_DIRS = ["papers", "concepts", "questions", "projects", "daily", "reviews"]
LOCATION = re.compile(r"(\bpp?\.\s*\d|§\s*\d|\bsec(tion)?\.?\s*\d|\bfig(ure)?\.?\s*\d|\btab(le)?\.?\s*\d|"
                      r"\beq(uation)?\.?\s*\(?\d|\balg(orithm)?\.?\s*\d|\bapp(endix)?\.?\s*[A-Z0-9])", re.I)
CALLOUT = re.compile(r"^>\s*\[!(\w+)\][+-]?\s*(.*)$")
WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")
CITEKEY_LIKE = re.compile(r"^[a-z][a-z0-9\-]*\d{4}[a-z0-9]*$")
VALID = {
    "status": {"to-read", "skimmed", "read-deep"},
    "trust": {"draft", "verified", "trusted"},
    "metadata_source": {"zotero", "arxiv", "semantic-scholar", "unresolved"},
}


def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    fm = {}
    if not m:
        return fm, None
    key = None
    for line in m.group(1).splitlines():
        line = re.sub(r"\s+#.*$", "", line)
        if re.match(r"^\s+-\s+", line) and key:
            fm.setdefault(key, [])
            if isinstance(fm[key], list):
                fm[key].append(line.split("-", 1)[1].strip().strip("'\""))
            continue
        kv = re.match(r"^([\w\-]+):\s*(.*)$", line)
        if kv:
            key, val = kv.group(1), kv.group(2).strip()
            if val.startswith("[") and val.endswith("]"):
                fm[key] = [v.strip().strip("'\"") for v in val[1:-1].split(",") if v.strip()]
            else:
                fm[key] = val.strip("'\"") if val else ""
    return fm, m


def callouts(text):
    """Yield (type, header, [(lineno, content)]) for each callout block."""
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        m = CALLOUT.match(lines[i])
        if m:
            kind, header, body, start = m.group(1).lower(), m.group(2), [], i
            i += 1
            while i < len(lines) and lines[i].startswith(">") and not CALLOUT.match(lines[i]):
                body.append((i + 1, lines[i][1:].strip()))
                i += 1
            yield kind, (start + 1, header), body
        else:
            i += 1


def link_target(name):
    name = name.strip()
    return any((VAULT / d / f"{name}.md").exists() for d in CHECK_DIRS + ["dashboards", "inbox"]) or \
        any(VAULT.rglob(f"{name}.md"))


def main(fix=False):
    errors, warnings, fixed = [], [], []
    trust_of = {}
    notes = [p for d in CHECK_DIRS for p in (VAULT / d).rglob("*.md")]
    for p in notes:
        fm, _ = frontmatter(p.read_text(encoding="utf-8"))
        trust_of[p.stem] = fm.get("trust")

    for p in notes:
        rel = p.relative_to(VAULT)
        text = p.read_text(encoding="utf-8")
        fm, fm_match = frontmatter(text)
        has_unverified = False

        for kind, (hline, header), body in callouts(text):
            if kind == "unverified":
                has_unverified = has_unverified or bool(header.strip() or any(c for _, c in body))
            if kind == "paper":
                items = ([(hline, header)] if header.strip() else []) + [(n, c) for n, c in body if c]
                for n, c in items:
                    if c.startswith("```") or c in {"-", "*"} or re.fullmatch(r"[-*]\s*", c):
                        continue
                    if not LOCATION.search(c):
                        errors.append(f"{rel}:{n}: [!paper] line has no page/section: {c[:80]}")

        if fm.get("type") == "paper":
            if fm.get("citekey") and fm["citekey"] != p.stem:
                errors.append(f"{rel}: citekey '{fm['citekey']}' does not match file name '{p.stem}'")
            if not fm.get("citekey"):
                errors.append(f"{rel}: missing citekey")
            for field in ("status", "trust", "metadata_source"):
                v = fm.get(field)
                if not v:
                    errors.append(f"{rel}: missing {field}")
                elif v not in VALID[field]:
                    errors.append(f"{rel}: {field} '{v}' not in {sorted(VALID[field])}")
            if fm.get("status") in {"skimmed", "read-deep"} and not fm.get("date_read"):
                errors.append(f"{rel}: status {fm['status']} but no date_read")
            if fm.get("metadata_source") == "unresolved":
                warnings.append(f"{rel}: metadata unresolved, needs a real source")

        t = fm.get("trust")
        if t == "verified" and not fm.get("verified_on"):
            errors.append(f"{rel}: trust verified but no verified_on")
        if t == "trusted" and not fm.get("signed_off_on"):
            errors.append(f"{rel}: trust trusted but no signed_off_on (only the owner can sign off)")

        if fm.get("type") == "question" and fm.get("origin") == "gaps-review":
            for b in fm.get("based_on") or []:
                name = WIKILINK.sub(r"\1", b).strip()
                if trust_of.get(name) != "trusted":
                    errors.append(f"{rel}: based_on '{name}' is not a trusted note")

        for target in {m.group(1).strip() for m in WIKILINK.finditer(text)}:
            if CITEKEY_LIKE.match(target) and not link_target(target):
                warnings.append(f"{rel}: links to [[{target}]] but no such note (create a stub via /read)")

        if fix and fm_match and fm.get("type") in {"paper", "concept"}:
            tags = fm.get("tags") if isinstance(fm.get("tags"), list) else []
            want = (tags + ["has-unverified"]) if has_unverified and "has-unverified" not in tags else \
                [x for x in tags if not (x == "has-unverified" and not has_unverified)]
            if want != tags:
                block = fm_match.group(1)
                new_line = f"tags: [{', '.join(want)}]"
                if re.search(r"^tags:.*$", block, re.M):
                    block = re.sub(r"^tags:.*$", new_line, block, count=1, flags=re.M)
                else:
                    block += "\n" + new_line
                text = f"---\n{block}\n---\n" + text[fm_match.end():]
                p.write_text(text, encoding="utf-8")
                fixed.append(f"{rel}: tags -> {want}")

    for title, items in (("ERRORS", errors), ("WARNINGS", warnings), ("FIXED", fixed)):
        if items:
            print(f"{title} ({len(items)})")
            for x in items:
                print("  " + x)
    if not (errors or warnings or fixed):
        print(f"OK: {len(notes)} notes checked, no problems.")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main(fix="--fix" in sys.argv)
