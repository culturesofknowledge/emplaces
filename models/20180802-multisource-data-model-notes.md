# EMPlaces data model for multiple "core data" sources

(The contents of this note will eventually be incorporated into the main data model notes, but arer being kept separate for now to highlight the proposed changes.)

## Problem with the previous model

See [Data model for EMPlaces using annotations (draft 2018-07-09)](PDFs/20180305-EMPlaces-data-model-using-annotations.pdf).

The previous model tried to apply core vs non-core distinctions at the level of individual properties, and in so doing ended mixing up the model-source information with the actual data model.  For example, there were two properties for place type information: `em:corePlaceType` and `em:placeType`.

The main reason for distinguishing "core" data from other data is to be able to refresh the core data when the underlying source (e.g. GeoNames) is updated, without disturbing any editorial content that has been added as a result of EMPlaces curation activities.

An additional concern not addressed by the original model was that there wasn't proper provision for the possibility of "core" data coming from multiple sources.

And finally, the distinction between a minimum set of "core" data for a place, and data that was derived from existing sources _vs_ data that was a contribution of EMPlaces has rather been lost.

The new design aims to rectify these problems:

1. The term "core" data is now taken to mean data that is populated for every EMPlaces place record (and which may vary with the type of place).

2. The term "direct data" is used to indicate place information that is taken directly from an exernal source, or directly derived from that source, and is presumed to be applicable to the indiocated place in all of its period of existence and other aspects.

3. The term "qualified data" is used to indicate place information that is qualified by some aspect of a place's existence; typically this will be a historical period within the lifetime of the place.  Current qualified data values include temporally qualified relations, and other information included by way of annotations that could include other qualifications.  Currently, none of the available "direct data" considered has been qualified, so the term "qualified data" corresponds roughly to non-direct data, but this may not always be the case.


## The basic place data model

See [Data model for EMPlaces using annotations (draft 2018-07-09)](PDFs/20180802-EMPlaces-data-model-multisource.pdf), page 1.

The revised basic place data model is a slight simplification of the previous data model, in that it removes distinctions between "core data" and other data:

- the `em:corePlaceType` property is removed, and just `em:placeType` is used.

- the `em:coreDataRef` property and "reference gazetteer" entry resource are removed.  The functionally provided by these will re-use the `em:source` property and `em:Source_desc` class (was previously `em:Source`, but the class name was not actually used in the data examples).

    (NOTE: I have separately been renaming classes to avoid having class names that differ from property names by case only.)

- the `em:canonicalURI` remains part of the basic data model, but the intent is that it will be used only with the merged place data (see below).


## Multiple-sources data model

See [Data model for EMPlaces using annotations (draft 2018-07-09)](PDFs/20180802-EMPlaces-data-model-multisource.pdf), page 2.

For place data that comes from a single source, a new subclass `em:Place_sourced`of `em:Place` is introduced.  This is explicitly used for data from a single source, and must use the `em:source` property to indicate the main source from which the data is derived.

For place data that combines data from multiple sources, a new class `em:Place_merged` is introduced, with a new property `em:place_data` that references a separate place data resource (which would generally be a `em:Place_sourced`).

The idea is that, for display purposes, all the properties of all the referenced place data resources are considered to apply to the merged place resource (except, maybe, `em:source` properties.)

For example, the following SPARQL CONSTRUCT statement might be used to construct a graph of data about a place for display purposes:

    CONSTRUCT
        {
            ?place ?p ?o
        }
    WHERE
        {
            ?place a em:Place_merged ;
            {
                ?place ?p ?o
            }
        UNION
            {
                ?place em:place_data [ ?p ?o ]
                FILTER ( ?p != em:source )
                FILTER ( ?p != rdf:type )
            }
        }

@@This query is untested, but I trust it conveys the general idea

@@We might find some additional smarts are needed to avoid problems from properties that appear in multiple sourced data; e.g. multiple rdfs:label values.

NOTE: I'm not actually proposing this method for displaying EMPlaces data, but using it to illustrate how the probe query patterns might be modified when extracting data for display.

NOTE: the exclusion of `em:source` properties is intended to avoid multiple conflicting source information.  One might consider allow multiple em:source values, but I feel that could conflict with the intuitive semantics of `em:source`.  E.g. if a particular source is considered trusted, it could be unintentionally applied to untrusted elements of the merged data.

NOTE `em:source` is also used with "qualified data", such as qualified relations and annotations.  In these cases, it provides additional information about the source of the qualified data (and its qualification).  Roughly, the main source of place data may be considered as providing a reference to the qualified data, and the qualified data itself provides a reference to the source used. Thus, in a sense, the main place data source and the qualified data source are both contributing the the information.


