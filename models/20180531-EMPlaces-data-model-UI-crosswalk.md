# EMPlaces Data model to UI crosswalk

UI sample for [Opole](../images/current_display.pdf).

Data model sample for [Opole](20180410-opole-example-data.ttl).

The crosswalk is presented here using SPARQL query patterns that could be used to access info9rmation for the cvarious UI elements.  This is not meant to implie that they should be implemented using SPARQL: in this instanmce, I';m just using SPARQL as a ind of formal specification for designating bits of the data model.

In each case, the variable `?place` is assumed to be bound to the root node for the place description.  So in the Opole example, that would be `ex:Opole_P`.

## Place name

    { ?place em:preferredName ?place_name }

## Alternate names

NOTE: we probably have to do som,e work here, as the intent is not to list *every* elternate name from  Geonames, but to apply some heuristic so that a useful selection is displayed.  In any case, duplicate values should be eliminated.


    { ?place em:alternateName ?alternate_name }



## Current hierarchy

This uses the `em:Qualified_relation` structure, but needs to select on relation types that are specific to the current administrative hierarchy.  (Other relation types are used for historical hierarchies, which may be qualified by time span values.)

Each place includes links to its immediate parents in a hierarchy, so to build the complete hierarchy will require multiple probes (or a rather clever SPARQL query) to traverse the hierarchy up to the top level.

This pattern accesses the administrative division parent of a populated place:

    { ?place em:hasRelation
        [ em:relationType em:P_PART_OF_A ;
          em:relationTo   ?administrative_division ;
          em:source
            [ rdfs:label  ?parent_source_label ;
              em:link     ?parent_source_url
            ] ;
        ] ;
    }

This pattern, where `?administrative_division` is bound to an administrative division, accesses its immediate parent in the current administrative hierarchy:

    { ?administratve_division em:hasRelation
        [ em:relationType em:A_PART_OF_A ;
          em:relationTo   ?admin_parent_division ;
          em:source
            [ rdfs:label  ?admin_parent_source_label ;
              em:link     ?admin_parent_source_url
            ] ;
        ] ;
    }

The second pattern can be applied recursively until no result is returned.

## Location (current)

    { ?place em:where
        [ em:when emt:Current ;
          em:location
            [ wgs84_pos:lat  ?location_latitude ;
              wgs84_pos:long ?location_longitude
            ] ;
          em:source
            [ rdfs:label ?location_source_label ;
              em:link    ?location_source_url
            ]
        ]
    }

## Citation

## Permanent URI

## Authorities

## Name attestations

## Calendars

## Related places

(None yet)

## Related resources

## Bibliography

## Place record metadata

(@@TBD)

### Creator

### Contributors

### Reference gazetteers

### Licences

## Maps

### Current

### Historic

## Description

## Historical hierarchies

### Administrative

### Eccliastical

(@@TBD)

### Military

(@@TBD)

### Judicial

(@@TBD)

