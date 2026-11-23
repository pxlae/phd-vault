# Trust queue

Notes move draft → verified (`/verify`) → trusted (you set `trust: trusted` and `signed_off_on`).
Only trusted notes feed `/gaps`.

## Needs /verify (draft, already read)
```dataview
TABLE status, date_read FROM "papers" WHERE trust = "draft" AND status != "to-read" SORT date_read DESC
```

## Needs your sign-off (verified)
```dataview
TABLE verified_on FROM "papers" OR "concepts" WHERE trust = "verified" SORT verified_on DESC
```

## Trusted but missing sign-off date
```dataview
LIST FROM "papers" OR "concepts" WHERE trust = "trusted" AND !signed_off_on
```

## Unresolved metadata
```dataview
LIST FROM "papers" WHERE metadata_source = "unresolved"
```

## Notes with unverified callouts
```dataview
LIST FROM "papers" OR "concepts" WHERE contains(file.tags, "has-unverified")
```
