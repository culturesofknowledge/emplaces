# Core and Extended Metadata

There two main sources of data in EM Places. _Core metadata_ is periodically drawn by API from reference gazetteers (GeoNames and Getty TGN) and will be comprised of the following fields:

* Preferred Place Name (GeoNames)
* Alternative Names (GeoNames: all entries are indexed, not all are displayed)
* Latitude/Longitude (GeoNames: including polygons, if available)
* Current administrative/political hierarchy (GeoNames)
* Related Resources (TBD: links to other gazetteers)

Core metadata will form the spine of the gazetteer. This is data which EM Places will accept 'as is' and will not be editing. It can  be replaced at regular intervals (e.g. quarterly) with minimal editorial oversight in order to benefit from corrections/additions upstream.

By contrast, _Extended metadata_ is data which will be provided and revised by CofK staff and contributors on an ongoing basis or be otherwise set-up on a case by case basis from external data sources (Related Resources and Linkbacks).

Not all records in EM Places will be found in the reference gazetteers. In such cases, a user with the necessary privileges will create a new record with manually entered core metadata.

# Sample Workflow

A typical workflow for a new record would request the user to first attempt to identify the place in a reference gazetteer (GeoNames) and to enter that ID in EM Places. On this basis, EM Places will pull the relevant core metadata and use it to populate the draft record in a staging area. If the required place cannot be found, a new record cannot be created until a user with higher privileges has confirmed that the place is not available in GeoNames and provided a draft record for the user with manually entered core metadata.
