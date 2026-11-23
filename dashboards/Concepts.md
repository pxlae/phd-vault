# Concepts

```dataview
TABLE prerequisites, length(file.inlinks) AS "used by", trust FROM "concepts" SORT length(file.inlinks) DESC
```

## Concepts linked but not written yet
```dataviewjs
const missing = new Map();
for (const p of dv.pages('"papers" or "concepts"')) {
  for (const l of p.file.outlinks) {
    if (!dv.page(l.path) && !/\d{4}/.test(l.path)) missing.set(l.path, (missing.get(l.path) || 0) + 1);
  }
}
dv.table(["Concept", "Linked from"], [...missing].sort((a, b) => b[1] - a[1]).map(([k, n]) => [dv.fileLink(k), n]));
```
