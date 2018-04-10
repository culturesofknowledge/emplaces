# Overview (Display View)

The descriptions below are best read alongside [images](/images) of the current draft interface. 

The following draft descriptions offer an overview of the different areas of functionality offered by the detail/display view for a single place record. The ‘Priority’ sub-heading is meant to track the relative importance of the feature as a development priority for the v.1 gazetteer.

Please [get in touch with us][https://github.com/culturesofknowledge/emplaces#feedback-and-comments] with your comments and criticism – we value your feedback!

## Basic Concepts

### Core and Additional Metadata

There are two main sources for data in EM Places. _Core metadata_ is periodically drawn by API from the reference gazetteer (currently: GeoNames) and will be comprised of:

* Preferred Place Name
* Alternative Names (all entries are indexed, not all are displayed)
* Location (lat/long but also including polygons where available for regions)
* Current administrative/political hierarchy (GeoNames)
* Related Resources (TBD: links to other gazetteers)

Core metadata will form the spine of the gazetteer. This is data which EM Places will accept 'as is' and will not be editing. It can be replaced at regular intervals (e.g. quarterly) with minimal oversight to benefit from corrections/additions upstream.

By contrast, _additional metadata_ is primarily scholary and historical data (over and beyond core metadata) which will be provided and revised by CofK staff and contributors. 

### Current and Historical Places

The term ‘current’ refers to a currently existing, physical place and as such will generally also be found in the reference gazetteer. Consequently, a current place will also have a current administrative hierarchy (e.g. ADM1, ADM2, ADM3..) and a physical location (lat/long) maintained for it by the reference gazetteer.  

A ‘historical’ place will generally be a former (hence historical) place with a temporal validity (e.g. the Habsburg Monarchy, 1526-1804). Though, in principle, some historical places could be additionally be described as an aggregation of one or more physical regions, EM Places will not attempt to capture this form of location data (i.e. polygons for historical regions). Instead, we will link to external resources/projects with the necessary expertise in this area (e.g. to [FNZGIS][1] for Central/Eastern Europe). 

Consequently, a current place (e.g. Augsburg) will have a current (GeoNames derived) administrative hierarchy as well as several historical hierarchies associated with it (to account, for example, for when Augsburg was part of the Holy Roman Empire). However, a historical place (e.g. the Holy Roman Empire) while being part of (many) other historical hierarchies will never have a current hierarchy.

### Workflow

**Priority:** Required

**Source:** Core Data  (unless no reference gazetteer ID is present).

The basic workflow for a new record will request the user to first identify the place in the reference gazetteer (GeoNames) and to enter its ID in EM Places. EM Places will then pull the relevant core metadata from GeoNames and use it to populate the draft record in a staging area. If the place cannot be found in the reference gazetteer, a new record cannot be created until a user with appropriate privileges has confirmed that no GeoNames ID is available. Following this, a new record can be created in the staging area with custom core metadata. After this, the record can be amended as usual with additional metadata. 

We expect that the vast majority of place names will be found in GeoNames. However, core data for all historical places (e.g. Bohemian Crown) and most buildings (e.g. Christ Church, Oxford) will need to be created by hand. 

A workflow for supporting bulk imports via e.g. CSV files will also be provided. 

## Place Names

**Priority:** Required

**Source:** Core Data

The default/preferred place name and its alternate names will come from the reference gazetteer. All alternative names and their labels will be stored and indexed but only some will be displayed. For example, while we will allow users to find places using e.g. a Chinese transliteration there may be no need to display this transliteration in the list of alternative names. For the display list, alternative names from a short list of major European languages and historical forms (i.e. Latin) should suffice. Next, the list of alternative names will be compared with one or more additional gazetteers (preferably Getty TGN). From these, a merged set of unique alternative names will be shown (to avoid havinh to list e.g. Rome, Rome, Rome for each GeoName supported language). The sources for the alternative names will be recorded and made accessible.

## Current Hierarchy

**Priority:** Required

**Source:** Core Data

The administrative/political hierarchy for a current place provided by the reference gazetteer. By definition, a historical (i.e. former) place can’t display its administrative hierarchy here – instead, a placeholder message will refer the user to the section on ‘Historical Hierarchies’. 

## Location

**Priority:** Required

**Source:** Core Data

The representative center point for a place displayed as decimal lat/long and degrees (image just shows decimal). It should be accompanied by a button allowing the URI to be copied to the clipboard on mouseclick.

## Citation

**Priority:** Required

**Source:** Generated

A simple means to represent the canonical URI as an academic citation, in several standard formats and copy it on mouseclick for reuse. 

## Permanent URI

**Priority:** Required

**Source:** Generated

This should be a short form permanent URI based on the custom domain for EM Places (e.g. emplaces.info). It should be accompanied by a button allowing the URI to be copied to the clipboard on mouseclick.

## Name Attestations

**Priority:** Required

**Source:** Additional metadata

Attestations are sourced instances of name variants of the preferred and alternative names in core data. For example, if a scholar finds a reference to Siena in a manuscript written 'Ciena' and (TBD via the editorial policy) this form is not already listed as an alternative name, then this toponym can be recorded here, along with the language, date, and source for the attestation. 

TBD structure for the source supporting the attestation. 

## Calendars

**Priority:** Required

**Source:** Additional metadata

A visualization of the predominant calendars (Julian, Gregorian) in use between 1500 and 1800 at that place. One possibility for realizing this is via a hierarchy of inherited calendars. So, for example, in the absence of any more specific information, assume (but also make this clear in the interface) that the place transitioned from Julian to Gregorian in 1582. If a place or set of places (such as a region) transitioned at a different date, then note this, and have all places under it inherit this (and override the default 1852 transition). If a more specific place such as a town transitioned in a different manner, then note this for that town, and override the regional transition etc.

Much remains to be discussed. Given the sparsity of data for these  transitions and the great danger of generalizing it may be useful to supplement (or replace?) the overview visualization with something like ‘Calendar Attestations’ to allow individual cases to be recorded. 

## Related Resources

**Priority:** Required

**Source:** Core data + additional metadata

A list of predominantly online resources and references (for traditional scholarly resources, contributors can make use of the Bibliography) some of which will be derived from core data (e.g. links to Wikipedia, WikiData, certain other gazetteers) but most of which will be manually entered. 

## Linkbacks

**Priority:** Required (form of implementation optional)

**Source:** Core data + additional metadata

A list of dynamic links to resources which can be queried programmatically for more information about a place. The data would be polled and updated at an appropriate interval. For example, X number of letters were sent from this place, and Y number of letters were received at this place. 

If dynamic links can’t be implemented in v.1, then periodically refreshed, static data from a small set of important sources is acceptable as well.

## Bibliography

**Priority:** Required (form of implementation optional)

**Source:** Core data + additional metadata

A list of bibliographic resources (predominantly offline, scholarly). At minimum, an unstructured free text list would suffice for v.1. Ideally, a structured list, with the ability to apply place tags to each entry, so making it easier for subsequent contributors to find and select existing bibliographic entries in a consistent manner. This is intended to help avoid contributors working on different places in e.g. the same region and period repeatedly entering the same reference, possibly in different formats. 

## Creator/Contributors/License

**Priority:** Required

**Source:** Generated

An indication of the Creator of the record (i.e. the person or organization which created the initial record), one or more subsequent Contributors, a credit line for the reference gazetteer, and a notice of the licenses in use. We will require two licenses – CC0 for the reference gazetteer (core data), and CC-BY (v4 or possibly higher – since changes will be logged in Timbuctoo) for the remaining, additional metadata.

## Export

**Priority:** Required (form of implementation optional)

**Source:** Generated

A means to manually export the current record (only) in several common formats, currently thought to be CSV, Excel, Turtle, GraphML, and GeoJSON-LDT. The exact list will be dependant on the capabilities of the infrastructure at launch and (in the case of GeoJSON-LDT) whether this standard has been settled yet (if not, the broader standard, GeoJSON-LD can be used instead).

## Maps

**Priority:** Required (current) + Optional (historical)

**Source:** Core Data (current) + Additional metadata (historical)

The required (for current places) default map view will be an e.g. OpenStreetMap view using the location provided by core data. 

Optionally, it will be possible, via tabs, to view a finite number (e.g. max. 4) of historical, open-access geo-referenced and live-tiled maps of the place drawn from a provider such as https://www.davidrumsey.com or http://www.oldmapsonline.org or http://retromap.ru. Alternatively, one could substitute a single tile as a thumbnail for the historical map, and link this to the external historical map resource.

## Description

**Priority:** Required

**Source:** Additional metadata 

This field will initially be (semi?)-automatically populated with data from the Getty TGN and then further revised as needed by users/editors.

## Historical Hierarchies

**Priority:** Required (form of implementation optional)

**Source:** Additional metadata 

This section is best understood by looking at the draft [interface mockups](/images).

Historical hierarchies show the historical administrative, ecclesiastical, judicial, and military hierarchies for both historical and current places. Initially, this will be limited to showing the period a certain relationship existed. For example, from an administrative/political perspective, the Silesian town of Opole fell under the Duchy of Opole from 1281-1521. In each part of the hierarchy (with the precise mode of display TBD) a user will also be able to view the period of existence of each place entity (e.g. the Bohemian Crown existed from 1348 to 1918). Together, a set of dated entities, linked in hierarchial order by a set of dated relations, forms one (from a possible four kinds of) hierarchy. In the case of ecclesiastical hierarchies, an additional row of tabs will be needed to show what kind of hierarchy (e.g. what confession) is being tracked. 

Several aspects of historical hierarchies remain to be discussed, including, for example, how to establish an editorial policy for what could often be subjective or uncertain start/end dates for a relation or an entity.

## Feedback

**Priority:** Required

**Source:** Generated

A link to a simple comment form, referencing the current record and (if present) a link to the logged-in users profile, or else a simple mailto: link, referencing the current record (e.g. in the subject field).

## Share

**Priority:** Required

**Source:** Generated

A means to share a link to the current record on social media. If possible, this should be implemented in a way which does not promote cross-site tracking of visitors to the gazetteer.

[1]:	https://www.uni-bamberg.de/histgeo/forschung/aktuell/
