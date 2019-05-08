# Data extraction utility tasks

See also `src/annalistdataexport/TODO.md`

## Outstanding at 2019-03-26
 
### From 2018-11-08 meeting (20181108-CofK-Arno-meeting-notes):

- [ ] Review Annalist definitions with Arno
    - this was intended to be a face-to-face session, but was previously stymied by an Annalist login bug.  This has been fixed.
    - See: https://demo.annalist.net/annalist/c/EMPlaces_defs/

- [x] Push ahead on Wikidata cross-referencing for alternate authorities
    - [x] find wikidata Id for given Geonames Id
    - [x] Logic to extract selected place data from wikidata
    - [x] Finalize data to be extracted from Wikidata
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

    - [x] Provide extra pieces as required for data gathering and management workflows.
        - This rather depends on what form it is decided that the workflows should take.
        - See: https://github.com/culturesofknowledge/emplaces/blob/master/design/edit.md

- [ ] Create capability to import EMPLaces data into Annalist, based on existing data (e.g., a new option for "get_annalist_data").
    - This would be used, for example, importing Geonames data in an Annalist collectiobn, via get_geonames_data.


### From 2018-11-23 meeting (20181123-EMPlaces-meeting-Oxford):

- [x] Arno send "related places" details;
    - I think this was to be a small number of examples and associated details, but my notes don't say.
    - Arno to send place with postal relations.
    - Also, use St Adalberts church for Opole.
    - See Arno's email of 2019-03-22
- [ ] GK to prototype one or two "related places" cases


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
- [x] GK+AB continue review of Opole example data (by Skype) (ongoing)
- [x] GK check about licence information in data model: the multi source diagram should have license links.
    - em:Source_desc entity has em:licence property.  Intent is that the target URI both identifies the license, and locates a description of it.
    - Still need to review and check needed cases are covered.
        - overall place record (multiple licences - how to combine)
- [x] GK for sourced information, provide property that records date of retrieval from source.  (e.g. date of retrieval from GeoNames.)
    - Model change and extractor software affected?
- [x] Time_span: rethink properties used; particularly with reference to applicability of map deduced from publication date.  What are semantics of em:start, em:end
    - See: [models/notes/20190325-current-place-time-period.md](../models/notes/20190325-current-place-time-period.md).
- [x] Update GeoNames extractor to reflect model changes (cf. models/20190329-opole-example-multisourced.ttl)


### Later, and 2019-03-28/29 telecons:

- [x] Are there existing vocabs covering competence, etc.
    - e.g. http://www.tema.unina.it/index.php/tema/article/view/2530/0
        - maybe-useful diagram
        - seems to focus more on degrees rather than kinds of incertainty
        - seems to be oriented towards prediction rather that recording
    - https://www.lri.fr/~antoine/Papers/PUBLIES/Ontology_Uncertainty_and_Food_Risk_v2.pdf
    - https://www.w3.org/2005/Incubator/urw3/wiki/UncertaintyOntology.html
    - http://c4i.gmu.edu/ursw/2008/talks/URSW2008_P6_CeravoloEtAl_talk.pdf
    - Based on the above survey, I conclude there has been lots of work on this topic, but that there are not really any obvious ready-to-use Ontologies.  It is possible that the proposed EMPlaces competencies could be refined somewhat usinbg the W3C 'urw3' work (last 2 links), but it's not clear that any specific value would come from such work.
- [x] GK revisit identifiers for records vs identifiers for places.
    - Currently, particularly with the introduction of the multi-source model, all em:Place values are data resources, and their properties are thus implicitly making claims about a place _described by_ their subject resource.
    - Added foaf:primaryTopic http://xmlns.com/foaf/spec/#term_primaryTopic
- [ ] Workflow notes: need to add some specifics:
    - selection of place label and type label for overall place record.
    - generation of em:Source_desc/em:Authority entity for data added
    - generation of em:Time_period entity for each place
    - introduction of new kinds of annotation
    - explicitly cover how wikidata information is incorporated.
    - explicitly cover how EMPlaces data may be initialized from other sources
    - ...
    - (leave open)
- [ ] Publish EMPlaces vocabulary as RDF schema and/or OWL ontology (curently in Annalist). (leave open)
- [ ] GK think about trust models and how they can be applied to EMPlaces model when displaying a curated view on the data.  Specifically, how to deal with competing/inconsistent claims?  This could be about a curation model that can be applied to create a consistent view of data. (leave open)
- [x] GK add licence information to Opole example data and data extractor
- [x] GK think about licence representation: need another level of indirection so we can add local label?
    - possible model change
    - Need to update GeoNames extractor.
