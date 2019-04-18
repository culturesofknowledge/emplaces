# EMPlaces data model notes

## Shapes

- large round-ended shapes designate classes, or entitity types, which in actual place descriptions appear as instances of the described class.  The underlying rectangles to the upper left of the main class symbol indicate URIs or CURIEs (compact URIs) for one or more classes of which the designated value is a member.

- large rectangular shapes designate literal values, which in actual place descriptions appear as strings, numbers or other literal data values.

- large 8-sided shapes (roughly, rectangles with their corners truncated) are used for "instance" values; i.e. specific instances of some type that are defined by the EMPlaces data model to represent specific values.  E.g., these are used to indicate specific anotation types for name attestations, map resources and calendar-in-use descriptions.

## Relationships (properties, connections)

- single-headed arrows are used to indicate a one-to-one relationship between the subject ("from") and the object ("to") entities.  E.g., a place has a single preferred name.

- double-headed arrows are used to indicate a one-to-many relationship between subject and object.  E.g., a place may have multiple alternative names.

- labels on arrows identify a relationship between subjects and objects.  They indicate the URI of the property that connects a subject to an object when represented as linked data.

## Colours

Colour is used in the diagrams to give a sense of the role and/or source of information in EMPlaces descriptions:

-   Yellow usually indicates "core data" which is derived from a reference gazetteer, or other authority, without editorial intervention.  The general intent is that core data may be present for all place descriptions.

    A key property of this core data is that it may be automatically updated if the reference gazeteer entry is updated; as such it should not normally be edited ("messed with") in EMPlaces cataloguing workflows.  (In the case of a historical place that does not exist in the reference gazetteer, this core data will need to be created manually.)

-   Orange indicates EMPlaces additional data about a place that (generally) if not provided by a conventional gazetteer.  This data represents editorial contributions of EMPlaces to the information about a place.  The intent is that EMPlaces additional data will be provided where available, and is not necessarily poresent for every Place instance.

-   Green is used for spatial location information.

-   Blue/lilac is used for temporal information.

Some entities are shown with both yellow and orange colouring.  This indicates that the corresponding entity types may be used to represent either core data or additional data about a place.


# Classes

## Place (`em:Place`)

This class represents the central idea described by EMPlaces.  Instances of this class represent a place, in the sense used by Pleiades: "constructed by human experience".

