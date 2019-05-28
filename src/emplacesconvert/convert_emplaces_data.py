# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# convert_emplaces_data.py - command line tool to convert EMPlaces data
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
import urllib
import logging
import errno
import json
import requests
import datetime

from rdflib         import Graph, Namespace, URIRef, Literal, BNode, RDF, RDFS
from rdflib.paths   import Path

log = logging.getLogger(__name__)

dirhere = os.path.dirname(os.path.realpath(__file__))
emproot = os.path.dirname(os.path.join(dirhere))
comroot = os.path.dirname(os.path.join(dirhere, "../"))
sys.path.insert(0, emproot)
sys.path.insert(0, comroot)

from commondataexport.getargvalue    import getargvalue, getarg
from commondataexport.dataextractmap import (
    DataExtractMap, find_entity_url, make_query_url, http_get_json
    )
from commondataexport.emplaces_defs  import (
    SKOS, XSD, SCHEMA, OA, CC, DCTERMS, FOAF, BIBO,
    ANNAL, GN, GEONAMES, WGS84_POS, 
    TIME, PROV, CITO, CRM,
    WD, WDT,
    EM, EMP, EMT, EML, EMS, EMC,

    COMMON_PREFIX_DEFS,
    COMMON_EMPLACES_DEFS,
    COMMON_GEONAMES_DEFS,
    COMMON_LANGUAGE_DEFS,
    add_emplaces_common_namespaces
    )

from commondataexport.rdf_data_utils import (
    progname, show_error,
    get_emplaces_id, get_emplaces_id_uri_node, get_emplaces_uri_node, get_many_inputs,
    get_rdf_graph, get_geonames_graph_data,
    add_turtle_data, add_resource_attributes,
    get_geonames_place_type_id, get_geonames_place_type_label, 
    format_id_name, format_id_text
    )

#   ===================================================================
#
#   Data constants
#
#   ===================================================================

#   Software version

EMP_VERSION = "0.1"

#   Status return codes

EMP_SUCCESS             = 0         # Success
EMP_BADCMD              = 2         # Command error
EMP_UNKNOWNCMD          = 3         # Unknown command
EMP_UNIMPLEMENTED       = 4         # Unimplemented command or feature
EMP_UNEXPECTEDARGS      = 5         # Unexpected arguments supplied

#   URL data

DATA_BASE_URL   = "file://"+urllib.pathname2url(os.getcwd())+"/"   # Relative data URLs based on current file directory

#   More namespaces

LPO             = Namespace("http://linkedpasts.org/ontology/lpo_latest.ttl#")
LAWD            = Namespace("http://lawd.info/ontology/")
GVP             = Namespace("http://vocab.getty.edu/ontology#")
AAT             = Namespace("http://vocab.getty.edu/aat/")
TGN             = Namespace("http://vocab.getty.edu/tgn/")
GEOJSON         = Namespace("https://purl.org/geojson/vocab#")
GEOJSON_T       = Namespace("https://github.com/kgeographer/geojson-t/")

#   ===================================================================
#
#   RDF mapping data
#
#   ===================================================================

M = DataExtractMap

# annalist_resource_copy = M.ref_subgraph(
#     M.tgt_subj, M.src_prop, M.src_obj,
#     [ M.set_subj(M.prop_eq(ANNAL.uri),          M.src_obj)
#     , M.emit(M.prop_eq(ANNAL.id),               M.stmt_copy())
#     , M.emit(M.prop_eq(ANNAL.type_id),          M.stmt_copy())
#     , M.emit(M.prop_nsne(ANNAL[None]),          M.stmt_copy())
#     ])

