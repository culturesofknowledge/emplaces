# EM Places
Early Modern Places (EM Places) is a historical geo-gazetteer under development by the [Cultures of Knowledge](culturesofknowledge.org) project at Oxford University with funding from the Andrew W. Mellon Foundation. It is the first of three Linked Data resources later also comprising [EM People and EM Dates](http://www.culturesofknowledge.org/?p=8455) built on a [shared humanities infrastructure platform](https://github.com/HuygensING/timbuctoo) in collaboration with the [Huygens Institute](https://www.huygens.knaw.nl/?lang=en) (KNAW). 

## Goals
EM Places is designed to meet several goals. 

The first is to _serve as a resource for identifying early modern places_ by means of their historical name variants. To this end, EM Places will combine place name (and alternative place name) data from reference gazetteers (GeoNames, TGN Getty) and extend this with additional name attestations. 

The second is to provide _means to share historical place data not captured by reference gazetteers_. Initially, this will consist of a) calendar data (e.g. a record for the use of the Julian calendar in a place), and ii) basic data on the historical place related entities. To achieve this, EM Places will combine current data from reference gazetteers on the political/administrative hierarchy of a place with additional basic data on their historical political/administrative, ecclesiastical, military, and judicial hierarchies. In the future, EM Places may be extended with further support for temporal places, such as postal routes. 

Our third goal, is to provide _functionality to correctly credit, properly source, and easily cite individual contributions to the gazetteer_ by external researchers and project teams. To this end, we will be providing means for registered users to amend or contribute records using either a web interface or bulk upload facility. We will also provide means to dynamically link back to other early modern collections who are publishing their place IDs as Linked Open Data. 

Our fourth goal is to _make the EM Places source code and datasets easily accessible and reusable by others_. To this end, the EM Places application source code will be shared under open source and made available as a Docker container. All data in EM Places will be shared under open access over multiple channels: via manual, user initiated exports from the EM Places applications and periodic data dumps to external repositories in commonly used formats (CSV, Excel, GraphML, RDF-XML, GeoJSON) and programmatically via the EM Places API. In addition, we are working closely with the [Pelagios](http://commons.pelagios.org) and [World Historical Gazetteer](http://whgazetteer.org) project teams to ensure that EM Places data will be able to share its data in the [Pelagios Gazetteer Interconnection Format](https://github.com/pelagios/pelagios-cookbook/wiki/Pelagios-Gazetteer-Interconnection-Format) via a [Peripleo](https://github.com/pelagios/peripleo) compatible API.

Our long-term goal is to use EM Places as the datastore for place data for [Early Modern Letters Online](http://emlo.bodleian.ox.ac.uk) (EMLO) and to facilitate this type of reuse by other projects as well. 

## Features
The draft design document offers further details on the planned features for EM Places together with an initial set of schematic design mock-ups. 

## Data Model 
The draft data model document provides an overview of the current data model for EM Places.

## Current Status
**March 2018**: First public draft of the design document describing the features of the gazetteer with schematic mock-ups of potential (display and search) UI elements. First public draft of the overview data model document. 

## Feedback and Comments
We greatly value your interest and feedback in this project. Please forward your comments to us (preferably) as new issues in this GitHub repository, or else by contacting Arno Bosse at arno.bosse@history.ox.ac.uk or @kintopp on Twitter.