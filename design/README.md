# Draft Feature Overview (Display View)

The informal descriptions below are intended to offer an overview of the different areas of functionality offered by the detail/display view for a single place record. The ‘Priority’ sub-heading is meant to track the relative importance of the feature as a development priority for the v.1 gazetteer.

It will be helpful read the text alongside images of the draft interface (PDF, PNG). Following this much which is described below will (or should!) already be self-explanatory.  

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

## Creator/Contributors/Provenance + License

**Priority:** Required

**Source:** Generated

An indication of the Creator of the record (i.e. the person or organization which created the initial record), the Initial Provenance (a credit line for the reference gazetteer which provided the core data for the record), and the Contributors (a comma separated list of names of the registered full-names of the contributors to the record). An indication of the license(s) under which data of this record can be released.

TBD is the need to list one (CC0) or possibly two licenses to account for core and Additional metatdata (CC0 + CC-BY). Probably this will need to be a single CC0 license.

## Maps

**Priority:** Required (current) + Optional (historical)

**Source:** Core Data (current) + Additional metadata (historical)

The required (for current places) default map view will be an e.g. OpenStreetMap view using the location provided by core data. 

Optionally, it will be possible, via tabs, to view a finite number (e.g. max. 4) of historical, open-access geo-referenced and live-tiled maps of the place drawn from a provider such as https://www.davidrumsey.com or http://www.oldmapsonline.org or http://retromap.ru. Alternatively, one could substitute a single tile as a thumbnail for the historical map, and link this to the external historical map resource.

## Historical Hierarchies

## Description

This field will initially be (manually) populated with data from the Getty TGN and then revised as needed by users. 

An "info" link to a pop-up provides a means to explain the function sourcing for its data. 

## Bibliography

## Related Resources

## Linkbacks

## Export

**Priority:** Required

**Source:** Generated

A means to manually export the current record (only) in a variety of formats, currently CSV, Excel, RDF-XML, GraphML, and GeoJSON.

## Share

**Priority:** Required

**Source:** Generated

A means to share a link to the current record on social media.

## Feedback

**Priority:** Required

**Source:** Generated

A means to be directed either to a comment form, referencing the current record, or else a simple mailto: link.

[1]:	https://www.uni-bamberg.de/histgeo/forschung/aktuell/