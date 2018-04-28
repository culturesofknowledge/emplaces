# Overview (Display View)

The draft description below offers an informal overview of the functionality of the gazetteer. It is best read alongside the [interface mockup][1] of the detail/display view for a typical place record. 

Note: The ‘Priority’ sub-headings are intended as a simple means for tracking the relative importance of individual features as development priorities for the v.1 gazetteer.

Please [get in touch with us][2] with your comments and feedback.

## Concepts and Principles

### Scope

EM Places is focused on the 16-18th centuries. As such, additional historical contexts (e.g. regional calendars) and historical place entities (e.g. parishes and dioceses) will be limited to those which intersect this period. 

### Sources and Contributors

The initial (pilot) release of EM Places will be limited to c. 50-100 sample records, to serve as representative examples of full entries and demonstrate the gazetteer's features. The records will be selected, in large part, from those places in [Early Modern Letters Online (EMLO)][5] with the greatest number of letters sent, received, or mentioned.

Over time, we expect to add further records to EM Places in much the same way as we have grown EMLO's database – that is, slowly and incrementally, in a way which allows us to meet, wherever possible, the particular needs of our individual and institutional contributors. Although EM Places will draw on reference gazetteers for certain core data (e.g. location data) it will not be a large scale aggregator of place data. Our emphasis will be on far fewer, but richer records, directed at the needs of early modern scholars. 
We expect that, once complete, EM Places will hold perhaps 6,000 to 10,000 place entities (current and historical).  

### Current and Historical Place Entities

The term ‘current’ refers to still currently existing places and as such will generally also be found in our reference gazetteers (e.g. Oxford, U.K.). Consequently, a current place will also have a current administrative hierarchy (e.g. ADM1, ADM2, ADM3..) and a physical location (i.e. lat/long) which  maintained for it outside of EM Places by a reference gazetteer(s).  

In contrast, a ‘historical’ place is no longer extant (hence historical) entity with a defined temporal validity (e.g. the Habsburg Monarchy, 1526-1804). EM Places will not attempt to capture spatial data on historical regions (i.e. polygons). Instead, we will either provide a single representative lat/long location (e.g. Vienna) or external link, where available to external resources/projects with the necessary expertise and data (e.g. to [FNZGIS][3] for Central/Eastern Europe).

Let's take, for example, the town of Opole in Poland. This is a currently extant place, and would be listed with alternative name and location data from our reference gazetteers (at present, GeoNames and Getty TGN). Amongst its alternative names (toponyms) will be a historical name, Oppeln. EM Places will merely record the name as an attribute of the main entry on Opole, since the alternative name data will have come from a reference gazetteer (GeoNames) which does not provide further historical context for alternative names.

Optionally, the record for a current place can also include additional historical information and contexts, such as data on historical calendar use, further attestations of toponyms, or various kinds of hierarchies associated with it (e.g. ecclesiastical, offering data on parishes, dioceses etc.). These additional contexts can be shared with EM Places by individual researchers and projects. When this additional data is itself a place (e.g. the Bohemian Crown, 1490-1742) then this place is recorded in EM Places as separate, historical place entity, linked to the current places with which it is associated.

Thus, all 'current places' in EM Places will have a current hierarchy and location (taken from reference gazetteers) and, optionally, can be associated with several more early modern 'historical places', contributed by individual researchers and projects. 

The larger intent of EM Places (and alongside it, EM People, and EM Dates) is to provide a series of [Linked Open Data resources for computable, historical entities][6].

### Core and Additional Metadata

There are two main sources for data in EM Places. _Core metadata_ is periodically drawn by API from reference gazetteers (currently: GeoNames, Getty TGN) and will be comprised of:

* Preferred Place Name
* Alternative Names (all entries are indexed, not all languages are displayed)
* Location (lat/long is displayed, and polygons where available for regions)
* Current administrative/political hierarchy and labels
* Related Resources (corresponding entries in other gazetteers)

This core metadata will form the spine of the gazetteer. This is data which EM Places will accept 'as is' without editing (though, as noted above, not everything indexed for search purposes will also be displayed in the individual place entry – GeoNames records  alternative names in many languages). The intent is that EM Places will be able to refresh this data at regular intervals (e.g. bi-annually) with minimal editorial oversight in order to benefit from corrections/additions upstream.

