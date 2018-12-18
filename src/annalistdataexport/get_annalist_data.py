# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# get_annalist_data.py - command line tool to create EMPlaces core from Annalist data
#

from __future__ import print_function
from __future__ import unicode_literals

__author__      = "Graham Klyne (GK@ACM.ORG)"
__copyright__   = "Copyright 2018, Graham Klyne and University of Oxford"
__license__     = "MIT (http://opensource.org/licenses/MIT)"

import sys
import os
import os.path
import re
import argparse
import urlparse
import logging
import errno

from rdflib         import Graph, Namespace, URIRef, Literal, BNode, RDF, RDFS
from rdflib.paths   import Path

from getargvalue    import getargvalue, getarg
from dataextractmap import DataExtractMap

log = logging.getLogger(__name__)

dirhere = os.path.dirname(os.path.realpath(__file__))
gadroot = os.path.dirname(os.path.join(dirhere))
sys.path.insert(0, gadroot)

#   ===================================================================
#
#   Data constants
#
#   ===================================================================

#   Software version

GAD_VERSION = "0.1"

#   Status return codes

GAD_SUCCESS             = 0         # Success
GAD_BADCMD              = 2         # Command error
GAD_UNKNOWNCMD          = 3         # Unknown command
GAD_UNIMPLEMENTED       = 4         # Unimplemented command or feature
GAD_UNEXPECTEDARGS      = 5         # Unexpected arguments supplied
GAD_NO_PLACE_REFS       = 6         # No place ids given
GAD_NO_ANNALIST_URL     = 7         # No Annalist URL
GAD_SOME_ANNALIST_URLS  = 8         # Some but not all all URLs matched GeoNames IDs

#   Namespaces

SKOS      = Namespace("http://www.w3.org/2004/02/skos/core#")
XSD       = Namespace("http://www.w3.org/2001/XMLSchema#")

OA        = Namespace("http://www.w3.org/ns/oa#")
CC        = Namespace("http://creativecommons.org/ns#")
DCTERMS   = Namespace("http://purl.org/dc/terms/")
FOAF      = Namespace("http://xmlns.com/foaf/0.1/")
BIBO      = Namespace("http://purl.org/ontology/bibo/")

ANNAL     = Namespace("http://purl.org/annalist/2014/#")    # Annalist ontology
GN        = Namespace("http://www.geonames.org/ontology#")  # GeoNames ontology
GEONAMES  = Namespace("http://sws.geonames.org/")           # GeoNames place 
WGS84_POS = Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#")
EM        = Namespace("http://id.emplaces.info/vocab/")
EMP       = Namespace("http://id.emplaces.info/timeperiod/")
EMT       = Namespace("http://id.emplaces.info/timespan/")
EML       = Namespace("http://id.emplaces.info/language/")
EMS       = Namespace("http://id.emplaces.info/source/")
EMC       = Namespace("http://id.emplaces.info/calendar/")

PLACE     = Namespace("http://id.emplaces.info/place/")
AGENT     = Namespace("http://id.emplaces.info/agent/")
REF       = Namespace("http://id.emplaces.info/reference/")

# Base URL for collection
# (@@TODO: extract this automatically from supplied reference)

COLLECTION_BASE = "http://localhost:8000/annalist/c/EMPlaces_defs/d"

#   ===================================================================
#
#   Common definitions for EMPlaces data
#
#   ===================================================================

# @@TODO: refactor

COMMON_PREFIX_DEFS = (
    """
    @prefix rdf:        <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs:       <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix owl:        <http://www.w3.org/2002/07/owl#> .
    @prefix skos:       <http://www.w3.org/2004/02/skos/core#> .
    @prefix xsd:        <http://www.w3.org/2001/XMLSchema#> .
    @prefix oa:         <http://www.w3.org/ns/oa#> .
    
    @prefix cc:         <http://creativecommons.org/ns#> .
    @prefix dcterms:    <http://purl.org/dc/terms/> .
    @prefix foaf:       <http://xmlns.com/foaf/0.1/> .
    @prefix bibo:       <http://purl.org/ontology/bibo/> .
    
    @prefix geonames:   <http://sws.geonames.org/> .                # GeoNames place IDs
    @prefix gn:         <http://www.geonames.org/ontology#> .       # GeoNames vocabulary terms
    @prefix wgs84_pos:  <http://www.w3.org/2003/01/geo/wgs84_pos#> .
    
    @prefix em:         <http://id.emplaces.info/vocab/> .
    @prefix emp:        <http://id.emplaces.info/timeperiod/> .
    @prefix emt:        <http://id.emplaces.info/timespan/> .
    @prefix eml:        <http://id.emplaces.info/language/> .
    @prefix ems:        <http://id.emplaces.info/source/> .
    @prefix emc:        <http://id.emplaces.info/calendar/> .

    @prefix place:      <http://id.emplaces.info/place/> .          # Canonical place URIs
    @prefix agent:      <http://id.emplaces.info/agent/> .          # People and institutions
    @prefix ref:        <http://id.emplaces.info/reference/> .      # Bibliographic entries
    """)

