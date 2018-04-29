# Overview (Display View)

The draft description below offers an informal overview of the functionality of the gazetteer. It is best read alongside the [interface mockup][1] of the detail/display view for a typical place record. 

Note: The ‘Priority’ sub-headings are intended as a simple means for tracking the relative importance of individual features as development priorities for the v.1 gazetteer.

Please [get in touch with us][2] with your comments and feedback.

## Concepts and Principles

### Scope

EM Places is centered on the 16-18th centuries. As such, historical contexts and historical places recorded in the gazetteer will be limited to those whose existence clearly intersects this period.

### Sources and Contributors

The initial release of EM Places will be limited to c. 50-100 sample records serving as representative examples of full entries and and as a means to demonstrate the gazetteer's features to contributors. The records will be selected, in large part, from those places in [Early Modern Letters Online (EMLO)][5] with the greatest number of letters sent, received, or mentioned.

Over time, we expect to add records to EM Places in much the same way as we have grown EMLO's database – that is, slowly and incrementally, in a way which allows us to meet, wherever possible, the particular needs of our individual and institutional contributors. Although EM Places will draw on reference gazetteers for certain core data (e.g. locations) it is not designed to be a bulk aggregator of place data. Our emphasis will be on much fewer, but richer records, directed towards the needs of early modern scholars.  

### Current and Historical Place Entities

Our use of ‘current’ refers to still currently existing places and thus generally also  found in our reference gazetteers (GeoNames, Getty TGN). Consequently, a current place will also have a current administrative hierarchy (e.g. ADM1, ADM2, ADM3..) and a physical location (i.e. lat/long)  maintained for it outside of EM Places by our reference gazetteer(s).  

In contrast, a ‘historical’ place is no longer extant entity with a temporal validity (e.g. the Habsburg Monarchy, 1526-1804). EM Places will not attempt to capture spatial data on historical regions (i.e. polygons). Instead, we will either provide a single representative lat/long location (e.g. Vienna) or external link, where available to external resources/projects with the necessary expertise and data (e.g. to [FNZGIS][3] for Central/Eastern Europe).

Let's take, for example, the town of Opole in Poland. This is a currently extant place, and would be listed with alternative name and location data from our reference gazetteers. Amongst its alternative names (toponyms) is a historical name, Oppeln. EM Places will   record 'Oppeln' without attempting to contextualize it historically. This is because our alternative name data for current places will come from reference gazetteers which themselves typically do not offer this data (see section below on Core vs. Additional Metadata).

However, the record for a current place can optionally include additional historical information and contexts, such as data on historical calendar use, further attestations of toponyms, or various kinds of hierarchies associated with it (e.g. ecclesiastical, offering data on parishes, dioceses etc.). These additional contexts can be shared with EM Places by individual researchers and projects. When this is itself a place (e.g. the Bohemian Crown, 1490-1742) it is recorded in the gazetteer as a separate, historical place entity, linked to the current places with which it is associated. For example, in the period 1490-1521 the town of Opole (current place) was a part of the (historical place) 'Duchy of Opole' which itself was part of the (historical place) Governorate of the Duchy of Silesia etc. culminating in the (historical place) 'Holy Roman Empire'. 

In summary, all 'current places' in EM Places will have a current hierarchy and location (taken from reference gazetteers) and, optionally, can be associated with several more 'historical places' and contexts (e.g. calendars), contributed to the gazetteer by scholars and projects. 

Ultimately, the intent of EM Places (and alongside it, EM People, and EM Dates) is to provide a series of [Linked Open Data resources for computable, historical entities][6].

### Core and Additional Metadata

There are two main sources for data in EM Places. _Core metadata_ is periodically drawn by API from reference gazetteers (currently: GeoNames, Getty TGN) and will be comprised of:

* Preferred Place Name
* Alternative Names (all entries are indexed, not all languages are displayed)
* Location (lat/long is displayed, and polygons where available for regions)
* Current administrative/political hierarchy and labels
* Related Resources (corresponding entries in other gazetteers)

This core metadata will form the spine of the gazetteer. This is data which EM Places will accept 'as is' without editing (though, as noted above, not everything indexed for search purposes will also be displayed in the individual place entry – GeoNames records  alternative names in many languages). The intent is that EM Places will be able to refresh this data at regular intervals (e.g. bi-annually) with minimal editorial oversight in order to benefit from corrections/additions upstream.

