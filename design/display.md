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

For the first release of EM Places we have chosen (as an editorial decision) to bracket mythical, imaginary and similar conceptual places. The 'Elysian Fields', for example, would (regrettably) find no place in the gazeteer. This is because, in the first instance, our emphasis is on creating a resource for describing places from which real people in the early modern world wrote and received letters.

Of course, this distinction is not as clear as it may initially seem, and this is where the Pleiades conceptual model gives us the flexibility we need to account for other types of places. For example, as will be shown below, EM Places is interested in describing  administrative-political, ecclesiastical and potentially other types of historical entities in their respective hierarchies. In practice, it will be impossible to define such entities in spatio-temporal terms – we will never be able to define and trace the changing boundaries of such entities. For this reason, they need to be treated as conceptual places associated with temporal ranges. 

A conceptual separation of place and location is necessary for working with letters well, in order to describe places such as 'At Sea', 'In the field', 'In my lodging' and similar examples where no straightforward locations can be assigned. 

### Temporal Extent

EM Places is focused on places referenced in historical records from the 16-18th centuries. As such, historical contexts and historical places recorded in the gazetteer will be limited to those whose existence clearly intersects with this period.

### Initial Scope and Future Growth

The pilot release of EM Places will be limited to c. 50-100 sample records serving as representative examples of full place entries as a means to best demonstrate all of the gazetteer's features to potential users and contributors. These records will be selected from the c. 6,500 current places in [Early Modern Letters Online (EMLO)][5] associated with the greatest number of letters sent, received, or mentioned. This small set of full records will be accompanied by a much larger (TBD) sample of records containing only 'core' or 'reference gazetteer' metadata capable of being extended with additional metadata from contributors.

Over time, we expect to add new place records to EM Places in much the same way as we have grown EMLO's epistolary database – that is, slowly and incrementally, in a way which allows us to adapt our resource, wherever possible, to meet the research needs of our individual and institutional contributors. Thus, while EM Places will draw on a small number of reference gazetteers for its core place metadata we are not designing the gazetteer  bulk aggregator of place data. Our emphasis will be on much fewer, but richer records, directed towards the needs of early modern scholars.  

### Core and Extended Metadata

All EM Places records will be composed of two distinct classes of metadata: 1) a minimal, and required set of basic or 'core' current metadata ingested without modification from a small number of reference geo-gazetteers, and 2) an additional, and optional set of extended historical metadata defined by EM Places provided by contributors.

By default, _Core Metadata_ will be ingested semi-automatically from a small number of reference geo-gazetteers (currently: GeoNames, Getty TGN, and WikiData) and will be comprised of data fields on:

* The preferred (i.e. default) name
* A set of unique (i.e. non-repeating) alternative place names and variants 
* Location data (typically a single latitude/longitude pair, with multiple pairs representing regions where these are available)
* The current administrative-political hierarchy
* Links to other external gazetteer authorities (e.g. the German GND authority)

This metadata will, in effect, form the spine of the gazetteer. This is data which EM Places will accept 'as is' from its reference gazetteers without further editing (with the exception of some processing steps to e.g. remove duplicate entries and standardize how the data is indexed and/or displayed). On the basis of this data, EM Places will additionally represent the place on a map, produce a set of formated bibliographic references, and, crucially, create its permanent URI.

In practice, due to its size, GeoNames will be the primary reference gazetteer for EM Places, with the Getty TGN (and in the future, possibly further gazetteers) serving as a secondary and supplementary resource. WikiData, by contrast, will be drawn on primarily as a means for getting a list of additional linked authorities, and as a supplementary resource. 

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

(Further details of the features and implementation of extended metadata are discussed in the sections below).

### Current and Historical Entities

Because our primary reference gazetteer (GeoNames) is itself an aggregator of the most up-to-date gazetteer information sources available, all core metadata (i.e. the preferred place name, alternative names, location, administrative-political hierarchy) derived from it will consequently also be based on 'current' and not historical place data. This was a deliberate design decision which acknowledged that the great majority of historical inhabited places such as towns referenced in early modern documents still exist today, and that the most reliable and detailed information on such places may be found in large scale, current geo-gazetteers and authorities. 