COMMON_EMPLACES_DEFS = (
    """
    em:Place a rdfs:Class ;
        rdfs:label "Place" ;
        rdfs:comment
            '''
            A resource that provides information about a place (which is 
            considered in the sense of being "constructed by human experience").
            '''
        .

    em:Place_sourced a rdfs:Class ;
        rdfs:subClassOf em:Place ;  #@@TODO: review this
        rdfs:label "Place information from single source" ;
        rdfs:comment
            '''
            A resource that provides information about a place that comes from 
            a single source.  Property `em:source` references a description of 
            that source.
            '''
        .

    em:Place_merged
        rdfs:subClassOf em:Place ;  #@@TODO: review this
        rdfs:label "Place information merged from multiple sources" ;
        rdfs:comment
            '''
            A resource that provides information about a place that comes from 
            multiple sources.  One or more em:place_data properties reference 
            single-sourced information about the place.
            '''
        .

    # Time period for "current" data
    emp:Current a em:Time_period ;
        rdfs:label   "Current, as of 2018" ;
        rdfs:comment "For ease of retrieval, use this specific resource to label any current information (e.g. data extracted from GeoNames).  Additional Timespan values could be indicated if required to convey more specific information." ;
        em:timespan
          [ a em:Time_span ;
            em:latestStart: "2018" ;
            em:earliestEnd: "2018" ;
          ]
        .

    #   Combined place type to avoid having to create extra historical places 
    #   corresponding to a current P.  References GeoNames place types.
    #   See also relation type em:AH_PART_OF_AH.
    em:P_OR_A a skos:Concept ;
        skos:broader gn:A ;
        skos:broader gn:P ;
        rdfs:label    "Former populated place or admin division" ;
        rdfs:comment  "Former populated place or administrative division, used in historical administrative relations" 
        .

    # Place relations
    em:P_PART_OF_A a em:Relation_type ;
        em:fromType   gn:P ;
        em:toType     gn:A ;
        rdfs:label    "Administered by" ;
        rdfs:comment  "Relates a populated place to its administrative division." 
        .
    em:A_PART_OF_A a em:Relation_type ;
        em:fromType   gn:A ;
        em:toType     gn:A ;
        rdfs:label    "Subdivision of" ;
        rdfs:comment  "Relates a subdivision of an administrative division to its parent division." 
        .
    em:AH_PART_OF_AH a em:Relation_type ;
        em:fromType   em:P_OR_A ;
        em:toType     gn:A ;
        rdfs:label    "Former part of" ;
        rdfs:comment  "Records a historical relationship between a historical place or administrative division and its parent division." 
        .
    em:S_PART_OF_P a em:Relation_type ;
        em:fromType   gn:S ;
        em:toType     gn:P ;
        rdfs:label    "Located within" ;
        rdfs:comment  "Relates a spot feature to a populated place within which it may be found."
        #@@NOTE: this is quite specific - we may later want to allow for 
        #        a looser style of relationship; e.g. `em:S_PART_OF_PA`
        .

    # Information competence (certainty)
    #
    # Information in a qualified relation or annotation may be uncertain.  These properties and 
    # values are used to qualify these claims.  Information that is directly attached to an 
    # em:Place (i.e. not as a qualified relation or annotation) is considered to be definitive.
    #
    # Specifically, annotations for calendar-in-use and alternate name attestations should have 
    # associated competence values.
    #
    # Approximate date ranges are represented by range values in the corresponding 
    # Timespan value.
    em:competence a rdf:Property ;
        rdfs:label "Certainty, or quality, of information" ;
        rdfs:comment "Records the quality or certaintly of some information.  Note that in the absence of an explicit value, no competence should be assumed." ;
        rdfs:range em:Competence_value ;
        .
    em:DEFINITIVE a em:Competence_value ;
        rdfs:label   "Definitive" ;
        rdfs:comment "The associated value is definitively true for the purposes of EMPlaces.  Such information should ideally be backup up be appropiate source references."
        .
    em:INFERRED a em:Competence_value ;
        rdfs:label   "Inferred" ;
        rdfs:comment "The associated value has been inferred from (preferably?) definitive informaton."
        .
    em:ASSUMED a em:Competence_value ;
        # Assumed data is like uncertain, but maybe with better foundation?
        rdfs:label   "Assumed" ;
        rdfs:comment "The associated value is assumed from context."
        .
    em:UNCERTAIN a em:Competence_value ;
        rdfs:label   "Uncertain" ;
        rdfs:comment "The associated value is uncertain."
        .
    em:APPROXIMATE a em:Competence_value ;
        rdfs:label   "Approximate" ;
        rdfs:comment "The associated value is a date whose value is only approximately known.  @@NOTE: this value may prove spurious, as timespan already has a way to represent approximation ranges."
        .

    # Use em:corePlaceType for place type info that is obtained, and 
    # may be refreshed,from the reference gazetteer(s)
    em:corePlaceType rdfs:subPropertyOf em:placeType .

    # em:coreDataRef indicates source (reference gazetteer) for core data
    # Use em:source for other gazetteer references
    em:coreDataRef rdfs:subPropertyOf em:source .

    # Annotation motivations
    em:MAP_RESOURCE a oa:Motivation ;
        rdfs:label "Map resource" ;
        rdfs:comment "References a current or historical map resource associated with a place." ;
        .
    em:NAME_ATTESTATION
        rdfs:label "Name attestation" ;
        rdfs:comment "References a historical name attestation for a place, with source and compenence information." ;
        .
    em:CALENDAR_IN_USE
        rdfs:label "Calendar in use" ;
        rdfs:comment "References a historical calendar used in a place, with source and compenence information." ;
        .
    em:DEDICATED_TO a oa:Motivation ;
        rdfs:label "Dedicated to" ;
        rdfs:comment "Generally used with a related place that is a church or a place or worship, to indicate a person or historical figure to whom the place has been dedicated.  The annotation body directly references a resource for the dedicatee, which is assumed to have an rdfs:label value that can be used for display purposes." ;
        .
    em:USED_FOR a oa:Motivation ;
        rdfs:label "Used for" ;
        rdfs:comment "Generally used with a related place that is a building or site for some activity, to indicate a purpose for which the place was used.  The annotation body directly references a resource describing the purpose, which is assumed to have an rdfs:label value that can be used for display purposes.  The annotation itself may carry a temporal constraint (`em:where`) that gives some indication of when the place was used for that purpose." ;
        .
    """)

