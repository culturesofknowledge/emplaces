# EMPlaces Data model to UI crosswalk

UI sample for [Opole](../images/current_display.pdf).

Data model sample for [Opole](20180802-opole-example-multisourced.ttl).

The crosswalk is presented here using SPARQL query patterns that could be used to access information for the cvarious UI elements.  This is not meant to imply that they should be implemented using SPARQL: in this instance, I'm just using SPARQL as a kind of formal specification for designating bits of the data model.

In each case, the variable `?place` is assumed to be bound to the root node for the place description.  So in the Opole example, that would be `ex:Opole_P` (c. line 328).

# Place multi-source structure @@@

Each place description is formed from multiple collections of data, each from a single source. @@@@

Example:

    ex:Opole_P a em:Place, em:Place_merged ;
        em:canonicalURI ex:Opole_P ;
        em:alternateURI
          [ rdfs:label "GeoNames URI" ;
            em:link <http://sws.geonames.org/3090048/>
          ] ;
        em:place_data ex:Opole_P_EMPlaces, ex:Opole_P_Geonames ;
        .

    ex:Opole_P_EMPlaces a em:Place_sourced ;
        em:source   ems:EMPlaces ;
        rdfs:label  "City of Opole" ;
         :
        (etc.)


# Place data

@@@@ copied from older document; needs revision @@@@

@@@@ Add example snippets in each case

## Place name

Pattern:

    { ?place em:place_data [ em:preferredName ?place_name ] }

Example:

    ex:Opole_P_Geonames
         :
        em:preferredName "Opole" ;


## Alternate names and display names

@@@ reword this

@@NOTE: we probably have to do some work here, as the intent is not to list *every* alternate name from  GeoNames, but to apply some heuristic so that a useful selection is displayed.  In any case, duplicate values should be eliminated.

Patterns:

    { ?place em:place_data [ em:alternateName ?alternate_name ] }

@@NOTE This is currently under review, using instead:

    { ?place em:place_data [ em:displayName ?display_name ] }

Example:

    ex:Opole_P_Geonames a em:Place, em:Place_sourced ;
         :
        em:alternateName "Opole" ;
        em:alternateName "Oppein" ;
        em:alternateName "Oppeln" ;
        em:alternateName "오폴레"@ko ;
        em:alternateName "オポーレ"@ja ;
        em:alternateName "ออปอเล"@th ;
        em:alternateName "Opole"@da ;
        em:alternateName "Opole"@en ;
        em:alternateName "Opole"@eo ;
         :
        em:displayName "Opole" ;
        em:displayName "Oppein" ;
        em:displayName "Oppeln" ;
         :

## Current hierarchy

This uses the `em:Qualified_relation` structure, but needs to select on relation types that are specific to the current administrative hierarchy.  (Other relation types are used for historical hierarchies, which may be qualified by time span values.)

Each place includes links to its immediate parents in a hierarchy, so to build the complete hierarchy will require multiple probes (or a rather clever SPARQL query) to traverse the hierarchy up to the top level.

Example:

    ex:Opole_P_Geonames a em:Place, em:Place_sourced ;
             :
        em:hasRelation
          [ a em:Qualified_relation ;
            em:relationTo ex:Opole_ADM3 ;
            em:relationType em:P_PART_OF_A ;
            em:competence em:DEFINITIVE ;
            em:source
              [ rdfs:label "GeoNames data" ;
                em:link <http://sws.geonames.org/3090048/about.rdf>
              ] ;
          ] ;

     :

    em:P_PART_OF_A a em:Relation_type ;
        em:fromType   gn:P ;
        em:toType     gn:A ;
        rdfs:label    "Administered by" ;
        rdfs:comment  "Relates a populated place to its administrative division." 
        .

     :

    gn:P a skos:Concept ; 
        rdfs:label "Populated place" ;
        rdfs:comment "Populated place - from GeoNames (feature class)." 
        .
    
    gn:A  a skos:Concept ; 
        rdfs:label   "Administrative division" ;
        rdfs:comment "Administrative division - from GeoNames (feature class)." 
        .


This pattern accesses the administrative division parent of a populated place:

Pattern:

    { ?place em:place_data
        [ em:hasRelation
            [ em:relationType em:P_PART_OF_A ;
              em:relationTo   ?administrative_division ;
              em:source         # OPTIONAL, may be repeated
                [ rdfs:label  ?parent_source_label ;
                  em:link     ?parent_source_url
                ] ;
            ] ;
        ]
    }

This pattern, where `?administrative_division` is bound to an administrative division, accesses its immediate parent in the current administrative hierarchy:

    { ?administratve_division em:place_data
        [  em:hasRelation
            [ em:relationType em:A_PART_OF_A ;
              em:relationTo   ?admin_parent_division ;
              em:source
                [ rdfs:label  ?admin_parent_source_label ;
                  em:link     ?admin_parent_source_url
                ] ;
            ] ;
        ]
    }

