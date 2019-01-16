# Overview

The draft description below offers an overview of the functionality of the EM Places gazetteer. It is best consulted alongside the current [mock-up][1] of the detail view of a an individual place record. 

The first section of this document describes some of the key 'Concepts, Principles, and Definitions' which inform the design of EM Places. The second section, 'Interface (Detail View)' offers an overview of key features of the gazetteer by describing the user interface of a single record's detail view. 

We welcome anyone interested in the project to [get in touch with us][2] with comments and feedback.

## Concepts, Principles, and Definitions

### Places, Names, and Locations

EM Places is indebted to the [Pleiades] gazetter of Ancient Places for its [key concepts of place, name, and location][21] (see also ['Pleiades: Conceptual Overview'][22]):

> A _Place_ is a geographical and historical context for Names and
> Locations. Places may have within their core some features of the
> physical world – a sea, a bay, a river, a mountain range, a pass, a
> road, a settlement, or an ethnic region – but their primary quality is
> that, in the words of Yi-fu Tuan [1], they are constructed by human
> experience. Places may be no larger than a family dwelling or as big as
> an empire, be temporally enduring or fleeting. They may expand,
> constract and evolve over time. A place may be unnamed, unlocated,
> falsely attested, or even mythical.
> 
> A _Location_ is a current or former, concrete spatial entity. The
> midline of a river channel is a location. The center of a bridge's span
> is a location. The perimeter of a walled settlement is a location. Every
> location belongs to a place. The highest point of a mountain summit, for
> example, would be a location while the entirety of the mountain: its
> faces, ridges, couloirs, and forested slopes – and its significance in
> human history – would be the place context. The location entitled
> "Temple of Vesta" is but a small part of its context, Rome, while the
> place entitled "Hafir far west of Araba" provides only the barest
> semi-anonymous context for its sole desert waterhole location.
> 
> A _Name_ is a current or former, abstract textual entity. Like a
> location, a name belongs to a place. The Πάπρημις of Herodotus 2.59 is
> one of many with no known locations in the same place. At the other end
> of the spectrum, Ἀφροδισιάς belongs to a place rich in locations and
> names.

> [1] Y. Tuan, "Place: An Experiential Perspective," Geographical Review, 
> vol. 65, Apr. 1975, pp. 151-165.

For the first release of EM Places we have chosen (as an editorial decision) to largely bracket out mythical, extra-terrestrial and similar places referenced in historical texts. The 'Elysian Fields', for example, or 'Saturn' will as yet find no place in EM Places. This is because, in the first instance, our emphasis was on creating (for EMLO) a gazetteer for describing real places from which living people in the early modern world wrote and received letters, and secondly, as a resource for other early modern historians working with analogous sources.

Of course, this distinction is not as quite clearcut as it may initially seem, and this is where the Pleiades conceptual model gives us the flexibility we need to also account for other types of places. For example, as will be shown below, EM Places is interested in describing administrative-political, ecclesiastical and potentially other types of historical entities (judicial, military..) in their respective partitive hierarchies. In practice, it will be impossible to define such entities in spatio-temporal terms because we will never be able to accurately define and trace the changing boundaries of such entities. For this reason, such entities will need to be treated as conceptual places, and associated with temporal periods.  

Moreover, a conceptual separation of name, place and location is necessary for working with letters well, in order to describe ambiguous places of sending recorded as 'At Sea', 'In the field', 'In my lodging' and similar examples where no straightforward locations can be assigned. 

### Temporal Extent

EM Places is primarily designed for places referenced in historical records from the 16-18th centuries. As such, historical contexts and historical places recorded in the gazetteer will be limited to those whose existence clearly intersect with this period. Thus, for example, the Holy Roman Empire is a perfectly legitimate place in EM Places, even though its origins reach back long before the early modern period, and its existence ended well after it. The only exception to this rule are the polities included in the administrative-political hierarchies of current places (see 'Core and Extended Metadata', and 'Current and Historical Entities' below). The EM Places record for Augsburg, for example, will have the Federal Republic of Germany at the top of its current administrative-political hierarchy, a polity which only came into existence in 1949.

