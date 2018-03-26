# Display Features

## Place Name

**Category:** Required

**Source:** Core Data

The default/preferred place name and its alternate names come from the reference gazetteer. All alternative names and their labels should be stored and indexed but only some will be displayed. For example, while we can silently allow users to find places using a Chinese transliteration there is no need to display the transliteration in the list of alternative names. For these, names in a TBD list of major European languages and historical forms will suffice.

It will be useful to compare the list of alternative names in GeoNames with those in the Getty TGN. If these often diverge, then a merged set under the above criteria should be shown. 

## Canonical URI

**Category:** Required

**Source:** Generated

This should be a short form permanent URI based on the custom domain for EM Places (e.g. emplaces.info). It should be accompanied by a javascript link to allow the URI to be copied to the clipboard on mouseclick.

## Latitude/Longitude

**Category:** Required

**Source:** Core Data

The representative center point for a place displayed as decimal lat/long and degrees (image just shows decimal). It should be accompanied by a javascript link to allow the URI to be copied to the clipboard on mouseclick. 

## Citation

**Category:** Required

**Source:** Generated

A means to represent and make available for copying to the clipboard the canonical URI as an academic citation, in several standard formats. Other than in the image, it will better to show the citation format, so that users can have faith that it is being represented correctly. In other words, a list of major academic citation formats which shows the full citation on mouseclick. BibTex will not be needed here, since this is a single citation.

It may be possible to combine this with the canonical URI.

## Attestations

**Category:** Required

**Source:** Extended Data

Attestations are sourced instances of name variants to the preferred and alternative names in core data. For example, if a scholar finds a reference to Siena in a manuscript written as 'Ciena' and (TBD via editorial policy) this form is not already listed as an alternative name, then this data point can be recorded here, along with the language, date, and source for the attestation. 

TBD how to represent the attestation source. Most will be named links, but others may need to refer to other kinds of sources. 

An "info" link to a pop-up provides a means to explain the function of the attestation.

## Maps

**Category:** Required + Optional

**Source:** Core Data + Extended Data

The required default map view will be an e.g. OpenStreetMap or Google etc. current view of a region surrounding the place with a flag dropped on the location using core data. 

Optionally, it will be possible, via tabs, to view a small, finite number (e.g. 3) additional but historical, open-access geo-referenced maps of the region drawn from a provider such as https://www.davidrumsey.com or http://www.oldmapsonline.org or http://retromap.ru. It may be necessary, for space reasons, to open the historical maps in a new window/tab.

TBD: Explore a library such as http://leafletjs.com which can display both vector and image tiled maps, or else (just for tiled maps) the IIIF compatible http://www.georeferencer.com. 

An "info" link to a pop-up provides a means to explain the function of the widget. However, TBD is whether a similar, but separate means will be needed to indicate the sourcing for in particular the historical maps, perhaps via a "sources" link. 

## Calendars

**Category:** Required

**Source:** Extended Data

A simple visualization of the calendars in use between 1500 and 1800. In the initial release, the calendars potentially shown here will be (TBD) the Julian O.S., Julian N.S., Gregorian, Swedish, Ottoman and Hebrew. Dates will be expressed in full years, with only a simplified indication of uncertainty (e.g. c. 1683).

An "info" link to a pop-up provides a means to explain the function of the widget. However, TBD is whether a similar, but separate means will be needed to indicate the sourcing for the calendar, perhaps via a "sources" link. 

## Creator/Contributors/Provenance + License

**Category:** Required

**Source:** Generated

An indication of the Creator of the record (i.e. the person or organization which created the initial record), the Initial Provenance (a credit line for the reference gazetteer which provided the core data for the record), and the Contributors (a comma separated list of names of the registered full-names of the contributors to the record). An indication of the license(s) under which data of this record can be released.

TBD is the need to list one (CC0) or possibly two licenses to account for core and extended metatdata (CC0 + CC-BY). Probably this will need to be a single CC0 license.




