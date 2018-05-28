# Linked data model for EMPlaces

This directory contains [diagrams](PDFs) and [documentation](20180405-EMPlaces-data-model-notes.md) and [sample data](20180410-opole-example-data.ttl) for a proposed linked data model for EMPlaces.

See also [links](Links.md) for related information.

NOTE: this is WORK-IN-PROGRESS, and NOT FINAL.

(In due course, the documentation itself may be moved into this page)

# TODO

- [ ] Finish assembling example data for Opole
    - [x] Fix structure and vocabulary for bibliography
        - Candidates: Bibo, Fabio(SPAR), BibFrame, @@@ 
    - [x] Historical hierarchies
    - [x] Fix vocabularies for timespans (PeriodO?)
    - [x] Uncertainties, approximations, etc
    - [ ] Record metadata (maybe later when we see what Timbuctoo provides)
- [ ] Decide how to flag "core data" in structures used for both core and additional data (needed for refresh of core data from source).  It seems what is really needed is a reference source indication.
    - Thought: maybe handle under record metadata by providing property+source information for core place data?
- [x] Decide on structure for place categories and annotation types (using skos:Concepts)
- [x] Check that proposed Web Annotation extensions don't break anything (email with Robert Sanderson)
- [x] Pin down location/timespan vocabularies (the structure here follows ideas from Topotime/GeoJSON-LDT (also a work-in-progress?) but the vocabularies haven't yet been checked.)
- [ ] Update [Data model notes](./20180405-EMPlaces-data-model-notes.md); resolve any remaining TODOs there
- [ ] Update [diagrams](./PDFs/)
    -  multiple reference gazetteers - use TGN for labels
- [ ] Crosswalk between UI and data model
- [x] Dealing with uncertainty
    - See example, em:competence
    - How to represent?  
       - Confidence flag (high/medium/low)? Not really going to work for us?
       - Permutation of (Uncertain, Inferred, Approximate) per EMLO.  But be explicit in all cases.
    - Where to represent: calendars, date of hierarchical relations
    - For places: Uncertain, Inferred
    - For dates: Uncertain, Inferred, Approximate (implicit the timespan value)
- [ ] ... "related place"??? not available from reference gazetteer source ...
    - located within infomation (additional/alternative hierarchy to admin div)
- [ ] Preferred name: ??? (lost notes?)
- [x] Characterize calendars (inherited calendars; need to materialize for indexing; need source indication that it is inherited)
    - Handled by em:competence
    - general issue here about materialization of inferred/implied/deduced information.
    - note that name attestations are *additions* to the primary info; no such for calendars.
- [ ]note 2 kinds of Julian calendars
    - currently using "Old style" and "New style", but this is probably not enough.
    - suggestion that we might add start-of-year date to calendar details, but even that isn't always enough: in some cases 25 Dec start of year occurs in the year BEFORE that indicated?
- [ ] ...



# Notes

- Should Qualified relation have an optional "em:source" value?


# Identifying "core" values in place data

1. em:coreDataRef indicates the main source of core data

    @@ allow multiple em:coreDataRef values?
    @@ use em:primaryDataRef and em:secondaryDataRef?  (e.g. to allow for label data extracted from TGN.)

2. Some properties are always core: em:preferredName, em:alternateName, 

3. Some properties may be core or additional

        em:placeType
        em:hasRelation
        em:where
        em:hasAnnotation

    Apart from em:placeType, these all refer to entities that can be tagged.

    a. For em:hasRelation, attach em:source to the qualified relation value

    b. For em:where, attach em:source to the setting value

    c. For em:hasRelation, use em:source attached to the qualified relation value

    d. What to do about em:placeType?

        * use subproperty of em:placeType; e.g. em:CorePlaceType
        * record mutually exclusive group(s) of core place type values, and update accordingly
        * use separate place type entities per-source, attach em:source to the place type description

    e. When updating details from agiven source, all existing details tagged with that same source are replaced (i.e. removed first).


4. Places themselves may be core or additional (e.g. current vs historical)

Is this really an important issue for now?  If we are responsible for the code that extracts core data in the first place, we will know what needs replacing.  Longer term, we shouldn't depend on such knowledge, so I suggest adding appropriate em:source data from the outset.