# annalist_when_mapping = M.ref_subgraph(
#     M.tgt_subj, M.src_prop, M.src_obj,
#     [ M.set_subj(M.prop_eq(ANNAL.uri),          M.src_obj)
#     , M.emit(M.prop_eq(RDF.type),               M.stmt_copy())
#     , M.emit(M.prop_eq(RDFS.label),             M.stmt_copy())
#     , M.emit(M.prop_eq(RDFS.comment),           M.stmt_copy())
#     , M.emit(M.prop_eq(ANNAL.id),               M.stmt_copy())
#     , M.emit(M.prop_eq(ANNAL.type_id),          M.stmt_copy())
#     , M.emit(M.prop_eq(EM.time_period), # em:time_period
#         M.ref_subgraph(
#             M.tgt_subj, M.src_prop, M.src_obj,
#             [ M.set_subj(M.prop_eq(ANNAL.uri),          M.src_obj)
#             , M.emit(M.prop_eq(RDF.type),               M.stmt_copy())
#             , M.emit(M.prop_eq(RDFS.label),             M.stmt_copy())
#             , M.emit(M.prop_eq(RDFS.comment),           M.stmt_copy())
#             , M.emit(M.prop_eq(ANNAL.id),               M.stmt_copy())
#             , M.emit(M.prop_eq(ANNAL.type_id),          M.stmt_copy())
#             , M.emit(M.prop_eq(EM.timespan),     # em:timespan
#                 M.ref_subgraph(
#                     M.tgt_subj, M.src_prop, M.src_obj,
#                     [ M.set_subj(M.prop_eq(ANNAL.uri),          M.src_obj)
#                     , M.emit(M.prop_eq(RDF.type),               M.stmt_copy())
#                     , M.emit(M.prop_eq(RDFS.label),             M.stmt_copy())
#                     , M.emit(M.prop_eq(RDFS.comment),           M.stmt_copy())
#                     , M.emit(M.prop_eq(EM.start),               M.stmt_copy())
#                     , M.emit(M.prop_eq(EM.end),                 M.stmt_copy())
#                     ])
#                 )
#             ])
#         )
#     ])

# annalist_source_mapping = M.ref_subgraph(
#     M.tgt_subj, M.src_prop, M.src_obj,
#     [ M.set_subj(M.prop_eq(ANNAL.uri),          M.src_obj)
#     , M.emit(M.prop_eq(RDF.type),               M.stmt_copy())
#     , M.emit(M.prop_eq(RDFS.label),             M.stmt_copy())
#     , M.emit(M.prop_eq(RDFS.comment),           M.stmt_copy())
#     , M.emit(M.prop_eq(ANNAL.id),               M.stmt_copy())
#     , M.emit(M.prop_eq(ANNAL.type_id),          M.stmt_copy())
#     , M.emit(M.prop_eq(EM.link),                M.stmt_copy_obj_ne(COLLECTION_BASE+"/"))
#     , M.emit(M.prop_eq(EM.short_label),         M.stmt_copy())
#     ])

# annalist_location_mapping = M.ref_subgraph(
#     M.tgt_subj, M.src_prop, M.src_obj,
#     [ M.set_subj(M.prop_eq(ANNAL.uri),          M.src_obj)
#     , M.emit(M.prop_eq(RDF.type),               M.stmt_copy())
#     , M.emit(M.prop_eq(RDFS.label),             M.stmt_copy())
#     , M.emit(M.prop_eq(RDFS.comment),           M.stmt_copy())
#     , M.emit(M.prop_eq(ANNAL.id),               M.stmt_copy())
#     , M.emit(M.prop_eq(ANNAL.type_id),          M.stmt_copy())
#     , M.emit(M.prop_eq(WGS84_POS.lat),          M.stmt_copy())
#     , M.emit(M.prop_eq(WGS84_POS.long),         M.stmt_copy())
#     ])

# annalist_where_mapping = M.ref_subgraph(
#     M.tgt_subj, M.src_prop, M.src_obj,
#     [ M.set_subj(M.prop_eq(ANNAL.uri),          M.src_obj)
#     , M.emit(M.prop_eq(RDF.type),               M.stmt_copy())
#     , M.emit(M.prop_eq(RDFS.label),             M.stmt_copy())
#     , M.emit(M.prop_eq(RDFS.comment),           M.stmt_copy())
#     , M.emit(M.prop_eq(ANNAL.id),               M.stmt_copy())
#     , M.emit(M.prop_eq(ANNAL.type_id),          M.stmt_copy())
#     , M.emit(M.prop_eq(EM.location),            annalist_location_mapping)
#     , M.emit(M.prop_eq(EM.when),                annalist_when_mapping)
#     , M.emit(M.prop_eq(EM.source),              annalist_source_mapping)
#     ])