COMMON_GEONAMES_DEFS = (
    """
    # Place categories
    gn:P a skos:Concept ; 
        rdfs:label "Populated place" ;
        rdfs:comment "Populated place - from GeoNames (feature class)." 
        .
    gn:A  a skos:Concept ; 
        rdfs:label   "Administrative division" ;
        rdfs:comment "Administrative division - from GeoNames (feature class)." 
        .

    gn:S a skos:Concept ; 
        rdfs:label "Spot feature" ;
        rdfs:comment "Spot feature (spot, building, farm)." 
        .

    # Place types
    gn:P.PPL a skos:Concept ;
        skos:narrower gn:P ;
        rdfs:label    "Populated place" ;
        rdfs:comment  "A populated place (town, city, village, etc.)." 
        .
    gn:P.PPLA a skos:Concept ;
        skos:narrower gn:P ;
        rdfs:label    "Seat of 1st-order admin div" ;
        rdfs:comment  "Populated place that is a seat of a first-order administrative division." 
        .
    gn:P.PPLH a skos:Concept ;
        skos:narrower gn:P ;
        rdfs:label    "Former populated place" ;
        rdfs:comment  "A former populated place that no longer exists." 
        .
    gn:A.PCLI a skos:Concept ;
        skos:narrower gn:A ;
        rdfs:label    "Independent political entity" ;
        rdfs:comment  "An independent political entity, typically a country."
        .
    gn:A.ADM1 a skos:Concept ;
        skos:narrower gn:A ;
        rdfs:label    "First-order admin division" ;
        rdfs:comment  "A primary administrative division of a country, such as a state in the United States."
        .
    gn:A.ADM2 a skos:Concept ;
        skos:narrower gn:A ;
        rdfs:label    "Second-order admin division" ;
        rdfs:comment  "A subdivision of a first-order administrative division."
        .
    gn:A.ADM3 a skos:Concept ;
        skos:narrower gn:A ;
        rdfs:label    "Third-order admin division" ;
        rdfs:comment  "A subdivision of a second-order administrative division."
        .
    gn:A.PCLH a skos:Concept ;
        skos:narrower gn:A ;
        rdfs:label    "Former independent political entity" ;
        rdfs:comment  "A former independent political entity, typically a country."
        .
    gn:A.ADM1H a skos:Concept ;
        skos:narrower gn:A ;
        rdfs:label    "Former first-order admin division" ;
        rdfs:comment  "A former first-order administrative division."
        .
    gn:A.ADM2H a skos:Concept ;
        skos:narrower gn:A ;
        rdfs:label    "Former second-order admin division" ;
        rdfs:comment  "A former first-order administrative division."
        .
    gn:A.ADM3H a skos:Concept ;
        skos:narrower gn:A ;
        rdfs:label    "Former Third-order admin division" ;
        rdfs:comment  "A former third-order administrative division."
        .

    gn:S.CH a skos:Concept ;
        skos:narrower gn:S ;
        rdfs:label    "Church" ;
        rdfs:comment  "A church; a building for public Christian worship." 
        .

    #@@ more to add here
    """)

COMMON_LANGUAGE_DEFS = (
    """
    # Language resources @@TODO: generate as-needed@@
    eml:en a em:Language_value ;
        # em:tag "en" ; 
        em:tag_639_1 "en" ;
        em:tag_639_2 "eng" ;
        rdfs:label   "English" ;
        rdfs:comment "# English" ;
        .

    eml:de a em:Language_value ;
        # em:tag "de" ; 
        em:tag_639_1 "de" ;
        em:tag_639_2 "deu" ;
        rdfs:label   "German" ;
        rdfs:comment "# German" ;
        .
        
    eml:pl a em:Language_value ;
        # em:tag "pl" ; 
        em:tag_639_1 "pl" ;
        em:tag_639_2 "pol" ;
        rdfs:label   "Polish" ;
        rdfs:comment "# Polish" ;
        .

    eml:la a em:Language_value ;
        # em:tag "la" ; 
        em:tag_639_1 "la" ;
        em:tag_639_2 "lat" ;
        rdfs:label   "Latin" ;
        rdfs:comment "# Latin" ;
        .
    """)

#   ===================================================================
#
#   RDF mapping data
#
#   ===================================================================

M = DataExtractMap

annalist_reference_mapping = M.ref_subgraph(
    # If an `annal:uri` value is defined for an entity, use it to
    # refer to that entity.
    M.tgt_subj, M.src_prop, M.src_obj,
    [ M.set_subj(M.prop_eq(ANNAL.uri),      M.src_obj)
    ])

annalist_resource_copy = M.ref_subgraph(
    M.tgt_subj, M.src_prop, M.src_obj,
    [ M.set_subj(M.prop_eq(ANNAL.uri),          M.src_obj)
    , M.emit(M.prop_eq(ANNAL.id),               M.stmt_copy())
    , M.emit(M.prop_eq(ANNAL.type_id),          M.stmt_copy())
    , M.emit(M.prop_nsne(ANNAL[None]),          M.stmt_copy())
    ])

annalist_when_mapping = M.ref_subgraph(
    M.tgt_subj, M.src_prop, M.src_obj,
    [ M.set_subj(M.prop_eq(ANNAL.uri),          M.src_obj)
    , M.emit(M.prop_eq(RDF.type),               M.stmt_copy())
    , M.emit(M.prop_eq(RDFS.label),             M.stmt_copy())
    , M.emit(M.prop_eq(RDFS.comment),           M.stmt_copy())
    , M.emit(M.prop_eq(ANNAL.id),               M.stmt_copy())
    , M.emit(M.prop_eq(ANNAL.type_id),          M.stmt_copy())
    , M.emit(M.prop_eq(EM.time_period), # em:time_period
        M.ref_subgraph(
            M.tgt_subj, M.src_prop, M.src_obj,
            [ M.set_subj(M.prop_eq(ANNAL.uri),          M.src_obj)
            , M.emit(M.prop_eq(RDF.type),               M.stmt_copy())
            , M.emit(M.prop_eq(RDFS.label),             M.stmt_copy())
            , M.emit(M.prop_eq(RDFS.comment),           M.stmt_copy())
            , M.emit(M.prop_eq(ANNAL.id),               M.stmt_copy())
            , M.emit(M.prop_eq(ANNAL.type_id),          M.stmt_copy())
            , M.emit(M.prop_eq(EM.timespan),     # em:timespan
                M.ref_subgraph(
                    M.tgt_subj, M.src_prop, M.src_obj,
                    [ M.set_subj(M.prop_eq(ANNAL.uri),          M.src_obj)
                    , M.emit(M.prop_eq(RDF.type),               M.stmt_copy())
                    , M.emit(M.prop_eq(RDFS.label),             M.stmt_copy())
                    , M.emit(M.prop_eq(RDFS.comment),           M.stmt_copy())
                    , M.emit(M.prop_eq(EM.start),               M.stmt_copy())
                    , M.emit(M.prop_eq(EM.end),                 M.stmt_copy())
                    ])
                )
            ])
        )
    ])

