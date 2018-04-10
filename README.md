# EM Places
Early Modern Places (EM Places) is a historical geo-gazetteer under development by the [Cultures of Knowledge](culturesofknowledge.org) project at Oxford University with funding from the Andrew W. Mellon Foundation. It is the first of three Linked Data resources later also comprising [EM People and EM Dates](http://www.culturesofknowledge.org/?p=8455) built on a [shared humanities infrastructure platform](https://github.com/HuygensING/timbuctoo) in collaboration with the [Huygens Institute](https://www.huygens.knaw.nl/?lang=en) (KNAW). 

## Goals
EM Places is designed to meet several goals. 

The first is to be a resource for identifying early modern places by means of their current and historical name variants. To this end, EM Places will combine current place (and alternative) place names, a current political/administrative hierarchy and location data from reference gazetteers (GeoNames, TGN Getty) and extend this with additional name attestations provided by contributors from historical sources (e.g. manuscripts or maps).

The second is to provide means for researchers to contribute additional historical contexts on places. Initially, this will consist of means for recording, i) basic data (name, period, related resources) for the governing political/administrative, ecclesiastical, military, and judicial hierarchies associated with a place, ii) data on the dominant calendar (e.g. Julian, Gregorian) in use at that place over one or more historical periods. In the future, EM Places may be extended with further support for temporal features, such an ability to record basic data on early modern postal routes.

The third is to properly credit, source, and cite contributions to the gazetteer both by individual researchers and project teams. Contributing users with registered accounts on EM Places should be able to submit or amend data using either a web interface or a bulk upload facility. Editorial and administrative users should have means to assign and review these contributions. The gazetteers sources should be consistently recorded using a structured bibliography. And means should also be provided to both manually link to related resources and dynamically link back to other early modern collections who are publishing their places as Linked Open Data.

The fourth is to make the EM Places source code and datasets easily accessible and reusable by others. To this end, the EM Places  source code, which will be based on the Huygens Institute's Timbuctoo infrastructure will be shared under open source and made accessible for reuse on the basis of Docker containers. All data in EM Places will be shared under open access over multiple channels: in the form of user initiated exports from the EM Places applications itself and as periodic data dumps to external repositories in multiple formats (e.g. CSV, Excel, GraphML, Turtle, GeoJSON-LD) and via the EM Places public API. In addition, EM Places will be able to share its data in the (currently in discussion) enhanced versions of the [Pelagios Gazetteer Interconnection Format](https://github.com/pelagios/pelagios-cookbook/wiki/Pelagios-Gazetteer-Interconnection-Format) and [Peripleo](https://github.com/pelagios/peripleo) standards maintained by the [Pelagios Community](http://commons.pelagios.org).

On the basis of these goals, work was begun on a high-level data model and a prioritized list of specific features which could be used to fix the initial scope of the gazetteer given the time and resources available for its development. This document was supported by a set of schematic user-interface mock-ups of the display and search modes of the gazetteer and an outline workflow for creating and editing gazetteer records (see Appendix). The majority of time during the STSM was devoted to these latter tasks.

In the future, we plan to use EM Places as the datastore for place data for [Early Modern Letters Online](http://emlo.bodleian.ox.ac.uk) (EMLO) and to facilitate this type of reuse by other projects as well. 

## Features
The draft design document offers further details on the planned features for EM Places together with an initial set of schematic design mock-ups. 

## Data Model 
The draft data model document provides an overview of the current data model for EM Places.

## Current Status
**March 2018**: First public draft of the design document describing the features of the gazetteer with schematic mock-ups of potential (display and search) UI elements. First public draft of the overview data model document. 

## Feedback and Comments
We greatly value your interest and feedback in this project. Please forward your comments to us (preferably) as new issues in this GitHub repository, or else by contacting Arno Bosse at arno.bosse@history.ox.ac.uk or @kintopp on Twitter.
