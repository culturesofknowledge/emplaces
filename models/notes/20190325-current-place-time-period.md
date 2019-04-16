# Time periods for current places

Currently, the GeoNames extractor assumes a pre-defined time period value `emp:Current` or similar that is used to denote a time period up to the current year, whatever that may be.  The problem is that the pesky "current year" keeps on changing, so the data as specified isn't stable, though the way it's defined means that if it is true of a given place for some specified year, then it remains true for that combination of place and year, even though more precise statements could be possible.

It's all a bit unsatisfactory, despite being technically correct, not least becasue it can be confusing.

```
emp:Current a em:Time_period ;
    rdfs:label   "Current" ;
    rdfs:comment "For ease of retrieval, use this specific resource to label any current information (e.g. data extracted from GeoNames).  Additional Timespan values could be indicated if required to convey more specific information." ;
    em:timespan
      [ a em:Time_span ;
        em:latestStart: "2018" ;
        em:earliestEnd: "2018" ;
      ]
    .
```

# Some alternative proposals

1. introduce a notion of `emp:Current` that represents a period that extends up to the time of retrieval of the source data.  It would not be possible to associate a stable timespan with such an entity, so the `em:timespan` property would need to be dropped.  This in turn would mean that the current places could not be selected by time-based retrieval filters.

2. For each place retrieved from GeoNames, auto-generate and reference an `em:Time_period` resource which reflects available information (or the actual time of retrieval).  This has no obvious disadvantage except that it may result in a large number of auto-generated `em:Time_period` and `em:Time_span` values.

3. Basically the same as 2, except that the generated `em:Time_period` values would be restricted to yearly granularity and named accordingly (like the `emp:Current_2018` example above.)  The timespan value would be allocated a similar URI to facilitate merging.  When loaded into a triple store, this would allow a hight degree of data sharing as the generated time period and time span values would be merged into a small number of distinct instances (one per year from which data is sourced).   Use a specified URI pattern so that data can be merged on ingest.


# Proposal

I suggest using option 3 from above.

Thus, we have someting like this:

```
emp:Current_2018 a em:Time_period ;
    rdfs:label   "Current, as of 2018" ;
    rdfs:comment "Time period resource for information about a place that exists (or is presumed to exist) in 2018." ;
    em:timespan
      [ a em:Time_span ;
        em:latestStart: "2018" ;
        em:earliestEnd: "2018" ;
      ]
    .
```


# Time periods for maps, names, hirerachies

(These notes are taken almost verbatim from a discussion email)

Revisiting the time period and time span descriptions for maps.

Considering, e.g., a (presumed-then-current) map published in 1561, I note this is very similar to the current-place description:

```
emp:Current_1561 a em:Time_period ;
    rdfs:label     "Current in 1561" ;
    rdfs:comment   "Time period that includes at least part of the year 1561" ;
    em:short_label "1561" ;
    em:timespan    emt:Current_1561 ;
    .

emt:Current_1561 a em:Time_span
    rdfs:label     "Current in 1561" ;
    rdfs:comment   "Time span that includes at least part of the year 1561" ;
    em:short_label "1561" ;
    em:latestStart "1561" ;
    em:earliestEnd "1561" ;
    .
```

Also similar is the time period for use of "Opole" as a Polish name for Opole:

```
emp:Since_1146 a em:Time_period ;
    rdfs:label     "Since 1146" ;
    rdfs:comment   "Time period including since year 1146" ;
    em:short_label "1146-" ;
    em:timespan    emt:Since_1146 ;
    .

emt:Since_1146 a em:Time_span ;
    rdfs:label     "Since 1146" ;
    rdfs:comment   "Time span including since year 1146" ;
    em:short_label "1146-" ;
    em:latestStart  "1146" ;
    em:earliestEnd  "2018" ;
    .
```

Noting that we don't actually know the date when the name will stop being used, but that it must be no earlier than the current year.

I also note that there are at least two kinds descriptive patterns here:

Time spans that cover at least part of some interval (as above), and time spans that fall within some interval.  This is why I got confused, as these call for different properties.  So if the duration of Opole is known to fall within the period 1281 to 1521, we might express the period as:


```
emp:Within_1281_1521 a em:Time_period ;
    rdfs:label     "Within 1281-1521" ;
    rdfs:comment   "Time period within 1281 to 1521" ;
    em:short_label "1281-1521" ;
    em:timespan    emt:Within_1281_1521 ;
    .

emt:Within_1281_1521 a em:Time_span ;
    rdfs:label       "Within 1281-1521" ;
    rdfs:comment     "Time span within 1281 to 1521" ;
    em:short_label   "1281-1521" ;
    em:earliestStart "1281" ;
    em:latestEnd     "1521" ;
    .
```

Note that the early/late properties are different than above.

Finally, if we actually want to express the above range as spanning all the years 1281-1521, and none outside that range, we could express that as:

```
emp:Range_1281_1521 a em:Time_period ;
    rdfs:label     "Period 1281-1521" ;
    rdfs:comment   "Time period from 1281 to 1521" ;
    em:short_label "1281-1521" ;
    em:timespan    emt:Range_1281_1521 ;
    .

emt:Range_1281_1521 a em:Time_span ;
    rdfs:label       "Time span 1281-1521" ;
    rdfs:comment     "Time span from 1281 to 1521" ;
    em:short_label   "1281-1521" ;
    em:earliestStart "1281" ;
    em:latestStart   "1281" ;
    em:earliestEnd   "1521" ;
    em:latestEnd     "1521" ;
    .
```

Which with two new properties might be expressed as:

```
emp:Range_1281_1521 a em:Time_period ;
    rdfs:label     "Period 1281-1521" ;
    rdfs:comment   "Time period from 1281 to 1521" ;
    em:short_label "1281-1521" ;
    em:timespan    emt:Range_1281_1521 ;
    .

emt:Range_1281_1521 a em:Time_span ;
    rdfs:label     "Time span 1281-1521" ;
    rdfs:comment   "Time span from 1281 to 1521" ;
    em:short_label "1281-1521" ;
    em:start       "1281" ;
    em:end         "1521" ;
    .
```

Thus, we end up with 6 properties for describing timespans:

    em:earliestStart
    em:latestStart
    em:start

    em:earliestEnd
    em:latestEnd
    em:end

As I currently present these, that values are all years, but I think it would be a reasonable extension to allow values that include months or years, corresponding to closer bounds on the corresponding point in time.

[Later] I note that some data already uses day granularity in timespan descriptions.

Also, where I have used the current-year to represent timespans up to the present date, one might also consider not specifying the end of the range.  But that is a weaker assertion, as it doesn't preclude a timespan that ended, say, 10 years ago.  What is hard to express within the semantic framework is "until the current date", because such a claim could change to become false, violating semantic expectations.

I haven't checked the alignment of this structure with the LPIF work, but I'm pretty confident it faithfully covers LPIF-supported cases.