# annalist_reference_mapping = M.ref_subgraph(
#     M.tgt_subj, M.src_prop, M.src_obj,
#     [ M.set_subj(M.prop_eq(ANNAL.uri),      M.src_obj)
#     , M.emit(M.prop_eq(RDF.type),           M.stmt_copy())
#     , M.emit(M.prop_eq(RDFS.label),         M.stmt_copy())
#     , M.emit(M.prop_eq(RDFS.comment),       M.stmt_copy())
#     , M.emit(M.prop_eq(ANNAL.id),           M.stmt_copy())
#     , M.emit(M.prop_eq(ANNAL.type_id),      M.stmt_copy())
#     , M.emit(M.prop_eq(DCTERMS.title),      M.stmt_copy())
#     , M.emit(M.prop_eq(DCTERMS.publisher),  annalist_reference_mapping)
#     , M.emit(M.prop_eq(DCTERMS.date),       M.stmt_copy())
#     , M.emit(M.prop_eq(DCTERMS.source),     M.stmt_copy())
#     , M.emit(M.prop_eq(BIBO.authorList),
#         M.ref_list(
#             M.tgt_subj, M.src_prop, M.src_obj,
#             [ M.set_subj(M.prop_eq(ANNAL.uri),      M.src_obj)
#             , M.emit(M.prop_eq(RDF.type),           M.stmt_copy())
#             , M.emit(M.prop_eq(RDFS.label),         M.stmt_copy())
#             , M.emit(M.prop_eq(RDFS.comment),       M.stmt_copy())
#             , M.emit(M.prop_eq(ANNAL.id),           M.stmt_copy())
#             , M.emit(M.prop_eq(ANNAL.type_id),      M.stmt_copy())
#             ])
#         )
#     , M.emit(M.prop_eq(BIBO.isbn10),    M.stmt_copy())
#     , M.emit(M.prop_eq(BIBO.isbn13),    M.stmt_copy())
#     ])

# annalist_relation_mapping = M.ref_subgraph(
#     M.tgt_subj, M.src_prop, M.src_obj,
#     [ M.set_subj(M.prop_eq(ANNAL.uri),      M.src_obj)
#     , M.emit(M.prop_eq(RDF.type),           M.stmt_copy())
#     , M.emit(M.prop_eq(RDFS.label),         M.stmt_copy())
#     , M.emit(M.prop_eq(RDFS.comment),       M.stmt_copy())
#     , M.emit(M.prop_eq(ANNAL.id),           M.stmt_copy())
#     , M.emit(M.prop_eq(ANNAL.type_id),      M.stmt_copy())
#     , M.emit(M.prop_eq(EM.relationTo),      M.stmt_copy())
#     , M.emit(M.prop_eq(EM.relationType),    annalist_reference_mapping)
#     , M.emit(M.prop_eq(EM.when),            annalist_when_mapping)
#     , M.emit(M.prop_eq(EM.competence),      annalist_reference_mapping)
#     , M.emit(M.prop_eq(EM.source),          annalist_source_mapping)
#     ])

# annalist_body_copy = M.ref_subgraph(
#     M.tgt_subj, M.src_prop, M.src_obj,
#     [ M.set_subj(M.prop_eq(ANNAL.uri),          M.src_obj)
#     , M.emit(M.prop_eq(ANNAL.id),               M.stmt_copy())
#     , M.emit(M.prop_eq(ANNAL.type_id),          M.stmt_copy())
#     , M.emit(M.prop_nsne(ANNAL[None]),
#         M.alt_values(
#             M.test_prop_in({EM.language}),
#             M.stmt(M.tgt_subj, M.src_prop, M.src_obj_or_val(ANNAL.uri)),
#             M.stmt_copy()
#             )
#         )
#     ])

