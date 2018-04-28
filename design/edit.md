# Overview (Edit)

TBA

## Concepts and Principles

TBA

### Workflow

**Priority:** Essential (individual records); High (bulk import)

**Source:** Core data, additional data

The basic workflow for a single record not yet in EM Places will request that a contributor first identify the place in a reference gazetteer (GeoNames or Getty TGN) and enter its ID in EM Places. EM Places will then pull the relevant core metadata from the reference gazetteer APIs and use this to populate a draft record for that place in a private staging area. Following this, the user will optionally be able to contribute additional metadata, and save the draft record, which will queue it for review by an editor.

If a place cannot be found by the user in the reference gazetteer, a draft record cannot be created until an editor with appropriate privileges has confirmed this, and created the necessary core data manually (for example, a small village, or a building, not found in our reference gazetteers).Once this is done, the draft record can be made accessible to the user, who is then able to contribute additional metadata as before.

We expect that the vast majority of new place names will be found in GeoNames. However, core data for all historical places will aways beed to be created by hand, by a user with the necessary editing privileges. Core data for a historical place be more limited, but (by editorial policy) all new historical places should be accompanied by least one full administrative hierarchy in order to put the new historical place entity into context. 

For example, if the historical place 'Duchy of Opele' is created for the first time, then this new entry should be accompanied by additional, new entries (as needed) for e.g. the 'Governorate of the Duchy of Silesia', the 'Bohemian Crown', and the 'Holy Roman Empire' as well. 

A separate workflow based on this outline will be provided for bulk imports via templates in e.g. Excel or CSV format. 