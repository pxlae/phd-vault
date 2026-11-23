# Reading

## Queue (to-read)
```dataview
TABLE year, venue, choice(stub, "stub (foundation)", "") AS note FROM "papers"
WHERE status = "to-read" SORT file.ctime DESC
```

## Read deep
```dataview
TABLE year, date_read, trust FROM "papers" WHERE status = "read-deep" SORT date_read DESC
```

## Skimmed
```dataview
TABLE year, date_read, trust FROM "papers" WHERE status = "skimmed" SORT date_read DESC
```

## Papers by year
```dataview
TABLE length(rows) AS papers FROM "papers" WHERE year GROUP BY year SORT year DESC
```
