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

- [x] GK email Martijn with details of GeoNames script and how I run it.
- [x] GK rethink use of emt:Current in place data.  Probably need to auto-generate when generating place data.
- [x] GK research current consensus about http vs https for identifier URIs.
    - https://github.com/w3c/web-annotation/issues/193
    - https://www.w3.org/blog/2016/05/https-and-the-semantic-weblinked-data/
    - https://github.com/schemaorg/schemaorg/issues/1914
    - 
    - ...
    - it appears to me that the current preference is to use http: in namespace URIs, and let the infrastructure handle upgrading to HTTPS for secure data transmission.
- [ ] GK+AB continue review of Opole example data (by Skype)
- [ ] GK check about licence information in data model: the multi source diagram should have license links.
    - em:Source_desc entity has em:licence property.  Intent is that the target URI both identifies the license, and locates a description of it.
    - Still need to review and check needed cases are covered.
- [ ] GK for sourced information, provide property that records date of retrieval from source.
- [ ] Update geoNames extractor to reflect model changes (cf. models/20190329-opole-example-multisourced-arno.ttl)


Later:

- [x] Are there existing vocabs covering competence, etc.
    - e.g. http://www.tema.unina.it/index.php/tema/article/view/2530/0
        - maybe-useful diagram
        - seems to focus more on degrees rather than kinds of incertainty
        - seems to be oriented towards prediction rather that recording
    - https://www.lri.fr/~antoine/Papers/PUBLIES/Ontology_Uncertainty_and_Food_Risk_v2.pdf
    - https://www.w3.org/2005/Incubator/urw3/wiki/UncertaintyOntology.html
    - http://c4i.gmu.edu/ursw/2008/talks/URSW2008_P6_CeravoloEtAl_talk.pdf
    - Based on the above survey, I conclude there has been lots of woprk on this topic, but that there are not really any obvious ready-to-use Ontologies.  It is possible that the proposed EMPlaces competencies could be refined somewhat usinbg the W3C 'urw3' work (last 2 links), but it's not clear that any specific value would come from such work.
- [ ] Workflow notes: need to add some specifics:
    - generation of em:Source_desc/em:Authority entity for data added
    - generation of em:Time_period entity
    - introduction of new kinds of annotation
    - ...
- [ ] Publish EMPlaces vocabulary as RDF schema and/or OWL ontology (curently in Annalist).
- [ ] GK think about trust models and how they can be applied to EMPlaces model when displaying a curated view on the data.  Specifically, how to deal with competing/inconsistent claims?  This about a curation model than can be applied to create a consistent view of data.

Preparing for EMPeople:

Prosopographical workshop 2019-05-16/17
(Hotel from 15th)

- [ ] GK read prosopography data model (e.g. end April) (Arno to provide)
- [ ] GK research other prosopographical data models (Arno to provide list)
- [ ] GK review prosopographical workshop notes (what are we aiming to get out of this?)


## Other:

- [x] Define minimal viable information model for historical place definitions (with no GeoNames data to seed)
    - See meeting notes from 2019-03-25 (20190325-EMLO-oxford-meeting)
- [x] Clean up documentation.  Move superseded documents to "historic" subfolder.
- [ ] Test wrangled data with Timbuctoo
    - with data at `src/geonamesdataexport/data-20190322`

## Techical debt and unscheduled:

- [ ] Update `src/commondataexport/README.md` (documentation)
- [ ] Create capability to import EMPLaces data into Annalist, based on existing data (e.g., a new option for "get_annalist_data").
- [ ] Test suite for data wrangling utilities

