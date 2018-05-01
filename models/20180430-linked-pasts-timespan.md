# Notes on timespan representation proposed for Linked-pasts

The original project to use JSON-LD to capture temporally qualified place descriptions appears to have been withdrawn in favour of focusing on a pure JSON representation.

The community of interest for EMPlaces has a good deal overlap with that for Linked-pasts, so it makes sense to at least try and use the same semantics, even if we are more focused on a linked data representation.

To this end, I'm working through https://github.com/LinkedPasts/lp-network/blob/master/PGIFv2/pgif_v2e_annotated.txt to capture the proposed structure that is used as the value of a `when` attribute, and proposing an RDF representation based on that structure.

(See also https://github.com/LinkedPasts/lp-network/issues/1 for some earlier discussions.  The concerns raised there are to do with the way `when` is interpreted, not to do with the actual representation of timespans.)

Also note the related work of PeriodO, which is less concerned with quantified timespan representations as creating a catalogue of documented references to named or otherwise identified periods.  My intent/hope is that a timespan representation can alteranatively refer to a PeriodO entry.

## Time period representation

Looking at https://github.com/LinkedPasts/lp-network/blob/master/PGIFv2/pgif_v2e_annotated.txt, as of commit https://github.com/LinkedPasts/lp-network/commit/3d8a31ee46689f6c604027f011f29ce7967efa4e#diff-a8b77c1f52cf7884b93c4b857b1232f1.

Line 40:

    "when": {
       "timespans": [ { "start": {"in": "-0750"}, "end": {"in": "0640"} } ],
       "periods": [ {"name": "", "uri": "http://n2t.net/ark:/99152/p03wskd389m"} ],
       "label": ""
    },

Line 74:

    "when": {"periods": [{"label": "", "uri": ""}]},

Line 86:

    "when": {
      "label": "",
      "timespans": [
        {  
          "start": {
            "in": "nnnn-nn"
          },
          "end": {
            "earliest": "nnnn",
            "latest": "nnnn-nn-nn"
          }
        }
      ]
    },

Line 117:

    "when": {
      "label": "for approx. 200 years, sometime between {start} and {end}",
      "timespans":[
        {
          "start": {"in": "nnnn"},
          "end": {"earliest": "-nnnn","latest": "nnnn"}
        }
      ],
      "duration": "~200y"
    },

Line 134:

    "when": {
      "periods": [
        {"label": "", "uri": ""},
        {"label": "", "uri": ""}],       
      "label": "roughly during the {x} and {y} periods"
    }

Line 205:

    "when": {
      // label for the overall expression
      "label": "",
      
      // >=1; optional; 1-4 ISO-8601 parts
      "timespans": [
        {  
          // interpreted as earliestStart if latestStart
          "start": "nnnn-nn-nn", 

          // optional; enables 'fuzzy' start/end
          "latestStart": "nnnn-nn-nn",
          "earliestEnd": "nnnn-nn-nn",

          // if no end, interpreted as "present" or now()
          // if earliestEnd, interpreted as latestEnd 
          "end": "nnnn-nn-nn",

          // Optional, 'for {duration} during' timespan described above
          // if omitted, phenomena is 'throughout' timespan
          "duration": "3m" // d, m, y
        }
      ],
      // >=1, optional
      "periods": [
        {  "name": "", 
          "uri": ""
        }
      ],

      // optional, for sequences
      "follows": "<uri>",

      // optional, stub for future use
      // default is Gregorian
      "calendar": ""
    }

The last example/template here (line 205) pretty much captures the proposed structure.

Some notes for representation as RDF:

1.  The names used for keys above can be used directly as local parts of a CURIE.  For the time being, I'll define a prefix "emt", but we may subsequently be able to use a value in common with linked pasts.  e.g.

        @prefix emt: <http://emplaces.namespace.example.org/temporal/> .

2.  The above structure uses `timespans` and `periods` with a list of values.  I assume the union of the indicated values is intended.  A simple representation in RDF using multiple property instances would yield an intersection.  The nearest RDF representation, which could be represented as above using JSON-LD, would be to use an `rdf:List` structure.  Unfortunately this leads to rather more complex RDF in what seems to be the very common case of a single value, so I propose to use singular properties `emt:timespan` and `emt:period` for now.

    In future, when we have a need for union time periods, the plural names could be used with `rdf:List` values, possibly combined with a singular timespan describing a single period that subsumes the individual values inthe list.

    It may turn out be that a singular `period` is less useful.  Cases I (vaguely) recall seeing have two or more named periods that together represent a contiguous timespan.  The simple singular timespan may turn out to be most useful for presentation and sorting purposes (somewhat like quantified periods in PeriodO?).

3. The optional `follows` and `calendar` properties will not be used for the initial EMPlaces model (but could be considered for later inclusion).

4. Simlarly for the optional `duration` property.

    Rather than inventing a new syntax for this, I would prefer to use the ISO8601 representation (https://en.wikipedia.org/wiki/ISO_8601#Durations), which is also defined as an XML schema data type (http://www.w3.org/TR/xmlschema-2/#duration), hence is available as an RDF literal data type.

    E.g. 3 months would be `P3M`

    I note this is almost compatible with the proposed syntax, except that a preceding `P` is required.

5. Thinking in terms of RDF semantics, I would note that interpreting the absence of `end` as "now" could lead to some potential problems with formal reasoning.  If one infers conclusions that are based on the premise that a period extends to the present time, then subsequently add an `end` with an earlier date, RDF semantics would require that the original conclusions are still logically valid, which might be dsifferent to what is intended.  A logically sounder approach (when using RDF) is to consider that lack of an `end` property simply means "unknown".



## Example for EMPlaces

From the above, the period information for the example of [Opole](20180410-opole-example-data.ttl) would look like this (using Turtle syntax):

    @prefix em:  <http://emplaces.namespace.example.org/> .
    @prefix emt: <http://emplaces.namespace.example.org/temporal/> .
     :
    ex:Opole_P a em:Place ;
         :
        em:when 
          [ a emt:TimePeriod ;
            rdfs:label "1322-1417" ;
            emt:timespan
              [ a emt:Timespan ;
                emt:start "1322" ;
                emt:end   "1417" ;
              ] ;
          ]
         :



