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
    - [x] Related resource, include optional license (see LPiF proposal)
        - also, type of resource?
    - [ ] Record metadata (maybe later when we see what Timbuctoo provides)
- [x] Decide how to flag "core data" in structures used for both core and additional data (needed for refresh of core data from source).  It seems what is really needed is a reference source indication.
    - A declared set of properties of the central em:Place resource are always core data: see em:Place class declaration.
    - Qualified relations, settings and annotation resources have (optional) em:source properties: the corresponding values are considered to be core data if the `em:source/em:link` value is the same as the place's `em:coreDataRef/em:link` value.
    - Note that the place's `em:coreDataRef/em:link` and corresponding `em:source/em:link` values refer to the gazeteer defining document, not the gazetteer place Id.
- [x] Decide on structure for place categories and annotation types (using skos:Concepts)
- [x] Check that proposed Web Annotation extensions don't break anything (email with Robert Sanderson)
- [x] Pin down location/timespan vocabularies (the structure here follows ideas from Topotime/GeoJSON-LDT (also a work-in-progress?) but the vocabularies haven't yet been checked.)
- [ ] Update [Data model notes](./20180405-EMPlaces-data-model-notes.md); resolve any remaining TODOs there
- [.] Update [diagrams](./PDFs/)
    - [x] main diagram done
    - [x] name attestation diagram done
    - [ ] other annotation diagrams still to do
- [.] Crosswalk between UI and data model
- [x] Dealing with uncertainty
    - See example, em:competence
    - How to represent?  
       - Confidence flag (high/medium/low)? Not really going to work for us?
       - Permutation of (Uncertain, Inferred, Approximate) per EMLO.  But be explicit in all cases.
    - Where to represent: calendars, date of hierarchical relations
    - For places: Uncertain, Inferred
    - For dates: Uncertain, Inferred, Approximate (implicit the timespan value)
- [x] Characterize calendars (inherited calendars; need to materialize for indexing; need source indication that it is inherited)
    - Handled by em:competence
    - general issue here about materialization of inferred/implied/deduced information.
    - note that name attestations are *additions* to the primary info; no such for calendars.

- [ ] Generate data from EMLO data
- [x] Review way that core data is represented

- [ ] note 2 kinds of Julian calendars
    - currently using "Old style" and "New style", but this is probably not enough.
    - suggestion that we might add start-of-year date to calendar details, but even that isn't always enough: in some cases 25 Dec start of year occurs in the year BEFORE that indicated?
- [ ] Review handling of date uncertainty/aprroximation, and how it relates to PGiF proposal to use USO 8601-2 (https://github.com/LinkedPasts/lpif)
- [ ] Type URIs for places that don't have same kind of info (cf. "related places", 20180726-St-Adalbert-example.ttl)
- [ ] Record metadata design (creator, contributor, license, etc. - waiting to see what Timbuctoo provides)
- [ ] Record timespans as identified resources (rather than inline blank nodes)
- [ ] Finalize some URIs to be used
- [ ] Finalize prefixes
- [ ] URIs for language codes (consider lexvo?)
- [ ] Review format for timespan data; consider alignment with emerging LPiF activity
- [ ] ...


# Notes (questions and ideas)



# Priorities (2018-08-01)

1. Modelling of core data to deal with multiple core data sources
    - update diagrams
    - update sample data
    - update core data extractor
2. Need to start getting data into RDF and/or Timbuctoo
    - e.g.
    - 4 more towns like Opole to comparable detail
3. Loose ends
    - Modelling and Opole data
    - Related places
    - Historical place record: minimum viable information
       - differs from current place
4. Info for Lancaster talk - long talk later in August

- Sample bibliographies to enter
- Dealing with sources (see issue)
- Integration of date conversions

## Actions

1. Revised data model for multiple core data sources
    - (Try using Getty TGN)
2. Annalist definitions for place data entry
3. Session to ensure Arno can present EMPlaces to geographers

- Invoice September time before going away (up to including September)