### Initial Scope and Future Growth

The pilot release of EM Places will be limited to c. 50-100 sample records serving as representative examples of full place entries as a means to best demonstrate all of the gazetteer's features to potential users and contributors. These records will be selected from the c. 6,500 current places in [EMLO][5] associated with the greatest number of letters sent, received, or those in which such places are mentioned. This deliberately limited set of full records will be accompanied by a much larger (TBD) sample of records containing only 'core' or 'reference gazetteer' metadata (see below) capable of being extended with additional metadata from contributors. 

Over time, we expect to add new place records to EM Places in much the same way as we have grown EMLO's epistolary database – that is, slowly and deliberately, in a way which allows us to adapt our resource, wherever possible, to meet the research needs of our individual and institutional contributors. Thus, while EM Places will draw on a small number of reference gazetteers for its core place metadata we are not designing the gazetteer  bulk aggregator of place data. Our emphasis will be on much fewer, but richer records, directed towards the needs of early modern scholars.  

### Core and Extended Metadata

All EM Places records will be composed of two distinct classes of metadata: 1) a minimal, and required set of basic or 'core' current metadata ingested without modification from several reference geo-gazetteers, and 2) an additional, and optional set of extended historical metadata defined by EM Places provided by contributors.

By default, _Core Metadata_ will be ingested semi-automatically from a small number of reference geo-gazetteers (currently: GeoNames, Getty TGN, and WikiData) and will consist of data on:

* The preferred (i.e. default) place name
* A set of unique (i.e. non-repeating) alternative place names (toponyms)
* Location data (typically a single latitude/longitude pair, with multiple pairs representing regions where these are available)
* The current administrative-political hierarchy
* Links to other external gazetteer authorities (e.g. the German GND authority)

Core metadata will, in effect, form the spine of the gazetteer. This is data which EM Places will accept 'as is' from its reference gazetteers without further editing (with the exception of some processing steps to e.g. remove duplicate entries and standardize how the data is indexed and/or displayed). On the basis of this data, EM Places will additionally represent the place on a map, produce a set of formated bibliographic references, and, crucially, create its permanent URI for reference and reconciliation.

In practice, due to its size, GeoNames will be the primary reference gazetteer for EM Places, with the Getty TGN (and in the future, possibly further gazetteers) serving as a secondary and supplementary resource. WikiData, by contrast, will be drawn on primarily as a means for importing a list of additional linked authorities and because the information in WikiData (while often richer in detail) is likely to be of more variable quality than GeoNames. 

By limiting our requirements for a minimal, valid EM Places record in this manner, we gain the ability to a) create bulk records on demand from an existing set of authority data (e.g. a list of GeoNames IDs), and thereby b) increase the utility of our resource for users who wish to use EM Places to disambiguate and reconcile their existing records. The intent is that EM Places will be able to refresh its core data at regular intervals (e.g. bi-annually) with minimal editorial intervention to benefit from upstream corrections/additions at their sources.

(Further details of the features and implementation of core metadata, including an overview of how EM Places will work with places which cannot be found in its reference gazetteers, are discussed in the sections below).

By contrast, all other data fields in EM Places will be made up of optional _Extended Metadata_ contributed by our users and partner projects. Each place record will be able to capture additional historical data on:

* Attestations to additional place name variants
* A brief text description to assist with its disambiguation, initially seeded (where available) from Wikipedia
* One or more images and/or links to geo-referenced, historial maps
* Administrative, Ecclesiastical (and in future releases, potentially Military and Judicial) historical hierarchies
* The date(s) of transition to a new calendar (e.g. from Julian to Gregorian)
* Bespoke data associated with a place (e.g. its function as station on a named postal route)
* Related historical resources
* Bibliography

(Further details of the features and implementation of extended metadata are discussed below).

### Current and Historical Entities

