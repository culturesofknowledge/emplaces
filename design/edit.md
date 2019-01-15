# Overview (draft 22.12.18)

The basic workflow for a single record not yet in EM Places will request that a contributor first identify the place in a reference gazetteer (GeoNames or Getty TGN) and enter its ID in EM Places. EM Places will then pull the relevant core metadata from the reference gazetteer APIs and use this to populate a draft record for that place in a private staging area. Following this, the user will optionally be able to contribute additional metadata, and save the draft record, which will queue it for review by an editor.

If a place cannot be found by the user in the reference gazetteer, a draft record cannot be created until an editor with appropriate privileges has confirmed this, and created the necessary core data manually (for example, a small village, or a building, not found in our reference gazetteers).Once this is done, the draft record can be made accessible to the user, who is then able to contribute additional metadata as before.

We expect that the vast majority of new place names will be found in GeoNames. However, core data for all historical places will aways need to be created by hand, by a user with the necessary editing privileges. Core data for a historical place be more limited, but (by editorial policy) all new historical places should be accompanied by least one full historical administrative hierarchy in order to put the new historical place entity into context. 

For example, if the historical place 'Duchy of Opele' is created for the first time, then this new entry should be accompanied by additional, new entries (as needed) for e.g. the 'Governorate of the Duchy of Silesia', the 'Bohemian Crown', and the 'Holy Roman Empire' as well. 

A separate workflow based on this outline will be provided for bulk imports via templates in e.g. Excel or CSV format. 

## Searching/Browsing

### Find and view individual records

1. search (v1) for toponym in basic, place-centric search field
	- a search returns ranked (TBD) list of preferred place names and their  variants (from both reference gazetteers and historical hierarchies), and named attestations of place names.
2. select a place and view its detail record. 
3. copy ID and/or geo-coordinates
4. optionally export individual record

### Find and export multiple records

1. search (v1) for toponym in basic, place-centric search field
	- a search returns ranked (TBD) list of preferred place names and their  variants (from both reference gazetteers and historical hierarchies), and named attestations of place names.
2. select multiple or all records. 
3. export selected records 

### Use EM Places with OpenRefine 

1. select EM Places as reconciliation service in OpenRefine
2. [workflow determined by OpenRefine]
3. optionally contribute records to EM Places (see below)

### Use EM Places with its API

1. Deference one or more EM Places URIs to retrieve EM Places linked data as RDF
2. [TBA; workflow determined by user]
3. optionally contribute records to EM Places (see below)

## Classes of Users

All three main classes of user profiles ('standard contributors', 'trusted contributors' and 'editors') must first login to EM Places to add/revise data:

- standard contributors may suggest i) new records, ii) edits to extended metadata (core metadata cannot be edited by contributors)
- trusted contributors may additionally edit extended metadata without review. New records still require review.
- editors may additionally create and edit core metadata without review. In addition, they:
	- review all submissions by standard contributors and new record submissions (only) by trusted contributors
	- may edit any field
	- import bulk records
	- merge, delete, add records

## Contributing data


### Add a single place record to EM Places

1. search for place record in EM Places to verify it does not yet exist
2. look-up GeoNames ID for the missing place
	- If ID can be found
				i). enter GeoNames ID in web form; EM Places returns data from reference gazetteers and pre-fills the core data fields
				ii). if data looks correct, submit data for review by editors
		- If ID cannot be found, submit request for EM Places ID to editors
3. editors accept submitted place record, or create new place record; contributor allowed to submit extended metadata
4. submit extended metadata; submit to editors for review
	- (data quality rules/guidelines tbd)

### Add many tabular records to EM Places

[picking up from OpenRefine above]

1. Save unmatched records previously identified using OpenRefine in tabular format
2. if needed, restructure to meet EM Places contribution format
3. email data to EM Places editors  

### Edit one or more existing records in EM Places

- navigate to detail view of place record; edit record
	- standard contributors can edit and submit for review changes to extended metadata (core metadata is not editable by contributors
	- trusted contributors can edit extended metadata directly
- (data quality rules/guidelines tbd) 