- [ ] GK source information in example data should be URI-labeled and refenced (like periods, etc.).  Also ensure extractor does likewise. (done in extractor; leave open in sample data)
- [ ] GK consider how alternative to single-point representation of location_value (e.g. bounding polygons)  (Maybe later when we have actual data; need to find out about possible spources; see also: http://www.geonames.org/products/premium-data-polygons.html)
    - e.g. https://histogis.acdh.oeaw.ac.at/shapes/shape/detail/8004
- [x] GK em:editorialNote becomes em:description/rdfs:comment.  Applicable to (say) name attestations.  Distinct from description of process: note em:editorialNote becomes more about the curation and creation of a record.  Update geonames extractor here. Note em:description and em:editorialNote may both be kinds of rdfs:comment - about the described place and (curation) process.
- [ ] AB add more authorities to Opole example.
- [x] GK update model diagrams:
    - page 2: note the model as described privileges EMPLaces place data (cf. "propose how place label and type label are derived from merged data" above).
    - page 6: ???

- [x] GK Note that qualified relation could be modeled as an annotation: is this an inconsistency of style?
- [ ] GK think about RDF semantics of multiple name attestations and multiple languages. (open)
- [x] GK Note that em:Source_desc rdfs:comment is for curatorial/editorial notes

- [ ] Update crosswalk?? (on hold unless needed)

Urgent Tasks?

1. Settle down any model changes noted above; update diagrams and examples and notes
    - [x] licensing
    - [x] licence representation: label and link
    - [x] source retrieval date
    - [x] em:editorialNote/em:description/rdfs:comment
    - [x] Time spans (diagram p6)
    - [x] Add diagram page for Location
2. Update Geonames extractor
    - [x] Update common definitions (copy from example)
    - [x] Add licencing data (see notes below)
    - [x] Update shape-shifter patterns (see notes below)
3. [ ] Flesh out workflow details and script support
    - AB loooking at this (2019-04-18)
4. [x] Generation of URI-identified resources where these might be shared
5. [x] Place identifiers (_contra_, record identifiers)
    - punt for now, but maintain awareness
    - note that if place id is available, can use foaf:primaryTopic to link it
6. [x] Generate URIs for source data descriptions

Notes for updating get_geonames_data:
- [x] em:licence: related resource (p1), alternate authority (p1), source (p8)
    - added indirection to reference URI:  --em:licence--> [] --em:link--> 
- [x] ems:EMPlaces -> ems:CofK
- [x] added foaf:primaryTopic to em:Place_merged diagram (could also apply to any em:Place)
- [x] added em:accessed to source descriptions
- [x] em:editorialNote -> em:description (applied to place).  em:description is subproperty of rdfs:comment. (used with wiki text)
- [x] em:editorialNote on em:Place / em:Source_desc is curational information.  em:editorialNote is subproperty of rdfs:comment.
- [x] MISSING: map wikidata to EMPlaces (alternate authority, etc.); add licence.
- [x] Need to connect generated place data from geonames with alternate authority data from wikidata


## 20190418 telecon

- AB: place type labels 
- AB: add authorities to Opole sample
- AB: licence for Rumsey maps
- AB: Looking at workflow details (e.g. how information is assembled from various sources)
- GK: sorting out 'alternateAuthority' construction in get_geonames_data

Later:
- AB: dealing with conflicting contributions (editorial)
    - dates need to be "just one truth" for EMDates
    - historical hierarchies: need one true definitive hierarchy for adding contributions


## 20190508 telecon

[ ] GK: Ask Karl about status of LPIF: planning to look at conversion.  Maybe tackle at hackathon.  Also ask about how to get bounding box data from Genomes.  Other sources
[ ] GK: next activity into look at postal data per Arno email 2019-03-22


### Preparing for EMPeople:

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
    - with data at `https://github.com/culturesofknowledge/emplaces/tree/develop/src/geonamesdataexport/data-test-alternate-authorities`

## Technical debt and unscheduled:

- [ ] Update `src/commondataexport/README.md` (documentation)
- [ ] Create capability to import EMPLaces data into Annalist, based on existing data (e.g., a new option for "get_annalist_data").
- [ ] Test suite for data wrangling utilities


