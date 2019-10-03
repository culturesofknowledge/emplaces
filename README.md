# EM Places
Early Modern Places (EM Places) is a collaboratively curated, historical geo-gazetteer for the sixteenth- to eighteenth-century under development by the [Cultures of Knowledge][1] project at Oxford University. It is the first of what will eventually become [three Linked Open Data resources][2] also comprising EM People and [EM Dates][26] built on a [shared humanities infrastructure platform][3] in collaboration with the [Humanities Cluster][5] of the Royal Dutch Academy of Arts and Sciences (KNAW) in Amsterdam. 

## Goals
EM Places is being designed to meet four goals: 

The first is to be __a resource for identifying early modern places by means of their current and historical name variants__. To this end, EM Places will combine current place (and alternative) place names, a current administrative hierarchy and location data from reference gazetteers such as GeoNames and WikiData and extend this with further place name attestations provided by contributors from primary sources. Users will be able to browse and search for places on multiple criteria, refine their results over facets, and export their search results. To facilitate semi-automatic disambiguation of bulk metadata EM Places will function as a [reconciliation service][28] for [OpenRefine][29]. 

The second is to provide __a means for researchers to contribute richer historical contexts to places__. EM Places will provide means for capturing i) basic partitive data on historical polities in political-administrative and ecclesiastical hierarchies (later, also military and judicial hierarchies), ii) either current, or where available, georeferenced historical maps, iii) the dates of transition between official calendars in a region (e.g. from the Julian to the Gregorian) for reuse in [EM Dates][26], iv) custom attributes describing ‘associations’ between places' (e.g. the time and cost for mail to travel between two postal stations on a named postal route), and v) links to additional historical resources and bibliographies. 

The third is to __fully credit, source, and cite all contributions to the gazetteer by individual researchers__. Regular contributors with registered accounts on EM Places will be able to submit new data or suggest revisions to existing data using either a web interface or a bulk upload facility. More experienced users with editorial privileges will have the means to review and approve these contributions. Users will be able to see whether data in the gazetteer originated from a reference gazetteer such as GeoNames or was added by an individual contributor. All contributors to EM Places will be able to call up a listing of their contributions and revisions to the gazetteer. 

The fourth and final goal is to __make the EM Places source code and datasets easily accessible and reusable by others__. To this end, the source code for EM Places, based on the [Timbuctoo technical infrastructure][3] developed by the KNAW [Humanities Cluster][5], will be shared under open source and made available for reuse in virtual Docker containers. The data in EM Places will be shared under open access licenses and distributed over multiple channels: as user-initiated exports of individual records from the application itself, on popular open repositories such as GitHub, and via the EM Places GraphQL API. 

Our intent is to prepare the gazetteer in a transparent and collaborative manner as possible to allow it to become a useful resource for for the early modern community and an active participant in the proposed [Pelagios][8] network. In support of this, in addition to CSV, Excel, and RDF-Turtle, EM Places will support the export of structured data in the new Geo-JSON-T [Linked Places Interconnection Format][4]. 

## Design
The draft [design documents][10] (display, search, edit) offer an informal description of the planned features for EM Places together with a first set of [interface mock-ups][21]. More details will be added here as the gazetteer’s features are finalized.

## Data Model
An draft of the [proposed data model][11] for EM Places and a set of data model diagrams. More details will be added here as the data model is refined.

## Status
**June 2019**: Data model complete, sample data created, search/results & record detail interfaces refined; development sprints now underway; first beta scheduled for end of August. 

**December 2018**: Second revision of internal tool for creating core metadata for place records from reference gazetteers; created sample dataset from EMLO places; reviewed Timbuctoo infratructure dependancies; defined basic editorial workflows; 

**November 2018** Further revisions to the data model; provisional plan for searching and browsing place records. Initial version of internal Linked Data web editor to be used for prototyping and data entry until the EM Places web editor is ready.

**August 2018**: Provisional full draft of complete data model completed; first release of tool for processing GeoNames data; completed draft user interface for record detail view

**July 2018**: First public draft of the design document describing the proposed features of the gazetteer with schematic mock-ups of potential UI elements. First public draft of the overview data model document. 

**March - June 2018**: Private drafts of the gazetter's design document and data model.

## Feedback and Comments
We are keen to get your comments and feedback on EM Places. Please get in touch by contacting Arno Bosse (Digital Project Manager, [Cultures of Knowledge][12]) by email [arno.bosse@history.ox.ac.uk][13] via [@kintopp][14] on Twitter or by creating a new GitHub issue in the repository with your comment/question.

## Contributors
Arno Bosse (Oxford - Project Management), Howard Hotson (Oxford - Director), Graham Klyne (Oxford – Data Modelling), Miranda Lewis (Oxford - Editor), Martijn Maas (HuC – Systems Development), Glauco Mantegari (Design Consultant), Jauco Noordzij (HuC – Systems Development), Marnix van Berchum (HuC - Project Management), Mat Wilcoxson (Oxford – Systems Development), Rob Zeeman (HuC – Systems Development).

## Acknowledgements
We would like to acknowledge the inspiration we drew, and the help we received from several related projects, including the [COST Action 'Reassembling the Republic of Letters'][22], [GeoNames][17], [Das Geschichtliche Orts-Verzeichnis (GOV)][15], the [Getty TGN][16], the [Herder Institute for Historical Research on East Central Europe][20], the [Pelagios Project][8], [WikiData][18], and the [World Historical Gazetteer][19]. Particular thanks are due to [Dariusz Gierczak][23] for providing us with sample historical gazetteer data on Silesia.

EM Places, EM People, and EM Dates were [funded 2017-2019 by a grant][2] to the University of Oxford from the Andrew W. Mellon Foundation.

[1]:	culturesofknowledge.org
[2]:	http://www.culturesofknowledge.org/?p=8455
[3]:	https://github.com/HuygensING/timbuctoo
[4]:	https://github.com/LinkedPasts/linked-places
[5]:	https://huc.knaw.nl
[6]:	https://github.com/pelagios/pelagios-cookbook/wiki/Pelagios-Gazetteer-Interconnection-Format
[7]:	https://github.com/pelagios/peripleo
[8]:	http://commons.pelagios.org
[9]:	http://commons.pelagios.org/groups/linked-pasts/forum/topic/from-linking-places-to-a-linked-pasts-network/
[10]:	/design
[11]:	/models
[12]:	http://culturesofknowledge.org
[13]:	mailto:arno.bosse@history.ox.ac.uk
[14]:	http://twitter.com/kintopp
[15]:	http://gov.genealogy.net/search/index
[16]:	https://www.getty.edu/research/tools/vocabularies/tgn/
[17]:	http://geonames.org
[18]:	https://www.wikidata.org
[19]:	http://whgazetteer.org
[20]:	https://www.herder-institut.de/startseite.html
[21]:	/images
[22]:	http://republicofletters.net
[23]:	http://www.republicofletters.net/index.php/portfolio_page/dariusz-gierczak/
[24]: https://github.com/LinkedPasts/lpif
[25]: http://linkedpasts.org
[26]: https://github.com/culturesofknowledge/emdates
[27]: http://emlo.bodleian.ox.ac.uk
[28]: https://github.com/OpenRefine/OpenRefine/wiki/Reconciliation
[29]: https://openrefine.org