By contrast, _additional metadata_ is primarily further historical context and data (i.e. over and beyond core metadata) contributed to the gazetteer by individual researchers and projects, which will need to be reviewed by EM Places editors. Examples of additional metadata would include data on historical calendars, historical hierarchies, bibliographic entries, and historical maps.

## Preferred Place Name; alternative names

**Priority:** High

**Source:** Core Data

The default/preferred place name and its alternate names will come from the reference gazetteers. All alternative names and their labels will be stored and indexed but only some will be displayed. For example, while we will allow users to search for and find places using a Chinese transliteration there may be no need to display this transliteration in the list of alternative names. For the display list, alternative names from a short list of major European languages and historical forms (i.e. Latin) should suffice. Next, the list of alternative names will be compared with one or more additional gazetteers (preferably Getty TGN). From these, a merged set of unique alternative names will be shown. This is to avoid having to list multiple, identical instances of 'Rome' for each of the many languages supported by GeoNames. The (typically) language label(s) for an alternative name should be revealed on mouseover.

## Current Hierarchy

**Priority:** High

**Source:** Core Data

The administrative/political hierarchy for a current place provided by the reference gazetteer. Note that GeoNames only provides data for ADM1, ADM2 etc. It does not attempt to label these as states, provinces, counties etc. However, Getty TGN does provide this information. Therefore, when these are imported, an attempt should be made to automatically match these, and flag them to an editor for subsequent review. 

By definition, a historical (i.e. former) place can’t display its administrative hierarchy here – instead, a placeholder message will refer the user to the section on ‘Historical Hierarchies’. 

Further discussion is required on what should constitute core data for historical places. 

## Location

**Priority:** High

**Source:** Core Data

The representative center point for a place displayed as decimal lat/long and degrees (image just shows decimal). It should be accompanied by a link allowing the URI to be copied as decimal lat/long on mouseclick. What will be copied should be revealed on mouseover. 

We will not attempt to override what GeoNames considers to be the representative point for a current place. 

## Citation

**Priority:** High

**Source:** Generated

A simple means to represent the canonical URI as an academic citation, in several standard bibliographic formats and copy it on mouseclick for reuse. What will be copied should be revealed on mouseover, allowing the user to see in advance what the entry will look like in the different citation styles.

## Permanent URI

**Priority:** High

**Source:** Generated

This should be a short form permanent URI based on the custom domain for EM Places (emplaces.info). It should allow the URI to be copied to the clipboard on mouseclick and reveal what will be copied on mouseover.

## Name Attestations

**Priority:** High

**Source:** Additional metadata

Attestations are sourced instances of name variants of the preferred and alternative names in core data. For example, if a scholar finds a reference to Siena in a manuscript written 'Ciena' and (TBD via the editorial policy) this form is not already listed as an alternative name, then this toponym can be recorded here, along with the language, date, and source for the attestation. 

TBD structure for the source supporting the attestation. 

## Calendars

**Priority:** High (form of implementation TBD)

**Source:** Additional metadata

A visualization of the predominant calendars (Julian, Gregorian) in use between 1500 and 1800 at that place. One possibility for realizing this is via a hierarchy of inherited calendars. So, for example, in the absence of any more specific information, assume (but also make this clear in the interface) that the place transitioned from Julian to Gregorian in 1582. If a place or set of places (such as a region) transitioned at a different date, then note this, and have all places under it inherit this (and override the default 1852 transition). If a more specific place such as a town transitioned in a different manner, then note this for that town, and override the regional transition etc.

Much remains to be discussed. Given the sparsity of data for these  transitions and the great danger of generalizing it may be useful to supplement (or replace?) the overview visualization with something like ‘Calendar Attestations’ to allow individual cases to be recorded. 

## Includes

**Priority:** High (form of implementation TBD)

**Source:** Additional metadata

TBA


## Related Resources

**Priority:** High

**Source:** Core data + additional metadata

A list of predominantly online resources and references (for traditional scholarly resources, contributors can make use of the Bibliography) some of which will be derived from core data (e.g. links to Wikipedia, WikiData, certain other gazetteers) but most of which will be manually entered. 

## Linkbacks