# annalist_annotation_mapping = M.ref_subgraph(
#     M.tgt_subj, M.const(OA.hasAnnotation), M.src_obj,
#     [ M.set_subj(M.prop_eq(ANNAL.uri),      M.src_obj)
#     , M.emit(M.prop_eq(RDF.type),           M.stmt_copy())
#     , M.emit(M.prop_eq(RDFS.label),         M.stmt_copy())
#     , M.emit(M.prop_eq(RDFS.comment),       M.stmt_copy())
#     , M.emit(M.prop_eq(ANNAL.id),           M.stmt_copy())
#     , M.emit(M.prop_eq(ANNAL.type_id),      M.stmt_copy())
#     , M.emit(M.prop_eq(OA.hasBody),         annalist_body_copy)
#     , M.emit(M.prop_eq(OA.hasTarget),       M.stmt_copy())
#     , M.emit(M.prop_eq(OA.motivatedBy),     annalist_reference_mapping)
#     , M.emit(M.prop_eq(EM.when),            annalist_when_mapping)
#     , M.emit(M.prop_eq(EM.competence),      annalist_reference_mapping)
#     , M.emit(M.prop_eq(EM.source),          annalist_source_mapping)
#     , M.emit(M.prop_eq(DCTERMS.creator),    annalist_reference_mapping)
#     , M.emit(M.prop_eq(DCTERMS.created),    M.stmt_copy())
#     ])

# annalist_sourced_place_mapping = (
#     [ M.set_subj(M.prop_eq(ANNAL.uri),          M.src_obj)
#     , M.emit(M.prop_eq(RDF.type),               M.stmt_copy())
#     , M.emit(M.prop_eq(RDFS.label),             M.stmt_copy())
#     , M.emit(M.prop_eq(RDFS.comment),           M.stmt_copy())
#     , M.emit(M.prop_eq(RDFS.seeAlso),           M.stmt_copy())
#     , M.emit(M.prop_eq(ANNAL.id),               M.stmt_copy())
#     , M.emit(M.prop_eq(ANNAL.type_id),          M.stmt_copy())
#     , M.emit(M.prop_eq(EM.preferredName),       M.stmt_copy())
#     , M.emit(M.prop_eq(EM.editorialNote),       M.stmt_copy())
#     , M.emit(M.prop_eq(EM.placeCategory),       M.stmt_copy())
#     , M.emit(M.prop_eq(EM.placeType),           M.stmt_copy())
#     , M.emit(M.prop_eq(EM.relatedResource),     annalist_source_mapping)
#     , M.emit(M.prop_eq(EM.source),              annalist_source_mapping)
#     , M.emit(M.prop_eq(EM.alternateAuthority),  annalist_source_mapping)
#     , M.emit(M.prop_eq(EM.when),                annalist_when_mapping)
#     , M.emit(M.prop_eq(EM.where),               annalist_where_mapping)
#     , M.emit(M.prop_eq(EM.reference),           annalist_reference_mapping)
#     , M.emit(M.prop_eq(EM.hasRelation),         annalist_relation_mapping)
#     , M.emit(M.prop_eq(EM.hasNameAttestationAnnotation),    annalist_annotation_mapping)
#     , M.emit(M.prop_eq(EM.hasMapResourceAnnotation),        annalist_annotation_mapping)
#     , M.emit(M.prop_eq(EM.hasCalendarUsedAnnotation),       annalist_annotation_mapping)
#     ])


      # "properties":{
      #   "title": "Abingdon (UK)",
      #   "ccodes": ["GB"]
      # },


