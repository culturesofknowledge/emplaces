# Workflow notes for discussion (GK)

@@for discussion, with a view to flushing out what needs to be done@@

See [basic workflow for a single record not yet in EM Places](./edit.md).

My foicus here is on possible workflows involving Annalist; it's entirely possible that something similar could be done using a spreadsheet input format as an alternative, or additional mechanism for adding place data.  Annalist may be better suited to low volume idiosyncratic entries; spreadsheet input mayt be easier for bulk data acquisition.


## Tasks

1. Add new populated/administrative place (P, A)
2. Add new "related" place (without expectation of core data, and not following minimum information requirements for 1.)
3. Add additional metadata to existing place


## Add new populated/administrative place

Cf. [Add a single place record to EM Places](./edit.md#add-a-single-place-record-to-em-places)

This assumes a good possibility that "core" data will be obtainable from GeoNames, maybe supplemented by other authority data (currently Wikidata; TGN under consideration).  I'm trying to focus on tech infrastructure requirements, so am eliding issues of authority to perform certain types of update to EMPlaces.

1.  [Manual] New place is identified.  Assume that suitably diligent search for match with existing place has been conducted.  Need to know:
    - GeoNames Id OR
    - Reference in some other gazetteer
    - a location and name and date range and type of place and ...
        - i.e. sufficient to reasonably distiguish and characterize this place

    The intend here is that sufficient basic information is available to populate a new record according to established mionimum information requirements.

2.  [Manual] Also need to know:
    - an existing place of which the new place is a "part" (administratively or geographically)

3.  Create core data for new place:

    1.  [Auto] if GeoNames Id, use `geonamesdataexport` to generate EMPlaces RDF.  This will also include information about known containing regions from EMPlaces.
    2.  [Manual/auto] if no Geonames Id; e.g., historical place without modern existence (_proposed interim, TBC.  Long-term, this will probably be using Timbuctoo UI_):

        1. [Manual] enter data from other sources into Annalist
        2. [Auto] export from Annalist using `annalistdataexport`

        If necessary, additional records for new historical "containing" places may need to be created by a similar process.

4.  [?] Allocate permanent URI for new place...

5.  Import new data into EMPlaces (Timbuctoo), using allocated permanent URI.


## Add new "related" place

This assumes no availability of "core" data.  Available place information may be highly dependent on the kind of place.

1.  [Manual] New place is identified.  Need to know:
    - A name
    - Type of place
    - Description
    - Date of reference, if needed (e.g., for ship)
    - @@is this enough? Too much?

    The intend here is that sufficient basic information is available to populate a new record with just enough information to distinguish this place.  This does not necessarily confoirm to minimum gazetteer requirements, and the place record doesn't necessarily become part of the EMPlaces main gazetteer.

2.  Create basic data for new place in Annalist.

3.  Add any additional information about the new place as ad-hoc properties, entered through Annalist.

4.  ?? Export data from Annalist in EMPlaces model format
    - @@probably needs enhancements to `annalistdataexport`
}

5.  ??allocate id for new place

6.  ??publish data for new place in appripriate location

Need to make decisions about where this "related places" darta may be stored.  I suggest a goal shopuld be tomprovide a range of storage options that can connect through the web, avoiding the need to stuff everything into the main EMPlaces gazetteer.


## Add additional metadata to existing place

@@This is all pretty speculative; I'm assuming here that at least some of the new data is suitable for incorporation in an existing EMPlace record.@@

See also: [Edit one or more existing records in EM Places][./edit.md#edit-one-or-more-existing-records-in-em-places]


1. Create new "single source" place record in Annalist.  Add core and/or related information as above (probably use the "related place" form for flexibility.)

2. Create additional "merged data" record in Annalist for EMPlaces record, with reference to new "single source" record.

3. Export data from Annalist using (possible enhanced) `annalistexportdata`.

4. Import exported data into EMPlaces/Timbuctoo.  (As this is merged with existing data, the new "merged data" triples will cause the new simngle source record to be referenced from the existing EMPlaces description.)

    @@will need to be clear about what identifer is being used for the "merged data" record to ensure that this works as intended.


