## Key Concepts and Definitions

### Places, Names, and Locations

EM Places is indebted to the [Pleiades](https://pleiades.stoa.org) gazetteer of ancient places for its key concepts of [place, name, and location](https://pleiades.stoa.org/help/conceptual-overview) (see also their ['Technical Introduction to Places'](https://pleiades.stoa.org/help/technical-intro-places)):

> A Place is a geographical and historical context for Names and Locations. Places may have within their core some features of the physical world – a sea, a bay, a river, a mountain range, a pass, a road, a settlement, or an ethnic region – but their primary quality is that, in the words of Yi-fu Tuan 1, they are constructed by human experience. Places may be no larger than a family dwelling or as big as an empire, be temporally enduring or fleeting. They may expand, contract and evolve over time. A place may be unnamed, unlocated, falsely attested, or even mythical.
> 
> A Location is a current or former, concrete spatial entity. The midline of a river channel is a location. The center of a bridge's span is a location. The perimeter of a walled settlement is a location. Every location belongs to a place. The highest point of a mountain summit, for example, would be a location while the entirety of the mountain: its faces, ridges, couloirs, and forested slopes – and its significance in human history – would be the place context. The location entitled "Temple of Vesta" is but a small part of its context, Rome, while the place entitled "Hafir far west of Araba" provides only the barest semi-anonymous context for its sole desert waterhole location.
> 
> A Name is a current or former, abstract textual entity. Like a location, a name belongs to a place. The Πάπρημις of Herodotus 2.59 is one of many with no known locations in the same place. At the other end of the spectrum, Ἀφροδισιάς belongs to a place rich in locations and names.
> 
> Y. Tuan, "Place: An Experiential Perspective," Geographical Review, vol. 65, Apr. 1975, pp. 151-165.

Drawing closely on this definition, a ‘place’ in EM Places is a geographical and historical context for an entity 'constructed by human experience'. A place therefore, does not only include geographically known locations at specific points in time (e.g. regions and cities) but is also able to accommodate, where required, subjective and even fictional references. To quote again from the Pleiades gazetteer, ‘Places may be no larger than a family dwelling or as big as an empire, be temporally enduring or fleeting. They may expand, contract and evolve over time. A place may be unnamed, unlocated, falsely attested, or even mythical.’  

A 'location' is a spatial reference, typically represented as a single point, expressed as a latitude/longitude geo-coordinate, or else as a region, represented as a polygon constructed from multiple geo-coordinates. Many place records in EM Places, in particular those of historical regions, will have unknown, uncertain, or approximate locations. But if a location exists, it must be of a place. Finally, a 'name' (place name) is a textual reference belonging to a place. In EM Places, a place may have one name, or several names, or (strictly speaking) no name at all. On this basis, the minimum requirement for a valid place record in EM Places is simply to the place itself. A place may have a name, or a location, but both are strictly optional.

For the pilot release of EM Places we have chosen to largely bracket out fictional, mythical, extra-terrestrial and similar places referenced in historical texts. ‘Atlantis’, for example, or 'Saturn' are not likely to be found in this version of EM Places. This is because, in the first instance, our focus is on creating a gazetteer for describing the kinds of places from which real people wrote and received letters. Of course, distinctions between ‘real’ and ‘imaginary’ are never quite as strict as they may initially seem, and this is where the Pleiades model gives us the flexibility we will need to (at minimum) also account for ambiguous, allusive, and temporally curtailed places. 

### Core and Supplementary Metadata

EM Places records are composed of two classes of data: 1) a required, minimal set of core metadata, and 2) an optional, larger set of predominantly historical, supplementary metadata provided by contributing scholars and projects.
When a new place record is added to EM Places, we will first attempt to locate that place in GeoNames, our primary reference gazetteer. If the place is found, we ingest and record in EM Places a set of core metadata from a small number of contemporary reference authorities (currently: GeoNames, Getty TGN, and WikiData):

- Preferred (i.e. default) place names from GeoNames
- A set of unique (i.e. non-repeating) alternative place names (toponyms) from GeoNames, Getty TGN, and WikiData
- Location (i.e. geo-coordinate) data from GeoNames
- The current administrative-political (polity) hierarchy from GeoNames
- A list of matching place authority IDs from WikiData

From this data, EM Places is then able to locate a place on a map, generate a Linked Data authority ID (URI), and provide means to cite the record in an academic publication.

If the place we wish to add cannot be found in GeoNames, the data in these fields can be added manually by an EM Places editor. In many cases, the necessary data will be found in other authorities, such as the German National Library’s ‘Gemeinsame Normdatei’ (GND).  However, for historical (i.e. no longer extant) entities, this may not be possible. In particular, we cannot record in core data all of the possible political-administrative hierarchies of which this entity was a part over the duration of its existence. In this case, the core data entry will instead point to the entity’s historical hierarchies recorded in supplementary metadata (see below). 
All other major data fields in EM Places consist of optional supplementary metadata contributed by our users and partner projects. Each place record will be able to capture additional historical data on:

- Attestations of further toponyms, or variant attestations of existing toponyms
- A short text description, initially seeded (if available) from Wikipedia
- One or more images and/or links to geo-referenced, historical maps
- Administrative, Ecclesiastical (and in future releases, potentially Military and Judicial) historical hierarchies
- The date(s) of transition between calendars (e.g. from the Julian to the Gregorian)
- Data associated with a place (e.g. its role as station on a named postal route)
- Links to related historical resources
- Suggested bibliography 

