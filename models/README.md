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
    - [ ] Uncertainties, approximations, etc
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
- [ ] Dealing with uncertainty
    - How to represent?  
       - Confidence flag (high/medium/low)? Not really going to work for us?
       - Permutation of (Uncertain, Inferred, Approximate) per EMLO.  But be explicit in all cases.
    - Where to represent: calendars, hierarchical relations
- [ ] ... "related place"??? not available from reference gazetteer source ...
    - located within infomation (additional/alternative hierarchy to admin div)

- [ ] Preferred name:

- [ ] Characterize calendars (inherited calendars; need to materialize for indexing; need source indication that it is inherited)
    - [ ] general issue here about materialization of inferred/implied/deduced information.
    - [ ] note that name attestations are *additions* to the primary info; no such for calendars.
    - [x] note 2 kinds of Julian calendars
- [ ] ...

