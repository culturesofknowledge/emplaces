# EMPlaces data model notes

## Shapes

- round-ended shapes designate classes or prototypical values, which in actual place descriptions appear as instances of the described class.  The underlying boxes to thye upper left of the main class symbol indicate UREIs or CURIEs (compact URIs) for one or more classes of which the designated value is a member.

- rectangular shapes designate literal values, which in actual place descriptions appear as strings, numbers or other literal data values.

## Relationships (properties, connections)

- single-headed arrows are used to indicate a one-to-one relationship between the subject ("from") and the object ("to") entities.  E.g., a place has a single preferred name.

- double-headed arrows are used to indicate a one-to-many relationship between subject and object.  E.g., a place may have multiple alternative names.

- labels on arrows identify a relationship between subjects and objects.  They indicate the URI of the property that connects a subject to an object when represented as linked data.

## Colours

Colour is used in the diagrams to give a sense of the role and/or source of information in EMPlaces descriptions:

-   Yellow indicates "core data" which is derived from a reference gazetteer.  The "Reference gazeteer entry", indicated by property "em:coreDataRef" whose subject is the Place concerned.  The general intent is that core data will be present for all place descriptions.

    A key property of this core data is that it may be automatically updated if the reference gazeteer entry is updated; as such it is not available for editing in EMPlaces cataloguing workflows.

-   Orange indicates EMPlaces additional data about a place that (generally) if not provided by a conventional gazetteer.  This data represents editorial contributions of EMPlaces to the information about a place.  The intent is that EMPlaces additional data will be provided where available, and is not necessarily poresent for every Place instance.

    Some entities are shown with both yellow and orange colouring.  This indicates that the same vocabulary terms may be used in the representation of both core and additional data about a place.

    @@TODO: indicate a simple generic mechanism that reliably distinguishes core data instances from added data, so that thgey can be reliably superseded when gazetteer-provided informaton is refreshed.  Possibilities ofr this include: flag associated with value; type associated with core value; subtypes for core values; separate properties for core values; subproperties for core values; etc.

-   Green is used for spatial location information.

-   Blue/lilac is used for temporal information.


# Classes

## Place (`em:Place`)

This class represents the central idea described by EMPlaces.  Instances of this class represent a place, in the sense used by Pleiades: "constructed by human experience"

## Place type (_term TBD_)

A value that indicates a type of a place (e.g. city, battlefield, country, etc.).  A place may (and generally does) have more than one type.

## Place category (_term TBD_)

Place types may be associated with categories (e.g. administrative, ecclesiastical, etc.)  These associations with categories are initially intended to describe groupings of place types that are associated with various hierarchies.  But the notion is quite general, and other uses may emerge over time (e.g. a "geographical feature" category might cover mountains, lakes, rivers, seas, islands, etc., for which there is no specific hierarchy).

## Reference gazetteer entry

A node that references a gazetteer entry and also provides a label for that entry.

## Preferred name

A string that is the preferred name for a place; this is the default name used when referring to that place.

## Alternate name

A string, possibly with a language code, that is an alernative name for a place.  Alternative names are generally alternative transliterations and language representations for the name of the place.

## Description

A description of a place.

The description is initially populated from the reference gazeteer entry, but is editorialy controlled by EMPlaces.  Its focus is on the historical exiastence and context of the place, and may diverge from the gazetteer description.  As such, it is not intended to be updated when the other core data obtained from the reference gazetteer entry is refreshed.

## Qualified relation

A Qualified relation represents a historical relationship between two places.  Specifically, the relationship ismone that generally exists only for a limited perod of time (e.g. the City of Opole being administratively part of the Duchy of Opole during the period 1281 to 1521).

Thus, in addition to being linked to the two related places, a Qualified relation is also linked to a Timespan during which the relationship existed, and a Relation type that indicates the type of relationship (e.g. administrative part, ecclesiastic part, etc.)

The primary intent of these Qualified relations is to represent multiple time-varying hierarchical relationships between places (something that is not provided by most exsting gazetteers).  But the mechaism here is quire general, and other uses, not necessarily hierarchical in nature, could be adopted in due course (e.g. treaties, communication links).

See also: Relation type, Place type and Place catagory.

## Relation type

A Relation type is a value associated with a Qualified relation to indicate the type of relation (e.g. administrative part, ecclesiastic part, etc.).  It also indicates the types of places between which the relation may hold (e.g. an administrative part relationship may hold between empires, countries, administrative regions, cities, etc.).

A Relation type is part of the general structure for representing relationships, and is generally not linked to any particular places.

Future usage could associate structural constraints on Relation types (e.g. that they are hierarchical in nature), but this is not covered in the present proposal.

See also: Qualified relation, Place type and Place catagory.

## Place type

A value that represents a type of place (e.g. city, battlefield, empire, etc.)

See also: Relation type and Place category.

