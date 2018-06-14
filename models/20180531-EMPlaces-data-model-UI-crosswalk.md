# EMPlaces Data model to UI crosswalk

UI sample for [Opole](../images/current_display.pdf).

Data model sample for [Opole](20180410-opole-example-data.ttl).

The crosswalk is presented here using SPARQL query patterns that could be used to access information for the cvarious UI elements.  This is not meant to imply that they should be implemented using SPARQL: in this instance, I'm just using SPARQL as a kind of formal specification for designating bits of the data model.

In each case, the variable `?place` is assumed to be bound to the root node for the place description.  So in the Opole example, that would be `ex:Opole_P`.

## Place name

    { ?place em:preferredName ?place_name }

## Alternate names

@@NOTE: we probably have to do some work here, as the intent is not to list *every* alternate name from  GeoNames, but to apply some heuristic so that a useful selection is displayed.  In any case, duplicate values should be eliminated.

    { ?place em:alternateName ?alternate_name }

@@NOTE This is currently under review, using instead:

    { ?place em:displayName ?display_name }

This would mean that selecting the appropriate names would be a task for data wrangling by Oxford rather than selection in the Timbuctoo web interface.




## Current hierarchy

This uses the `em:Qualified_relation` structure, but needs to select on relation types that are specific to the current administrative hierarchy.  (Other relation types are used for historical hierarchies, which may be qualified by time span values.)

Each place includes links to its immediate parents in a hierarchy, so to build the complete hierarchy will require multiple probes (or a rather clever SPARQL query) to traverse the hierarchy up to the top level.

This pattern accesses the administrative division parent of a populated place:

    { ?place em:hasRelation
        [ em:relationType em:P_PART_OF_A ;
          em:relationTo   ?administrative_division ;
          em:source         # OPTIONAL, may be repeated
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

N/A

@@TODO: Shouldn't this be down with the "Export" links?

## Permanent URI

    { ?place em:canonicalURI ?permanent_uri }

@@TODO: review this when we better understand Tibbuctoo URI/URL handling.

## Authorities

    { ?place em:coreDataRef
        [ rdfs:label ?authority_label ;
          em:link    ?authority_data
        ]
    }

Note: the `?authority_data` here identifies the authority *data* resource, not the authority's UREI for the the place itself.  I.e. this is a document reference; the intent is that this can be dereferenced to obtain the aurthroity's RDF data.

See also:

    { ?place em:alternateURI
        [ rdfs:label ?alternate_uri_label ;
          em:link    ?alternate_uri
        ] ;
    }

Here, the intent is that `?alternate_uri` is an alternative identifier for the place itself, which may be the reference gazetteer's URI.

@@TODO: I think this may need to be reviewed.  I suspect we should have a way to specify both an authority identifier and a corresponding authority data URL.

## Name attestations

Name attestations are based on web Annotations:

    { ?place em:hasAnnotation _:name_annotation .
      _:name_annotation
        oa:motivatedBy em:NAME_ATTESTATION ;
        oa:hasTarget   ?place ;   # should be redundant
        oa:hasBody     _:body
      OPTIONAL { 
        _:name_annotation em:when _:time_period .
        _:time_period rdfs:label ?time_period_label .
        OPTIONAL {
          _:time_period em:timespan _:time_span .
          OPTIONAL { _:time_span em:start ?time_span_start }
          OPTIONAL { _:time_span em:end   ?time_span_end }
          }
        }
      _:body em:name ?attestedname
      OPTIONAL { _:body em:language  ?attested_name_langcode }
      OPTIONAL { _:body rdfs:comment ?attested_name_comment }
      OPTIONAL { 
        _:name_annotation em:source
          [ rdfs:label   ?name_attestation_source_label ;
            rdfs:comment ?name_attestation_source_comment ;
            em:link      ?name_attestation_source_link ;
          ]
        }
    }

The SPARQL structure here is complicated by the optionality of some fields.
The underlying pattern is this:

    { ?place em:hasAnnotation
      [ oa:motivatedBy em:NAME_ATTESTATION ;
        oa:hasTarget   ?place ;   # should be redundant
        oa:hasBody 
          [ em:name      ?attestedname ;
            em:language  ?attestedname_langcode ;   # OPTIONAL
            rdfs:comment ?attested_name_comment ;   # OPTIONAL
          ] ;
        em:when                                     # OPTIONAL ??
          [ rdfs:label   ?time_period_label ;       # REQUIRED if period given
            emt:timespan                            # OPTIONAL
              [ emt:start ?time_span_start ;        # OPTIONAL
                emt:end   ?time_span_end ;          # OPTIONAL
              ]
          ] ;
        em:source                                   # OPTIONAL ??
          [ rdfs:label ?name_attestation_source_label ;
            em:link    ?name_attestation_source_link ;
          ]
        ]
    }

## Calendars

Calendar-in-use details are based on web Annotations.  The general pattern is this:

    { ?place em:hasAnnotation
      [ a oa:Annotation ;
        oa:motivatedBy em:CALENDAR_IN_USE ;
        oa:hasTarget   ?place ;   # should be redundant
        oa:hasBody 
          [ rdfs:label   ?calendar_label ;
            em:link      ?calendar_link             # OPTIONAL
          ] ;
        em:when                                     # OPTIONAL ??
          [ rdfs:label   ?time_period_label ;       # REQUIRED if period given
            et:timespan                             # OPTIONAL
              [ emt:start ?time_span_start ;        # OPTIONAL
                emt:end   ?time_span_end ;          # OPTIONAL
              ]
          ] ;
        em:source                                   # OPTIONAL ??
          [ rdfs:label ?calendar_source_label ;
            em:link    ?calendar_source_link ;
          ]
      ]
    }

## Related places

(None yet)

## Related resources

The intent here is that a related resource may be a descriptive label, a link, or both.
If no label provided, use the em:link value as the label.
If no link provided, present as plain text rather than as a hyperlink.

    { ?place em:relatedResource
      [ rdfs:label ?related_resource_label ;  # OPTIONAL
        em:link    ?related_resource_label ;  # OPTIONAL
      ]
    }

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

    { ?place em:hasRelation
      [ a em:Qualified_relation ;
        em:relationType em:AH_PART_OF_AH ;
        em:relationTo ?parent_adm ;
        em:when 
          [ a em:Time_period ;
            rdfs:label ?period_label ;
            em:timespan                             # OPTIONAL
              [ a em:Time_span ;                    # OPTIONAL
                em:start ?period_start_year ;       # OPTIONAL, integer value
                em:end   ?period_end_year ;         # OPTIONAL, integer value
                em:latestStart ?latest_start_year ; # OPTIONAL, integer value
                em:earliestEnd ?earliest_end_year ; # OPTIONAL, integer value
              ]
          ] ;
        em:source                                   # OPTIONAL
          [ rdfs:label ?relation_source_label ;     # OPTIONAL if em:link present
            em:link    ?relation_source_link ;      # OPTIONAL
          ]
        em:competence ?competence ;                 # OPTIONAL
      ]
    }

This pattern, where `?place` is bound to a current or historical place, accesses its immediate parents in a historical administrative hierarchy.  Note there may be several such parents with overlapping or non-overlapping time periods.  The pattern can be re-applied to the parents (i.e. values returned as ?parent_adm) to build up a adminstrative hierarchy graph.

### Eccliastical

(@@TBD)

### Military

(@@TBD)

### Judicial

(@@TBD)

