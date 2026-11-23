# Weekly progress

Target per week: **3 deep reads** and **10 skims**. Change the numbers below to adjust.

```dataviewjs
const TARGET = { deep: 3, skim: 10 };
const weeks = 6;
const start = dv.date("today").startOf("week");
const pages = dv.pages('"papers"').where(p => p.date_read);
const rows = [];
for (let i = 0; i < weeks; i++) {
  const s = start.minus({ weeks: i }), e = s.plus({ days: 7 });
  const inWeek = pages.where(p => { const d = dv.date(p.date_read); return d && d >= s && d < e; });
  const deep = inWeek.where(p => p.status === "read-deep").length;
  const skim = inWeek.where(p => p.status === "skimmed").length;
  const bar = (n, t) => "█".repeat(Math.min(n, t)) + "░".repeat(Math.max(t - n, 0)) + (n > t ? ` +${n - t}` : "");
  rows.push([s.toFormat("kkkk-'W'WW"), `${deep}/${TARGET.deep} ${bar(deep, TARGET.deep)}`,
             `${skim}/${TARGET.skim} ${bar(skim, TARGET.skim)}`]);
}
dv.table(["Week", "Deep reads", "Skims"], rows);
```

## Read this week
```dataview
TABLE status, trust, date_read FROM "papers"
WHERE date_read >= date(sow) AND date_read <= date(eow)
SORT date_read DESC
```