Because our primary reference gazetteer (GeoNames) is itself an aggregator of the most up-to-date gazetteer information sources available, all core metadata (i.e. the preferred place name, alternative names, location, administrative-political hierarchy) derived from it will consequently also be based on 'current' and not historical place data. This was a deliberate design decision which acknowledged that the great majority of historical inhabited places such as towns referenced in early modern documents still exist today, and that the most reliable and detailed information on such places may be found in large scale, current geo-gazetteers and authorities. 

In many cases, though the main historical name for a place may have changed over time, at least some of these historical variants will still be listed in its GeoNames, Getty TGN, and/or WikiData entries, even usually with little or no associated temporal period attached to it. This is even more true for its location. In contrast, very few if any current places today will share the same political-administrative hierarchies they had during the early modern period. 

To accomodate this, EM Places provides a separate means (discussed in more detail below) in extended metadata for listing all of the historical political-administrative and ecclesiastical hierarchies of which it was part in the past. Because the historical polities making up these hierarchies (e.g. the Bohemian Crown) often do not exist anymore, and do not have clearly demarcated spatial boundaries, they will not be found in GeoNames, and we expect that we will need to collect and curate their data ourselves and with the help of our contributors.

In summary, while conceptually (i.e. from the perspective of the EM Places data model) 'current' and 'historical' places are identical – in our implementation, 'current' places will draw their core metadata from our primary reference gazetteer (GeoNames) while 'historical' places not found in GeoNames will have their core metadata added manually. Such places will not include a 'current administrative hierarchy' in core data, nor will they include a single, representative location expressed as geospatial coordinates. Instead, where these are available, we will link to a suitable digitized historical maps.


### Uncertainties

[TBD]

### Dates and Periods

[TBD]

### Provenance

[TBD]

## Interface (Detail View)

This section reviews key features of EM Places with the aid of a mock-up interface of the detail view of a single place record. The place selected for this example, Opole, is a town in Poland with a [current entry in GeoNames][25]. Please refer to the [full-size PDF image][1] for a high-resolution mock-up of the place record detail view interface.

Note: The _Info_ links shown next to each user-interface element will link to a pop-up window briefly describing its functionality. It is intended as a help text. The _Provenance_ links will lead to a separate page with provenance metadata the data shown in that interface element. 

### Preferred place name, alternative place names, current administrative hierarchy, location, citations.

