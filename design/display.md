
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

_Related Resources_ provide a means for listing additional, predominant digital resources related to a place which aren't usefully represented in traditional bibliographies. In many instances, these will be live links to searches carried out on external databases. For example, to all letters sent to or from a place, or to all mentions of a place in a text. 

The _Bibliography_ is intended for recording predominantly offline, scholarly print publications. In the initial release of EM Places, this will be a simple formatted text list. However, our intent is that in the future, contributors creating the list will be able to easily see if a certain entry had previously been added to a different record, and to select this, so that bibliographic entries can be added in a consistent manner. In addition, contributors should ideally also have a means to add a bibliographic entry to a whole class of records (e.g. to have an entry appear in all places which are grouped together at the same level in a hierarchy). This feature would help prevent contributors working independently on different places (in e.g. the same region and period) from repeatedly entering the same reference in different records.

A link to a simple _Feedback_ form, or else a mailto: link, referencing the current record in the subject field.

### Creator, Contributors, License, and Export
 
[Screenshot](https://github.com/culturesofknowledge/emplaces/blob/master/images/screenshots/credits-export.png)

Our intent is to distinguish and separately credit the (single) _Creator_ of a place record, and the potentially multiple _Contributors_ to the data in it. Although we would be able, in principle, to record and display as a contributor each user who made a change to a data field in EM Places, it is unlikely that we will want to do so, as this would give equal credit to the person contributing the original data, and the person who made a trivial change to the data. Moreover, not all contributions to the gazetteer are equal. Deciding which types of edits to count as contributions will be managed under an editorial policy. 

EM Places will incorporate data from multiple sources, not all of which will have the same open-access _License_. Thus, for example, data from GeoNames is licensed under CC0, while research data from a contributor is likely to be shared under CC-BY. Which, and how many of these licenses to display here for users who wish to export data from EM Places will need to be settled under an editorial policy.

Users will have the opportunity to _Export_ the open-access data in EM Places on-demand for reuse. We anticipate to provide support for sharing this data in tabular formats (CSV, Excel), as Linked Open Data (Turtle-RDF), and in the Geo-JSON format employed by the Pelagios Gazetteer Interchange Format. In the context of a single record, shown here, an export will only include the data for one place record. In the Search and Browse interface, EM Places users will additionally have the opportunity to export bulk records matching all or a selection of their search criteria. 

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
[30]: https://pleiades.stoa.org