## Place category

See also: Relation type and Place type.

A value that reprents a category of places, or a set of place types (e.g. administrative, ecclesiastical, military, geographical, etc.).

A place type may belong to several cvatagories.

The intent of this value is to provide a means to identifty the various place types that may appear in a given hierarchy:  in this use, the place categiory identifies a hierarchy.  But the mechanism provided is quite general, and could be used to identify other groupings of place types (e.g. habitations).

## Setting

Represents a bounded region in space and time (cf. CIDOC CRM [E92 Spacetime Volume](http://www.cidoc-crm.org/lrmoo/entity/e92-spacetime-volume/version-6.2))

## Bibliographic entry

A formal bibliographic entry to some published work.

## Source

A reference to a source of a claim made buy an Annotation.  May be descriptive or informal (e.g. a URL).  May also convey contextual information about the appicability of the claim.

## Related resource

Areference to a resource that is believed to contain relevant additional information about a place (or other entity).

@@TODO: use with `rdfs:seeAlso` instead of `em:relatedesource`?

## Timespan

Represents a period of time.

May be with reference to a specific calendar dates, or more generally to some identified but maybe unspecified period (cf. PeriodO).

## Location

Provides information that physically locates a Place in some way.

May be connected to specific geographic or spatial location, or simply a reference to some unspecified location

@@TODO: try to be clear about the distinction between Place (as "constructed by human experience") and Location.

@@TODO: refer to existing work.  Intend to not invent here.


# Annotations general model

@@@describe general approach; per-annotation details come later

## Annotations general structure

## `em:hasAnnotation` Annotation 

This statement indicates an annoation associated with a place.  The annotation may carry different information about the place, dependent on the value of the associated Annotation type.

`em:hasAnnotation` functions roughly as an inverse of `oa:hastarget`, and is defined to simplify JSON-LD representations of annotations associated with a place.  The annotation itself should also have an `oa:hastarget` property with the asscoated place as its object, to be a valid web annoation.

@@TODO: would it be better to associate an anotation container with the place (e.g. using `em:hasAnnotations`), or to treat the place itself as an annotation container?  Or maybe have a separate annotation container for all places?

### `oa:hasTarget` Place

Connection from an annotation back to the associated place.

See also `em:hasAnnotation` Annotation.

### `oa:motivatedBy` Annotation type

The purpose of the annotation type is to make it easy to find particiular annotation values associated with a place.

@@TODO: is this the appropriate property?  Maybe `oa:purpose` (doesn't seem quite right), some new property, or an additional `rdf:type associated` with the annotation body?

### `oa:hasBody` Annotation body

The Annotation body conveys specific information associated with the associated place.  The structure of this information is definbed by the corresponding Annotation type value.

@@TODO: should the annotation body also reference the place directly?  (This would make it stand more independently, maybe easier to process separately from the annotation itself, but could it also cause some semantic problems?)

@@TODO: should the temporal information be attached to the annotation body, or to the annotation (as now)?

@@TODO: should the annotation type be attached to the annotation body, or to the annotation (as now)?

@@TODO: should the annotation carry an editorial note: currently, that is attached to the annotation body.

@@TODO: the above questions arise in part from tghinking about the "annotation" as being a reification of an association between the place and the annotation body, thereby allowing that association to be qualified in various ways.

@@TODO: the above questions also beg the question: "why annoations?".  A possible answer is that they provide a seamless way to incorporate 3rd-party data, externally stored and managed, into an overall description.  This could support a number of potential usage models for EWMPlaces and friends (researcher notebooks, 3rd party submissions for incorporaton, use-dependent trust models fopr annotation data, etc.)

## `em:when` Timespan

Temporal qualification of association described by the annotation.

@@TODO: is this OK applied to the annotation, or should it be the annotation body?

### `em:source` Source

Indicates the source of information for the claim represented by this annotation.


# Specific Annotation details

## Calendar in use

Annotation type: `em:CalendarInUse`

### Calendar label

A short string or phrase used as a label for the calendar; e.g., "Julian", "Gregorian", etc.

### `em:uri` Calendar resource

@@TODO: `em:uri` is probably a poor name (implies mention rather than use).  Maybe `em:resource`?  Or `rdf:value`?  Or ...?

An arbitrary resource identifying and describing the calendar.  May be content negotiated to retrieve different formats.  Ideally, content negotion can provide a linked data representation, but this may not always be possible.  At least, the URI of this resource should be a way of uniquely identifying the calendar concerned.

### `rdfs:comment` Editorial note

A textual description of the calendar's applicability to the associated place.

NOTE: the calendar itself may be described by a textual description associated with the calendar resource.  Where the same calendar is in use at several different places and/or times, it should be described just once.

### `em:when` Timespan

Indicates a period during which the calendar was used at the associated place.


# Properties

@@TODO?