annalist_source_mapping = M.ref_subgraph(
    M.tgt_subj, M.src_prop, M.src_obj,
    [ M.set_subj(M.prop_eq(ANNAL.uri),          M.src_obj)
    , M.emit(M.prop_eq(RDF.type),               M.stmt_copy())
    , M.emit(M.prop_eq(RDFS.label),             M.stmt_copy())
    , M.emit(M.prop_eq(RDFS.comment),           M.stmt_copy())
    , M.emit(M.prop_eq(ANNAL.id),               M.stmt_copy())
    , M.emit(M.prop_eq(ANNAL.type_id),          M.stmt_copy())
    , M.emit(M.prop_eq(EM.link),                M.stmt_copy_obj_ne(COLLECTION_BASE+"/"))
    , M.emit(M.prop_eq(EM.short_label),         M.stmt_copy())
    ])

annalist_location_mapping = M.ref_subgraph(
    M.tgt_subj, M.src_prop, M.src_obj,
    [ M.set_subj(M.prop_eq(ANNAL.uri),          M.src_obj)
    , M.emit(M.prop_eq(RDF.type),               M.stmt_copy())
    , M.emit(M.prop_eq(RDFS.label),             M.stmt_copy())
    , M.emit(M.prop_eq(RDFS.comment),           M.stmt_copy())
    , M.emit(M.prop_eq(ANNAL.id),               M.stmt_copy())
    , M.emit(M.prop_eq(ANNAL.type_id),          M.stmt_copy())
    , M.emit(M.prop_eq(WGS84_POS.lat),          M.stmt_copy())
    , M.emit(M.prop_eq(WGS84_POS.long),         M.stmt_copy())
    ])

annalist_where_mapping = M.ref_subgraph(
    M.tgt_subj, M.src_prop, M.src_obj,
    [ M.set_subj(M.prop_eq(ANNAL.uri),          M.src_obj)
    , M.emit(M.prop_eq(RDF.type),               M.stmt_copy())
    , M.emit(M.prop_eq(RDFS.label),             M.stmt_copy())
    , M.emit(M.prop_eq(RDFS.comment),           M.stmt_copy())
    , M.emit(M.prop_eq(ANNAL.id),               M.stmt_copy())
    , M.emit(M.prop_eq(ANNAL.type_id),          M.stmt_copy())
    , M.emit(M.prop_eq(EM.location),            annalist_location_mapping)
    , M.emit(M.prop_eq(EM.when),                annalist_when_mapping)
    , M.emit(M.prop_eq(EM.source),              annalist_source_mapping)
    ])

annalist_reference_mapping = M.ref_subgraph(
    M.tgt_subj, M.src_prop, M.src_obj,
    [ M.set_subj(M.prop_eq(ANNAL.uri),      M.src_obj)
    , M.emit(M.prop_eq(RDF.type),           M.stmt_copy())
    , M.emit(M.prop_eq(RDFS.label),         M.stmt_copy())
    , M.emit(M.prop_eq(RDFS.comment),       M.stmt_copy())
    , M.emit(M.prop_eq(ANNAL.id),           M.stmt_copy())
    , M.emit(M.prop_eq(ANNAL.type_id),      M.stmt_copy())
    , M.emit(M.prop_eq(DCTERMS.title),      M.stmt_copy())
    , M.emit(M.prop_eq(DCTERMS.publisher),  annalist_reference_mapping)
    , M.emit(M.prop_eq(DCTERMS.date),       M.stmt_copy())
    , M.emit(M.prop_eq(DCTERMS.source),     M.stmt_copy())
    , M.emit(M.prop_eq(BIBO.authorList),
        M.ref_list(
            M.tgt_subj, M.src_prop, M.src_obj,
            [ M.set_subj(M.prop_eq(ANNAL.uri),      M.src_obj)
            , M.emit(M.prop_eq(RDF.type),           M.stmt_copy())
            , M.emit(M.prop_eq(RDFS.label),         M.stmt_copy())
            , M.emit(M.prop_eq(RDFS.comment),       M.stmt_copy())
            , M.emit(M.prop_eq(ANNAL.id),           M.stmt_copy())
            , M.emit(M.prop_eq(ANNAL.type_id),      M.stmt_copy())
            ])
        )
    , M.emit(M.prop_eq(BIBO.isbn10),    M.stmt_copy())
    , M.emit(M.prop_eq(BIBO.isbn13),    M.stmt_copy())
    ])

annalist_relation_mapping = M.ref_subgraph(
    M.tgt_subj, M.src_prop, M.src_obj,
    [ M.set_subj(M.prop_eq(ANNAL.uri),      M.src_obj)
    , M.emit(M.prop_eq(RDF.type),           M.stmt_copy())
    , M.emit(M.prop_eq(RDFS.label),         M.stmt_copy())
    , M.emit(M.prop_eq(RDFS.comment),       M.stmt_copy())
    , M.emit(M.prop_eq(ANNAL.id),           M.stmt_copy())
    , M.emit(M.prop_eq(ANNAL.type_id),      M.stmt_copy())
    , M.emit(M.prop_eq(EM.relationTo),      M.stmt_copy())
    , M.emit(M.prop_eq(EM.relationType),    annalist_reference_mapping)
    , M.emit(M.prop_eq(EM.when),            annalist_when_mapping)
    , M.emit(M.prop_eq(EM.competence),      annalist_reference_mapping)
    , M.emit(M.prop_eq(EM.source),          annalist_source_mapping)
    ])

