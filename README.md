# EM Places
Early Modern Places (EM Places) is a historical geo-gazetteer under development by the [Cultures of Knowledge][1] project at Oxford University with funding from the Andrew W. Mellon Foundation. It is the first of what will eventually be three Linked Open Data resources also comprising [EM People and EM Dates][2] built on a [shared humanities infrastructure platform][3] in collaboration with the [Huygens Institute][4] (KNAW). 

## Goals
EM Places is designed to meet several goals. 

The first is to be __a resource for identifying early modern places__ by means of their current and historical name variants. To this end, EM Places will combine current place (and alternative) place names, a current political/administrative hierarchy and location data from reference gazetteers (GeoNames, TGN Getty) and extend this with additional name attestations provided by contributors from historical sources (e.g. manuscripts or maps).

The second is to provide __a means for researchers to contribute additional historical contexts for places__. Initially, this will consist of means for recording, i) basic data (name, period, related resources) for the governing political/administrative, ecclesiastical, military, and judicial hierarchies associated with a place, ii) data on the dominant calendar (e.g. Julian, Gregorian) in use at that place over one or more historical periods. In the future, EM Places may be extended with further support for temporal features, such an ability to record basic data on early modern postal routes.

The third is to __properly credit, source, and cite all contributions__ to the gazetteer by individual researchers and project teams. Contributing users with registered accounts on EM Places should be able to submit or amend data using either a web interface or a bulk upload facility. Editorial and administrative users should have means to assign and review these contributions. The gazetteers sources should be consistently recorded using a structured bibliography. And means should also be provided to both manually link to related resources and dynamically link back to other early modern collections who are publishing their places as Linked Open Data.

The fourth is to __make the EM Places source code and datasets easily accessible and reusable by others__. To this end, the EM Places  source code, which will be based on the Huygens Institute's Timbuctoo infrastructure will be shared under open source and made accessible for reuse on the basis of Docker containers. All data in EM Places will be shared under open access over multiple channels: in the form of user initiated exports from the EM Places applications itself and as periodic data dumps to external repositories in multiple formats (e.g. CSV, Excel, GraphML, Turtle, GeoJSON-LD) and via the EM Places public API. In addition, EM Places will be able to share its data in the (currently in discussion) enhanced versions of the [Pelagios Gazetteer Interconnection Format][5] and [Peripleo][6] standards maintained by the [Pelagios Community][7].

On this basis , work was begun earlier this year on a high-level data model and a prioritized description of the gazetteer’s features which could be used to fix its initial scope given the time and resources available to us for its development. These document are supported by a series of draft mock-ups of the gazetteer’s user-interface.

## Features
The draft design document offers an informal description on the planned features for EM Places together and an intial set of draft design mock-ups. More details will be provided here as the gazetteer’s features are finalized.

## Data Model
An early draft of the proposed data model for EM Places and a set of data model diagrams. More details will be provided here as the data model set is finalized.

## Current Status
**April 2018**: First public draft of the design document describing the proposed features of the gazetteer with schematic mock-ups of potential UI elements. First public draft of the overview data model document. 

**March 2018**: Private drafts of the gazetter's design document and data model.

## Feedback and Comments
We are very interested in your feedback and comments on this project! Please get in touch by contacting Arno Bosse (Digital Project Manager, Cultures of Knowledge) by email arno.bosse@history.ox.ac.uk or via @kintopp on Twitter or by creating a new issue in this repository.

[1]:	culturesofknowledge.org
[2]:	http://www.culturesofknowledge.org/?p=8455
[3]:	https://github.com/HuygensING/timbuctoo
[4]:	https://www.huygens.knaw.nl/?lang=en
[5]:	https://github.com/pelagios/pelagios-cookbook/wiki/Pelagios-Gazetteer-Interconnection-Format
[6]:	https://github.com/pelagios/peripleo
[7]:	http://commons.pelagios.org
