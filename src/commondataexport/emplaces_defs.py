# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# emplaces_defs - definitions for EMPlaces linked data
#

from __future__ import print_function
from __future__ import unicode_literals

__author__      = "Graham Klyne (GK@ACM.ORG)"
__copyright__   = "Copyright 2019, Graham Klyne and University of Oxford"
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

log = logging.getLogger(__name__)

#   ===================================================================
#
#   Data constants
#
#   ===================================================================

#   Namespaces

SKOS      = Namespace("http://www.w3.org/2004/02/skos/core#")
XSD       = Namespace("http://www.w3.org/2001/XMLSchema#")
OA        = Namespace("http://www.w3.org/ns/oa#")
TIME      = Namespace("http://www.w3.org/2006/time#")
PROV      = Namespace("http://www.w3.org/ns/prov#")
WGS84_POS = Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#")

SCHEMA    = Namespace("http://schema.org/")
CC        = Namespace("http://creativecommons.org/ns#")
DCTERMS   = Namespace("http://purl.org/dc/terms/")
FOAF      = Namespace("http://xmlns.com/foaf/0.1/")
BIBO      = Namespace("http://purl.org/ontology/bibo/")
CITO      = Namespace("http://purl.org/spar/cito#")
CRM       = Namespace("http://erlangen-crm.org/current/")

ANNAL     = Namespace("http://purl.org/annalist/2014/#")    # Annalist ontology
GN        = Namespace("http://www.geonames.org/ontology#")  # GeoNames ontology
GEONAMES  = Namespace("http://sws.geonames.org/")           # GeoNames place 
WDT       = Namespace("http://www.wikidata.org/prop/direct/")
WD        = Namespace("http://www.wikidata.org/entity/")

EM        = Namespace("http://id.emplaces.info/vocab/")
EMP       = Namespace("http://id.emplaces.info/timeperiod/")
EMT       = Namespace("http://id.emplaces.info/timespan/")
EML       = Namespace("http://id.emplaces.info/language/")
EMS       = Namespace("http://id.emplaces.info/source/")
EMC       = Namespace("http://id.emplaces.info/calendar/")

PLACE     = Namespace("http://id.emplaces.info/place/")
AGENT     = Namespace("http://id.emplaces.info/agent/")
REF       = Namespace("http://id.emplaces.info/reference/")

#   ===================================================================
#
#   Common definitions for EMPlaces data
#
#   ===================================================================