annalist_body_copy = M.ref_subgraph(
    M.tgt_subj, M.src_prop, M.src_obj,
    [ M.set_subj(M.prop_eq(ANNAL.uri),          M.src_obj)
    , M.emit(M.prop_eq(ANNAL.id),               M.stmt_copy())
    , M.emit(M.prop_eq(ANNAL.type_id),          M.stmt_copy())
    , M.emit(M.prop_nsne(ANNAL[None]),
        M.alt_values(
            M.test_prop_in({EM.language}),
            M.stmt(M.tgt_subj, M.src_prop, M.src_obj_or_val(ANNAL.uri)),
            M.stmt_copy()
            )
        )
    ])

annalist_annotation_mapping = M.ref_subgraph(
    M.tgt_subj, M.const(OA.hasAnnotation), M.src_obj,
    [ M.set_subj(M.prop_eq(ANNAL.uri),      M.src_obj)
    , M.emit(M.prop_eq(RDF.type),           M.stmt_copy())
    , M.emit(M.prop_eq(RDFS.label),         M.stmt_copy())
    , M.emit(M.prop_eq(RDFS.comment),       M.stmt_copy())
    , M.emit(M.prop_eq(ANNAL.id),           M.stmt_copy())
    , M.emit(M.prop_eq(ANNAL.type_id),      M.stmt_copy())
    , M.emit(M.prop_eq(OA.hasBody),         annalist_body_copy)
    , M.emit(M.prop_eq(OA.hasTarget),       M.stmt_copy())
    , M.emit(M.prop_eq(OA.motivatedBy),     annalist_reference_mapping)
    , M.emit(M.prop_eq(EM.when),            annalist_when_mapping)
    , M.emit(M.prop_eq(EM.competence),      annalist_reference_mapping)
    , M.emit(M.prop_eq(EM.source),          annalist_source_mapping)
    , M.emit(M.prop_eq(DCTERMS.creator),    annalist_reference_mapping)
    , M.emit(M.prop_eq(DCTERMS.created),    M.stmt_copy())
    ])

annalist_sourced_place_mapping = (
    [ M.set_subj(M.prop_eq(ANNAL.uri),          M.src_obj)
    , M.emit(M.prop_eq(RDF.type),               M.stmt_copy())
    , M.emit(M.prop_eq(RDFS.label),             M.stmt_copy())
    , M.emit(M.prop_eq(RDFS.comment),           M.stmt_copy())
    , M.emit(M.prop_eq(RDFS.seeAlso),           M.stmt_copy())
    , M.emit(M.prop_eq(ANNAL.id),               M.stmt_copy())
    , M.emit(M.prop_eq(ANNAL.type_id),          M.stmt_copy())
    , M.emit(M.prop_eq(EM.preferredName),       M.stmt_copy())
    , M.emit(M.prop_eq(EM.editorialNote),       M.stmt_copy())
    , M.emit(M.prop_eq(EM.placeCategory),       M.stmt_copy())
    , M.emit(M.prop_eq(EM.placeType),           M.stmt_copy())
    , M.emit(M.prop_eq(EM.relatedResource),     annalist_source_mapping)
    , M.emit(M.prop_eq(EM.source),              annalist_source_mapping)
    , M.emit(M.prop_eq(EM.alternateAuthority),  annalist_source_mapping)
    , M.emit(M.prop_eq(EM.when),                annalist_when_mapping)
    , M.emit(M.prop_eq(EM.where),               annalist_where_mapping)
    , M.emit(M.prop_eq(EM.reference),           annalist_reference_mapping)
    , M.emit(M.prop_eq(EM.hasRelation),         annalist_relation_mapping)
    , M.emit(M.prop_eq(EM.hasNameAttestationAnnotation),    annalist_annotation_mapping)
    , M.emit(M.prop_eq(EM.hasMapResourceAnnotation),        annalist_annotation_mapping)
    , M.emit(M.prop_eq(EM.hasCalendarUsedAnnotation),       annalist_annotation_mapping)
    ])

annalist_merged_place_mapping = (
    [ M.set_subj(M.prop_eq(ANNAL.uri),          M.src_obj)
    , M.emit(M.prop_eq(RDF.type),               M.stmt_copy())
    , M.emit(M.prop_eq(RDFS.label),             M.stmt_copy())
    , M.emit(M.prop_eq(RDFS.comment),           M.stmt_copy())
    , M.emit(M.prop_eq(ANNAL.id),               M.stmt_copy())
    , M.emit(M.prop_eq(ANNAL.type_id),          M.stmt_copy())
    , M.emit(M.prop_eq(EM.canonicalURI),        M.stmt_copy())
    , M.emit(M.prop_eq(EM.alternateURI),        M.stmt_copy())
    , M.emit(M.prop_eq(EM.place_data),          M.ref_subgraph(
        M.tgt_subj, M.src_prop, M.src_obj,
        annalist_sourced_place_mapping)
        )
    ])

#   ===================================================================
#
#   Command line parsing and help
#
#   ===================================================================

command_summary_help = ("\n"+
    "Commands:\n"+
    "\n"+
    "  %(prog)s help [command]\n"+
    "  %(prog)s get ANNALISTREF\n"+
    "  %(prog)s resource ANNALISTREF\n"+
    # "  %(prog)s manyget\n"+
    # "  %(prog)s placehierarchy ANNALISTREF\n"+
    # "  %(prog)s manyplacehierarchy\n"+
    # "  %(prog)s geonamesid URL [REGEXP]\n"
    # "  %(prog)s manygeonamesids [REGEXP]\n"
    "  %(prog)s version\n"+
    "")

def progname(args):
    return os.path.basename(args[0])

def gad_version(gadroot, userhome, options):
    """
    Print software version string to standard output.

    gadroot     is the root directory for the Annalist software installation.
    userhome    is the home directory for the host system user issuing the command.
    options     contains options parsed from the command line.

    returns     0 if all is well, or a non-zero status code.
                This value is intended to be used as an exit status code
                for the calling program.
    """
    status = GAD_SUCCESS
    print(sitesettings.GAD_VERSION)
    return status

