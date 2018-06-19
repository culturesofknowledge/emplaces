# Overview (Display View)

The draft description below offers an informal overview of the functionality of the gazetteer. It is best read alongside the [interface mockup][1] of the detail/display view for a typical place record. We welcome anyone interested in the project to [get in touch with us][2] with comments and feedback.

## Concepts and Principles

### Scope

EM Places is centered on the 16-18th centuries. As such, historical contexts and historical places recorded in the gazetteer will be limited to those whose existence clearly intersects this period.

### Sources and Contributors

The initial release of EM Places will probably be limited to c. 50-100 sample records serving as representative examples of full entries and and as a means to demonstrate the gazetteer's features to contributors. The records will be selected, in large part, from those places in [Early Modern Letters Online (EMLO)][5] with the greatest number of letters sent, received, or mentioned. An alternative approach is to match a small number (again, c. 50-100) complete sample records with a larger group (e.g. 5-6K) of minimal place entries.

Over time, we expect to add records to EM Places in much the same way as we have grown EMLO's database – that is, slowly and incrementally, in a way which allows us to meet, wherever possible, the particular needs of our individual and institutional contributors. Although EM Places will draw on reference gazetteers for certain core data (e.g. locations) it is not designed to be a bulk aggregator of place data. Our emphasis will be on much fewer, but richer records, directed towards the needs of early modern scholars.  

### Current and Historical Place Entities

Our use of ‘current’ refers to still currently existing places and thus generally also found in our reference gazetteers (GeoNames, Getty TGN). Consequently, a current place will also have a current administrative hierarchy (e.g. ADM1, ADM2, ADM3..) and a physical location (i.e. lat/long)  maintained for it outside of EM Places by our reference gazetteer(s).  

In contrast, a ‘historical’ place is no longer extant entity with a temporal validity (e.g. the Habsburg Monarchy, 1526-1804). EM Places will not attempt to capture spatial data on historical regions (i.e. polygons). Instead, we will either provide a single representative lat/long location (e.g. Vienna) or external link, where available to external resources/projects with the necessary expertise and data (e.g. to [FNZGIS][3] for Central/Eastern Europe). A second, alternative approach is to provide low resolution bitmap maps of historical places where these are available (e.g. a [EurAtlas map][12] of the Holy Roman Empire in 1700).

Let's take, for example, the town of Opole in Poland. This is a currently extant place, and would be listed with alternative name and location data from our reference gazetteers. Amongst its alternative names (toponyms) is a historical name, Oppeln. EM Places will   record 'Oppeln' as an toponym without attempting to contextualize it historically. This is because our alternative name data for current places will come from reference gazetteers which themselves typically do not offer this data (see section below on Core vs. Additional Metadata).

However, the record for a current place can optionally include additional historical information and contexts, such as data on historical calendar use, further attestations of toponyms, or various kinds of hierarchies associated with it (e.g. ecclesiastical, offering data on parishes, dioceses etc.). These additional contexts can be shared with EM Places by individual researchers and projects. When this is itself a place (e.g. the Bohemian Crown, 1490-1742) it is recorded in the gazetteer as a separate, historical place entity, linked to the current places with which it is associated. For example, in the period 1490-1521 the town of Opole (current place) was a part of the (historical place) 'Duchy of Opole' which itself was part of the (historical place) Governorate of the 'Duchy of Silesia' etc. culminating in the (historical place) 'Holy Roman Empire'. 

In summary, all 'current places' in EM Places will have a current hierarchy and location (taken from reference gazetteers) and, optionally, can be associated with several more 'historical places' and contexts (e.g. calendars), contributed to the gazetteer by scholars and projects. 

Ultimately, the intent of EM Places (and alongside it, EM People, and EM Dates) is to provide a series of [Linked Open Data resources for computable, historical entities][6].

### Core and Additional Metadata

We envision several sources for data in EM Places. _Core metadata_ is periodically drawn by API from reference gazetteers (currently: GeoNames, Getty TGN) and will be comprised of:

* Preferred Place Name
* Alternative Names (all entries are indexed, not all languages are displayed)
* Location (lat/long is displayed, and polygons where available for regions)
* Current administrative/political hierarchy (with labels under consideration for a future version)
* Authorities (corresponding entries in other gazetteers)

