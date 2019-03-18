# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# rdf_data_utils.py - support functions for accessing and processing RDF data
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
import urlparse
import logging

from rdflib         import Graph, Namespace, URIRef, Literal, BNode, RDF, RDFS
from rdflib.paths   import Path

from emplaces_defs  import GN, SKOS, PLACE, COMMON_PREFIX_DEFS
from dataextractmap import DataExtractMap

log = logging.getLogger(__name__)

#   ===================================================================
#
#   Data constants
#
#   ===================================================================

# Base URL for collection
# (@@TODO: extract this automatically from supplied reference)

COLLECTION_BASE = "http://localhost:8000/annalist/c/EMPlaces_defs/d"

#   ===================================================================
#
#   Common command execution helpers
#
#   ===================================================================

def progname(args):
    return os.path.basename(args[0])

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

def get_emplaces_id(place_name, place_type, unique_id, suffix=""):
    """
    Given a place name, place type, Id and optional suffix,
    returns a place Id, URI and Node.
    """
    type_id       = get_geonames_place_type_id(place_type)
    name_slug     = place_name.replace(" ", "_")
    name_slug     = name_slug[:40]
    emplaces_id   = "%s_%s_%s%s"%(name_slug, type_id, unique_id, suffix)
    return emplaces_id

def get_emplaces_uri_node(emplaces_id, suffix=""):
    """
    Given a place name, place type, Id and optional suffix,
    returns a place Id, URI and Node.
    """
    emplaces_sid  = emplaces_id + suffix
    emplaces_uri  = PLACE[emplaces_sid]
    emplaces_node = URIRef(emplaces_uri)
    return (emplaces_sid, emplaces_uri, emplaces_node)

# @@TODO: refactor to use above...
def get_emplaces_id_uri_node(place_name, place_type, unique_id, suffix=""):
    """
    Given a place name, place type, Id and optional suffix,
    returns a place Id, URI and Node.
    """
    type_id       = get_geonames_place_type_id(place_type)
    name_slug     = place_name.replace(" ", "_")
    name_slug     = name_slug[:40]
    emplaces_id   = "%s_%s_%s%s"%(name_slug, type_id, unique_id, suffix)
    emplaces_uri  = PLACE[emplaces_id]
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

def get_geonames_graph_data(geonames_url):
    """
    Returns graph of GeoNames place data
    """
    geonames_rdf = get_rdf_graph(geonames_url, format="xml")
    return geonames_rdf

def get_annalist_graph_data(annalist_url):
    """
    Returns graph of Annalist place data
    """
    annalist_rdf = get_rdf_graph(annalist_url, format="turtle")
    return annalist_rdf

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
        data=COMMON_PREFIX_DEFS+turtle_str, 
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

# def get_annalist_resource_data(gadroot, annalist_ref, resource_rdf=None):
#     """
#     Extract direct resource statements for a specified Annalist reference.
#     """
#     annalist_uri, annalist_url = get_annalist_uri(annalist_ref)
#     annalist_rdf = get_annalist_graph_data(annalist_url)
#     # Initial empty graph
#     if resource_rdf is None:
#         resource_rdf = Graph()
#         add_emplaces_common_namespaces(resource_rdf)
#     M = DataExtractMap
#     # ----- mapping table -----
#     annalist_data_mapping = (
#         [ M.set_subj(M.prop_eq(ANNAL.uri), M.src_obj)
#         , M.emit(M.prop_ne(ANNAL.uri), M.stmt_copy())
#         ])
#     # -----
#     m = DataExtractMap(annalist_uri, annalist_rdf, resource_rdf)
#     m.extract_map(annalist_data_mapping)
#     return resource_rdf

# def get_annalist_ref_data(gadroot, annalist_ref, mapping, emplaces_rdf=None):
#     """
#     Build EMPlaces place data for a specified Annalist place reference,
#     using an indicated mapping table.
#     """
#     annalist_uri, annalist_url = get_annalist_uri(annalist_ref)
#     annalist_rdf = get_annalist_graph_data(annalist_url)
#     # Initial empty graph
#     if emplaces_rdf is None:
#         emplaces_rdf = Graph()
#         add_emplaces_common_namespaces(emplaces_rdf)
#     # -----
#     m = DataExtractMap(annalist_uri, annalist_rdf, emplaces_rdf)
#     m.extract_map(mapping)
#     return emplaces_rdf

# def get_common_defs(options, emplaces_rdf):
#     if options.emplaces_defs or options.common_defs:
#         add_turtle_data(emplaces_rdf, COMMON_EMPLACES_DEFS)
#     if options.geonames_defs or options.common_defs:
#         add_turtle_data(emplaces_rdf, COMMON_GEONAMES_DEFS)
#     if options.language_defs or options.common_defs:
#         add_turtle_data(emplaces_rdf, COMMON_LANGUAGE_DEFS)
#     return emplaces_rdf

def get_geonames_place_type_id(place_type):
    """
    Returns id for supplied GeoNames place type
    """
    # place_type_ids = (
    #     { GN["P.PPL"]:   "PPL"
    #     , GN["P.PPLA"]:  "PPLA"
    #     , GN["A.ADM5"]:  "ADM5"
    #     , GN["A.ADM4"]:  "ADM4"
    #     , GN["A.ADM3"]:  "ADM3"
    #     , GN["A.ADM2"]:  "ADM2"
    #     , GN["A.ADM1"]:  "ADM1"
    #     , GN["A.PCLI"]:  "PCLI"
    #     , GN["L.RGN"]:   "RGN"
    #     })
    # if place_type in place_type_ids:
    #     type_id = place_type_ids[place_type]
    tokens  = [t for t in re.split(r'\W', place_type) if t]
    type_id = tokens[-1]
    return type_id

def get_geonames_place_type_label(place_type, geo_ont_rdf):
    """
    Returns label for supplied GeoNames place type
    """
    # Alternatives to ontology labels
    place_type_labels = (
        { GN["P.PPL"]:   "Populated place (P.PPL)"
        , GN["P.PPLA"]:  "Populated place (P.PPLA)"
        , GN["A.ADM5"]:  "City   (A.ADM5)"
        , GN["A.ADM4"]:  "City   (A.ADM4)"
        , GN["A.ADM3"]:  "City   (A.ADM3)"
        , GN["A.ADM2"]:  "County (A.ADM2)"
        , GN["A.ADM1"]:  "Region (A.ADM1)"
        , GN["A.PCLI"]:  "Country"
        , GN["L.RGN"]:   "Region (L.RGN)"
        })
    if place_type in place_type_labels:
        type_label = place_type_labels[place_type]
    else:
        type_labels = geo_ont_rdf[place_type:SKOS.prefLabel:]
        for l in type_labels:
            if getattr(l, "language", "en") == "en":
                type_label  = Literal(" ".join(str(l).split()))
                # https://stackoverflow.com/a/46501496/324122
    return type_label

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

# End.