By contrast, _additional metadata_ is primarily further historical context and data (i.e. over and beyond core metadata) contributed to the gazetteer by individual researchers and projects, which will need to be reviewed by EM Places editors. Examples of additional metadata would include data on historical calendars, historical hierarchies, bibliographic entries, and historical maps.

See also the section on 'Includes' below, for an early discussion of what may need to become a third class of metadata (or a sub-class of 'additional). 

## Preferred Place Name; alternative names

**Priority:** High

**Source:** Core Data

The default/preferred place name and its alternate names will come from the reference gazetteers. All alternative names and their labels will be stored and indexed but only some will be displayed. 

For example, while we will allow users to search for and find places using a Persian transliteration of a place (Opole: اوپوله) there is no need to display this particular transliteration in the list of alternative names. For the display list, alternative names will be drawn from a short list of major European languages and historical forms (i.e. Latin). Next, the list of alternative names will be compared with one or more additional gazetteers. From this these lists, a merged set of unique alternative names will finally be shown. This is to avoid having to list multiple, identical instances of e.g 'Opole' for the many language transliterations supported by GeoNames. The language label(s) for an alternative name should be revealed on mouseover.

## Current Hierarchy

**Priority:** High

**Source:** Core Data

The administrative/political hierarchy for a current place provided by the reference gazetteer. Note that GeoNames only provides data for ADM1, ADM2 etc. It does not attempt to label these as states, provinces, counties etc. However, Getty TGN does provide this information. Therefore, when these are imported, an attempt should be made to automatically match these, and flag them to an editor for subsequent review. 

By definition, a historical (i.e. former) place can’t display its administrative hierarchy here – instead, a placeholder message will refer the user to the section on ‘Historical Hierarchies’. 

Further discussion is required on what will constitute core data for historical places. 

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

Attestations are sourced instances of name variants of the preferred and alternative names in core data. For example, if a scholar finds a reference to Siena in a manuscript written 'Ciena' and (TBD via the editorial policy) this is not already listed as an alternative name in our reference gazetteers, then this toponym can be recorded here, along with the language, date, and source for the attestation. 

TBD structure for the source supporting the attestation. If possible, we will reuse the standard, basic format we have defined for bibliographic entries.

## Calendars

**Priority:** High (form of implementation TBD)

**Source:** Additional metadata

A visualization of the predominant calendars (Julian, Gregorian) in use between 1500 and 1800 at that place. This value will be pre-populated via a hierarchy of inherited calendars. So, for example, in the absence of any more specific information in use in a region, we will assume (but also make this clear in the interface) that the place transitioned, for example, from Julian to Gregorian in 1582 (the year of Gregory XIII's papal bull). If a place or set of places (such as a region) transitioned at a different date, then note this, and have all places under it inherit this (and override the default 1852 transition). If a more specific place such as a town transitioned in a different manner, then note this for that town, and override the regional transition etc.

We will not attempt to record variances from regionbal calendar use patterns at smaller scales such as individual towns. For example, we will not note as an exception or override if we are presented with a record of someone living in the town of Calais in 1632 (with the Gregorian calendar in use in France), writing to someone else in England in the Julian calendar. Our assumption is that the choice to use the Julian in this instance was dependant on the addresse and/or place of receipt (England did not change to the Gregorian calendar until 1752), not the place of sending.

## Includes

**Priority:** High (form of implementation TBD)

**Source:** Additional metadata (TBD)

In some cases, we may wish to capture information on places (current or historical) below the level of an inhabited place. For example, a set of buildings representing an institution (e.g. Christ Church College) or an individual building or locale (e.g. an inn, or a street). For these and similar kinds of places, especially if they are historical, we may have very little data – perhaps not even enough to create a full core data record. 

To accomodate this, we are proposing that this class of places could be grouped under the full/regular record of the place (conceptually, or spatially) enclosing it. Thus, for example, Christ Church College, would be included under the entry for Oxford etc. Such places will be listed under a separate section in the full entry for the 'containing' place as separate links. For example, in a section titled (as in the current mockup) 'Includes'. 

Following such a link will lead to a separate page, where the metadata for that place will be shown. The intent is to allow contributors to EM Places to offer metadata on places in a structure close to the form in which it was collected. If a researcher, for example, wishes to share with EM Places, data on a set of streets in London, then we should try to accomodate this data structure as far as feasible. 

Further discussion is required.


## Related Resources

**Priority:** High

**Source:** Core data + additional metadata

A list of what we expect will be predominantly online resources (for traditional scholarly references, contributors can make use of the bibliography section) at least some of which will be derived  automatically from our reference gazetteers (e.g. links to Wikipedia, WikiData, certain other gazetteers) but most of which will be manually entered. 

## Linkbacks

**Priority:** Medium (form of implementation TBD)

**Source:** Core data + additional metadata

A list of dynamic links to resources which can be queried programmatically for more information about a place in the gazetteer. The data would be polled and updated at an appropriate interval. For example, X number of letters were sent from this place, and Y number of letters were received at this place. 

If dynamic links can’t be implemented in v.1, then periodically refreshed, static data from a small set of important sources is acceptable as well.

## Bibliography

**Priority:** Medium (form of implementation TBD)

**Source:** Core data + additional metadata

A list of bibliographic resources (predominantly offline, scholarly references). At minimum, an unstructured free text list would suffice for v.1. However, our assumption is that this can be a simply structured list, and with the ability to apply place tags to each entry, making it much easier for subsequent contributors to find and select existing bibliographic entries in a consistent manner. This helps avoid contributors working independently on different places (in e.g. the same region and period) repeatedly entering the same reference in different records, possibly in different formats. 

## Creator/Contributors/License

**Priority:** High

**Source:** Generated

A listing (machine readable) of the Creator of the record (i.e. the person or organization which created the initial record), one or more subsequent Contributors, a credit line for the reference gazetteers, and a notice of the licenses in use. We will require two licenses – CC0 for the reference gazetteer (core data), and CC-BY (v4 or possibly higher – since changes will be logged in Timbuctoo) for the remaining, additional metadata.

## Export

**Priority:** High (form of implementation TBD)

**Source:** Generated

A means to manually export the current record (only) in several common formats, currently assumed to be CSV, Excel, Turtle, GraphML, and GeoJSON-LD. 

## Maps

**Priority:** High (current) + Medium/Low (historical)

**Source:** Core Data (current) + Additional metadata (historical)

The required (for current places) default map view will be an e.g. OpenStreetMap view using the location provided by core data. 

Optionally, it will be possible, via tabs, to view a finite number of (e.g. 4) historical, open-access geo-referenced and live-tiled maps of the place drawn from a provider such as https://www.davidrumsey.com or http://www.oldmapsonline.org or http://retromap.ru. Alternatively, one could substitute a single tile as a thumbnail for the historical map, and link this to the external historical map resource.

## Description

**Priority:** High

**Source:** Additional metadata 

This field will initially be (semi?)-automatically populated with data from the Getty TGN and then further revised as needed by users/editors.

## Historical Hierarchies

**Priority:** High (form of implementation TBD)

**Source:** Additional metadata 

This section is best understood by looking at the draft [interface mockups][4].

Historical hierarchies show the historical administrative, ecclesiastical, judicial, and military hierarchies for both historical and current places. Initially, this will show the period a certain relationship existed. For example, from an administrative/political perspective, the Silesian town of Opole fell under the Duchy of Opole from 1281-1521. In each part of the hierarchy (with the precise mode of display TBD, for example via mouseover) a user will also be able to view the period of existence of each place entity (e.g. the Bohemian Crown existed from 1348 to 1918). Together, a set of dated entities, linked in hierarchial order by a set of dated relations, forms one (from a possible four kinds of) historical hierarchy. In the case of ecclesiastical hierarchies, an additional row of tabs will be needed to show what kind of hierarchy (e.g. what religion and/or confession) is being tracked. 

Further discussion is needed on the necessary editorial policies. We expect that administrative and ecclesiastical data will be easier to collect from contributors than judicial and military. 

## Feedback

**Priority:** High

**Source:** Generated

A link to a simple comment form, referencing the current record and (if present) a link to the logged-in users profile, or else a mailto: link, referencing the current record (e.g. in the subject field).

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

