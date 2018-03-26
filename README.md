# EM Places
Early Modern Places (EM Places) is a historical geo-gazetteer under development by the [Cultures of Knowledge][1] project at Oxford University with funding from the Andrew W. Mellon Foundation. It is the first of three Linked Data resources later also comprising [EM People and EM Dates][2] built on a [shared humanities infrastructure platform][3] in collaboration with the [Huygens Institute][8] (KNAW). 

## Goals
EM Places is designed to meet several goals. 

The first is to _serve as a resource for identifying early modern places_ by means of their historical name variants. To this end, EM Places will combine place name (and alternative place name) data from reference gazetteers (GeoNames, TGN Getty) and extend this with additional name attestations. 

The second is to provide _means to share historical place data not captured by reference gazetteers_. Initially, this will consist of a) calendar data (e.g. a record for the use of the Julian calendar in a place), and ii) basic data on the historical place related entities. To achieve this, EM Places will combine current data from reference gazetteers on the political/administrative hierarchy of a place with additional basic data on their historical political/administrative, ecclesiastical, military, and judicial hierarchies. In the future, EM Places may be extended with further support for temporal places, such as postal routes. 

Our third goal, is to provide _functionality to correctly credit, properly source, and easily cite individual contributions to the gazetteer_ by external researchers and project teams. To this end, we will be providing means for registered users to amend or contribute records using either a web interface or bulk upload facility. We will also provide means to dynamically link back to other early modern collections who are publishing their place IDs as Linked Open Data. 

Our fourth goal is to _make the EM Places source code and datasets easily accessible and reusable by others_. To this end, the EM Places application source code will be shared under open source and made available as a Docker container. All data in EM Places will be shared under open access over multiple channels: via manual, user initiated exports from the EM Places applications and periodic data dumps to external repositories in commonly used formats (CSV, Excel, GraphML, RDF-XML, GeoJSON) and programmatically via the EM Places API. In addition, we are working closely with the [Pelagios][4] and [World Historical Gazetteer][5] project teams to ensure that EM Places data will be able to share its data in the [Pelagios Gazetteer Interconnection Format][6] via a [Peripleo][7] compatible API.

In the long-term, we plan to use EM Places as the datastore for place data for [Early Modern Letters Online][9] (EMLO) and to facilitate this type of reuse by other projects as well. 

## Current Status
**March 2018**: First public draft of an overview document describing the main features of the gazetteer its (display) UI elements. First public draft of a high-level data model. 

## Feedback and Comments
We greatly value your interest and feedback in this project. Please forward your comments to us (preferably) as new issues in the EM Places GitHub repository, or else by contacting Arno Bosse at arno.bosse@history.ox.ac.uk or @kintopp on Twitter.

[1]:	culturesofknowledge.org
[2]:	http://www.culturesofknowledge.org/?p=8455
[3]:	https://github.com/HuygensING/timbuctoo
[4]:	http://commons.pelagios.org
[5]:	http://whgazetteer.org
[6]:	https://github.com/pelagios/pelagios-cookbook/wiki/Pelagios-Gazetteer-Interconnection-Format
[7]:	https://github.com/pelagios/peripleo
[8]:  https://www.huygens.knaw.nl/?lang=en
[9]:  http://emlo.bodleian.ox.ac.uk