[Screenshot](https://github.com/culturesofknowledge/emplaces/blob/master/images/screenshots/core-data.png)

Alongside the _Preferred Name_ name of the place, we show a merged list of all unique _Alternative Place Names_ (toponyms) found in our reference gazetteers. While useful for disambiguation purposes, these will seldom be able to provide us with historical, early modern toponyms. As we will see below, these can later be added as part of the record's extended metadata in the 'Name Attestations' section. 

The _Current Administrative Hierarchy_ shows the partitive relationships between a place its polities. Here, the town of Opole, is part of a third-order administrative polity (called Opole), which in turn is part of a second-order polity (also called Opole), which is part of the Opole Voivodeship, which in turn is part of Poland. The data in the Current Administrative Hierarchy is derived exclusively from GeoNames. This is because gazetteers interpret such hierarchies in different ways. For example, in the [Getty TGN entry for Opole][26], there is only one administrative polity between the town of Opole and Poland and it is called differently (Opolskie). In addition, the Getty TGN hierarchy does not terminate in Poland but in 'Europe' and 'World'. Moreover, Poland itself is not defined as a 'Country' (as in GeoNames) but a 'Nation'. This is not just a question of labels. As a consequence of this, GeoNames and the Getty TGN use quite different models, for example, to characterise England, Great-Britain, and the United-Kingdom. 

To avoid having to arbitrate and resolve such conflicts manually, we have opted for the Current Administrative Hierarchy to rely exclusively on the data maintained by GeoNames. A regrettable side-effect of this is that the polities in the hierarchy are shown with generic GeoNames feature codes (e.g. ADM1, PPLA). In the Getty TGN, these label are bespoke, and contextual. 

_Location_ data will in most instances be in the form of a single latitude/longitude coordinate pair and will be copied from GeoNames. Today, geo-spatial coordinates drawn up with respect to the Greenwich Prime Meridian in accordance with the WGS84 geodetic standard. However, in the early modern modern period (and well into the nineteenth century) multiple [prime meridians were in active use][27]. Amongst the most important of these were the El Hiero (Ferro), Cadiz, and Paris meridians. To raise awareness of their use, and to help disambiguate historical latitude and longitude references, users will have the option of viewing location coordinates as based on several different prime meridian systems and in degrees, minutes, and seconds. 

A _Permanent URI_ for each place record in EM Places will be generated automatically by the underlying [Timbuctoo infrastructure][28] for reuse by others to reconcile their places against EM Places, and, crucially, as the basis for sharing our records as Linked Open Data. Drawing on this permanent identifier, we plan to offer a simple means to reference an EM Places record in several standard bibliographic _Citation_ formats.

### Map and Description 

[Screenshot](https://github.com/culturesofknowledge/emplaces/blob/master/images/screenshots/map-description.jpg)

If location data is available for a current place, it will be default be represented as a single point on and (OpenStreetMap) _Map_. Optionally, if the required georeferenced data is available, the modern representation can be accompanied by a small number of additional historical cartographic representations from a source such as the [David Rumsey Map Collection](https://www.davidrumsey.com). The different maps will be identified, in the first instance, by date of publication, with further metadata recorded in their provenance fields.

To help further disambiguate the places, and to provide more context for full-text search, each place record will be seeded with a paragraph of _Descriptive Text_ from WikiPedia. 

### Name Attestations, Calendars, Associated Places

[Screenshot](https://github.com/culturesofknowledge/emplaces/blob/master/images/screenshots/attestations-cal-assoc.png)

_Name Attestations_ are documented instances of name variants of the preferred and alternative names in core data. For example, if a scholar finds a new reference to Siena recorded as 'Ciena' and this toponym is not already listed as an alternative name in our reference gazetteers, then this it can be recorded here, along with the language, date, and source for the attestation. It is important to note that the EM Places editors will not be required to merge or select amongst conflicting attestations provided to us by our contributors. Such differences can be recorded in the provenance metadata for the attestation, and independently evaluated by users of the gazetteer.

The _Calendars_ element is a simple visualization of the predominant calendars (Julian, Gregorian) in use between 1500 and 1800 at that place. This data will be pre-populated via a hierarchy of inherited calendars. So, for example, in the absence of any more specific information for a region, we will assume that this place transitioned from Julian to Gregorian in October 1582 (the date of Gregory XIII's papal bull). However, if a region transitioned to the Gregorian calendar at a different date, then all places under it (e.g. towns and cities) will inherit this date and override the default 1582 transition. 

We will not attempt to record variances from regional calendar use patterns at smaller scales such as individual towns. For example, we will not note as an exception or override the default if we have a record of person writing from Calais in 1632 to someone else in England in the Julian calendar (as opposed to the Gregorian calendar, then widely used in France). Our assumption is that the choice to use the Julian in this particular instance was dependant on the addresse and/or place of receipt (England did not change to the Gregorian calendar until 1752), and not the place of sending. 

_Associated Places_. In some cases, we may wish to capture additional, bespoke information on places or to express the relationship between two or more places. For example, metadata describing a set of buildings in a town or the distance and time required to travel between two postal stations. For this kind of information, our existing data fields are of limited use, as these would not be able to capture the kinds of custom properties relevant to such places or to their relationships.

To accomodate this, we are considering listing such places (in addition to their own, primary place record entries) under 'Associated Places' in the place(s) best associated with it (e.g. in the case of 'Merton College', this would be the town of 'Oxford) together with a link to a separate page, where their bespoke metadata can be shown. This arrangement will allow contributors the freedom to share their metadata in a manner closer to the form in which it was collected. If a researcher, for example, wishes to share with EM Places, a data on a set of streets, then will try to accomodate the original data structure as far as feasible by permitting the use of additional 'street relevant' properties on this page. 

The appropriate functionality and data model for 'Associated Places' are currently under discussion. 

[TBC]

### Historical hierarchies

[Screenshot](https://github.com/culturesofknowledge/emplaces/blob/master/images/screenshots/historical-hierarchies.png)

The _Historical Hierarchies_ element shows the historical Administrative-political, Ecclesiastical (and in future releases of EM Places, potentially also Judicial, and Military hierarchies) for a place. For example, in the screenshot above, we can see from its administrative-political hierarchy, that the Silesian town of Opole fell under the Duchy of Opole from 1281-1521. For each part of the hierarchy, we will provide users with a means to view the period during which this entity existed (e.g. for the Bohemian Crown, from 1348 to 1918).

We anticipate that administrative and ecclesiastical data will be easier to collect from contributors than judicial and military. As a result, displaying data on the latter two categories might not be included in the initial release.

### Related Resources, Bibliography, and Feedback

[Screenshot](https://github.com/culturesofknowledge/emplaces/blob/master/images/screenshots/resources-bib-feedback.png)

_Related Resources_ provide a means for listing additional, predominant digital resources related to a place which aren't usefully represented in traditional bibliographies. In many instances, these will be live links to searches carried out on external databases (for example, all letters sent to or from a place). 

The _Bibliography_ is intended for recording predominantly offline, scholarly print publications. In the initial release of EM Places, this will be a simple formatted text list. However, our intent is that in the future, contributors creating the list will be able to easily see if a certain entry had previously been added to a different record, and to select this, so that bibliographic entries can be added in a consistent manner. In addition, contributors should ideally also have a means to add a bibliographic entry to a whole class of records (e.g. to have an entry appear in all places which are grouped together at the same level in a hierarchy). This feature would help prevent contributors working independently on different places (in e.g. the same region and period) from repeatedly entering the same reference in different records.

#### Feedback

A link to a simple comment form, referencing the current record and (if present) a link to the logged-in users profile, or else a mailto: link, referencing the current record (e.g. in the subject field).

[Screenshot](https://github.com/culturesofknowledge/emplaces/blob/master/images/screenshots/credits-export.png)

#### Credits, Contributors, License, and Export
 
[TBA]

[1]: /images/current_display.pdf
[2]: https://github.com/culturesofknowledge/emplaces#feedback-and-comments
[3]: https://www.uni-bamberg.de/histgeo/forschung/aktuell/
[4]: /images
[5]: http://emlo.bodleian.ox.ac.uk
[6]: http://www.culturesofknowledge.org/?p=8455
[7]: http://gov.genealogy.net/item/show/OPPELNJO80XQ
[8]: https://omeka.org/s/
[9]: http://www.geonames.org/export/codes.html
[10]: https://www.getty.edu/research/tools/vocabularies/aat/
[11]: http://linkedpasts.org
[12]: http://euratlas.com
[13]: https://github.com/whosonfirst
[14]: https://spelunker.whosonfirst.org/id/101752159/
[15]: http://www.bibtex.org
[16]: https://en.wikipedia.org/wiki/RIS_(file_format)
[17]: https://citationstyles.org
[18]: http://blogs.bodleian.ox.ac.uk/digital/2017/03/23/wikimedia-for-public-engagement/
[19]: http://vocab.getty.edu/page/aat/300108377
[20]: https://zabytek.pl/en/obiekty/opole-kosciol-parafialny-pw-matki-boskiej-bolesnej-i-sw-wojc
[21]: https://www.wikidata.org/wiki/Q55338793\
[22]: https://pleiades.stoa.org/help/technical-intro-places
[23]: https://pleiades.stoa.org/help/conceptual-overview
[24]: https://www.davidrumsey.com
[25]: http://www.geonames.org/3090048/opole.html
[26]: http://www.getty.edu/vow/TGNFullDisplay?find=Opole&place=&nation=Poland&subjectid=7007751&english=Y
[27]: https://en.wikipedia.org/wiki/Prime_meridian
[28]: https://timbuctoo.huygens.knaw.nl
[29]: http://n2t.net/e/ark_ids.html 