This core metadata will form the spine of the gazetteer. This is data which EM Places will accept 'as is' without editing (though, as noted above, not everything indexed for search purposes will also be displayed in the individual place entry – GeoNames records  alternative names in many languages). The intent is that EM Places will be able to refresh this data at regular intervals (e.g. bi-annually) with minimal editorial oversight in order to benefit from corrections/additions upstream.

By contrast, _additional metadata_ is primarily further historical context and data (i.e. over and beyond core metadata) contributed to the gazetteer by individual researchers and projects, which will first need to be reviewed by EM Places editors. Examples of additional metadata would include data on historical calendars, historical hierarchies, bibliographic entries, and historical maps.

See also the section on 'Related Places' below, for an early discussion of what may become a third class of additional metadata.

### Uncertainties (TBD)

Data on calendars, and on historical hierarchies (only) will need to be optionally marked as any combination of 'Uncertain', 'Inferred', and 'Approximate'. TBD how to indicate this in the interface (possibly using a set of symbols, and possibly only in the associated 'Source' pop-up). We may also need to look into the use of 'Assumed' to handle our generic, fallback position for the effective date of the conversion to the Gregorian calendar in cases where no local specific information is available

## Preferred Place Name; alternative names

The default/preferred place name and its alternate names (toponyms) will come from the reference gazetteer but only a subset of unique names will be displayed. 

For example, while we can allow users to search for and find places using a Persian transliteration of a place (Opole: اوپوله) there is no need to display this particular transliteration in the list of alternative names. For the display list, alternative names will be drawn from a short list of major European languages and historical forms (i.e. Latin). Next, the list of alternative names will be compared with one or more additional gazetteers. From this these lists, a merged set of unique alternative names will finally be shown. This is to avoid having to list multiple, identical instances of e.g. 'Opole' for the many language transliterations supported by GeoNames.  

## Current Hierarchy

