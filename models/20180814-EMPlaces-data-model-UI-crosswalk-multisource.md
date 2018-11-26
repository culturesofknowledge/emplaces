# EMPlaces Data model to UI crosswalk

UI sample for [Opole](../images/current_display.pdf).

Data model sample for [Opole](20180802-opole-example-multisourced.ttl).

The crosswalk is presented here using SPARQL query patterns that could be used to access information for the cvarious UI elements.  This is not meant to imply that they should be implemented using SPARQL: in this instance, I'm just using SPARQL as a kind of formal specification for designating bits of the data model.

In each case, the variable `?place` is assumed to be bound to the root node for the place description.  So in the Opole example, that would be `ex:Opole_P` (c. line 328).

# Place multi-source structure

Each place description is formed using data from one or more sources.  Data from each resource is associated with a distinct `em:Place_sourced` resource, which may also include information about the source of the data.  Data which is generated and managed under local editorial control of the Cultures of Knowledge EMPlaces deployment is associated with the special source `ems:EMPlaces`.  The combined (or merged) data from all sources is represented by an `em:Place_merged` resource, which in turn references each of the contributing `em:Place_sourced` resources.

Example:

    ex:Opole_P a em:Place, em:Place_merged ;
        em:canonicalURI ex:Opole_P ;
        em:alternateURI
          [ rdfs:label "GeoNames URI" ;
            em:link <http://sws.geonames.org/3090048/>
          ] ;
        em:place_data ex:Opole_P_EMPlaces, ex:Opole_P_Geonames ;
        .

    ex:Opole_P_Geonames a em:Place, em:Place_sourced ;
        em:source
          [ a em:Authority ;
            rdfs:label "GeoNames data" ;
            em:link <http://sws.geonames.org/3090048/about.rdf>
          ] ;
        rdfs:label       "Opole (PPLA)" ;
        em:placeCategory gn:P ;             # from gn:featureClass
        em:placeType gn:P.PPLA ;            # from gn:featureCode
        em:preferredName "Opole" ;          # from gn:name
         :
        (etc.)

    ex:Opole_P_EMPlaces a em:Place_sourced ;
        em:source   ems:EMPlaces ;
        rdfs:label  "City of Opole" ;
         :
        (etc.)


# Place data

## Place name

The (preferred) place name is used as the main label used to identify the place in web page displays.

Pattern:

    { ?place em:place_data [ em:preferredName ?place_name ] }

Example:

    ex:Opole_P_Geonames a em:Place, em:Place_sourced ;
         :
        em:preferredName "Opole" ;


## Alternate names and display names

Alternate names are typically thoise in common use in multiple languages or scripts for referring to a place.  The alternate names are recorded in the data with language tags (where available).

Display names are a subset of of the alternate names with the language tags stripped and resulting duplicates removed.  (Often, the same alternate name string may appear with differeng language tags.)  This list of display names is shown under the main place name heading.

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

Pattern for accessing all display names:

    { ?place em:place_data [ em:displayName ?display_name ] }


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

This pattern, where `?administrative_division` is bound to a previously discovered administrative division, accesses its immediate parent in the current administrative hierarchy:

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

The goals are (a) to provide a clear way for users to cite a record, and (b) to ensure that contributors to a record can be credited.

@@TODO: add em:citation property with reference to em:Bib_entry (uses bibo)


## Permanent (canonical) and Alternate URIs

Note that the canonical and alternate URI properties are applied directly to the merged place resource.  These do not currently appear in the proposd UI.

Example:

    ex:Opole_P a em:Place, em:Place_merged ;
        em:canonicalURI ex:Opole_P ;
        em:alternateURI
          [ rdfs:label "GeoNames URI" ;
            em:link <http://sws.geonames.org/3090048/>
          ] ;
        em:place_data ex:Opole_P_EMPlaces, ex:Opole_P_Geonames ;
        .