emplace_lpif_merged_place_mapping = (
    [ M.set_subj(M.stmt_gen(EM.dummy_prop), M.const(BNode()))
    , M.emit(M.stmt_gen(RDF.type, GEOJSON.FeatureCollection), M.stmt_copy())
    , M.emit(M.prop_eq(EM.canonicalURI), M.loc_subgraph(
        M.tgt_subj, M.const(LPO.hasFeature),
        M.src_subj,
        [ M.set_subj(M.stmt_gen(EM.dummy_prop), M.ref_src_obj)
        , M.emit(M.prop_eq(EM.place_data), M.loc_subgraph(
            M.ref_tgt_subj, M.const(LPO.hasFeature),
            M.src_obj,
            [ M.set_subj(M.stmt_gen(EM.dummy_prop), M.ref_tgt_subj)
            , M.emit(M.stmt_gen(RDF.type, GEOJSON.Feature), M.stmt_copy())
            , M.emit(M.prop_eq(RDFS.label),             M.stmt_copy())
            , M.emit(M.prop_eq(RDFS.comment),           M.stmt_copy())
            ]))
        ]))
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
    "  %(prog)s to-lpif DATAURL PLACEURI\n"+
    "  %(prog)s version\n"+
    "")

def parseCommandArgs(argv):
    """
    Parse command line arguments

    argv            argument list from command line

    Returns a pair consisting of options specified as returned by
    OptionParser, and any remaining unparsed arguments.
    """
    # create a parser for the command line options
    parser = argparse.ArgumentParser(
                description="EMPlaces data converter",
                formatter_class=argparse.RawDescriptionHelpFormatter,
                epilog=command_summary_help
                )
    parser.add_argument('--version', action='version', version='%(prog)s '+EMP_VERSION)
    parser.add_argument("--debug",
                        action="store_true", 
                        dest="debug", 
                        default=False,
                        help="Run with full debug output enabled.  "+
                             "Also creates log file 'convert_emplaces_data.log' in the working directory"
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
        return EMP_UNEXPECTEDARGS
    status = EMP_SUCCESS
    if len(options.args) == 0:
        help_text = (
            command_summary_help+
            "\n"+
            "For more information about command options, use:\n"+
            "\n"+
            "  %(prog)s --help\n"+
            "")
    elif options.args[0].startswith("to-lpif"):
        help_text = ("\n"+
            "  %(prog)s to-lpif DATAURL PLACEURI\n"+
            "\n"+
            "\n"+
            "Reads EMPlaces data from DATAURL, locates a place identified as PLACEURI,\n"+
            "converts the place data to LPIF, and writes the JSON output to standard output.\n"+
            "\n"+
            "Not all data is necessarily converted: just those aspects of the place data that\n"+
            "can be represented as LPIF.\n"+
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
        status = EMP_UNKNOWNCMD
    print(help_text%{'prog': progname}, file=sys.stderr)
    return status

def show_version(emproot, userhome, options):
    """
    Print software version string to standard output.

    emproot     is the root directory for the `emplacesconvert` software installation.
    userhome    is the home directory for the host system user issuing the command.
    options     contains options parsed from the command line.

    returns     0 if all is well, or a non-zero status code.
                This value is intended to be used as an exit status code
                for the calling program.
    """
    if len(options.args) > 0:
        return show_error(
            "Unexpected arguments for %s: (%s)"%(options.command, " ".join(options.args)), 
            EMP_UNEXPECTEDARGS
            )
    status = EMP_SUCCESS
    print(EMP_VERSION)
    # with open(logfilename, "r") as logfile:
    #     shutil.copyfileobj(logfile, sys.stdout)
    return status

#   ===================================================================
#
#   RDF and data wrangling support
#
#   ===================================================================

def add_lpif_common_namespaces(lpif_graph, local_namespaces=None):
    """
    Add common EMPlaces definitions to supplied graph
    """
    lpif_graph.bind("skos",      SKOS.term(""))
    lpif_graph.bind("xsd",       XSD.term(""))
    lpif_graph.bind("oa",        OA.term(""))
    lpif_graph.bind("cc",        CC.term(""))
    lpif_graph.bind("dct",       DCTERMS.term(""))
    lpif_graph.bind("foaf",      FOAF.term(""))
    lpif_graph.bind("bibo",      BIBO.term(""))
    lpif_graph.bind("cito",      CITO.term(""))
    lpif_graph.bind("geonames",  GEONAMES.term(""))
    lpif_graph.bind("gn",        GN.term(""))
    lpif_graph.bind("wgs84_pos", WGS84_POS.term(""))
    lpif_graph.bind("time",      TIME.term(""))
    lpif_graph.bind("prov",      PROV.term(""))
    lpif_graph.bind("crm",       CRM.term(""))
    if local_namespaces is None:
        local_namespaces = (
            { "lpo":        LPO.term("")
            , "lawd":       LAWD.term("")
            , "gvp":        GVP.term("")
            , "aat":        AAT.term("")
            , "tgn":        TGN.term("")
            , "geojson":    GEOJSON.term("")
            , "geojson-t":  GEOJSON_T.term("")
            })
    for pref in local_namespaces:
        lpif_graph.bind(
            pref, 
            local_namespaces[pref]
            )
    return

#   ===================================================================
#
#   Data conversion
#
#   ===================================================================

def convert_to_lpif(emplaces_rdf, place_curie, lpif_rdf):
    """
    Extract and convert place data from supplied RDF graph, and return a new
    graph with data in LPIF format.
    """
    # If place_curie uses namespace in graph, build full URI node
    place_uri  = URIRef(place_curie)
    curieparts = place_curie.split(":", 1)
    if len(curieparts) == 2:
        # for prefix, ns_uri in wikidata_rdf.namespaces():
        #     result_rdf.bind(prefix, ns_uri)
        for pref, ns_uri in emplaces_rdf.namespaces():
            if curieparts[0] == pref:
                place_uri = URIRef(ns_uri+curieparts[1])
                break
    # Create new graph if requiored, and map data
    if lpif_rdf is None:
        lpif_rdf = Graph()
        add_lpif_common_namespaces(lpif_rdf)
    m = DataExtractMap(place_uri, emplaces_rdf, lpif_rdf)
    m.extract_map(emplace_lpif_merged_place_mapping)
    return lpif_rdf

#   ===================================================================
#
#   Command dispatch and execution
#
#   ===================================================================

def do_convert_to_lpif(emproot, options):
    """
    Get LPIF description for a place.
    """
    data_url     = getargvalue(getarg(options.args, 0), "EMPlaces data URL:  ")
    place_curie  = getargvalue(getarg(options.args, 1), "EMPlaces place URI: ")
    data_url     = urlparse.urljoin(DATA_BASE_URL, data_url)
    emplaces_rdf = get_rdf_graph(data_url, format="turtle")
    lpif_rdf = Graph()
    add_lpif_common_namespaces(lpif_rdf)
    lpif_rdf = convert_to_lpif(emplaces_rdf, place_curie, lpif_rdf)
    print(lpif_rdf.serialize(format='turtle', indent=4), file=sys.stdout)
    return EMP_SUCCESS

#   ===================================================================

def do_zzzzzz(emproot, options):
    print("Un-implemented sub-command: %s"%(options.command), file=sys.stderr)
    return EMP_UNIMPLEMENTED

#   ===================================================================

def run(userhome, userconfig, options, progname):
    """
    Command dispatcher.
    """
    if options.command.startswith("@@@"):
        return do_zzzzzz(emproot, options)
    if options.command.startswith("to-lpif"):
        return do_convert_to_lpif(emproot, options)
    if options.command.startswith("ver"):
        return show_version(emproot, userhome, options)
    if options.command.startswith("help"):
        return show_help(options, progname)
    print("Un-recognised sub-command: %s"%(options.command), file=sys.stderr)
    print("Use '%s --help' to see usage summary"%(progname), file=sys.stderr)
    return EMP_BADCMD

def runCommand(userhome, userconfig, argv):
    """
    Run program with supplied configuration base directory, 
    configuration directory and command arguments.

    This is called by main function (below), and also by test suite routines.

    Returns exit status.
    """
    options = parseCommandArgs(argv[1:])
    if options and options.debug:
        logging.basicConfig(level=logging.DEBUG, filename="convert_emplaces_data.log", filemode="w")
    else:
        logging.basicConfig(level=logging.INFO)
    log.debug("runCommand: userhome %s, userconfig %s, argv %s"%(userhome, userconfig, repr(argv)))
    log.debug("Options: %s"%(repr(options)))
    if options:
        progname = os.path.basename(argv[0])
        status   = run(userhome, userconfig, options, progname)
    else:
        status = EMP_BADCMD
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
    if status != EMP_SUCCESS:
        print("Exit status: %d"%(status,), file=sys.stderr)
    sys.exit(status)

# End.