The second pattern can be applied recursively until no result is returned.

## Location (current)

The location is a latitide and longitude value pair indicating a nomninal location for a place or region, referred to the Greenwich meridian.

(A pop-up coukd be provided to show alternative-meridian locations for a place, but we anticipate this would be performed by a simple calculation when generating the display, and driven by a table of alternative meridians described with label and longitude offset values.)

Example:

    ex:Opole_P_Geonames a em:Place, em:Place_sourced ;
         :
        em:where
          [ a em:Setting ;
            em:location
              [ a em:Location_value ;
                wgs84_pos:lat  "50.67211"^^xsd:double ;
                wgs84_pos:long "17.92533"^^xsd:double ;
              ] ;
            em:when emt:Current ;
            em:source
              [ rdfs:label "GeoNames data" ;
                em:link <http://sws.geonames.org/3090048/about.rdf>
              ] ;
          ] ;

Pattern:

    { ?place em:place_data
        [ em:where
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
        ]
    }

## Citation

The goals are (a) to provide a clear way for users to cite a record, and (b) toi ensure that controbutors to a record can be credited.

@@TODO: add em:citation property with reference to em:Bib_entry (uses bibo)


## Permanent (canonical) URI

Note that the canonical URI property is applied directly to the merged place data resource.

Example:

    @@@@

Pattern:

    { ?place em:canonicalURI ?permanent_uri }

@@@@ Planning to use ARKs.

See also:

    { ?place em:alternateURI
        [ rdfs:label ?alternate_uri_label ;
          em:link    ?alternate_uri
        ] ;
    }

Here, the intent is that `?alternate_uri` is an alternative identifier for the place itself, which may be a source gazetteer's reference URI.

@@TODO:  review this - should it applie to the source data??


## Authorities

Each `em:Place_sourced` resource that contributes a place data record has associated source data information.  Thus, the contributing authorities for merged place information can be discovered by examining the source information for the resources referenced using the `em:place_data` property.

Example:

    ex:Opole_P_Geonames a em:Place, em:Place_sourced ;
         :
        em:source
          [ a em:Authority ;
            rdfs:label "GeoNames data" ;
            em:link <http://sws.geonames.org/3090048/about.rdf>
          ] ;

Pattern:

    { ?place em:place_data
        [ em:source
            [ a em:Authority ;
              rdfs:label ?authority_label ;
              em:link    ?authority_data
            ]
        ]
    }

Note: the `?authority_data` here identifies the authority *data* resource, not the authority's URI for the the place itself.  I.e. this is a document reference; the intent is that this can be dereferenced to obtain the aurtority's RDF data.

@@TODO: revioew how to handle locally added data (e.g. ems:EMLO in diagrams)

## Name attestations

@@TODO: add citation/provenance/contributor section for annotations
@@TODO: allocate URIs for attestations (where for our purposes, the oa:Annotation denotes the attestation)

Name attestations are based on web Annotations.  The annotation body is details of the name attestation

Example:

ex:Opole_P_EMPlaces a em:Place_sourced ;
     :
    em:hasAnnotation
      [ a oa:Annotation ;
        oa:motivatedBy em:NAME_ATTESTATION ;
        oa:hasTarget   ex:Opole_P_EMPlaces ;
        oa:hasBody 
          [ a em:Place_name ;
            em:name      "Opole" ;
            em:language  eml:pl ;
            rdfs:comment "Polish" ;
          ] ;
        em:when 
          [ a em:Time_period ;
            rdfs:label   "1146-(today)" ;
            em:timespan
              [ em:start "1146" ;
              ]
          ] ;
        em:source
          [ rdfs:label   "Arno Bosse / Dariusz Gierczak" ;
            rdfs:comment "Heinrich Adamy: Die Schlesischen Ortsnamen ihre entstechung und bedeutung. Breslau." ;
          ] ;
        em:competence em:DEFINITIVE ;
      ] ,
     :

Pattern:

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
          [ rdfs:label    ?calendar_label ;
            em:link       ?calendar_link            # OPTIONAL
          ] ;
        em:when                                     # OPTIONAL ??
          [ rdfs:label    ?time_period_label ;      # REQUIRED if period given
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



Example:


    em:hasRelation
      [ a em:Qualified_relation ;
        em:relationTo ex:Opole_P ;
        em:relationType em:S_PART_OF_P ;
        em:competence em:DEFINITIVE ;
        em:source
          [ rdfs:label "Wikidata" ;
            em:link <https://www.wikidata.org/wiki/Q55338793>
          ] ;
      ] ;


Pattern:




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

(@@TBD)

## Place record metadata

(@@TBD)

### Creator

### Contributors

### Reference gazetteers

### Licences

## Maps

### Current

(@@TBD)

### Historic

(@@TBD)

## Description

    { ?place em:editorialNote ?description }

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

