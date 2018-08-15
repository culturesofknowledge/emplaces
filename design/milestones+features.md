## Features and Milestones

### v1 Data Goals

Metadata:

- Opole (current place) RDF w/content for all data fields
- Historical places (in Opole's admin historical hierarchy) RDF
- Five more full Silesian current places (as for Opole) 
- Circa 6K core records w/GeoName IDs imported from EMLO
- Circa 50 full records (as for Opole)

Maps:

- Preview and full PNG images for all full records

### Record View

Core Data:

- Preferred place name from reference gazetteer w/sorted list of unique alternative names (toponyms) and linked Provenance page.
- Current administrative hierarchy with reference gazetteer place type (feature code) labels.
- Location lat/longs with degree/minute/second representation. Clicking on Greenwich shows pop-up with table of early modern prime meridians (name, dates, offset, lat/long) for select place. Clicking on lat/long copies decimal lat/long into clipboard.
- Citation of selected EM Places record including contributors, permanent URL, last modified date. Clicking on citation style name copies formatted (rich text) citation of the selected citation format into the clipboard.
- Permanent URL expressed as an ARK identifier. Clicking on the URL copies the address into the clipboard.
- See Also lists the reconciled authorities for the selected place. Clicking on the authority name opens a new browser tab at the respective web address.
- Note: Current map (where available for a current place) also draws on core data.

Extended Data:

- Name attestations w/linked provenance page. Table showing attested name, language(s) using the name, date or period in which the name is in use, and Source.
- Calendars in use at the selected place w/linked Provenance page. Calendars are either directly in use (e.g. for a region) or inferred from the part-of region above it in their hierarchy. Show date of transition (s) from Julian to Gregorian, and type of transition (e.g. inferred), and type of Julian calendar (e.g. January 1 new year).
- Related Places w/linked provenance page. Table with Name of related place, place type, and association type. Link from name of related place to separate page listing replaced place details. 
- Bibliography for selected place w/link and bibliography item count. Link to separate page where the structured bibliographic entries for the selected place are listed. Item count is derived from this page. 
- Related Resources. List of external (typically online, and this linked) resources related to the selected place. Links open in new browser tabs.
- Feedback text with mailto link.
- Maps section w/linked Provenance page. If reference gazetteer can offer a lat/long then e.g. Google (TBD) map is shown centred on that location. If a historical place, optional historical maps are shown, identified with tab labels corresponding to their date of publication. Historical map can be a preview PNG linked to a website with geo-referenced map, or (fallback) linked to a higher-resolution PNG image. TBD if an additional mechanism (e.g. IIIF) will be supported in v1.
- Place Description. Initial text will be derived from first paragraph of Wikipedia entry for the selected place. 
- Creator/Contributors/Core Data/Licenses (links only)
- Export record in multiple formats
- Historical administrative hierarchies
- Historical ecclesiastical hierarchies w/multiple confessions
- Historical military and judicial hierarchies

#### Provenance pages

Separate, element specific provenance pages. See in-progress draft: https://github.com/culturesofknowledge/emplaces/issues/19 Note that in some cases unique URLs will be needed for the listed items in order to permit their citation.

#### Info pages

Modal pop-up with simple, formatted text describing the functionality of the respective element.

#### Import

- Import functionality TBD
- Supported import format(s) TBD

#### Export

- Export functionality TBD
- Supported export formats TBD
	- Must include LPIF (https://github.com/LinkedPasts/linked-places)

#### External APIs

- Timbuctoo APIs only (no Pelagios API in v1)

### Basic Search:

- Basic search functionality TBD
- Place centric, derived from default Timbuctoo search/result functionality

### Advanced Search:

- Advanced search functionality TBD in time for EM Places workshop/hack-a-thon (late April)