In many cases, though the main historical name for a place may have changed over time, at least some of these historical variants will still be listed in its GeoNames, Getty TGN, and/or WikiData entries, even usually with little or no associated temporal period attached to it. This is even more true for its location. In contrast, very few if any current places today will share the same political-administrative hierarchies they had during the early modern period. 

To accomodate this, EM Places provides a separate means (discussed in more detail below) in extended metadata for listing all of the historical political-administrative and ecclesiastical hierarchies of which it was part in the past. Because the historical polities making up these hierarchies (e.g. the Bohemian Crown) often do not exist anymore, and do not have clearly demarcated spatial boundaries, they will not be found in GeoNames, and we expect that we will need to collect and curate their data ourselves and with the help of our contributors.

In summary, while conceptually (i.e. from the perspective of the EM Places data model) 'current' and 'historical' places are identical – in our implementation, 'current' places will draw their core metadata from our primary reference gazetteer (GeoNames) while 'historical' places not found in GeoNames will have their core metadata added manually. Such places will not include a 'current administrative hierarchy' in core data, nor will they include a single, representative location expressed as geospatial coordinates. Instead, where these are available, we will link to a suitable historical maps from resources such as [FNZGIS][3], the [David Rumsey Historical Map Collection][23], and [EurAtlas][12].


### Uncertainties

