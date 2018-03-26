# Individual Features

## Place Name

![Place Names](https://github.com/culturesofknowledge/emplaces/blob/master/img/place-names.png)

**Category:** Required
**Source:** Core Data

The default/preferred place name and its alternate names come from the reference gazetteer. All alternative names and their labels should be stored and indexed but only some will be displayed. For example, while we can silently allow users to find places using a Chinese transliteration there is no need to display the transliteration in the list of alternative names. For these, names in a TBD list of major European languages and historical forms will suffice.

It will be useful to compare the list of alternative names in GeoNames with those in the Getty TGN. If these often diverge, then a merged set under the above criteria should be shown. 

## Canonical UTI

![Canonical URI](https://github.com/culturesofknowledge/emplaces/blob/master/img/canonical-uri.png)

**Category:** Required
**Source:** Generated

This should be a short form permanent URI based on the custom domain for EM Places (e.g. emplaces.info). It should be accompanied by a javascript link to allow the URI to be copied to the clipboard on mouseclick.

## Latitude/Longitude

![Place Names](https://github.com/culturesofknowledge/emplaces/blob/master/img/latlong.png)

**Category:** Required
**Source:** Core Data

The representative center point for a place displayed as decimal lat/long and degrees (image just shows decimal). It should be accompanied by a javascript link to allow the URI to be copied to the clipboard on mouseclick. 

## Citation

![Place Names](https://github.com/culturesofknowledge/emplaces/blob/master/img/citation.png)

**Category:** Required
**Source:** Generated

A means to represent and make available for copying to the clipboard the canonical URI as an academic citation, in several standard formats. Other than in the image, it will better to show the citation format, so that users can have faith that it is being represented correctly. In other words, a list of major academic citation formats which shows the full citation on mouseclick. BibTex will not be needed here, since this is a single citation.

It may be possible to combine this with the canonical URI.

## Attestations

![Place Names](https://github.com/culturesofknowledge/emplaces/blob/master/img/attestations.png)

**Category:** Required
**Source:** Extended Data

Attestations are sourced instances of name variants to the preferred and alternative names in core data. For example, if a scholar finds a reference to Siena in a manuscript written as 'Ciena' and (TBD via editorial policy) this form is not already listed as an alternative name, then this data point can be recorded here, along with the language, date, and source for the attestation. 

TBD how to represent the attestation source. Most will be named links, but others may need to refer to other kinds of sources. 

An info link to a pop-up provides a means to explain the function of the attestation.

## Attestations

![Place Names](https://github.com/culturesofknowledge/emplaces/blob/master/img/maps.png)

**Category:** Required + Optional
**Source:** Core Data + Extended Data






