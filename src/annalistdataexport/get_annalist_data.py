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
import json
import argparse
import urlparse
import logging
import errno
import requests

from rdflib         import Graph, Namespace, URIRef, Literal, BNode, RDF, RDFS
from rdflib.paths   import Path

log = logging.getLogger(__name__)

dirhere = os.path.dirname(os.path.realpath(__file__))
gadroot = os.path.dirname(os.path.join(dirhere))
comroot = os.path.dirname(os.path.join(dirhere, "../"))
sys.path.insert(0, gadroot)
sys.path.insert(0, comroot)

from commondataexport.getargvalue    import getargvalue, getarg
from commondataexport.dataextractmap import DataExtractMap, find_entity_url

from commondataexport.emplaces_defs import (
    SKOS, XSD, SCHEMA, OA, CC, DCTERMS, FOAF, BIBO,
    ANNAL, GN, GEONAMES, WGS84_POS, 
    EM, EMP, EMT, EML, EMS, EMC,
    PLACE, AGENT, REF,
    COMMON_PREFIX_DEFS,
    COMMON_EMPLACES_DEFS,
    COMMON_GEONAMES_DEFS,
    COMMON_LANGUAGE_DEFS,
    add_emplaces_common_namespaces
    )

from commondataexport.rdf_data_utils import (
    get_annalist_uri, get_emplaces_uri_node,
    get_rdf_graph, get_annalist_graph_data, 
    add_turtle_data
    )

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

# Base URL for collection
# (@@TODO: extract this automatically from supplied reference)