Note that places are subdivided into `em:Place_sourced` which denotes information about a place derived from a single specified source, and `em:Place_merged` which denotes information that is combined from multiple sources (see [MPlaces data model for multiple "core data" sources](./20180802-multisource-data-model-notes.md).

See also:
- https://pleiades.stoa.org/help/conceptual-overview
- https://pleiades.stoa.org/help/pleiades-data-model/
- 


## Place type (`em:placeType` -> `skos:Concept`)

A value that indicates a type of a place (e.g. city,  battlefield, country, etc.).  For core data populated from GeoNames, these would be GeoName feature class codes (A, ADM1, ADM2, etc.).  A place may (and generally does) have more than one type.

(We suggest that values used are based on Getty AAT terms)

## Place category (`em:placeCategory` -> `skos:Concept`)

Place types may be associated with categories (e.g. administrative, ecclesiastical, etc.)  These associations with categories are initially intended to describe groupings of place types that are associated with various hierarchies.  But the notion is quite general, and other uses may emerge over time (e.g. a "geographical feature" category might cover mountains, lakes, rivers, seas, islands, etc., for which there is no specific hierarchy).

A current place must have a type in the adminsitrative category.

Initial category values will be:

- Administrative
- Ecclesiastical
- Military
- Judicial


## Source entry

A node that references a source of information (e.g. a Reference gazetteer entry) and also provides a label and other information about that entry.

## Preferred name

A string that is the preferred name for a place; this is the default name used when referring to that place.

## Alternate name

A string, possibly with a language code, that is an alernative name for a place.  Alternative names are generally alternative transliterations and language representations for the name of the place.

## @@TODO: technical metadata

Supplied by underlying system, covers:
- creator
- contributors
- licenses (core, EMplaces)


## Description

(aka "Editorial Note")

A description of a place.

The description may be initially populated from the reference gazeteer entry, but is editorialy controlled by EMPlaces.  Its focus is on the historical existence and context of the place, and may diverge from the gazetteer description.  As such, it is not intended to be updated when the other core data obtained from the reference gazetteer entry is refreshed.

## Qualified relation

A Qualified relation represents a current or historical relationship between two places.  Specifically, the relationship is one that exists only for a limited perod of time (e.g. the City of Opole being administratively part of the Duchy of Opole during the period 1281 to 1521).

Thus, in addition to being linked to the two related places, a Qualified relation is also linked to a Timespan during which the relationship existed, and a Relation type that indicates the type of relationship (e.g. administrative part, ecclesiastic part, etc.)

The primary intent of these Qualified relations is to represent multiple time-varying hierarchical relationships between places.  But the mechanism here is quire general, and other uses, not necessarily hierarchical in nature, could be adopted in due course (e.g. treaties, communication links).

See also: Relation type, Place type and Place category.

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

The notion of a "Setting" was used previously in Karl Grossner's work on [Topotime](https://github.com/kgeographer/Topotime); e.g. see [Place, Period, and Setting for Linked Data Gazetteers](https://geog.ucsb.edu/~jano/GrossnerJanowiczKessler_submitted_draft.pdf), and has been adopted here.

Represents a bounded region in space and time (cf. CIDOC CRM [E92 Spacetime Volume](http://www.cidoc-crm.org/lrmoo/entity/e92-spacetime-volume/version-6.2)).

Where the location of a place changes over time, this can be captured through associating multiple settings with that place.

Example:

    em:where
      [ a em:Setting ;
        em:location
          [ a em:Location_value ;
            wgs84_pos:lat  "50.67211"^^xsd:double ;
            wgs84_pos:long "17.92533"^^xsd:double ;
          ] ;
        em:when emp:Current ;
        em:source
          [ a em:Authority ;
            rdfs:label "GeoNames data" ;
            em:link <http://sws.geonames.org/3090048/about.rdf>
          ] ;
      ] ;

## Time period and timespan

A time period represents a period of time, by reference to a specific timespan, or to some identified but maybe unspecified period (cf. PeriodO).

A timespan represents an temporal interval by reference to a specific calendar dates.

Example:

    em:when 
      [ a em:Time_period ;
        rdfs:label   "1281-1521" ;
        em:timespan
          [ a em:Time_span
            em:start  "1281" ;
            em:end    "1521" ;
          ]
      ] ;

Possible timespan properties:

- `em:start`: start of span contained within year (or other calendar interval)
- `em:end`: end of span contained within year (or other calendar interval)
- `em:latestStart`: start of span no later than given year (or other calendar interval)
- `em:earliestEnd`: end of span is no earlier than given year (or other calendar interval)
- _&more?_  (e.g. `em:year` for timespan that starts and ends within a given year/calendar interval?; LPIF might use this IIRC)

## Location

Provides information about a physical location.

Example:

    em:location
      [ a em:Location_value ;
        wgs84_pos:lat  "50.67211"^^xsd:double ;
        wgs84_pos:long "17.92533"^^xsd:double ;
      ] ;

May be connected to specific geographic or spatial location, or simply a reference to some unspecified location.

Note the distinction between "Place" (as "constructed by human experience") and "Location".

@@TODO: expand the options for specifying location (e.g. relative to other location, etc., as needs arise.)

## Bibliographic entry

A bibliographic entry (preferably structured) to some published work.

## Source

A reference to a source and/or provenance of a claim made by an Annotation.  May also convey contextual information about the applicability of the claim.

## Alternate authority

Reference to an alernative authority for information about a place (e.g. TGN, GeoNames, etc.)

Multiple authorities may be present.

## Related resource

A reference to a resource that is believed to contain relevant additional information about a place (or other entity).

Multiple related resources may be present.


# Annotations general model

## Annotations general structure

Web Annotations are a W3C web standard ([data model](http://www.w3.org/TR/annotation-model/) and [vocabulary](http://www.w3.org/TR/annotation-vocab/)) for connecting some descriptive information (a "body") with a resource (the "target").

![Basic Web Annotation (from W3C specification)](images/web_annotation_basic_model.png "Basic Web Annotation (W3C)")

Traditionally, Web Annotations have been associated with human-readable annotations of documents (which are a way of associating some additional information of opinion or context with the content of a document), but the underlying model is also applicable to associating machine-readable data with an arbitrary resource identified by a URI.

Web Annotations have been adopted for use in the EMPlaces for the following reasons:

1. They allow additional information to be associated with a place, along with contextual information; e.g. a name attestation may be associated with a period within which it is believed to have been in use.  In particular, Web Annotations allow association of provenance and contributor informaton with individual claims about a place.

2. They provide an extension point through which additional information about a place can be introduced using the same basic structures that are used for basic EMPlaces information.

3. They allow separately-published information to be associated with a place, which in turn provides a possible route for curation of third party contributions to EMPlaces while maintaining editorial integrity of the base service.

4. As an increasingly popular web standard, we anticipate that Web Annotations will be increasingly supported by a range of software systems, which should make EMPlaces data more accessible and flexible for use with independent information systems.

When reading a Web Annotation, think of the "target" as something that the annotation is about - in our case, this is commonly a place.  The "body" is then some additional information about that place (or thing).  In our use of annotations, the body is an RDF node that denotes some information about the target.

The annotation itself is a resource distinct from the target or body.  We use a "motivation" property applied to the annotation to indicate how the body is related to the target; e.g. a "Name attestation" motivation indicates that the body is information about a name atestation associated with a target place.  Generally, the expected structure of RDF information in the body depends on the motivation used (but note that the RDF's open world model allows providion of additional arbitrary information here).

Additional properties of the annotation can be used to provide additional context for the information provided.  Some commonly-used additional context values are:

- a time period in which the information is considered to be applicable
- an indication of the source or provenance of the information, which may in turn inform decisions about its trustworthiness
- an indication of the "competence" of the information provided; e.g. is it considered to be definitive (coming from a generally reliable source), inferred (deduced from other information), uncertain (a researchers informed guess), etc.
- bibliographic references that provide additional related information

(NOTE: one way of thinking about an annotation is as a "reification" of an association between the target place and the annotation body, thereby allowing that association to be qualified in various ways.)


## `em:hasAnnotation` Annotation 

This statement indicates an annotation associated with a place.  The annotation may carry different information about the place, dependent on the value of the associated Annotation type.

`em:hasAnnotation` functions roughly as an inverse of `oa:hastarget`, and is defined to simplify JSON-LD representations of annotations associated with a place.  The annotation itself should also have an `oa:hasTarget` property with the asscoated place as its object, to be a valid web annoation.

### `oa:hasTarget` Place

Connection from an annotation back to the associated place.

See also `em:hasAnnotation` Annotation.

### `oa:motivatedBy` Annotation type

The purpose of the annotation type is to make it easy to find particiular annotation values associated with a place.

### `oa:hasBody` Annotation body

The Annotation body conveys specific information associated with the associated place.  The expected structure of this information is defined by the corresponding Annotation type value.

### `em:when` Timespan

Temporal qualification of association described by the annotation.

### `em:source` Source

Indicates the source of information for the claim represented by this annotation.

### `em:competence` Quality of information

Information in a qualified relation or annotation may be uncertain.  These properties and values are used to qualify these claims.  Note that in the absence of an explicit value, no competence should be assumed.

Information that is directly attached to an em:Place (i.e. not as a qualified relation or annotation) is considered to be definitive.  

Specifically, annotations for calendar-in-use and alternate name attestations should have associated competence values.  Approximate date ranges are represented by range values in the corresponding Timespan value.

Possible values

- `em:DEFINITIVE`: Definitive; the associated value is definitively true for the purposes of EMPlaces.  Such information should ideally be backup up be appropiate source references.

- `em:INFERRED`: Inferred; the associated value has been inferred from (preferably?) definitive information.

- `em:ASSUMED`: Assumed; the associated value is assumed from context.  (Assumed data is like uncertain, but maybe with better foundation?)

- `em:UNCERTAIN`: Uncertain; the associated value is uncertain, maybe a best guess or informed opinoon but without good evidence.

- `em:APPROXIMATE`: Approximate;  the associated value is a date whose value is only approximately known.  @@NOTE: this value may prove spurious, as timespan already has a way to represent approximation ranges.


# Specific Annotation details

## Name attestation

Annotation type: `em:NAME_ATTESTATION`

Example annotation body:

    oa:hasBody 
      [ a em:Place_name ;
        em:name      "Oppeln" ;
        em:language  eml:de ;
        rdfs:label   "German" ;
        rdfs:comment "German" ;
      ] ;

## Calendar in use

Annotation type: `em:CALENDAR_IN_USE`

Example annotation body:

    oa:hasBody 
      [ a em:Calendar ;
        em:link      emc:Gregorian ;
        rdfs:label   "Gregorian" ;
        rdfs:comment "..." ;
      ] ;

### `rdfs:label`: Calendar label

A short string or phrase used as a label for the calendar; e.g., "Julian", "Gregorian", etc.

### `em:link` Calendar resource

An arbitrary resource identifying and describing the calendar.  May be content negotiated to retrieve different formats.  Ideally, content negotion can provide a linked data representation, but this may not always be possible.  At least, the URI of this resource should be a way of uniquely identifying the calendar concerned.

### `rdfs:comment` Description

A textual description of the calendar's applicability to the associated place.

NOTE: the calendar itself may be described by a textual description associated with the calendar resource.  Where the same calendar is in use at several different places and/or times, it should be described just once.

### `em:when` Time period

Indicates a period during which the calendar was used at the associated place.


## Map reference

Annotation type: `em:MAP_RESOURCE`

Example annotation body:

    oa:hasBody 
      [ a em:Map_resource ;
        rdfs:label     "Map of Silesia from 1561" ;
        rdfs:comment   "Map of Silesia from 1561" ;
        em:short_label "1561" ;
        em:link        <https://davidrumsey.georeferencer.com/maps/613891568775/view> ;
        em:preview     <https://davidrumsey.georeferencer.com/maps/613891568775/view> ;
      ] ;


## Canonical URI (and alternate reference URIs)

Applied to merged place data to indicate URIs that can be used to identify a place.

Example:

    ex:Opole_P a em:Place, em:Place_merged ;
    em:canonicalURI ex:Opole_P ;
    em:alternateURI
      [ rdfs:label "GeoNames URI" ;
        em:link <http://sws.geonames.org/3090048/>
      ] ;
    em:place_data ex:Opole_P_EMPlaces, ex:Opole_P_GeoNames ;
    .

## Linkback

A linkback annotation records a reference to the associated place from some external or separate published data.  For example, if a third party has published some additional data about an EMPlaces place, it may share a reference to that additional data via a published linkback annotation.

The data model does not constrain how a linkback is published; e.g., it may be part of the EMPlaces data, or the additional data service, or via some third-party annotation store.

@@@TODO: not currently used


# Properties

@@TODO: Full documentation would include a description of all properties.  In due course, generate from Annalist definitions?

See: http://demo.annalist.net/annalist/c/EMPlaces_defs/l/Field_list/