[TBA - review with Graham what we've put in place in the data model]

### Dates and Periods

[TBA - review with Graham what we've put in place in the data model]

## Interface (Detail View)

### Core Data



### Preferred Place Name; alternative names

The default/preferred place name and its alternate names (toponyms) will come from the reference gazetteer but only a subset of unique names will be displayed. 

For example, while we can allow users to search for and find places using a Persian transliteration of a place (Opole: اوپوله) there is no need to display this particular transliteration in the list of alternative names. For the display list, alternative names will be drawn from a short list of major European languages and historical forms (i.e. Latin). Next, the list of alternative names will be compared with one or more additional gazetteers. From this these lists, a merged set of unique alternative names will finally be shown. This is to avoid having to list multiple, identical instances of e.g. 'Opole' for the many language transliterations supported by GeoNames.  

### Current Hierarchy

The administrative/political hierarchy ('polity') for a current place provided by the reference gazetteer(s). Note that GeoNames only provides data for ADM1, ADM2 etc. It does not attempt to label these as states, provinces, counties etc. However, Getty TGN does provide this information. Unfortunately, Getty and GeoNames sometimes disagree on the depth of the hierarchy making automatic matching of Getty labels to GeoNames hierarchies difficult. For this reason v1 will not attempt to match places with labels. We may return to this in a future revision of EM Places or perhaps make us of generic labels (as appears to have been done by Mapzen for their ['Who's on First'][13] open-access dataset – see, for example, [their entry for Opele][14]).  

By definition, a historical (i.e. former) place can’t display its administrative hierarchy here – instead, a placeholder message could refer the user to the section on ‘Historical Hierarchies’. Alternatively, we may use this area to highlight the period of the historical place

Further discussion is required on what will constitute core data for historical places. 

### Location

The representative center for a place displayed as decimal lat/long and degrees (image just shows decimal). It should be accompanied by a link allowing the URI to be copied as decimal lat/long on mouseclick. What will be copied should be revealed on mouseover. 

We will not attempt to override what GeoNames considers to be the representative point for a current place. For a historical place, an editor will decide where to locate the center (e.g. Vienna for the Habsburg Empire). TBD how to capture a representative historical location can changing over time. We also need to think about what to do if we were to have temporal polygons for historcal places.

### Citation

A simple means to represent the canonical URI as an academic citation, in several standard bibliographic formats and copy it on mouseclick for reuse. What will be copied should be revealed on mouseover, allowing the user to see in advance what the entry will look like in the different citation styles. We had initially considered using [BibTeX][15] as the generic bibliography interchange format. However, [RIS][16] is more current and may be more appropriate. [CSL][17] could provide a means to convert amongst formats.

### Permanent URI

This should be a short form. Timbuctoo generated permanent URI based on the custom domain for EM Places (probably emplaces.info). It should allow the URI to be copied to the clipboard on mouseclick. We need to decide if we additionally want to offer e.g. a DOI or an ARK identifier. Amongst the issues to consider are whether the metadata required by such a service is suited to us (and whether we can then employ the same service for EM People as well). See further:

ARK info: http://n2t.net/e/ark_ids.html (n2t,net is the resolver service) and DOI CataCite info: https://schema.datacite.org/meta/kernel-4.0/

### Name Attestations

Attestations are sourced instances of name variants of the preferred and alternative names in core data. For example, if a scholar finds a reference to Siena in a manuscript written 'Ciena' and (TBD via the editorial policy) this is not already listed as an alternative name in our reference gazetteers, then this toponym can be recorded here, along with the language, date, and source for the attestation. 

TBD structure for the source supporting the attestation. If possible, we will reuse the standard, basic format we have defined for bibliographic entries.

### Calendars

A simple visualization of the predominant calendars (Julian, Gregorian) in use between 1500 and 1800 at that place. This value will be pre-populated via a hierarchy of inherited calendars. So, for example, in the absence of any more specific information in use in a region, we will assume (but also make this clear in the interface) that the place transitioned, for example, from Julian to Gregorian in 1582 (the year of Gregory XIII's papal bull). If a place or set of places (such as a region) transitioned at a different date, then note this, and have all places under it inherit this (and override the default 1852 transition). If a more specific place such as a town transitioned in a different manner, then note this for that town, and override the regional transition etc.

We will not attempt to record variances from regional calendar use patterns at smaller scales such as individual towns. For example, we will not note as an exception or override if we are presented with a record of someone living in the town of Calais in 1632 (with the Gregorian calendar in use in France), writing to someone else in England in the Julian calendar. Our assumption is that the choice to use the Julian in this instance was dependant on the addresse and/or place of receipt (England did not change to the Gregorian calendar until 1752), not the place of sending.

TBD are labels or symbols for recording different variants of one calendar. For example, Julian calendar with January 1 as the start of the year and Julian with a March 25 start of year. The current plan is to specify this in parentheses after the name of the calendar. e.g. 'Julian (Mar 25)' means Julian calendar with the first day of the year on March 25. We'll need something similar for the most generic case where we have no data at all on the calendar and thus assume (for conversion purposes only) that the switch to the Gregorian took place on 15 October 1582.

### Associated Places

In some cases, we may wish to capture information on places (current or historical) below the level of an inhabited place. For example, a set of buildings representing an institution (e.g. Christ Church College) or an individual building or locale (e.g. an inn, or a street). For these and similar kinds of places, especially if they are historical, we may have very little data – often not enough to create a full core data record. And even if we could, the format we've prepared for places is largely predicated on 'inhabited places'. It wouldn't be able to capture the kinds of properties relevant to a building (e.g. the name of the architect).

To accomodate this, we are proposing that this class of places be grouped under the full/regular record of the place (conceptually, or spatially) enclosing it. Thus, for example, Christ Church College, would be included under the entry for Oxford etc. Such places will be listed in a separate tabular section ('Related Resources') of the full entry for the 'containing' place.

Each entry in this table (following the example of GOV – e.g. for [Opele][7]) will include a link leading to a separate page, where the specific metadata for that class of place will be shown. The idea is to allow contributors more freedom to share their metadata in a manner closer to the form in which it was collected (which the default granulity terminating in 'inhabited place' would not allow). If a researcher, for example, wishes to share with EM Places, a large set of data on a set of streets, then we should try to accomodate the original data structure as far as feasible by permitting the use of additional 'street relevant' properties. Conversely, smaller and/or less common contributions could still be referenced here but may need to make do with the already list of available properties. That is to say, the decision to extend the availale list of properties to accomodate the needs of a contributor should be possible, but subject to prior discussion and agreement with the contributor.

In the current draft, the intent is for a simple wikidata-style interface where a contributor or editor selects a property from a preset list and enters a value. See [this blogpost][18] for an analogous example of how this could work. The tabular list (see [current mockup][1]) could, for example, consist of the follows:

| Place  | Type |  Relationship  |
| ------------- | ------------- |------------- |
| Our Lady of Sorrows and St. Adalbert  | Parish Church  |  PartOf  | 

If the contributed data does not already have a well-defined vocabulary, the feature 'type' may, for example, be drawn from a pre-selected subset of the [Getty AAT][10] vocabulary (here, ['Parish Church'][19] and matched, where applicable, with the appropriate [GeoNames feature code][9] so that this this data becomes easier to integrate by other, less granular gazetteers.

A test 'related place' record on [St. Adalbert Parish Church][21] has been created on WikiData and is being reviewed for inclusion in the [Opole sample RDF](/models/20180410-opole-example-data.ttl).

### Related Resources

A list of what we expect will be predominantly online, digital resources (for traditional scholarly references, contributors can make use of the bibliography section). Some of the URIs to these resources can be derived  automatically from our reference gazetteers (e.g. links to Wikipedia, WikiData, certain other gazetteers) but most of which will be suggested by contributors and confirmed by editors. 

This could also include dynamic links to resources which can be queried over an API for more information about a place in the gazetteer. The data would be polled and updated at an appropriate interval. For example, X number of letters were sent from this place, and Y number of letters were received at this place. 

### Bibliography

A list of bibliographic resources (predominantly offline, scholarly references). At minimum, an unstructured free text list would suffice for v.1. However, our assumption is that this can be a simply structured list, and with the ability to apply place tags to each entry, making it much easier for subsequent contributors to find and select existing bibliographic entries in a consistent manner. This helps avoid contributors working independently on different places (in e.g. the same region and period) repeatedly entering the same reference in different records, possibly in different formats. 

### Creators & Licenses

A listing (machine readable) of the Creator of the record (i.e. the person or organization which created the initial record), one or more subsequent Contributors, a credit line for the reference gazetteers, and a notice of the licenses in use. GeoNames is CC-BY v3 (or possibly v4, the site is inconsistent) so it appears that CC0 is not an option.

### Export

A means to manually export the current record (only) in several common formats, currently assumed to be CSV, Excel, Turtle, GraphML, and GeoJSON. 

Note: GeoJSON is required for Pelagios compatibility via [LPIF format][11].

### Maps

The required (for current places) default map view will be an e.g. OpenStreetMap view using the location provided by core data. 

Optionally, it will be possible, via tabs, to view a finite number of (e.g. 4) historical, open-access geo-referenced and live-tiled maps of the place drawn from a provider such as https://www.davidrumsey.com or http://www.oldmapsonline.org or http://retromap.ru. Alternatively, one could substitute a single tile as a thumbnail for the historical map, and link this to the external historical map resource.

### Description

This field will initially be (semi?)-automatically populated with data from the Getty TGN and then further revised as needed by users/editors.

### Historical Hierarchies 

This section is best understood by looking at the draft [interface mockups][4].

Historical hierarchies show the historical administrative, ecclesiastical, judicial, and military hierarchies for both historical and current places. Initially, this will show the period a certain relationship existed. For example, from an administrative/political perspective, the Silesian town of Opole fell under the Duchy of Opole from 1281-1521. In each part of the hierarchy (with the precise mode of display TBD, for example via mouseover) a user will also be able to view the period of existence of each place entity (e.g. the Bohemian Crown existed from 1348 to 1918). Together, a set of dated entities, linked in hierarchial order by a set of dated relations, forms one (from a possible four kinds of) historical hierarchy. In the case of ecclesiastical hierarchies, an additional row of tabs will be needed to show what kind of hierarchy (e.g. what religion and/or confession) is being tracked. 

Further discussion is needed on the necessary editorial policies. We expect that administrative and ecclesiastical data will be easier to collect from contributors than judicial and military. As a result, displaying data on the latter two categories might not be included in the initial release.

### Feedback

A link to a simple comment form, referencing the current record and (if present) a link to the logged-in users profile, or else a mailto: link, referencing the current record (e.g. in the subject field).

### Info and Sources pop-ups

Many sections in the individual record display will include 'Info' and/or 'Sources' links. Clicking this could, as one possibility, show a pop-up with text on that section. In the case of Sources, this could include both an unstructured text area, and a structured bibliographic area. 
 

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
