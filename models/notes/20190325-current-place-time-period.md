# Time periods for current places

Currently, the GeoNames extractor assumes a pre-defined time period value `emp:Current` or similar that is used to denote a time period up to the current year, whatever that may be.  The problem is that the pesky "current year" keeps on changing, so the data as specified isn't stable, though the way it's defined means that if it is true of a given place for some specified year, then it remains true for that combination of place and year, even though more precise statements could be possible.

```
emp:Current_2018 a em:Time_period ;
    rdfs:label   "Current, as of 2018" ;
    rdfs:comment "For ease of retrieval, use this specific resource to label any current information (e.g. data extracted from GeoNames).  Additional Timespan values could be indicated if required to convey more specific information." ;
    em:timespan
      [ a em:Time_span ;
        em:latestStart: "2018" ;
        em:earliestEnd: "2018" ;
      ]
    .
```

It's all a bit unsatisfactory, despite being technically correct, not least becasue it can be confusing.


# Some alternative proposals

1. introduce a notion of `emp:Current` that represents a period that extends up to the time of retrieval of the source data.  It would not be possible to associate a stable timespan with such an entity, so the `em:timespan` property would need to be dropped.  This in turn would mean that the current places could not be selected by time-based retrieval filters.

2. For each place retrieved from GeoNames, auto-generate and reference an `em:Time_period` resource which reflects available information (or the actual time of retrieval).  This has no obvious disadvantage except that it may result in a large number of auto-generated `em:Time_period` and `em:Time_span` values.

3. Basically the same as 2, except that the generated `em:Time_period` values would be restricted to yearly granularity and named accordingly (like the `emp:Current_2018` example above.)  The timespan value would be allocated a similar URI to facilitate merging.  When loaded into a triple store, this would allow a hight degree of data sharing as the generated time period and time span values would be merged into a small number of distinct instances (one per year from which data is sourced).   Use a specified URI pattern so that data can be merged on ingest.


# Proposal

I suggest using option 3 from above.