def parseCommandArgs(argv):
    """
    Parse command line arguments

    argv            argument list from command line

    Returns a pair consisting of options specified as returned by
    OptionParser, and any remaining unparsed arguments.
    """
    # create a parser for the command line options
    parser = argparse.ArgumentParser(
                description="EMPlaces Annalist data exporter",
                formatter_class=argparse.RawDescriptionHelpFormatter,
                epilog=command_summary_help
                )
    parser.add_argument('--version', action='version', version='%(prog)s '+GAD_VERSION)
    parser.add_argument("--debug",
                        action="store_true", 
                        dest="debug", 
                        default=False,
                        help="Run with full debug output enabled.  "+
                             "Also creates log file 'get-annalist-data.log' in the working directory"
                        )
    parser.add_argument("-e", "--include-emplaces-defs",
                        action="store_true", 
                        dest="emplaces_defs", 
                        default=False,
                        help="Include common EMPlaces defintions "+
                             "(e.g. for relation types, periods, competencies, etc.) "+
                             "in the output graph."+
                             ""
                        )
    parser.add_argument("-g", "--include-geonames-defs",
                        action="store_true", 
                        dest="geonames_defs", 
                        default=False,
                        help="Include common GeoNames defintions "+
                             "(e.g. for feature codes, categories, etc.) "+
                             "in the output graph."+
                             ""
                        )
    parser.add_argument("-l", "--include-language-defs",
                        action="store_true", 
                        dest="language_defs", 
                        default=False,
                        help="Include common language resource defintions "+
                             "(as referenced by name attestations, etc.) "+
                             "in the output graph."+
                             ""
                        )
    parser.add_argument("-c", "--include-common-defs",
                        action="store_true", 
                        dest="common_defs", 
                        default=False,
                        help="Include common EMPlaces, GeoNames and language resource "+
                             "defintions in the output graph."+
                             ""
                        )
    parser.add_argument("command", metavar="COMMAND",
                        nargs=None,
                        help="sub-command, one of the options listed below."
                        )
    parser.add_argument("args", metavar="ARGS",
                        nargs="*",
                        help="Additional arguments, depending on the command used."
                        )
    # parse command line now
    options = parser.parse_args(argv)
    if options:
        if options and options.command:
            return options
    print("No valid usage option given.", file=sys.stderr)
    parser.print_usage()
    return None

def show_help(options, progname):
    """
    Display command help

    options     contains options parsed from the command line.

    returns     0 if all is well, or a non-zero status code.
                This value is intended to be used as an exit status code
                for the calling program.
    """
    if len(options.args) > 1:
        print("Unexpected arguments for %s: (%s)"%(options.command, " ".join(options.args)), file=sys.stderr)
        return GAD_UNEXPECTEDARGS
    status = GAD_SUCCESS
    if len(options.args) == 0:
        help_text = (
            command_summary_help+
            "\n"+
            "For more information about command options, use:\n"+
            "\n"+
            "  %(prog)s --help\n"+
            "")
    elif options.args[0].startswith("getm"):
        help_text = ("\n"+
            "  %(prog)s getmerged ANNALISTREF\n"+
            "\n"+
            "Gets merged-source data about a referenced place from Annalist, and sends \n"+
            "corresponding EMPlaces data in Turtle format to standard output.\n"+
            "Referenced Annalist resources are extracted and included in the result, to\n"+
            "the extent required to generate valid and complete data for EMPLaces.\n"+
            "\n"+
            "To include some common non-place-specific supporting definitions, see options\n"+
            "'--include-common-defs', '--include-emplaces-defs', '--include-geonames-defs', \n"+
            "and '--include-language-defs'.\n"+
            "\n"+
            "")
    elif options.args[0].startswith("gets"):
        help_text = ("\n"+
            "  %(prog)s getsourced ANNALISTREF\n"+
            "\n"+
            "Gets single-source data about a referenced place from Annalist, and sends \n"+
            "corresponding EMPlaces data in Turtle format to standard output.\n"+
            "Referenced Annalist resources are extracted and included in the result, to\n"+
            "the extent required to generate valid and complete data for EMPLaces.\n"+
            "\n"+
            "To include some common non-place-specific supporting definitions, see options\n"+
            "'--include-common-defs', '--include-emplaces-defs', '--include-geonames-defs', \n"+
            "and '--include-language-defs'.\n"+
            "\n"+
            "")
    elif options.args[0].startswith("resource"):
        help_text = ("\n"+
            "  %(prog)s resource ANNALISTREF\n"+
            "\n"+
            "Gets data about an arbitrary resource served by Annalist and returns it\n"+
            "in Turtle format to standard output.  Only statements directly represented\n"+
            "for the indicated resourcfe are returned.\n"+
            "\n"+
            "To include some common non-place-specific supporting definitions, see options\n"+
            "'--include-common-defs', '--include-emplaces-defs', '--include-geonames-defs', \n"+
            "and '--include-language-defs'.\n"+
            "\n"+
            "")
    elif options.args[0].startswith("ver"):
        help_text = ("\n"+
            "  %(prog)s version\n"+
            "\n"+
            "Sends the software version string to standard output.\n"+
            "\n"+
            "")
    elif options.args[0].startswith("@@@"):
        help_text = ("\n"+
            "  %(prog)s @@@\n"+
            "\n"+
            "@@@.\n"+
            "\n"+
            "")
    else:
        help_text = "Unrecognized command for %s: (%s)"%(options.command, options.args[0])
        status = GAD_UNKNOWNCMD
    print(help_text%{'prog': progname}, file=sys.stderr)
    return status

def show_version(gadroot, userhome, options):
    """
    Print software version string to standard output.

    gadroot     is the root directory for the `annalistdataexport` software installation.
    userhome    is the home directory for the host system user issuing the command.
    options     contains options parsed from the command line.

    returns     0 if all is well, or a non-zero status code.
                This value is intended to be used as an exit status code
                for the calling program.
    """
    if len(options.args) > 0:
        return show_error(
            "Unexpected arguments for %s: (%s)"%(options.command, " ".join(options.args)), 
            GAD_UNEXPECTEDARGS
            )
    status = GAD_SUCCESS
    print(GAD_VERSION)
    # with open(logfilename, "r") as logfile:
    #     shutil.copyfileobj(logfile, sys.stdout)
    return status

def show_error(msg, status):
    print(msg, file=sys.stderr)
    return status