The administrative/political hierarchy ('polity') for a current place provided by the reference gazetteer(s). Note that GeoNames only provides data for ADM1, ADM2 etc. It does not attempt to label these as states, provinces, counties etc. However, Getty TGN does provide this information. Unfortunately, Getty and GeoNames sometimes disagree on the depth of the hierarchy making automatic matching of Getty labels to GeoNames hierarchies difficult. For this reason v1 will not attempt to match places with labels. We may return to this in a future revision of EM Places or perhaps make us of generic labels (as appears to have been done by Mapzen for their ['Who's on First'][13] open-access dataset – see, for example, [their entry for Opele][14]).  

By definition, a historical (i.e. former) place can’t display its administrative hierarchy here – instead, a placeholder message could refer the user to the section on ‘Historical Hierarchies’. Alternatively, we may use this area to highlight the period of the historical place

Further discussion is required on what will constitute core data for historical places. 

## Location

The representative center for a place displayed as decimal lat/long and degrees (image just shows decimal). It should be accompanied by a link allowing the URI to be copied as decimal lat/long on mouseclick. What will be copied should be revealed on mouseover. 

We will not attempt to override what GeoNames considers to be the representative point for a current place. For a historical place, an editor will decide where to locate the center (e.g. Vienna for the Habsburg Empire). TBD how to capture a representative historical location can changing over time. We also need to think about what to do if we were to have temporal polygons for historcal places.

## Citation

A simple means to represent the canonical URI as an academic citation, in several standard bibliographic formats and copy it on mouseclick for reuse. What will be copied should be revealed on mouseover, allowing the user to see in advance what the entry will look like in the different citation styles. We had initially considered using [BibTeX][15] as the generic bibliography interchange format. However, [RIS][16] is more current and may be more appropriate. [CSL][17] could provide a means to convert amongst formats.

## Permanent URI

This should be a short form. Timbuctoo generated permanent URI based on the custom domain for EM Places (probably emplaces.info). It should allow the URI to be copied to the clipboard on mouseclick. We need to decide if we additionally want to offer e.g. a DOI or an ARK identifier. Amongst the issues to consider are whether the metadata required by such a service is suited to us (and whether we can then employ the same service for EM People as well). See further:

ARK info: http://n2t.net/e/ark_ids.html (n2t,net is the resolver service) and DOI CataCite info: https://schema.datacite.org/meta/kernel-4.0/

## Name Attestations

Attestations are sourced instances of name variants of the preferred and alternative names in core data. For example, if a scholar finds a reference to Siena in a manuscript written 'Ciena' and (TBD via the editorial policy) this is not already listed as an alternative name in our reference gazetteers, then this toponym can be recorded here, along with the language, date, and source for the attestation. 

TBD structure for the source supporting the attestation. If possible, we will reuse the standard, basic format we have defined for bibliographic entries.

## Calendars

A simple visualization of the predominant calendars (Julian, Gregorian) in use between 1500 and 1800 at that place. This value will be pre-populated via a hierarchy of inherited calendars. So, for example, in the absence of any more specific information in use in a region, we will assume (but also make this clear in the interface) that the place transitioned, for example, from Julian to Gregorian in 1582 (the year of Gregory XIII's papal bull). If a place or set of places (such as a region) transitioned at a different date, then note this, and have all places under it inherit this (and override the default 1852 transition). If a more specific place such as a town transitioned in a different manner, then note this for that town, and override the regional transition etc.

We will not attempt to record variances from regional calendar use patterns at smaller scales such as individual towns. For example, we will not note as an exception or override if we are presented with a record of someone living in the town of Calais in 1632 (with the Gregorian calendar in use in France), writing to someone else in England in the Julian calendar. Our assumption is that the choice to use the Julian in this instance was dependant on the addresse and/or place of receipt (England did not change to the Gregorian calendar until 1752), not the place of sending.

TBD are labels or symbols for recording different variants of one calendar. For example, Julian calendar with January 1 as the start of the year and Julian with a March 25 start of year. The current plan is to specify this in parentheses after the name of the calendar. e.g. 'Julian (Mar 25)' means Julian calendar with the first day of the year on March 25. We'll need something similar for the most generic case where we have no data at all on the calendar and thus assume (for conversion purposes only) that the switch to the Gregorian took place on 15 October 1582.

## Related Places

In some cases, we may wish to capture information on places (current or historical) below the level of an inhabited place. For example, a set of buildings representing an institution (e.g. Christ Church College) or an individual building or locale (e.g. an inn, or a street). For these and similar kinds of places, especially if they are historical, we may have very little data – often not enough to create a full core data record. And even if we could, the format we've prepared for places is largely predicated on 'inhabited places'. It wouldn't be able to capture the kinds of properties relevant to a building (e.g. the name of the architect).

To accomodate this, we are proposing that this class of places be be grouped under the full/regular record of the place (conceptually, or spatially) enclosing it. Thus, for example, Christ Church College, would be included under the entry for Oxford etc. Such places will be listed in a separate tabular section of the full entry for the 'containing' place. For example, in a section titled (as in the current mockup) 'Related Places' (in a deliberate parallel to 'Related Resources' which point to external, related Linked Data resources not indexed by EM Places). 

Each entry in this table (following the example of GOV – e.g. for [Opele][7]) will includne a link leading to a separate page, where the specific metadata for that class of place will be shown. The idea is to allow contributors more freedom to share their metadata in a manner closer to the form in which it was collected. If a researcher, for example, wishes to share with EM Places, a large set of data on a set of streets in London, then we should try to accomodate the original data structure by permitting the use of 'street relevant' properties. Conversely, smaller and/or less common contributions may need to make do with the already list of available properties. That is to say, the decision to extend the list of properties to accomodate the needs of a contributor should be possible, but subject to prior agreement.

The current intent is for a simple wikidata-style interface where a contributor or editor selects a property from a preset list and enters a value. See [this blogpost][18] for an analogous example of how this could work. The tabular list (see [current mockup][1]) could, for example, consist of the follows:

| Place  | Type |  Relationship  |
| ------------- | ------------- |------------- |
| Our Lady of Sorrows and St. Adalbert  | Parish Church  |  PartOf  | 

The feature 'type' might be drawn from a pre-selected subset of the [Getty AAT][10] vocabulary (here, ['Parish Church'][19] and matched, where applicable, with the appropriate [GeoNames feature code][9] so that this this data becomes easier to integrate by other, less granular gazetteers.

TBA: Example data on St. Adalbert drawn from [National Heritage Board of Poland][20] website to be added to the [Opole sample RDF](/models/20180410-opole-example-data.ttl) file.

## Related Resources

A list of what we expect will be predominantly online, digital resources (for traditional scholarly references, contributors can make use of the bibliography section). Some of the URIs to these resources can be derived  automatically from our reference gazetteers (e.g. links to Wikipedia, WikiData, certain other gazetteers) but most of which will be suggested by contributors and confirmed by editors. 

This could also include dynamic links to resources which can be queried over an API for more information about a place in the gazetteer. The data would be polled and updated at an appropriate interval. For example, X number of letters were sent from this place, and Y number of letters were received at this place. 

## Bibliography

A list of bibliographic resources (predominantly offline, scholarly references). At minimum, an unstructured free text list would suffice for v.1. However, our assumption is that this can be a simply structured list, and with the ability to apply place tags to each entry, making it much easier for subsequent contributors to find and select existing bibliographic entries in a consistent manner. This helps avoid contributors working independently on different places (in e.g. the same region and period) repeatedly entering the same reference in different records, possibly in different formats. 

## Creators & Licenses

A listing (machine readable) of the Creator of the record (i.e. the person or organization which created the initial record), one or more subsequent Contributors, a credit line for the reference gazetteers, and a notice of the licenses in use. We will require two licenses – CC0 for the reference gazetteer (core data), and CC-BY (v4 or possibly higher – since changes will be logged in Timbuctoo) for the remaining, additional metadata.

## Export

A means to manually export the current record (only) in several common formats, currently assumed to be CSV, Excel, Turtle, GraphML, and GeoJSON. 

Note: GeoJSON is required for Pelagios compatibility via [LPIF format][11].

## Maps

The required (for current places) default map view will be an e.g. OpenStreetMap view using the location provided by core data. 

Optionally, it will be possible, via tabs, to view a finite number of (e.g. 4) historical, open-access geo-referenced and live-tiled maps of the place drawn from a provider such as https://www.davidrumsey.com or http://www.oldmapsonline.org or http://retromap.ru. Alternatively, one could substitute a single tile as a thumbnail for the historical map, and link this to the external historical map resource.

## Description

This field will initially be (semi?)-automatically populated with data from the Getty TGN and then further revised as needed by users/editors.

## Historical Hierarchies 

This section is best understood by looking at the draft [interface mockups][4].

Historical hierarchies show the historical administrative, ecclesiastical, judicial, and military hierarchies for both historical and current places. Initially, this will show the period a certain relationship existed. For example, from an administrative/political perspective, the Silesian town of Opole fell under the Duchy of Opole from 1281-1521. In each part of the hierarchy (with the precise mode of display TBD, for example via mouseover) a user will also be able to view the period of existence of each place entity (e.g. the Bohemian Crown existed from 1348 to 1918). Together, a set of dated entities, linked in hierarchial order by a set of dated relations, forms one (from a possible four kinds of) historical hierarchy. In the case of ecclesiastical hierarchies, an additional row of tabs will be needed to show what kind of hierarchy (e.g. what religion and/or confession) is being tracked. 

Further discussion is needed on the necessary editorial policies. We expect that administrative and ecclesiastical data will be easier to collect from contributors than judicial and military. As a result, displaying data on the latter two categories might not be included in the initial release.

## Feedback

A link to a simple comment form, referencing the current record and (if present) a link to the logged-in users profile, or else a mailto: link, referencing the current record (e.g. in the subject field).

### Info and Sources pop-ups

Many sections in the individual record display will include 'Info' and/or 'Sources' links. Clicking this could, as one possibility, show a pop-up with text on that section. In the case of Sources, this could include both an unstructured text area, and a structured bibliographic area. 
 

[1]:	/images/current_display.pdf
[2]:	https://github.com/culturesofknowledge/emplaces#feedback-and-comments
[3]:	https://www.uni-bamberg.de/histgeo/forschung/aktuell/
[4]:	/images
[5]:	http://emlo.bodleian.ox.ac.uk
[6]:	http://www.culturesofknowledge.org/?p=8455
[7]:	http://gov.genealogy.net/item/show/OPPELNJO80XQ
[8]:	https://omeka.org/s/
[9]:	http://www.geonames.org/export/codes.html
[10]:	https://www.getty.edu/research/tools/vocabularies/aat/
[11]:	http://linkedpasts.org
[12]: http://euratlas.com
[13]: https://github.com/whosonfirst
[14]: https://spelunker.whosonfirst.org/id/101752159/
[15]: http://www.bibtex.org
[16]: https://en.wikipedia.org/wiki/RIS_(file_format)
[17]: https://citationstyles.org
[18]: http://blogs.bodleian.ox.ac.uk/digital/2017/03/23/wikimedia-for-public-engagement/
[19]: http://vocab.getty.edu/page/aat/300108377
[20]: https://zabytek.pl/en/obiekty/opole-kosciol-parafialny-pw-matki-boskiej-bolesnej-i-sw-wojc

