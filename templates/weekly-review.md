---
type: weekly-review
week: {{week}} # YYYY-Www
start: 
end: 
deep_reads: 
skims: 
tags: [review]
---

# Week {{week}}

## Reading vs target (3 deep, 10 skims)
```dataview
TABLE status, date_read, trust FROM "papers"
WHERE date_read >= this.start AND date_read <= this.end
SORT date_read ASC
```

## What I learned
> [!idea]
> 

## Notes to verify or sign off
```dataview
TABLE trust, status FROM "papers" WHERE trust != "trusted" AND status != "to-read" AND !stub
```

## Open questions carried forward
- 

## Next week
- [ ] 