#   ===================================================================
#
#   Id and URI wrangling.  Hacky URI introspection is isolated here.
#
#   ===================================================================

def get_annalist_uri(annalist_ref):
    """
    Returns Annalist place URI, given relative reference.

    The reference is generally of the form "type_id/place_id"; e.g.

        Place_sourced/Opole_P_EMPlaces
        Place_merged/Opole_P
    """
    default_base_url = COLLECTION_BASE + "/"
    annalist_uri     = urlparse.urljoin(default_base_url, annalist_ref)
    annalist_url     = urlparse.urljoin(annalist_uri+"/", "entity_data.ttl")
    return (annalist_uri, annalist_url)

def get_emplaces_id_uri_node(place_name, place_type, unique_id, suffix=""):
    """
    Given a place name, place type, Id and optional suffix,
    returns a place Id, URI and Node.
    """
    type_id       = get_geonames_place_type_id(place_type)
    name_slug     = place_name.replace(" ", "_")
    name_slug     = name_slug[:40]
    emplaces_id   = "%s_%s_%s%s"%(name_slug, type_id, unique_id, suffix)
    emplaces_uri  = EMP[emplaces_id]
    emplaces_node = URIRef(emplaces_uri)
    return (emplaces_id, emplaces_uri, emplaces_node)

def get_many_inputs():
    inputs = []
    for line in sys.stdin:
        u_line = line.decode("utf8")
        bare_input = u_line.split("#", 1)[0].strip()
        if bare_input:
            inputs.append(bare_input)
    return inputs    

#   ===================================================================
#
#   RDF data wrangling
#
#   ===================================================================

def get_rdf_graph(url, format="turtle"):
    """
    Return RDF graph at given location.
    """
    # e.g. http://sws.geonames.org/3090048/about.rdf
    g = Graph()
    try:
        g.parse(location=url, format=format)
    except Exception as e:
        print("RDF parse error '%s' (%s)"%(url, e), file=sys.stderr)
    # result = g.parse(data=r.content, publicID=u, format="turtle")
    # result = g.parse(source=s, publicID=b, format="json-ld")
    return g

def get_annalist_graph_data(annalist_url):
    """
    Returns graph of Annalist place data
    """
    annalist_rdf = get_rdf_graph(annalist_url)
    return annalist_rdf

def add_emplaces_common_namespaces(emp_graph):
    """
    Add common EMPlaces definitions to supplied graph
    """
    emp_graph.bind("skos",      SKOS.term(""))
    emp_graph.bind("xsd",       XSD.term(""))
    emp_graph.bind("oa",        OA.term(""))
    emp_graph.bind("cc",        CC.term(""))
    emp_graph.bind("dcterms",   DCTERMS.term(""))
    emp_graph.bind("foaf",      FOAF.term(""))
    emp_graph.bind("bibo",      BIBO.term(""))
    emp_graph.bind("geonames",  GEONAMES.term(""))
    emp_graph.bind("gn",        GN.term(""))
    emp_graph.bind("wgs84_pos", WGS84_POS.term(""))
    emp_graph.bind("em",        EM.term(""))
    emp_graph.bind("emp",       EMP.term(""))
    emp_graph.bind("emt",       EMT.term(""))
    emp_graph.bind("eml",       EML.term(""))
    emp_graph.bind("ems",       EMS.term(""))
    emp_graph.bind("emc",       EMC.term(""))
    emp_graph.bind("place",     PLACE.term(""))
    emp_graph.bind("agent",     AGENT.term(""))
    emp_graph.bind("ref",       REF.term(""))
    emp_graph.bind("annal",     ANNAL.term(""))
    local_namespaces = (
        { "anno_cal":        "%(base)s/Calendar_used_annotation/"
        , "anno_map":        "%(base)s/Map_resource_annotation/"
        , "anno_nam":        "%(base)s/Name_attestation_annotation/"
        , "annotation":      "%(base)s/Contextualized_annotation/"
        , "place_merged":    "%(base)s/Place_merged/"
        , "place_sourced":   "%(base)s/Place_sourced/"
        , "place_category":  "%(base)s/Place_category/"
        , "place_relation":  "%(base)s/Qualified_relation/"
        , "place_type":      "%(base)s/Place_type/"
        , "place_name":      "%(base)s/Place_name/"
        , "setting":         "%(base)s/Setting/"
        , "location":        "%(base)s/Location_value/"
        , "person":          "%(base)s/foaf_Person/"
        # , "agent":           "%(base)s/foaf_Agent/"
        , "map_resource":    "%(base)s/Map_resource/"
        , "calendar":        "%(base)s/Calendar/"
        , "language_value":  "%(base)s/Language_value/"
        })
    for pref in local_namespaces:
        emp_graph.bind(
            pref, 
            local_namespaces[pref]%{"base": COLLECTION_BASE}
            )
    return

def add_turtle_data(emp_rdf, turtle_str):
    """
    Adds Turtle string data to a graph under construction.

    emp_rdf     is the graph to which statements are added
    turtle_str  is a string that contains Turtle startements 
                to be added to the graph.

    NOTE:
    Namespace prefixes already defined for the graph are not
    recognized in the Turtle data.
    """
    emp_rdf.parse(
        data=COMMON_PREFIX_DEFS+LOCAL_PREFIX_DEFS+turtle_str, 
        format="turtle"
        )
    return emp_rdf

def add_resource_attributes(emp_rdf, attributes, subject=None):
    """
    Adds a set of attributes to a graph.

    emp_rdf     is the graph to which statements are added
    attributes  is a dictionary of attributes and values to be added
    subject     is the common subject for statements to be added.  
                If not specified, a new blank node is used.

    Returns the subject node.
    """
    if subject is None:
        subject = BNode()
    for prop in attributes:
        emp_rdf.add((subject, prop, attributes[prop]))
    return subject

