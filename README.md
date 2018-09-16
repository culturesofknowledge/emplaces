# EM Places
Early Modern Places (EM Places) is a collaboratively curated, historical geo-gazetteer for the sixteenth- to eighteenth-century under development by the [Cultures of Knowledge][1] project at Oxford University. It is the first of what will eventually become [three Linked Open Data resources][2] also comprising EM People and [EM Dates][26] built on a [shared humanities infrastructure platform][3] in collaboration with the [Huygens Institute][4] (KNAW) in Amsterdam. 

## Goals
EM Places is being designed to meet four goals: 

The first is to be __a resource for identifying early modern places__ by means of their current and historical name variants. To this end, EM Places will combine current place (and alternative) place names, a current administrative hierarchy and location data from reference gazetteers and extend this with additional name attestations provided by contributors from other historical sources (e.g. manuscripts). Users will be able to browse and search for places on multiple criteria, refine their results over facets, and export their search results. 

The second is to provide __a means for researchers to contribute richer historical contexts__. For all places, this will provide means for capturing, i) basic data (e.g. names, periods, related resources, bibliography) for the administrative, ecclesiastical, military, and judicial hierarchies associated with a historical place, ii) data on the dominant calendars in use (e.g. Julian calendar – new year starting March 25), as well as iii) bespoke properties for what we are calling 'related places' such as streets and buildings. In the future, EM Places may be extended with further support for other related features, such as postal routes.

The third is to __fully credit, source, and cite all contributions__ to the gazetteer by individual researchers and project teams and provide means to link to other, associated resources. Contributing users with registered accounts on EM Places will be able to submit or amend data using either a web interface or via a bulk upload facility. Editorial users will have means to review these contributions. Place records in the gazetteer will be accompanied by bibliographical entries, related resources and a facility to link back to other early modern collections sharing their records as Linked Open Data.

The fourth is to __make the EM Places source code and datasets easily accessible and reusable by others__. To this end, the EM Places source code, based on the Huygens’ [Timbuctoo][5] technical infrastructure, will be shared under open source and made accessible for reuse. All data in EM Places will be shared under open access over multiple channels: in the form of user initiated exports from the applications itself, on external repositories, and via the EM Places API. Separately, EM Places will be able to share its data in the [Linked Places Interconnection Format][24]. 

Our intent is to prepare EM Places in a transparent and collaborative manner as possible to allow it to become a useful resource for the [Pelagios Community][8] and an active participant in the proposed [Linked Pasts Network][25].

## Design
The draft [design documents][10] (display, search, edit) offer an informal description of the planned features for EM Places together with a first set of [interface mock-ups][21]. More details will be added here as the gazetteer’s features are finalized.

## Data Model
An draft of the [proposed data model][11] for EM Places and a set of data model diagrams. More details will be added here as the data model is refined.

## Status
**August 2018**: Provisional full draft of complete data model completed; first release of tool for processing GeoNames data; provisional complete full record user interface

**July 2018**: First public draft of the design document describing the proposed features of the gazetteer with schematic mock-ups of potential UI elements. First public draft of the overview data model document. 

**March - June 2018**: Private drafts of the gazetter's design document and data model.

## Upcoming ToDo Items
- Collect and incorporate community feedback
- ~~Fix the main v.1 features of the gazetteer~~; revise documentation
- ~~Test data model with sample record~~; test model with 6K core data places from [EMLO][27]; prepare 25-50 sample full data records
- ~~Finalize the proposed record detail interface, create interface mockup~~
- Finalize the proposed search interface, create interface mockup
- Discuss proposed editorial workflow, create interface mockup
- Finalize bulk upload and export formats, review [Linked Places Interconnection Format][24]
- Prepare API, test interconnection with [EM Dates][26]

## Feedback and Comments
We are keen to get your comments and feedback on EM Places. Please get in touch by contacting Arno Bosse (Digital Project Manager, [Cultures of Knowledge][12]) by email [arno.bosse@history.ox.ac.uk][13] via [@kintopp][14] on Twitter or by creating a new GitHub issue in the repository with your comment/question.

## Team
Arno Bosse (Oxford - Project Management), Howard Hotson (Oxford - Director), Graham Klyne (Oxford – Data Modelling), Miranda Lewis (Oxford - Editor), Martijn Maas (Huygens – Systems Development), Glauco Mantegari (Design Consultant), Jauco Noordzij (Huygens – Systems Development), Marnix van Berchum (Huygens - Project Management), Mat Wilcoxson (Oxford – Systems Development).

## Acknowledgements
We would like to acknowledge the inspiration we drew, and the help we received from several related projects, including the [COST Action 'Reassembling the Republic of Letters'][22], [GeoNames][17], [Das Geschichtliche Orts-Verzeichnis (GOV)][15], the [Getty TGN][16], the [Herder Institute for Historical Research on East Central Europe][20], the [Pelagios Project][8], [WikiData][18], and the [World Historical Gazetteer][19]. Particular thanks are due to [Dariusz Gierczak][23] for providing us with sample historical gazetteer data on Silesia.

EM Places, EM People, and EM Dates are [funded by a grant][2] to the University of Oxford from the Andrew W. Mellon Foundation.

[1]:	culturesofknowledge.org
[2]:	http://www.culturesofknowledge.org/?p=8455
[3]:	https://github.com/HuygensING/timbuctoo
[4]:	https://www.huygens.knaw.nl/?lang=en
[5]:	https://github.com/HuygensING/timbuctoo
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
