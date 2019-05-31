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
from commondataexport.graphmapper    import GraphMapper

from commondataexport.emplaces_defs  import (
    SKOS, XSD, SCHEMA, OA, CC, DCTERMS, FOAF, BIBO,
    ANNAL, GN, GEONAMES, WGS84_POS, 
    TIME, PROV, CITO, CRM,
    WD, WDT,
    EM, EMP, EMT, EML, EMS, EMC,
    PLACE, AGENT, REF,
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

emplace_lpif_merged_place_mapping_unused_ = (
    # Top-level blank node for feature collection
    [ M.set_subj(M.stmt_gen(EM.dummy_prop), M.const(BNode()))
    , M.emit(M.stmt_gen(RDF.type, GEOJSON.FeatureCollection), M.stmt_copy())
    # Generate single feature using canonical URI
    , M.emit(M.prop_eq(EM.canonicalURI), M.loc_subgraph(
        M.tgt_subj, M.const(LPO.hasFeature),
        M.src_subj,
        [ M.set_subj(M.stmt_gen(EM.dummy_prop), M.ref_src_obj)
        # Scan all data sources, merging data to referring-statement target subject
        , M.emit(M.prop_eq(EM.place_data), M.loc_subgraph(
            None, None,     # Using same subject as referrer; no new link needed
            M.src_obj,
            [ M.set_subj(M.stmt_gen(EM.dummy_prop), M.ref_tgt_subj)
            , M.emit(M.stmt_gen(RDF.type, GEOJSON.Feature), M.stmt_copy())
            # , M.emit(M.prop_eq(EM.alternateAuthority),    M.stmt_copy())
            , M.emit(M.prop_eq(RDFS.label),             M.stmt_copy())
            # , M.emit(M.prop_eq(RDFS.comment),           M.stmt_copy())
            , M.emit(M.prop_eq(RDFS.label),             M.stmt_copy(p=M.const(DCTERMS.title)))
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
    lpif_graph.bind("place",     PLACE.term(""))
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

    #@@@@
    # m = DataExtractMap(place_uri, emplaces_rdf, lpif_rdf)
    # m.extract_map(emplace_lpif_merged_place_mapping)
    #@@@@

    # Extract and convert data for LPIF
    m = GraphMapper(emplaces_rdf, lpif_rdf)
    lpif_collection = BNode()
    lpif_place_properties = BNode()
    lpif_place_uri        = m.match(place_uri, [EM.canonicalURI]).leaf()
    m.emit(lpif_collection, RDF.type,           GEOJSON.FeatureCollection)
    m.emit(lpif_collection, LPO.hasFeature,     lpif_place_uri)
    m.emit(lpif_place_uri,  RDF.type,           GEOJSON.Feature)
    m.emit(lpif_place_uri,  GEOJSON.properties, lpif_place_properties)
    for src_place in m.match(place_uri, [EM.place_data]).leaves():
        log.debug("src_place %r"%(src_place))
        lpif_place_label = m.match(src_place, [RDFS.label]).leaf()
        lpif_place_match_result = m.match(
            src_place, 
            [ EM.hasRelation, m.filter([EM.relationType], EM.P_PART_OF_A), EM.relationTo, EM.place_data
            , m.repeat([EM.hasRelation, m.filter([EM.relationType], EM.A_PART_OF_A), EM.relationTo, EM.place_data])
            , m.filter([EM.placeType], GN.term("A.PCLI")), GN.countryCode
            ])
        for result in lpif_place_match_result:
            lpif_place_cc = result[-1]
            m.emit(lpif_place_properties, GN.countryCode, lpif_place_cc)

        # ...

    # Moved out of loop so that only one label is used
    m.emit(lpif_place_uri,        RDFS.label,    lpif_place_label)
    m.emit(lpif_place_properties, DCTERMS.title, lpif_place_label)

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