Patterns:

    { ?place em:canonicalURI ?permanent_uri }

    { ?place em:alternateURI
        [ rdfs:label ?alternate_uri_label ;
          em:link    ?alternate_uri
        ] ;

Here, the intent is that `?alternate_uri` is an alternative identifier for the place itself, which may be a source gazetteer's reference URI.

See also: "Authorities" (below).


## Authorities (displayed as "See also")

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


## Name attestations

@@TODO: add citation/provenance/contributor section for annotations
@@TODO: allocate URIs for attestations (where, for our purposes, the `oa:Annotation` denotes the attestation)

Name attestations are based on web Annotations.  The annotation body has details of the name attestation.

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

    { ?place em:place_data
      [ em:hasAnnotation
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
      ]
    }


## Calendars

Calendar-in-use details are based on web Annotations.

Example:

    ex:Opole_P_EMPlaces a em:Place_sourced ;
         :
        em:hasAnnotation
          [ a oa:Annotation ;
            oa:motivatedBy em:CALENDAR_IN_USE ;
            oa:hasTarget   ex:Opole_P_EMPlaces ;
            oa:hasBody 
              [ a em:Calendar ;
                rdfs:label   "Gregorian" ;
                em:link      em:Gregorian ;
              ] ;
            em:when 
              [ a em:Time_period ;
                rdfs:label   "Since 23-Feb-1584" ;
                em:timespan
                  [ em:start  "1584-02-23" ;
                  ]
              ] ;
            em:source
              [ rdfs:label   "Tomsa, Jan: Počìtánì času (Základy teorie kalendáře). Praha 1995" ;
              ],
              [ rdfs:label   "Bláhová, Marie: Historická chronologie. Praha 2001" ;
              ] ;
            rdfs:comment "Gregorian since 23/02/1584. The actual switch took place on 12.2.1584. The next day then became the 23.2.1584." ;
            em:competence em:DEFINITIVE ;
          ] ;
         :

Pattern:

    { ?place em:place_data
      [ em:hasAnnotation
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
      ]
    }


## Related places

Example:

    ex:Opole_St_Adalbert_EMPlaces a em:Building, em:Place, em:Place_sourced ;
        rdfs:label       "Church of Our Lady of Sorrows and St. Adalbert"@en ;
        rdfs:comment     "Parish Church in Opole"@en ;
         :
        em:placeCategory gn:S ;
        em:placeType gn:S.CH ;
        em:preferredName "Church of Our Lady of Sorrows and St. Adalbert"@en ;
         :
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
         :

Pattern:

    { ?place em:place_data
      [ em:hasRelation
        [ em:relationTo ?populated_place ;
          em:relationType em:S_PART_OF_P ;
          em:competence ?competence ;       # OPTIONAL
          em:source
            [ rdfs:label ?source_label ;    # OPTIONAL
              em:link    ?source_link ;     # OPTIONAL
              em:licence ?source_licence ;  # OPTIONAL
            ] ;
        ] ;
      ]
    }


## Related resources

The intent here is that a related resource may be a descriptive label, a link, or both.
If no label provided, use the em:link value as the label.
If no link provided, present as plain text rather than as a hyperlink.

Example:

    ex:Opole_P_EMPlaces a em:Place, em:Place_sourced ;
         :
        em:relatedResource
          [ em:link <https://dolny-slask.org.pl> ],
          [ em:link <http://www.dokumentyslaska.pl> ],
           :
          [ rdfs:label "Babik, Zbigniew 2001: Najstarsza warstwa nazewnicza na ziemiach polskich w granicach wczesnośredniowiecznej Słowiańszczyzny, Kraków." ],
           :

Pattern:

    { ?place em:place_data
      [ em:relatedResource
        [ rdfs:label   ?related_resource_label ;   # OPTIONAL
          rdfs:comment ?related_resource_comment ; # OPTIONAL
          em:link      ?related_resource_link ;    # OPTIONAL
        ]
      ]
    }


## Bibliography

A collection of bibliographic resources that support or supplement the data provided.

Example:

    ex:Opole_P_EMPlaces a em:Place, em:Place_sourced ;
         :
        em:reference ex:Opole_Emmerling_Zajaczkowska ;
         :

    ex:Opole_Emmerling_Zajaczkowska a em:Bib_entry, bibo:Book ;
        dcterms:title "Oppeln/Opole: Die Hauptstadt der Wojewodschaft Oppeln" ;
        bibo:authorList (ex:Ryszard_Emmerling ex:Urszula_Zajaczkowska) ;
        dcterms:publisher ex:Slaskie_Wydawnictwo ;
        dcterms:date "2003" ;
        bibo:isbn10 "8391537137" ;
        bibo:isbn13 "978-8391537138" ;
        dcterms:source "https://www.amazon.com/Opole-Capital-of-Opolskie-Province/dp/B0021JGAOI" .

    ex:Ryszard_Emmerling a foaf:Person ;
        rdfs:label "Ryszard Emmerling" ;
        foaf:firstName "Ryszard" ;
        foaf:surname "Emmerling" .

    ex:Urszula_Zajaczkowska a foaf:Person ;
        rdfs:label "Urszula Zajączkowska" ;
        foaf:firstName "Urszula" ;
        foaf:surname "Zajączkowska" .

    ex:Slaskie_Wydawnictwo a foaf:Organization ;
        foaf:name "Wydawnictwo Śląskie" .

Pattern:

    { ?place em:place_data
      [ em:reference   ?bib_entry
      ]
    }

(Then access the ?bib_entry resource to obtain full details of the bibliographic reference.)

A SPARQL query to determine the number of bibliographic references provided for a given `?place` could be:

    SELECT (COUNT(DISTINCT ?bib_entry) AS ?bib_count)
    WHERE
    {
        ?place em:place_data [ em:reference ?bib_entry ]
    }

@@TODO: test this query

## Place record metadata

This will be for data provided automatically by Timbuctoo.

(@@TBD)

### Creator

(To be supplied by Timbuctoo?)

(@@TBD)

### Contributors

(To be supplied by Timbuctoo?)

(@@TBD)


## Maps

Map resource details are based on Web Annotations, and provide:

1. A link to a (possibly interactive) map that can be displayed in a new browser window,
2. A link to a preview image that can be displayed under a tab in the map display pane, and
3. A short label that is used to label a tab in the map display pane

Both current and historic maps use the same general pattern (see below for examples):

    { ?place em:place_data
      [ em:hasAnnotation
        [ oa:motivatedBy em:MAP_RESOURCE ;
          oa:hasBody 
            [ rdfs:label     ?map_label ;               # OPTIONAL
              rdfs:comment   ?map_description ;         # OPTIONAL
              em:short_label ?tab_label ;
              em:link        ?map_view_link ;
              em:preview     ?map_preview_link ;
            ] ;
          em:when                                       # OPTIONAL
            [ a em:Time_period ;
              rdfs:label     ?perod_label ;
              em:timespan
                [ em:start   ?period_start ;
                  em:end     ?period_end ;
                ]
            ] ;
          em:source
            [ rdfs:label     ?map_source_label ;        # OPTIONAL
              em:link        ?map_source_link ;         # OPTIONAL
            ] ;
        ]
      ]
    }

### Current

Example:

    ex:Opole_P_Geonames a em:Place, em:Place_sourced ;
         :
        em:hasAnnotation
          [ a oa:Annotation ;
            oa:motivatedBy em:MAP_RESOURCE ;
            oa:hasTarget ex:Opole_P_EMPlaces ;
            oa:hasBody 
              [ rdfs:label     "Current map for Opole" ;
                rdfs:comment   "Current map for Opole" ;
                em:short_label "Current" ;       # Used for tab label
                em:link        <http://www.geonames.org/3090048/opole.html> ;
                em:preview     <http://www.geonames.org/3090048/opole.html> ;
              ] ;
            em:when emt:Current ;
            em:source
              [ a em:Authority ;
                rdfs:label "GeoNames data" ;
                em:link <http://sws.geonames.org/3090048/about.rdf>
              ] ;
          ] ;
         :

### Historic

Example:

    ex:Opole_P_EMPlaces a em:Place, em:Place_sourced ;
         :
        em:hasAnnotation
          [ a oa:Annotation ;
            oa:motivatedBy em:MAP_RESOURCE ;
            oa:hasTarget   ex:Opole_P_EMPlaces ;
            oa:hasBody 
              [ a em:MapResource ;
                rdfs:label     "Map of Silesia in 1561" ;
                rdfs:comment   "Map of Silesia in 1561" ;
                em:short_label "1561" ;   # Used for tab label
                em:link      <https://davidrumsey.georeferencer.com/maps/613891568775/view> ;
                em:preview   <https://davidrumsey.georeferencer.com/maps/613891568775/view> ;
              ] ;
            em:when 
              [ a em:Time_period ;
                rdfs:label   "1561" ;
                em:timespan
                  [ em:start  "1561" ;
                    em:end    "1561" ;
                  ]
              ] ;
            em:source
              [ rdfs:label   "David Rumsey Map Collection" ;
              ] ;
          ],
         :

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

Tab labels fornthe different hierarchies (administrative, ecclesiastical, military, judicial, etc.) will be determined by the relation type used; thus the relatrion type used here (`em:AH_PART_OF_AH`) would correspond to a historical administrative hierarchy.  Labels for the date ranges will need to be determined dynamically from the graph of hierarchies over time (e.g. find all paths in the hierarchy graph, and for each path determine the common date ranges for each relation.)

### Ecclesiastical

(@@TBD - similar pattern to above, but may also need to include denominational data)

### Military

(@@TBD - similar pattern to above)

### Judicial

(@@TBD - similar pattern to above)