# @@TODO: refactor; don't repeat URLs from above

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
    # ===== Classes =====

    em:Place a rdfs:Class ;
        rdfs:label "Place" ;
        rdfs:comment
            '''
            A resource that provides information about a place (which is 
            considered in the sense of being "constructed by human experience").
            ''' ;
        .

    em:Place_sourced a rdfs:Class ;
        rdfs:subClassOf em:Place ;  #@@TODO: review this
        rdfs:label "Place information from single source" ;
        rdfs:comment
            '''
            A resource that provides information about a place that comes from 
            a single source.  Property `em:source` references a description of 
            that source.
            ''' ;
        .

    em:Place_merged a rdfs:Class ;
        rdfs:subClassOf em:Place ;  #@@TODO: review this
        rdfs:label "Place information merged from multiple sources" ;
        rdfs:comment
            '''
            A resource that provides information about a place that comes from 
            multiple sources.  One or more em:place_data properties reference 
            single-sourced information about the place.
            ''' ;
        .

    em:Time_period a rdfs:Class ;
        rdfs:label   "Time period" ;
        rdfs:comment 
            '''
            Identified (historical) time period, whose temporal extent may or may not be known.
            ''' ;
        .

    em:Time_span a rdfs:Class ;
        rdfs:label   "Time span" ;
        rdfs:comment 
            '''
            A time span specified in terms of its temporal extent.  
            Some or all of the bounds of the temporal extent may be unknown or approximate.
            '''  ;
        .

    em:Licence_desc a rdfs:Class ;
        rdfs:label   "Licence description" ;
        rdfs:comment 
            '''
            A description of a licence for use of some data.
            ''' ;
        .

    em:Language_value a rdfs:Class ;
        rdfs:label   "Language identifier" ;
        rdfs:comment 
            '''
            Identifies a language, such as may be appliucable to a place name, etc.
            ''' ;
        .

    em:Source_desc a rdfs:Class ;
        rdfs:label   "Information source" ;
        
        rdfs:comment 
            '''
            Describes a source of information.
            ''' ;
        .

    em:Authority a rdfs:Class ;
        rdfs:subClassOf em:Source_desc ;
        rdfs:label   "Authoritative information source" ;
        rdfs:comment 
            '''
            Describes a source of information that is considered to be authoritative in some sense
            ''' ;
        .

    em:Qualified_relation a rdfs:Class ;
        rdfs:label   "Relationship between two places" ;
        rdfs:comment 
            '''
            A relationship between two places, which may be qualified in various ways.  
            The type of relationship is specified by a 'em:relationType' property on the 
            qualified relation.
            '''  ;
        .

    em:Relation_type a rdfs:Class ;
        rdfs:label "Relationship type identifier" ;
        .

    em:Competence_value a rdfs:Class ;
        rdfs:label "Information competence (certainty) indicator" ;
        .

    em:Setting a rdfs:Class ;
        rdfs:label   "Spatial and temporal extent" ;
        rdfs:comment 
            '''
            A spatial and temporal extent that a place may occupy or lie within.
            ''' ;
        .

    em:Map_resource a rdfs:Class ;
        rdfs:label   "Map resource" ;
        rdfs:comment 
            '''
            Describes a map resource.
            ''' ;
        .

    em:Place_name a rdfs:Class ;
        rdfs:label   "Place name" ;
        rdfs:comment 
            '''
            A name by which a place may be known or designated in some language.
            ''' ;
        .

    em:Bib_entry a rdfs:Class ;
        rdfs:label   "Bibliographic item" ;
        rdfs:comment 
            '''
            Bibliographic item description, based on BIBO.

            This is a superclass of the variou BIBO entity types, such as bibo:Book.
            ''' ;
        .


    # ===== Predefined time periods =====

    # Time period for "current" data
    emp:Current a em:Time_period ;
        rdfs:label   "Current, as of 2018" ;
        rdfs:comment
            '''
            For ease of retrieval, use this specific resource to label any current information
            (e.g. data extracted from GeoNames).  Additional Timespan values could be indicated 
            if required to convey more specific information.
            ''' ;
        em:timespan
          [ a em:Time_span ;
            em:latestStart: "2018" ;
            em:earliestEnd: "2018" ;
          ]
        .

    # ===== Additional place types =====
    #
    #   Place type identifiers used are generally taken directly from GeoNames,
    #   but additional values may be used.

    #   Combined place type to avoid having to create extra historical places 
    #   corresponding to a current P.  References GeoNames place types.
    #   See also relation type em:AH_PART_OF_AH.
    em:P_OR_A a skos:Concept ;
        skos:broader gn:A ;
        skos:broader gn:P ;
        rdfs:label    "Former populated place or admin division" ;
        rdfs:comment  
            '''
            Former populated place or administrative division, 
            used in historical administrative relations
            ''' ;
        .

    # ===== Place relation types =====

    em:P_PART_OF_A a em:Relation_type ;
        em:fromType   gn:P ;
        em:toType     gn:A ;
        rdfs:label    "Administered by" ;
        rdfs:comment  
            '''
            Relates a populated place to its administrative division.
            ''' ; 
        .

    em:A_PART_OF_A a em:Relation_type ;
        em:fromType   gn:A ;
        em:toType     gn:A ;
        rdfs:label    "Subdivision of" ;
        rdfs:comment  
            '''
            Relates a subdivision of an administrative division to its parent division.
            ''' ; 
        .

    em:AH_PART_OF_AH a em:Relation_type ;
        em:fromType   em:P_OR_A ;
        em:toType     gn:A ;
        rdfs:label    "Former part of" ;
        rdfs:comment
            '''
            Records a historical relationship between a historical place or administrative division 
            and its parent division.
            ''' ;
        .

    #@@NOTE: this is quite specific - we may later want to allow for 
    #        a looser style of relationship; e.g. `em:S_PART_OF_PA`
    em:S_PART_OF_P a em:Relation_type ;
        em:fromType   gn:S ;
        em:toType     gn:P ;
        rdfs:label    "Located within" ;
        rdfs:comment
            '''
            Relates a spot feature to a populated place within which it may be found.
            ''' ;
        .

    # ===== Information competence (certainty) =====
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
        rdfs:comment
            '''
            Records the quality or certaintly of some information.  
            Note that in the absence of an explicit value, no competence should be assumed.
            ''' ;
        rdfs:range em:Competence_value ;
        .

    em:DEFINITIVE a em:Competence_value ;
        rdfs:label   "Definitive" ;
        rdfs:comment
            '''
            The associated value is definitively true for the purposes of EMPlaces.  
            Such information should ideally be backup up be appropiate source references.
            ''' ;
        .

    em:INFERRED a em:Competence_value ;
        rdfs:label   "Inferred" ;
        rdfs:comment
            '''
            The associated value has been inferred from (preferably?) definitive informaton.
            ''' ;
        .

    em:ASSUMED a em:Competence_value ;
        # Assumed data is like uncertain, but maybe with better foundation?
        rdfs:label   "Assumed" ;
        rdfs:comment
            '''
            The associated value is assumed from context.
            ''' ;
        .

    em:UNCERTAIN a em:Competence_value ;
        rdfs:label   "Uncertain" ;
        rdfs:comment
            '''
            The associated value is uncertain."
            ''' ;
        .

    em:APPROXIMATE a em:Competence_value ;
        rdfs:label   "Approximate" ;
        rdfs:comment
            '''
            The associated value is a date whose value is only approximately known.  

            @@NOTE: this value may prove spurious, as timespan already has a way to 
            represent approximation ranges."
            ''' ;
        .

    # ===== Annotation motivations =====

    em:MAP_RESOURCE a oa:Motivation ;
        rdfs:label "Map resource" ;
        rdfs:comment
            '''
            References a current or historical map resource associated with a place.
            ''' ;
        .

    em:NAME_ATTESTATION
        rdfs:label "Name attestation" ;
        rdfs:comment
            '''
            References a historical name attestation for a place, with source and compenence information.
            ''' ;
        .

    em:CALENDAR_IN_USE
        rdfs:label "Calendar in use" ;
        rdfs:comment
            '''
            References a historical calendar used in a place, with source and compenence information.
            ''' ;
        .

    em:DEDICATED_TO a oa:Motivation ;
        rdfs:label "Dedicated to" ;
        rdfs:comment
            '''
            Generally used with a related place that is a church or a place or worship, 
            to indicate a person or historical figure to whom the place has been dedicated.  
            The annotation body directly references a resource for the dedicatee, which is 
            assumed to have an 'rdfs:label' value that can be used for display purposes.
            ''' ;
        .

    em:USED_FOR a oa:Motivation ;
        rdfs:label "Used for" ;
        rdfs:comment
            '''
            Generally used with a related place that is a building or site for some activity, 
            to indicate a purpose for which the place was used.  The annotation body directly 
            references a resource describing the purpose, which is assumed to have an 'rdfs:label'
            value that can be used for display purposes.  The annotation itself may carry a 
            temporal constraint ('em:where') that gives some indication of when the place was 
            used for that purpose.
            ''' ;
        .

    # ===== Calendar descriptions =====
    #
    # These are placeholders.  The intent is that calendar-in-use data
    # contains a reference to some external authority or description.

    emc:Gregorian a em:Calendar ;
        rdfs:label "Gregorian calendar" ;
        em:link emc:Gregorian ;
        rdfs:comment 
            '''# Gregorian calendar

            Calendar generally in use in Europe from about 23 Feb 1584.
            ''' ;
        .

    emc:Julian_old a em:Calendar ;
        rdfs:label "Julian calendar (25 Mar)" ;
        em:link emc:Julian_old ;
        rdfs:comment 
            '''# Julian calendar (Old)

            "Old style" Julian calendar, year begins on 25-Mar.
            ''' ;
        .

    emc:Julian_new a em:Calendar ;
        rdfs:label "Julian calendar (1 Jan)" ;
        em:link emc:Julian_new ;
        rdfs:comment 
            '''# Julian calendar (New)

            "New style" Julian calendar, year begins on 01-Jan.
            ''' ;
        .

    """)

COMMON_GEONAMES_DEFS = (
    """

    # ===== Place categories =====

    gn:P a skos:Concept ; 
        rdfs:label "Populated place" ;
        rdfs:comment 
        '''
        Populated place - from GeoNames (feature class).
        ''' ;
        .
    gn:A  a skos:Concept ; 
        rdfs:label   "Administrative division" ;
        rdfs:comment 
        '''
        Administrative division - from GeoNames (feature class).
        ''' ;
        .

    gn:S a skos:Concept ; 
        rdfs:label "Spot feature" ;
        rdfs:comment 
        '''
        Spot feature (spot, building, farm).
        ''' ;
        .

    # ===== Place types =====

    gn:P.PPL a skos:Concept ;
        skos:narrower gn:P ;
        rdfs:label    "Populated place" ;
        rdfs:comment 
        '''
        A populated place (town, city, village, etc.).
        ''' ;
        .

    gn:P.PPLA a skos:Concept ;
        skos:narrower gn:P ;
        rdfs:label    "Seat of 1st-order admin div" ;
        rdfs:comment 
        '''
        Populated place that is a seat of a first-order administrative division.
        ''' ;
        .

    gn:P.PPLH a skos:Concept ;
        skos:narrower gn:P ;
        rdfs:label    "Former populated place" ;
        rdfs:comment 
        '''
        A former populated place that no longer exists.
        ''' ;
        .

    gn:A.PCLI a skos:Concept ;
        skos:narrower gn:A ;
        rdfs:label    "Independent political entity" ;
        rdfs:comment 
        '''
        An independent political entity, typically a country.
        ''' ;
        .

    gn:A.ADM1 a skos:Concept ;
        skos:narrower gn:A ;
        rdfs:label    "First-order admin division" ;
        rdfs:comment 
        '''
        A primary administrative division of a country, such as a state in the United States.
        ''' ;
        .

    gn:A.ADM2 a skos:Concept ;
        skos:narrower gn:A ;
        rdfs:label    "Second-order admin division" ;
        rdfs:comment 
        '''
        A subdivision of a first-order administrative division.
        ''' ;
        .

    gn:A.ADM3 a skos:Concept ;
        skos:narrower gn:A ;
        rdfs:label    "Third-order admin division" ;
        rdfs:comment 
        '''
        A subdivision of a second-order administrative division.
        ''' ;
        .

    gn:A.PCLH a skos:Concept ;
        skos:narrower gn:A ;
        rdfs:label    "Former independent political entity" ;
        rdfs:comment 
        '''
        A former independent political entity, typically a country.
        ''' ;
        .

    gn:A.ADM1H a skos:Concept ;
        skos:narrower gn:A ;
        rdfs:label    "Former first-order admin division" ;
        rdfs:comment 
        '''
        A former first-order administrative division.
        ''' ;
        .

    gn:A.ADM2H a skos:Concept ;
        skos:narrower gn:A ;
        rdfs:label    "Former second-order admin division" ;
        rdfs:comment 
        '''
        A former first-order administrative division.
        ''' ;
        .

    gn:A.ADM3H a skos:Concept ;
        skos:narrower gn:A ;
        rdfs:label    "Former Third-order admin division" ;
        rdfs:comment 
        '''
        A former third-order administrative division.
        ''' ;
        .

    gn:S.CH a skos:Concept ;
        skos:narrower gn:S ;
        rdfs:label    "Church" ;
        rdfs:comment 
        '''
        A church; a building for public Christian worship.
        ''' ;
        .
    """)

COMMON_LANGUAGE_DEFS = (
    """
    # ===== Language resources -----
    #
    # @@TODO: generate as-needed@@

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
#   Bind namespace defintions in supplied graph for EMPlaces data
#
#   ===================================================================

# Base URL for collection
# (@@TODO: extract this automatically from supplied reference)

COLLECTION_BASE = "http://localhost:8000/annalist/c/EMPlaces_defs/d"

def add_emplaces_common_namespaces(emp_graph, local_namespaces=None):
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
    if local_namespaces is None:
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

# End.