COLLECTION_BASE = "http://localhost:8000/annalist/c/EMPlaces_defs/d"

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
    "  %(prog)s getmerged ANNALISTREF\n"+
    "  %(prog)s getsourced ANNALISTREF\n"+
    "  %(prog)s resource ANNALISTREF\n"+
    # "  %(prog)s manyget\n"+
    # "  %(prog)s placehierarchy ANNALISTREF\n"+
    # "  %(prog)s manyplacehierarchy\n"+
    # "  %(prog)s geonamesid URL [REGEXP]\n"
    # "  %(prog)s manygeonamesids [REGEXP]\n"
    "  %(prog)s getwikidata WIKIDATAID\n"+
    "  %(prog)s getwikitext WIKIDATAID\n"+
    "  %(prog)s version\n"+
    "")

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
    elif options.args[0].startswith("getwikid"):
        help_text = ("\n"+
            "  %(prog)s getwikidata WIKIDATAID\n"+
            "\n"+
            "Gets data about a referenced place from Wikidata, and sends \n"+
            "data in Turtle format to standard output.\n"+
            "\n"+
            "")
    elif options.args[0].startswith("getwikit"):
        help_text = ("\n"+
            "  %(prog)s getwikitext WIKIDATAID\n"+
            "\n"+
            "Gets summary text about a referenced place from Wikipedia, and sends \n"+
            "data in Turtle format to standard output.\n"+
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

#   ===================================================================
#
#   RDF data wrangling
#
#   ===================================================================

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

#   ===================================================================
#
#   Wikidata access
#
#   ===================================================================

def get_wikidata_uri(wikidata_id):
    """
    Returns Wikidata place URI, given Wikidata ID (e.g. "Q92212")
    """
    wikidata_base_uri = "http://www.wikidata.org/entity/"
    wikidata_uri     = urlparse.urljoin(wikidata_base_uri, wikidata_id)
    wikidata_url     = find_entity_url(wikidata_uri, "text/turtle")
    return (wikidata_uri, wikidata_url)

def get_wikidata_id(wikidata_uri):
    """
    Returns Wikidata ID (e.g. "Q92212") given Wikidata entity URI, or None.
    """
    wikidata_base_uri = "http://www.wikidata.org/entity/"
    if wikidata_uri.startswith(wikidata_base_uri):
        wikidata_id = wikidata_uri[len(wikidata_base_uri):]
    else:
        wikidata_id = None
    return wikidata_id

def get_wikidata_id_data(wikidata_id, result_rdf=None):
    """
    Get Wikidata place data for a given wikidata id
    """
    wikidata_uri, wikidata_url = get_wikidata_uri(wikidata_id)
    print("wikidata_uri: %s"%(wikidata_uri,), file=sys.stderr)
    print("wikidata_url: %s"%(wikidata_url,), file=sys.stderr)
    wikidata_rdf = get_rdf_graph(wikidata_url, format="turtle")
    # Initial empty graph
    if result_rdf is None:
        result_rdf = Graph()
    # ----- Copy prefixes -----
    use_namespaces = dict(wikidata_rdf.namespaces())
    for prefix, ns_uri in wikidata_rdf.namespaces():
        result_rdf.bind(prefix, ns_uri)
    WDT = Namespace(use_namespaces["wdt"])
    # ----- mapping table -----
    #@@TODO: fix this to pull selected details
    wikidata_data_mapping = (
        [ M.emit(M.prop_eq(RDFS.label), M.stmt_copy())
        , M.emit(M.prop_eq(WDT.P227),  M.stmt_copy())   # GND ID
        , M.emit(M.prop_eq(WDT.P268),  M.stmt_copy())   # BnF ID
        , M.emit(M.prop_eq(WDT.P1566), M.stmt_copy())   # Geonames ID
        , M.emit(M.prop_eq(WDT.P1667), M.stmt_copy())   # Getty TGN ID
        , M.emit(M.prop_eq(WDT.P2503), M.stmt_copy())   # GOV ID
        , M.emit(M.prop_eq(WDT.P1871), M.stmt_copy())   # CERL ID
        , M.emit(M.prop_eq(WDT.P6060), M.stmt_copy())   # MoEML ID
        ])
    # -----
    m = DataExtractMap(wikidata_uri, wikidata_rdf, result_rdf)
    m.extract_map(wikidata_data_mapping)
    return result_rdf

def get_wikidata_id_text(wikidata_id, result_rdf=None):
    """
    Returns Wikidata short text description as an RDF graph.
    """
    article_root = "https://en.wikipedia.org/wiki/"
    summary_root = "https://en.wikipedia.org/api/rest_v1/page/summary/"
    wiki_root    = "https://en.wikipedia.org/"
    # Get wikidata data
    wikidata_uri, wikidata_url = get_wikidata_uri(wikidata_id)
    print("wikidata_uri: %s"%(wikidata_uri,), file=sys.stderr)
    print("wikidata_url: %s"%(wikidata_url,), file=sys.stderr)
    wikidata_rdf = get_rdf_graph(wikidata_url, format="turtle")
    # print(wikidata_rdf.serialize(format='turtle', indent=4), file=sys.stdout)
    summary_url  = None
    summary_data = None
    place_article = None
    if wikidata_rdf:
        # Find reference to english Wikipedia article
        #
        # <https://en.wikipedia.org/wiki/Opole> a schema:Article ;
        # schema:about wd:Q92212 ;
        # schema:inLanguage "en" ;
        # schema:isPartOf <https://en.wikipedia.org/> ;
        # schema:name "Opole"@en .
        #
        place_articles = list(wikidata_rdf[:RDF.type:SCHEMA.Article])
        for a in place_articles:
            if ( (URIRef(wikidata_uri) in wikidata_rdf[a:SCHEMA.about:])    and
                 (URIRef(wiki_root)    in wikidata_rdf[a:SCHEMA.isPartOf:]) and
                 (Literal("en")        in wikidata_rdf[a:SCHEMA.inLanguage:]) ):
                place_article = a
    print("place_article: %s"%(place_article,), file=sys.stderr)
    if place_article:
        # Construct URI of summary page (use path segment from wikipedia page)
        if place_article and place_article.toPython().startswith(article_root):
            article_name = place_article[len(article_root):]
            summary_url  = summary_root + article_name
    if summary_url:
        # Read Summary as JSON, extract 
        # Content-Type: application/json; charset=utf-8; profile="https://www.mediawiki.org/wiki/Specs/Summary/1.4.0"
        # "extract": "Opole (listen) is a city located in southern Poland on the Oder River and the historical capital of Upper Silesia. With a population of approximately 127,792, it is currently the capital of the Opole Voivodeship and, also the seat of Opole County. With its long history dating back to the 8th century, Opole is one of the oldest cities in Poland.",
        # "extract_html": "<p><b>Opole</b> <span class=\"nowrap\" style=\"font-size:85%;\">(<span class=\"unicode haudio\"><span class=\"fn\"><span><figure-inline><span><img src=\"//upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Loudspeaker.svg/11px-Loudspeaker.svg.png\" height=\"11\" width=\"11\" srcset=\"//upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Loudspeaker.svg/22px-Loudspeaker.svg.png 2x, //upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Loudspeaker.svg/17px-Loudspeaker.svg.png 1.5x\" /></span></figure-inline></span>listen</span></span>)</span> is a city located in southern Poland on the Oder River and the historical capital of Upper Silesia. With a population of approximately 127,792, it is currently the capital of the Opole Voivodeship and, also the seat of Opole County. With its long history dating back to the 8th century, Opole is one of the oldest cities in Poland.</p>"
        req_headers = (
            { "accept":     "application/json" 
            })
        response = requests.get(summary_url, headers=req_headers)
        response.raise_for_status()  # raise an error on unsuccessful status codes
        summary_data = json.loads(response.text)
    if summary_data:
        # Assemble result graph (using EMPlaces structure)
        emp_id, emp_uri, emp_node = get_emplaces_uri_node(wikidata_id, suffix="_wikidata")
        if result_rdf is None:
            result_rdf = Graph()
            result_rdf.bind("em", EM.term(""))
            result_rdf.bind("place", PLACE.term(""))
        summary_text = summary_data["extract"]
        result_rdf.add((emp_node, EM.editorialNote, Literal(summary_text)))
    return result_rdf

#   ===================================================================
#
#   Command execution
#
#   ===================================================================

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
    Get arbitrary resource data from Annalist.

    This returns direct statements with minimal interpretation.
    """
    annalist_ref  = getargvalue(getarg(options.args, 0), "Annalist ref: ")
    emplaces_rdf = get_annalist_resource_data(gadroot, annalist_ref)
    get_common_defs(options, emplaces_rdf)
    print(emplaces_rdf.serialize(format='turtle', indent=4), file=sys.stdout)
    return GAD_SUCCESS

def do_get_wikidata_place_data(gadroot, options):
    """
    Get Wikidata RDF for a place
    """
    wikidata_id  = getargvalue(getarg(options.args, 0), "Wikidata ID: ")
    wikidata_rdf = get_wikidata_id_data(wikidata_id)
    print(wikidata_rdf.serialize(format='turtle', indent=4), file=sys.stdout)
    return GAD_SUCCESS

def do_get_wikidata_place_text(gadroot, options):
    """
    Get Wikidata descrioption text for a place, as EMPlaces format RDF.
    """
    wikidata_id  = getargvalue(getarg(options.args, 0), "Wikidata ID: ")
    wikidata_rdf = get_wikidata_id_text(wikidata_id)
    print(wikidata_rdf.serialize(format='turtle', indent=4), file=sys.stdout)
    return GAD_SUCCESS

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
    if options.command.startswith("getwikid"):
        return do_get_wikidata_place_data(gadroot, options)
    if options.command.startswith("getwikit"):
        return do_get_wikidata_place_text(gadroot, options)
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

