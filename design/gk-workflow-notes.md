# Workflow notes for discussion (GK)

@@for discussion, with a view to flushing out what needs to be done@@

See [basic workflow for a single record not yet in EM Places](./edit.md).

My focus here is on possible workflows involving Annalist; it's entirely possible that something similar could be done using a spreadsheet input format as an alternative, or additional mechanism for adding place data.  Annalist may be better suited to low volume idiosyncratic entries; spreadsheet input mayt be easier for bulk data acquisition.


## Tasks

1a. Add (single) new populated/administrative place (P, A) for which GeoNames data is available

1b. Add (single) new populated/administrative place (P, A) for which no authority data is available (e.g. historic places no longer extant)

2. Add (single) new "related" place (e.g. St Adalbert's church) (without expectation of core data, and not following minimum information requirements for 1, and with possibly unusual additional properties to be allowed.)

3. Add additional/extended (often historical) data to existing place records.

4. Bulk (probably tabular) data import and record creation (placeholder for now; not on current radar)

5. Create non-standard relation between existing places (placeholder)

6. Modify data already in EMPlaces (placeholder)


## Task 1a. Add new populated/administrative place (GeoNames data available)

Cf. [Add a single place record to EM Places](./edit.md#add-a-single-place-record-to-em-places)

This assumes that "core" data is obtainable from GeoNames, maybe supplemented by other authority data (currently Wikidata; TGN under consideration).  I'm trying to focus on tech infrastructure requirements, so am eliding issues of authority to perform certain types of update to EMPlaces.

1.  [Manual] Place not yet in EMPlaces is identified.  Assume that suitably diligent search for match with existing place has been conducted.  Need to know:
    - GeoNames Id

2.  Create core data for new place:

    - [Auto] Use `geonamesdataexport` to generate EMPlaces RDF.  This will also include information about known containing regions from GeoNames.
    - @@TODO: add details of merging additional description from Wikidata/Wikipedia

3.  Allocate permanent URI for new place...  (process unclear)

    - NOTE: `geonamesdataexport` will allocate a URI that is constructed using the GeoNames Id.

4.  Import new data into EMPlaces (Timbuctoo), using allocated permanent URI.



## Task 1b. Add new populated/administrative place (no GeoNames data)

Cf. [Add a single place record to EM Places](./edit.md#add-a-single-place-record-to-em-places)

1.  [Manual] Place not yet in EMPlaces is identified.

    - (Exactly same as option 1a above)

2.  [Manual] Minimally need to (also) know:

    Context: sufficient to reasonably distiguish and characterize this place.  The intend here is that sufficient basic information is available to populate a new record according to established minimum information requirements.)

    - MUST: place name
    - MUST: type of place
    - MUST: source and authority of information
    - MUST: licensing information
    - SHOULD: alternative names
    - SHOULD: current and/or historical hierarchy (editorial policy TBD)
        - typically an existing place of which the new place is a "part" (administratively or geographically)
        - this allows us to tie a new place record into existing hierachy structure in EMplaces
    - SHOULD: a location
    - SHOULD: authority information (where applicable)
    - SHOULD: brief description
    - SHOULD: a date range (e.g. current or historic period)
    - ...

3.  Create core data for new place:

    Proposed interim (TBC): 

        1. [Manual] enter data from other sources using Annalist
        2. [Auto] export from Annalist using `annalistdataexport`

        If necessary, additional records for new historical "containing" places may need to be created by a similar process.

    Expected eventual:

        This will be using Timbuctoo UI

4.  Allocate permanent URI for new place...

5.  (Staging, review, etc.)

6.  Import new data into EMPlaces (Timbuctoo), using allocated permanent URI.


## Task 2. Add new "related" place

This assumes no availability of "core" data for the place being added???.  Available place information will be highly dependent on the kind of place.

Context: a "related" place is any place for which the salient relation is not otherwise captured in an EMPlaces record.

Context: some "related" places may include information that doesn't conform to the content of a "typical" place record.

Context: thinking of using a Wikidata-like model for this.

@@TODO: any relation that is not political, administrative (or other historical hierarchy type) needs to be defined using appropriate "triple statements" and vocabulary in the related places section).

1.  [Manual] New place is identified.  Need to know:
    - MUST: A name
    - MUST: Type of place
    - MUST: Description/label
    - SHOULD: Date of reference, if needed (e.g., for ship)
    - MUST: Source and authority
    - MUST: some relation to some other place
    - @@is this enough? Too much?

    Context: The intend here is that sufficient basic information is available to populate a new record with just enough information to distinguish this place.  This does not necessarily conform to normal gazetteer requirements, and the place record doesn't necessarily become part of the EMPlaces main gazetteer.

2.  [Manual] Create data for new place in Annalist (or some other tool that can accept the data and generate appropriate RDF).

3.  [Manual] Add additional information about the new place as ad-hoc properties, entered through Annalist.  (cf. Wikidata model)

4.  Export data from Annalist in EMPlaces model format

    - @@probably needs enhancements to `annalistdataexport`

5.  Allocate URI for new place

6.  (Staging, review, etc.)

7.  Publish data for new place in EMPLaces or appropriate location

@@TODO: Need to make decisions about where this "related places" data may be stored.  I suggest a goal shopuld be tomprovide a range of storage options that can connect through the web, avoiding the need to stuff everything into the main EMPlaces gazetteer.


## Add additional metadata to existing place

@@This is all pretty speculative; I'm assuming here that at least some of the new data is suitable for incorporation in an existing EMPlace record.@@

@@Assuming Annalist here, could be other tool@@

See also: [Edit one or more existing records in EM Places][./edit.md#edit-one-or-more-existing-records-in-em-places]

1. Identify existing EMPlaces place record which data will augment.

2. Create new "single source" place record in Annalist.  Add core and/or related information as above (probably use the "related place" form for flexibility.)

3. Create additional "merged data" record in Annalist for EMPlaces record, with reference to new "single source" record.

4. Export data from Annalist using (possible enhanced) `annalistexportdata`.

5. (Staging, review, etc.)

6. Import exported data into EMPlaces/Timbuctoo.  (As this is merged with existing data, the new "merged data" triples will cause the new simngle source record to be referenced from the existing EMPlaces description.)

    @@will need to be clear about what identifer is being used for the "merged data" record to ensure that this works as intended.

