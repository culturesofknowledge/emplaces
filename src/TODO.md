# Data extraction utility tasks

See also `src/annalistdataexport/TODO.md`

## Outstanding at 2019-03-26
 
### From 2018-11-08 meeting (20181108-CofK-Arno-meeting-notes):

- [ ] Review Annalist definitions with Arno
    - this was intended to be a face-to-face session, but was previously stymied by an Annalist login bug.  This has been fixed.
    - See: https://demo.annalist.net/annalist/c/EMPlaces_defs/

- [ ] Push ahead on Wikidata cross-referencing for alternate authorities
    - [x] find wikidata Id for given Geonames Id
    - [x] Logic to extract selected place data from wikidata
    - [ ] Finalize data to be extracted from Wikidata
        - Most of the required data extraction logic is now in place, but we need to agree the workflows to be used for creating/managing EMPlaces data to wrap up loose ends (specifically, id generation for source data obtained from Annalist, Wikidata and GeoNames).
    - see: 
        - models/wikidata-opole.ttl
        - https://demo.annalist.net/annalist/c/EMPlaces_defs/d/Authority/Wikidata_Opole_source/
        - Have some basic logic working; see:
            - python get_geonames_data.py wikidataid 3090048
            - python get_annalist_data.py getwikidata Q92212
            - python get_annalist_data.py getwikitext Q92212
        - Would benefit from some refactoring: maybe create a separate get_wikidata utility?
        - The following external id properties are pulled from wikidata:
            - per email 2019-02-05, GND, BnF, GeoNames, TGN, GOV, CERL, MoEML:
            - https://www.wikidata.org/wiki/Property:P227 (GND)
            - https://www.wikidata.org/wiki/Property:P268 (BnF)
            - https://www.wikidata.org/wiki/Property:P1566 (GeoNames)
            - https://www.wikidata.org/wiki/Property:P1667 (Getty TGN)
            - https://www.wikidata.org/wiki/Property:P2503 (GOV)
            - https://www.wikidata.org/wiki/Property:P1871 (CERL)
            - https://www.wikidata.org/wiki/Property:P6060 (MoEML)
    - [ ] Provide extra pieces as required for data gathering and management workflows.
        - This rather depends on what form it is decided that the workflows should take.
        - See: https://github.com/culturesofknowledge/emplaces/blob/master/design/edit.md

- [ ] Create capability to import EMPLaces data into Annalist, based on existing data (e.g., a new option for "get_annalist_data").
    - This would be used, for example, importing Geonames data in an Annalist collectiobn, via get_geonames_data.

### From 2018-11-23 meeting (20181123-EMPlaces-meeting-Oxford):

- [ ] Arno send "related places" details;
    - I think this was to be a small number of examples and associated details, but my notes don't say.
    - See Arno's email of 2019-03-22
- [ ] GK to prototype one or two "related places" cases
    - Arno to send place with postal relations
    - Also, use St Adalberts church for Opole


### From 2019-03-25 meeting (20190325-EMLO-oxford-meeting):

NOTE: Annalist-related activity is on hold until Arno has discussed progress on Timbuctoo UI with Rob.

Wrapping up EMPlaces:

- [ ] GK email Martijn with details of GeoNames script and how I run it.
- [ ] GK rethink use of emt:Current in place data.  Probably need to auto-generate when generating place data.
- [ ] GK check about licence information in data model: the multi source diagram should have license links.
- [ ] GK for sourced information, provide property that records date of retrieval from source.
- [ ] GK think about trust models and how they can be applied to EMPlaces model when displaying a curated view on the data.  Specifically, how to deal with competing/inconsistent claims?  This about a curation model than can be applied to create a consistent view of data.
- [ ] GK+AB continue review of Opole example data (by Skype)
- [ ] GK research current consensus about http vs https for identifier URIs.

Preparing for EMPeople:

- [ ] GK read prosopography data model (e.g. end April) (Arno to provide)
- [ ] GK research other prosopographical data models (Arno to provide list)
- [ ] GK review prosopographical workshop notes (what are we aiming to get out of this?)

Other:

- [ ] Update `src/commondataexport/README.md` (documentation)
- [ ] Test wrangled data with Timbuctoo
    - with what data??
- [ ] Create capability to import EMPLaces data into Annalist, based on existing data (e.g., a new option for "get_annalist_data").
- [ ] Define minimal viable information model for historical place definitions (with no GeoNames data to seed)
- [ ] Test suite for data wrangling utilities
- [ ] Clean up documentation.  Move superseded documents to "historic" subfolder.

See also:

- https://www.wikidata.org/wiki/Wikidata:SPARQL_query_service

- https://query.wikidata.org/#SELECT%20%3Fs%20%3FsLabel%20WHERE%20%7B%0A%20%20%3Fs%20wikibase%3ApropertyType%20wikibase%3AExternalId.%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22%5BAUTO_LANGUAGE%5D%2Cen%22.%20%7D%0A%7D%0ALIMIT%201000%0A

- Query for wikidata properties for authority control of places (HT @Tagishsimon)
    SELECT ?property ?propertyLabel WHERE {
      ?property wdt:P31 wd:Q19829908.
      SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
    }

- https://query.wikidata.org/embed.html#SELECT%20%3Fproperty%20%3FpropertyLabel%20WHERE%20%7B%0A%20%20%3Fproperty%20wdt%3AP31%20wd%3AQ19829908.%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22%5BAUTO_LANGUAGE%5D%2Cen%22.%20%7D%0A%7D%0A