**Priority:** Medium (form of implementation TBD)

**Source:** Core data + additional metadata

A list of dynamic links to resources which can be queried programmatically for more information about a place. The data would be polled and updated at an appropriate interval. For example, X number of letters were sent from this place, and Y number of letters were received at this place. 

If dynamic links can’t be implemented in v.1, then periodically refreshed, static data from a small set of important sources is acceptable as well.

## Bibliography

**Priority:** Medium (form of implementation TBD)

**Source:** Core data + additional metadata

A list of bibliographic resources (predominantly offline, scholarly). At minimum, an unstructured free text list would suffice for v.1. Ideally, a structured list, with the ability to apply place tags to each entry, so making it easier for subsequent contributors to find and select existing bibliographic entries in a consistent manner. This is intended to help avoid contributors working on different places in e.g. the same region and period repeatedly entering the same reference, possibly in different formats. 

## Creator/Contributors/License

**Priority:** High

**Source:** Generated

An indication of the Creator of the record (i.e. the person or organization which created the initial record), one or more subsequent Contributors, a credit line for the reference gazetteer, and a notice of the licenses in use. We will require two licenses – CC0 for the reference gazetteer (core data), and CC-BY (v4 or possibly higher – since changes will be logged in Timbuctoo) for the remaining, additional metadata.

## Export

**Priority:** High (form of implementation TBD)

**Source:** Generated

A means to manually export the current record (only) in several common formats, currently thought to be CSV, Excel, Turtle, GraphML, and GeoJSON-LDT. The exact list will be dependant on the capabilities of the infrastructure at launch and (in the case of GeoJSON-LDT) whether this standard has been settled yet (if not, the broader standard, GeoJSON-LD can be used instead).

## Maps

**Priority:** High (current) + Medium/Low (historical)

**Source:** Core Data (current) + Additional metadata (historical)

The required (for current places) default map view will be an e.g. OpenStreetMap view using the location provided by core data. 

Optionally, it will be possible, via tabs, to view a finite number (e.g. max. 4) of historical, open-access geo-referenced and live-tiled maps of the place drawn from a provider such as https://www.davidrumsey.com or http://www.oldmapsonline.org or http://retromap.ru. Alternatively, one could substitute a single tile as a thumbnail for the historical map, and link this to the external historical map resource.

## Description

**Priority:** High

**Source:** Additional metadata 

This field will initially be (semi?)-automatically populated with data from the Getty TGN and then further revised as needed by users/editors.

## Historical Hierarchies

**Priority:** High (form of implementation TBD)

**Source:** Additional metadata 

This section is best understood by looking at the draft [interface mockups][4].

Historical hierarchies show the historical administrative, ecclesiastical, judicial, and military hierarchies for both historical and current places. Initially, this will be limited to showing the period a certain relationship existed. For example, from an administrative/political perspective, the Silesian town of Opole fell under the Duchy of Opole from 1281-1521. In each part of the hierarchy (with the precise mode of display TBD) a user will also be able to view the period of existence of each place entity (e.g. the Bohemian Crown existed from 1348 to 1918). Together, a set of dated entities, linked in hierarchial order by a set of dated relations, forms one (from a possible four kinds of) hierarchy. In the case of ecclesiastical hierarchies, an additional row of tabs will be needed to show what kind of hierarchy (e.g. what confession) is being tracked. 

Several aspects of historical hierarchies remain to be discussed, including, for example, how to establish an editorial policy for what could often be subjective or uncertain start/end dates for a relation or an entity.

## Feedback

**Priority:** High

**Source:** Generated

A link to a simple comment form, referencing the current record and (if present) a link to the logged-in users profile, or else a simple mailto: link, referencing the current record (e.g. in the subject field).

## Share

**Priority:** High

**Source:** Generated

A means to share a link to the current record on social media. If possible, this should be implemented in a way which does not promote cross-site tracking of visitors to the gazetteer.

[1]:	/images/display.pdf
[2]:	https://github.com/culturesofknowledge/emplaces#feedback-and-comments
[3]:	https://www.uni-bamberg.de/histgeo/forschung/aktuell/
[4]:	/images
[5]:	http://emlo.bodleian.ox.ac.uk
[6]:	http://www.culturesofknowledge.org/?p=8455