def get_annalist_resource_data(gadroot, annalist_ref, resource_rdf=None):
    """
    Extract direct resource statements for a specified Annalist reference.
    """
    annalist_uri, annalist_url = get_annalist_uri(annalist_ref)
    annalist_rdf = get_annalist_graph_data(annalist_url)
    # Initial empty graph
    if resource_rdf is None:
        resource_rdf = Graph()
        add_emplaces_common_namespaces(resource_rdf)
    M = DataExtractMap
    # ----- mapping table -----
    annalist_data_mapping = (
        [ M.set_subj(M.prop_eq(ANNAL.uri), M.src_obj)
        , M.emit(M.prop_ne(ANNAL.uri), M.stmt_copy())
        ])
    # -----
    m = DataExtractMap(annalist_uri, annalist_rdf, resource_rdf)
    m.extract_map(annalist_data_mapping)
    return resource_rdf

def get_annalist_ref_data(gadroot, annalist_ref, mapping, emplaces_rdf=None):
    """
    Build EMPlaces place data for a specified Annalist place reference,
    using an indicated mapping table.
    """
    annalist_uri, annalist_url = get_annalist_uri(annalist_ref)
    annalist_rdf = get_annalist_graph_data(annalist_url)
    # Initial empty graph
    if emplaces_rdf is None:
        emplaces_rdf = Graph()
        add_emplaces_common_namespaces(emplaces_rdf)
    # -----
    m = DataExtractMap(annalist_uri, annalist_rdf, emplaces_rdf)
    m.extract_map(mapping)
    return emplaces_rdf

def get_common_defs(options, emplaces_rdf):
    if options.emplaces_defs or options.common_defs:
        add_turtle_data(emplaces_rdf, COMMON_EMPLACES_DEFS)
    if options.geonames_defs or options.common_defs:
        add_turtle_data(emplaces_rdf, COMMON_GEONAMES_DEFS)
    if options.language_defs or options.common_defs:
        add_turtle_data(emplaces_rdf, COMMON_LANGUAGE_DEFS)
    return emplaces_rdf

def do_get_merged_place_data(gadroot, options):
    """
    Get merged-source place data from a given place reference
    """
    annalist_ref = getargvalue(getarg(options.args, 0), "Annalist ref: ")
    emplaces_rdf = get_annalist_ref_data(
        gadroot, annalist_ref,
        annalist_merged_place_mapping
        )
    get_common_defs(options, emplaces_rdf)
    print(emplaces_rdf.serialize(format='turtle', indent=4), file=sys.stdout)
    return GAD_SUCCESS

def do_get_source_place_data(gadroot, options):
    """
    Get single-source place data from a given place reference
    """
    annalist_ref = getargvalue(getarg(options.args, 0), "Annalist ref: ")
    emplaces_rdf = get_annalist_ref_data(
        gadroot, annalist_ref,
        annalist_sourced_place_mapping
        )
    get_common_defs(options, emplaces_rdf)
    print(emplaces_rdf.serialize(format='turtle', indent=4), file=sys.stdout)
    return GAD_SUCCESS

def do_get_resource_data(gadroot, options):
    """
    Get arbitrary resource data from annalst.

    This returns direct statements with minimal interpretation.
    """
    annalist_ref  = getargvalue(getarg(options.args, 0), "Annalist ref: ")
    emplaces_rdf = get_annalist_resource_data(gadroot, annalist_ref)
    get_common_defs(options, emplaces_rdf)
    print(emplaces_rdf.serialize(format='turtle', indent=4), file=sys.stdout)
    return GAD_SUCCESS

def format_id_name(pid, pname, ptype, geo_ont_rdf):
    log.debug("format_id_name: (%r, %r, %r)"%(pid, pname, ptype))
    return (
        unicode(pid).ljust(8) +
        "  # " + unicode(pname) +
        " ("   + get_geonames_place_type_label(ptype, geo_ont_rdf) +
        ")").encode('utf8')

def format_id_text(pid, ptext):
    log.debug("format_id_text: (%s, %s)"%(pid, ptext))
    return (
        unicode(pid).ljust(8) + "  # " + unicode(ptext)
        ).encode('utf8')

#   ===================================================================

def do_zzzzzz(gadroot, options):
    print("Un-implemented sub-command: %s"%(options.command), file=sys.stderr)
    return GAD_UNIMPLEMENTED

#   ===================================================================

def run(userhome, userconfig, options, progname):
    """
    Command dispatcher.
    """
    if options.command.startswith("@@@"):
        return do_zzzzzz(gadroot, options)
    if options.command.startswith("getm"):
        return do_get_merged_place_data(gadroot, options)
    if options.command.startswith("gets"):
        return do_get_source_place_data(gadroot, options)
    if options.command.startswith("resource"):
        return do_get_resource_data(gadroot, options)
    if options.command.startswith("ver"):
        return show_version(gadroot, userhome, options)
    if options.command.startswith("help"):
        return show_help(options, progname)
    print("Un-recognised sub-command: %s"%(options.command), file=sys.stderr)
    print("Use '%s --help' to see usage summary"%(progname), file=sys.stderr)
    return GAD_BADCMD

def runCommand(userhome, userconfig, argv):
    """
    Run program with supplied configuration base directory, 
    configuration directory and command arguments.

    This is called by main function (below), and also by test suite routines.

    Returns exit status.
    """
    options = parseCommandArgs(argv[1:])
    if options and options.debug:
        logging.basicConfig(level=logging.DEBUG, filename="get-annalist-data.log", filemode="w")
    else:
        logging.basicConfig(level=logging.INFO)
    log.debug("runCommand: userhome %s, userconfig %s, argv %s"%(userhome, userconfig, repr(argv)))
    log.debug("Options: %s"%(repr(options)))
    if options:
        progname = os.path.basename(argv[0])
        status   = run(userhome, userconfig, options, progname)
    else:
        status = GAD_BADCMD
    return status

def runMain():
    """
    Main program transfer function for setup.py console script
    """
    userhome   = os.path.expanduser("~")
    userconfig = os.path.join(userhome, ".emplaces")
    return runCommand(userhome, userconfig, sys.argv)

if __name__ == "__main__":
    """
    Program invoked from the command line.
    """
    p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, p)
    status = runMain()
    if status != GAD_SUCCESS:
        print("Exit status: %d"%(status,), file=sys.stderr)
    sys.exit(status)

# End.

