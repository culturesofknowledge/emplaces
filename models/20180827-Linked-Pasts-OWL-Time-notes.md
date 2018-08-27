# Notes about Linked Pasts time spans and OPL Time

Therse notes are my attempt to articulate some thoughts about representation of time spans described for [linked-places](https://github.com/LinkedPasts/linked-places) using semantics from the [OWL Time ontology](http://www.w3.org/TR/owl-time/).

I explore problems raised in the GitHub issue [`timespans`: inconsistent use of OWL Time ontology terms](https://github.com/LinkedPasts/linked-places/issues/6).

TL;DR: it's do-able, but not pretty.  See conclusion at end.

I shall take a 3-stage approach:

1. Informally review my understanding of the proposed JSON structure for time spans.
2. Propose a free-standing ontology structure (using `lpo`) for capturing this intent, and
3. Show how the proposed ontology can be mapped to the OWL Time ontology.

In this way, I hope to avoid the problems of tring to interpret the proposed JSON structure directly as JSON-LD using OWL Time terms (which I think is not possible).

## Proposed linked-places JSON structure

The proposed JSON structure looks like this:

    "timespans":
      [
        { "start": { "in": <date> | "earliest": <date> | "latest": <date> },
          "end":   { "in": <date> | "earliest": <date> | "latest": <date> }
        }
      ]

The value of the "timespans" property denotes a set of individual time span values.

A timespan value is some continuous period of time for which start and end points may or may not be known.  If "start" and/or "end" is omitted, the corresponding  information is unknown or unspecified.

A start or end point of a timespan is expressed as a (possibly open-ended) time interval within which it occurs.  `in` specifies a date (typically a year) within which the start or end point occurs.  `earliest` specifies that the start or end point occurs after the start of the indicated date (typically a year).  Similarly, `latest` indicates a date by which the start or end point has occurred.

A `<date>` value is a literal value indicating a time (typically a year, but greater precision may be offered using ISO 8601 date formats.  For now, I shall ignore possible use of ISO extensions to handle uncertainty.

Example (adapted from [linked-places](https://github.com/LinkedPasts/linked-places):

    { "@id": "Abingdon",
      "parthood": [
        { "@id": "Abingdon-in-Berkshire",
          "when": {
            "timespans":[
              {"start":{"latest":"1600"},"end":{"in":"1974"}}
            ]}
        },
        { "@id": "Abingdon-in-Oxfordshire",
          "when": {
            "timespans":
              [{"start":{"in":"1974"}}
            ]}
        }
      ]
    }


## Proposed free-standing ontology

This ontology is intended to be a direct representation of the JSON described above when interpreted as JSON-LD using an appropriate context definition.

In defining these termn, I have stayed away from referring to "time instants", as the literals that are used to describe what we might think of as instants are really all describing literals.  (I suggest it is not possible to have a literal to define any time instant: there will always be some limit of precision, so they are at best descriptive of an interval within which an instant occurs.)

### Classes

`lpo:Timespan`: instances represent some continuous period of time for which information about start and end points may or may not be known.  Properties include:

- `lpo:start`
- `lpo:end`

`lpo:Interval`: instances represent a specific interval within which a `lpo:Timespan` start and/or end point occurs.  Properties include:

- `lpo:in`
- `lpo:earliest`
- `lpo:latest`

### Properties

`lpo:start` indicates a time interval within which a `lpo:Timespan` starts.  That is, `t1 lpo:start t2` tells us that the start of interval `t1` occurs at or after the start of `t2`, and says nothing about the end of interval `t1`.
- domain: `lpo:Timespan`
- range: `lpo:Interval`

`lpo:end`: indicates a time interval within which a `lpo:Timespan` ends.  That is, `t1 lpo:end t2` tells us that the end of interval `t1` starts at or before the end of `t1`, and nothing about the start of `t1`.
- domain: `lpo:Timespan`
- range: `lpo:Interval`

`lpo:in`: indicates a literal date within which a `lpo:Interval` is completely contained.
- domain: `lpo:Interval`
- range: `xsd:DateTime` (literal)

`lpo:earliest` indicates a literal date after which a `lpo:Interval` occurs.  That is, the start of the `lpo:Interval` is on or after the start of the specified date, and the end of the interval is unspecified.
- domain: `lpo:Interval`
- range: `xsd:DateTime` (literal)

`lpo:latest` indicates a literal date before which a `lpo:Interval` occurs.  That is, the end of the `lpo:Interval` on or before the start of the specified date, and the start of the interval is unspecified.
- domain: `lpo:Interval`
- range: `xsd:DateTime` (literal)


### Example

This is the example from the previous section, expressed using Turtle syntax, and with additional identifiers introduced:

    :Abingdon
      :parthood :Abingdon_in_Berkshire, :Abingdon_in_Oxfordshire .
    :Abingdon_in_Berkshire
      :when
        [ :timespans
          [ a lpo:Timespan ;
            lpo:start [ a lpo:Interval ; lpo:latest "1600" ] ;
            lpo:end   [ a lpo:Interval ; lpo:in     "1974" ] ;
          ]
        ]
      .
    :Abingdon_in_Oxfordshire",
      :when
        [ :timespans
          [ a lpo:Timespan ;
            lpo:start [ a lpo:Interval ; lpo:in "1974" ] ;
          ]
        ]
      .


## Free standing ontology mapped to OWL Time

In mapping the above `lpo` terms to OWL Time, I note that `lpo:Timespan` and `lpo:Interval` correspond to `time:ProperInterval`, but the nearest equavalents to `lpo:start` and `lpo:end` appear to be `time:hasBeginning` and `time:hasEnd` which require object values that are instances of `time:Instant`.

The OWL Time ontology provides the following before/after temporal ordering relations:

`time:TemporalEntity` -> `time:TemporalEntity`:

- `time:after`
- `time:before`

`time:ProperInterval` -> `time:ProperInterval`:

- `time:intervalAfter`
- `time:intervalBefore`
- `time:intervalStarts`
- `time:intervalStartedBy`
- `time:intervalFinishes`
- `time:intervalFinishedBy`
- `time:intervalOverlaps`
- `time:intervalOverlappedBy` (These last two were surprising to me, as the names don't obviously imply ordering, but the definitions clearly do.)

The `time:before` and `time:after` relations enforce disjointness of the related intervals.

All of the `time:ProperInterval` ordering relations constrain both the starts and ends of the related intervals in ways that do not match the (presumed) intended semantics of `lpo:start`, `lpo:end`, `lpo:earliest` or `lpo:latest`.  (For example, `t1 time:intervalStarts t2` requires that the end of `t2` is after the end of `t1`.)

This leads me to the view that we need to introduce intermediate, auxiliary resources to capture the desired relations.

Consider, then:

    [ a lpo:Timespan ;
      lpo:start [ a lpo:Interval ; lpo:in "1974" ] ;
    ]

This describes an open-ended timespan whose start instance is some time in the year "1974".

    [ a lpo:Timespan, time:TemporalEntity ;
      time:hasStart
        [ a time:Instant ;
          ^time:inside
            [ a time:DateTimeInterval ;
              time:hasDateTimeDescription
                [ a time:GeneralDateTimeDescription ;
                  time:year "1974"
                ]
            ]
        ]
    ]

The syntax `^time:inside` is borrowed from SPARQL, and is used here to denote the inverse of `time:inside`.  This can be simplified some by using a deprecated property in the OWL Time ontology:

    [ a lpo:Timespan, time:TemporalEntity ;
      time:hasStart
        [ a time:Instant ;
          ^time:inside
            [ a time:DateTimeInterval ;
              time:xsdDateTime "1974"
            ]
        ]
    ]

And even further by using `time:inXSDDate`:

    [ a lpo:Timespan, time:TemporalEntity ;
      time:hasStart
        [ a time:Instant ;
          time:inXSDDate "1974"
        ]
    ]

Now consider:

    [ a lpo:Timespan ;
      lpo:start [ a lpo:Interval ; lpo:latest "1600" ] ;
    ]

We need to construct an open-ended interval to represent the start of this timespan:

    [ a lpo:Timespan, time:TemporalEntity ;
      time:hasStart
        [ a time:Instant ;
          ^time:inside
            [ a time:ProperInterval ;
              time:intervalFinishedBy
                [ a time:DateTimeInterval ;
                  time:hasDateTimeDescription
                    [ a time:GeneralDateTimeDescription ;
                      time:year "1600"
                    ]
                ]
           ]
        ]
    ]

or, again using the deprecated property:

    [ a lpo:Timespan, time:TemporalEntity ;
      time:hasStart
        [ a time:Instant ;
          ^time:inside
            [ a time:ProperInterval ;
              time:intervalFinishedBy
                [ a time:DateTimeInterval ;
                  time:xsdDateTime "1600"
                ]
            ]
        ]
    ]

@@TODO: spell out mapping for lpo: properties.

### Example

This represents the semantics of the example from the previous section using terms from OWL Time:

    :Abingdon
      :parthood :Abingdon_in_Berkshire, :Abingdon_in_Oxfordshire 
      .
    :Abingdon_in_Berkshire
      :when
        [ :timespans
            [ a lpo:Timespan, time:ProperInterval ;
              time:hasStart
                [ a time:Instant ;
                  ^time:inside
                    [ a time:ProperInterval ;
                      time:intervalFinishedBy
                        [ a time:DateTimeInterval ;
                          time:hasDateTimeDescription
                            [ a time:GeneralDateTimeDescription ;
                              time:year "1600"
                            ]
                        ]
                    ]
                ]
              time:hasEnd
                [ a time:Instant ;
                  ^time:inside
                    [ a time:DateTimeInterval ;
                      time:hasDateTimeDescription
                        [ a time:GeneralDateTimeDescription ;
                          time:year "1974"
                        ]
                    ]
                ]
            ]
        ]
      .
    :Abingdon_in_Oxfordshire",
      :when
        [ :timespans
            [ a lpo:Timespan, time:ProperInterval ;
              time:hasStart
                [ a time:Instant ;
                  ^time:inside
                    [ a time:DateTimeInterval ;
                      time:hasDateTimeDescription
                        [ a time:GeneralDateTimeDescription ;
                          time:year "1974"
                        ]
                    ]
                ]
            ]
        ]
      .


## Conclusion

While it's possible to capture the intended `lpo` semantics in the OWL Time ontology, the result isn't pretty, especially if represented in JSON-LD.

Hence, I'd suggest using the easier-to-use `lpo` terms in the JSON-LD context, and maintain the OWL Time mapping, maybe in the form of a set of inference rules, so that information exchange compatiblity with OWL Time can be achieved.

