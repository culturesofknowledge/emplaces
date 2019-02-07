# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# get_geonames_data.py - command line tool to create EMPlaces core from GeoNames data
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
import logging
import errno
import json

from rdflib         import Graph, Namespace, URIRef, Literal, BNode, RDF, RDFS
from rdflib.paths   import Path

log = logging.getLogger(__name__)

dirhere = os.path.dirname(os.path.realpath(__file__))
gcdroot = os.path.dirname(os.path.join(dirhere))
comroot = os.path.dirname(os.path.join(dirhere, "../"))
sys.path.insert(0, gcdroot)
sys.path.insert(0, comroot)

from commondataexport.getargvalue    import getargvalue, getarg
from commondataexport.dataextractmap import (
    DataExtractMap, make_query_url, http_get_json
    )
from commondataexport.emplaces_defs  import (
    SKOS, XSD, OA, CC, DCTERMS, FOAF, BIBO,
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
    progname, show_error,
    get_emplaces_id_uri_node, get_many_inputs,
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

GCD_VERSION = "0.1"

#   Status return codes

GCD_SUCCESS             = 0         # Success
GCD_BADCMD              = 2         # Command error
GCD_UNKNOWNCMD          = 3         # Unknown command
GCD_UNIMPLEMENTED       = 4         # Unimplemented command or feature
GCD_UNEXPECTEDARGS      = 5         # Unexpected arguments supplied
GCD_NO_PLACE_IDS        = 6         # No place ids given
GCD_NO_GEONAMES_URL     = 7         # No GeoNames URL
GCD_SOME_GEONAMES_URLS  = 8         # Some but not all all URLs matched GeoNames IDs
GCD_NO_WIKIDATA_IDS     = 9         # No Wikidata Ids for GeoNames ID
GCD_MANY_WIKIDATA_IDS   = 10        # Multiple Wikidata Ids for GeoNames ID

#   ===================================================================
#
#   Command line parsing and help
#
#   ===================================================================

command_summary_help = ("\n"+
    "Commands:\n"+
    "\n"+
    "  %(prog)s help [command]\n"+
    "  %(prog)s get GEONAMESID\n"+
    "  %(prog)s manyget\n"+
    "  %(prog)s placehierarchy GEONAMESID\n"+
    "  %(prog)s manyplacehierarchy\n"+
    "  %(prog)s geonamesid URL [REGEXP]\n"
    "  %(prog)s manygeonamesids [REGEXP]\n"
    "  %(prog)s wikidataid GEONAMESID\n"+
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
                description="EMPlaces GeoNames data extporter",
                formatter_class=argparse.RawDescriptionHelpFormatter,
                epilog=command_summary_help
                )
    parser.add_argument('--version', action='version', version='%(prog)s '+GCD_VERSION)
    parser.add_argument("--debug",
                        action="store_true", 
                        dest="debug", 
                        default=False,
                        help="Run with full debug output enabled.  "+
                             "Also creates log file 'get-geonames-data.log' in the working directory"
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
        return GCD_UNEXPECTEDARGS
    status = GCD_SUCCESS
    if len(options.args) == 0:
        help_text = (
            command_summary_help+
            "\n"+
            "For more information about command options, use:\n"+
            "\n"+
            "  %(prog)s --help\n"+
            "")
    elif options.args[0].startswith("manyget"):
        help_text = ("\n"+
            "  %(prog)s manyget\n"+
            "\n"+
            "\n"+
            "Reads GeoNames place Ids from stdin, one per line, retrieves data\n"+
            "for these from GeoNames, and sends corresponding EMPlaces data in\n"+
            "Turtle format to standard output.\n"+
            "\n"+
            "To include some common non-place-specific supporting definitions, see options\n"+
            "'--include-common-defs', '--include-emplaces-defs', '--include-geonames-defs', \n"+
            "and '--include-language-defs'.\n"+
            "\n"+
            "")
    elif options.args[0].startswith("get"):
        help_text = ("\n"+
            "  %(prog)s get GEONAMESID\n"+
            "\n"+
            "Gets data about a specified place from GeoNames, and sends corresponding\n"+
            "EMPlaces data in Turtle format to standard output.\n"+
            "\n"+
            "To include some common non-place-specific supporting definitions, see options\n"+
            "'--include-common-defs', '--include-emplaces-defs', '--include-geonames-defs', \n"+
            "and '--include-language-defs'.\n"+
            "\n"+
            "")
    elif options.args[0].startswith("placeh"):
        help_text = ("\n"+
            "  %(prog)s placehierarchy GEONAMESID\n"+
            "\n"+
            "Gets current administrative hierarchy about a place from GeoNames, \n"+
            "and outputs a list of place Ids, one per line, to standard output.\n"+
            "\n"+
            "The output can be used as input to a `manyget` command.\n"+
            "\n"+
            "")
    elif options.args[0].startswith("manyplaceh"):
        help_text = ("\n"+
            "  %(prog)s manyplacehierarchy\n"+
            "\n"+
            "Reads GeoNames place Ids from stdin, one per line, and for each retrieves\n"+
            "place ids in the current administrative hierarch up as far as country\n"+
            "level, and outputs the resuting list of place IDs (including the input IDs)\n"+
            "to stdout, one per line.\n"+
            "\n"+
            "The output can be used as input to a `manyget` command.\n"+
            "\n"+
            "")
    elif options.args[0].startswith("geo"):
        help_text = ("\n"+
            "  %(prog)s geonamesid URL [REGEXP]\n"+
            "\n"+
            "URL is presumed to be a GeoNames URL or other string containing a GeoNames Id.  \n"+
            "Extracts the Geonames Id and writes it to stdout, or a diagnostic message is \n"+
            "output to stderr along with an exit status of %d\n"%(GCD_NO_GEONAMES_URL)+
            "\n"+
            "If REGEXP is specified, this command uses it as a regular expression \n"+
            "(per https://docs.python.org/2/library/re.html#regular-expression-syntax) \n"+
            "which, if it matches the supplied URL, returns the substring matching the\n"+
            "first parenthesized sub-expression as the GeoNames Id.  E.g., for a GeoNames\n"+
            "URL of the form 'http://www.geonames.org/2638655/shropshire.html', use \n"+
            "a REGEXP like 'http://www\.geonames\.org/([0-9]+)/.+$'.\n"+
            "\n"+
            "If REGEXP is not matched, a diagnostic message is output to stderr.\n"+
            "\n"+
            "If REGEXP is not supplied, a range of internal REGEXPs is used to try and\n"+
            "extract the GeroNames id.\n"+
            "\n"+
            "The output can be used as input to a `manyget` or similar command.\n"+
            "\n"+
            "")
    elif options.args[0].startswith("manygeo"):
        help_text = ("\n"+
            "  %(prog)s manygeonamesids [REGEXP]\n"+
            "\n"+
            "Reads a list of GeoNames URLs (or other strings that are presumed to \n"+
            "contain a geoNames Id) one per line from stdin and, ignoring any that \n"+
            "start with a '#', extracts the embedded GeoNames place ids, and \n"+
            "outputs the resuting list of GeoNames IDs to stdout, one per line. \n"+
            "\n"+
            "Non-matching inputs are reported to stderr.\n"+
            "\n"+
            "REGEXP is an optional regular exression used for extracting the Ids.\n"+
            "See 'geonamesid' command for more details.\n"+
            "\n"+
            "Returns exit status:\n"+
            "  %d if all input strings are matched and processed,\n"%(GCD_SUCCESS)+
            "  %d if no input strings could be matched and processed, or\n"%(GCD_NO_GEONAMES_URL)+
            "  %d if some input strings could not be matched and processed.\n"%(GCD_SOME_GEONAMES_URLS)+
            "\n"+
            "The output can be used as input to a `manyget` or similar command.\n"+
            "\n"+
            "")
    elif options.args[0].startswith("wikidataid"):
        help_text = ("\n"+
            "  %(prog)s wikidataid geonamesid\n"+
            "\n"+
            "Determines a Wikidata Id corresponding to the supplied Geonames Id,\n"+
            "and writes it to stdout, or a diagnostic message is output to stderr\n"+
            "along with an exit status of %d or %d\n"%(GCD_NO_WIKIDATA_IDS, GCD_MANY_WIKIDATA_IDS)+
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
        status = GCD_UNKNOWNCMD
    print(help_text%{'prog': progname}, file=sys.stderr)
    return status

def show_version(gcdroot, userhome, options):
    """
    Print software version string to standard output.

    gcdroot     is the root directory for the `geonamesdataexport` software installation.
    userhome    is the home directory for the host system user issuing the command.
    options     contains options parsed from the command line.

    returns     0 if all is well, or a non-zero status code.
                This value is intended to be used as an exit status code
                for the calling program.
    """
    if len(options.args) > 0:
        return show_error(
            "Unexpected arguments for %s: (%s)"%(options.command, " ".join(options.args)), 
            GCD_UNEXPECTEDARGS
            )
    status = GCD_SUCCESS
    print(GCD_VERSION)
    # with open(logfilename, "r") as logfile:
    #     shutil.copyfileobj(logfile, sys.stdout)
    return status

#   ===================================================================
#
#   Id and URI wrangling.  Hacky URI introspection is isolated here.
#
#   ===================================================================

def get_geonames_uri(geonames_id):
    """
    Returns tuple of
        0. GeoNames place URI
        1. GeoNames place description URL
    """
    geonames_uri  = "http://sws.geonames.org/%s/"%(geonames_id,)
    geonames_url  = "http://sws.geonames.org/%s/about.rdf"%(geonames_id,)
    return (geonames_uri, geonames_url)

def get_geonames_id(geonames_uri):
    """
    Given a GeoNames place URI, returns the GeoNames place Id
    """
    geonames_path = geonames_uri.replace("http://sws.geonames.org/", "").split("/")
    geonames_id   = geonames_path[0]
    return geonames_id

def get_many_place_ids():
    geonames_ids = get_many_inputs()
    if not geonames_ids:
        print("No place Ids found", file=sys.stderr)
    return geonames_ids    

def get_many_geonames_urls():
    geonames_urls = get_many_inputs()
    if not geonames_urls:
        print("No GeoNames URLs found", file=sys.stderr)
    return geonames_urls    

#   ===================================================================
#
#   RDF data wrangling
#
#   ===================================================================

def get_geonames_ontology():
    """
    Return Graph of GeoNames ontology data
    """
    geo_ont_url  = "http://www.geonames.org/ontology/ontology_v3.1.rdf"
    geo_ont_rdf  = get_geonames_graph_data(geo_ont_url)
    return geo_ont_rdf

geonames_cache = {}     # Don't get data if we've already retrieved it.
def get_geonames_place_data(geonames_url):
    """
    Returns graph of GeoNames place data
    """
    if geonames_url not in geonames_cache:
        geonames_rdf = get_geonames_graph_data(geonames_url)
        geonames_cache[geonames_url] = geonames_rdf
    return geonames_cache[geonames_url]
    # return geonames_rdf

def add_place_location(emp_rdf, place_lat, place_long):
    """
    Create BNode for location - supplied lat, long are string literals
    """
    b_location = BNode()
    emp_rdf.add((b_location, RDF.type,       EM.Location_value))
    emp_rdf.add((b_location, WGS84_POS.lat,  Literal(str(place_lat),  datatype=XSD.double)))
    emp_rdf.add((b_location, WGS84_POS.long, Literal(str(place_long), datatype=XSD.double)))
    return b_location

def _unused_add_source(emp_rdf, label, link):
    """
    Create BNode for source
    """
    b_source = BNode()
    emp_rdf.add((b_source, RDF.type,    EM.Source_ref))
    emp_rdf.add((b_source, RDFS.label,  label        ))
    emp_rdf.add((b_source, EM.link,     link         ))
    return b_source

def add_place_setting(emp_rdf, location, when, source):
    b_setting  = BNode()
    emp_rdf.add((b_setting, RDF.type,    EM.Setting))
    emp_rdf.add((b_setting, EM.location, location  ))
    emp_rdf.add((b_setting, EM.when,     when      ))
    emp_rdf.add((b_setting, EM.source,   source    ))
    return b_setting

def add_place_relation(emp_rdf, reltype, relto, relwhen, relcompetence, source):
    """
    Adds a relaton description to the graph, and returns the node from which it is built.
    """
    b_relation = BNode()
    emp_rdf.add((b_relation, RDF.type,        EM.Qualified_relation))
    emp_rdf.add((b_relation, EM.relationType, reltype              ))
    emp_rdf.add((b_relation, EM.relationTo,   relto                ))
    emp_rdf.add((b_relation, EM.when,         relwhen              ))
    emp_rdf.add((b_relation, EM.source,       source               ))
    return b_relation

def get_emplaces_core_data(
    geonames_id, geonames_uri, geonames_url, geonames_rdf, geo_ont_rdf,
    emplaces_rdf=None
    ):
    """
    Constructs EMPlaces RDF data from supplied GeoNames place data.

    Returns tuple of:
        0. EMPlaces Id for place
        1. EMPlaces URI for place
        2. Graph of EMPlaces data
    """
    if geonames_rdf is None:
        msg = "No RDF data for %s"%(geonames_url,)
        log.error(msg)
        raise ValueError(msg)

    try:
        geonames_node     = URIRef(geonames_uri)
        place_name        = geonames_rdf[geonames_node:GN.name:].next()
        place_altnames    = list(geonames_rdf[geonames_node:GN.alternateName:])
        place_def_by      = URIRef(geonames_url)
        place_category    = geonames_rdf[geonames_node:GN.featureClass:].next()
        place_type        = geonames_rdf[geonames_node:GN.featureCode:].next()
        place_map         = geonames_rdf[geonames_node:GN.locationMap:].next()
        place_parent      = geonames_rdf[geonames_node:GN.parentFeature:].next()
        place_country     = geonames_rdf[geonames_node:GN.countryCode:].next()
        place_seeAlso     = list(geonames_rdf[geonames_node:(RDFS.seeAlso|GN.wikipediaArticle):])
        place_lat         = geonames_rdf[geonames_node:WGS84_POS.lat:].next()
        place_long        = geonames_rdf[geonames_node:WGS84_POS.long:].next()
        place_type_label  = get_geonames_place_type_label(place_type, geo_ont_rdf)
        display_label     = Literal("%s (%s)"%(place_name, place_type_label)) 
        display_names     = list(set([Literal(unicode(n)) for n in place_altnames]))
    except Exception as e:
        log.error("Problem accessing data for %s"%(geonames_url,), exc_info=True)
        raise
    log.debug("get_emplaces_core_data: geonames_node   %r"%(geonames_node))
    log.debug("get_emplaces_core_data: place_name:     %r"%(place_name))
    log.debug("get_emplaces_core_data: place_altnames: %r"%(place_altnames))
    log.debug("get_emplaces_core_data: place_def_by:   %r"%(place_def_by))
    log.debug("get_emplaces_core_data: place_category: %r"%(place_category))
    log.debug("get_emplaces_core_data: place_type:     %r"%(place_type))
    log.debug("get_emplaces_core_data: place_map:      %r"%(place_map))
    log.debug("get_emplaces_core_data: place_parent:   %r"%(place_parent))
    log.debug("get_emplaces_core_data: place_seeAlso:  %r"%(place_seeAlso))
    log.debug("get_emplaces_core_data: lat, long:      %r, %r"%(place_lat, place_long))
    log.debug("get_emplaces_core_data: display_label:  %r"%(display_label))
    log.debug("get_emplaces_core_data: display_names:  %s"%(",".join(display_names)))
    log.debug("get_emplaces_core_data: GeoNames graph:")
    log.debug(geonames_rdf.serialize(format='turtle', indent=4))

    # Initial empty graph
    if emplaces_rdf is None:
        emplaces_rdf = Graph()
        add_emplaces_common_namespaces(emplaces_rdf, local_namespaces={})
    # for gn_pre, gn_uri in geonames_rdf.namespaces():
    #     emplaces_rdf.bind(gn_pre, gn_uri)
    lit_geonames_data = Literal("GeoNames data for %s"%(place_name,))
    lit_geonames_uri  = Literal("GeoNames URI for %s"%(place_name,))

    # Allocate URIs and nodes for merged and geonames data
    emp_id_merged, emp_uri_merged, emp_node_merged = get_emplaces_id_uri_node(
        place_name, place_type, geonames_id
        )
    emp_id_geonames, emp_uri_geonames, emp_node_geonames = get_emplaces_id_uri_node(
        place_name, place_type, geonames_id, suffix="_geonames"
        )
    ems_uri_geonames_source  = EMS[emp_id_geonames]
    ems_node_geonames_source = URIRef(ems_uri_geonames_source)

    # Add em:Place_merged description
    emplaces_rdf.add((emp_node_merged, RDF.type, EM.Place))
    emplaces_rdf.add((emp_node_merged, RDF.type, EM.Place_merged))
    emplaces_rdf.add((emp_node_merged, EM.canonicalURI, emp_node_merged))
    b_alturi = BNode()
    emplaces_rdf.add((emp_node_merged,  EM.alternateURI,  b_alturi))
    emplaces_rdf.add((b_alturi,  RDFS.label, lit_geonames_uri ))
    emplaces_rdf.add((b_alturi,  EM.link,    geonames_node    ))
    emplaces_rdf.add((emp_node_merged, EM.place_data, emp_node_geonames))

    # Add description of GeoNames source
    emplaces_rdf.add((ems_node_geonames_source, RDF.type,       EM.Authority       ))
    emplaces_rdf.add((ems_node_geonames_source, RDFS.label,     lit_geonames_data  ))
    emplaces_rdf.add((ems_node_geonames_source, EM.short_label, Literal("GeoNames")))
    emplaces_rdf.add((ems_node_geonames_source, EM.link,        place_def_by       ))

    # Add em:Place_sourced description for GeoNames
    emplaces_rdf.add((emp_node_geonames,  RDF.type,         EM.Place                ))
    emplaces_rdf.add((emp_node_geonames,  RDFS.label,       display_label           ))
    emplaces_rdf.add((emp_node_geonames,  RDFS.isDefinedBy, place_def_by            ))
    emplaces_rdf.add((emp_node_geonames,  EM.source,        ems_node_geonames_source))
    emplaces_rdf.add((emp_node_geonames,  EM.placeCategory, place_category          ))
    emplaces_rdf.add((emp_node_geonames,  EM.placeType,     place_type              ))
    emplaces_rdf.add((emp_node_geonames,  EM.preferredName, place_name              ))
    for an in place_altnames:
        emplaces_rdf.add((emp_node_geonames, EM.alternateName, an))
    for dn in display_names:
        emplaces_rdf.add((emp_node_geonames, EM.displayName, dn))
    for sa in place_seeAlso:
        emplaces_rdf.add((emp_node_geonames, RDFS.seeAlso, sa))

    # Define setting for current location
    b_location = add_place_location(emplaces_rdf, place_lat, place_long)
    b_setting  = add_place_setting(emplaces_rdf, 
        b_location, 
        EMT.Current, 
        ems_node_geonames_source
        )
    emplaces_rdf.add((emp_node_geonames, EM.where, b_setting))

    # Add country code
    emplaces_rdf.add((emp_node_geonames, GN.countryCode, place_country))

    # Define relation for current admin hierarchy (1 level up only)
    parent_geonames_id = get_geonames_id(str(place_parent))
    parent_gn_node, parent_gn_rdf = get_geonames_place_rdf(parent_geonames_id)
    parent_name        = parent_gn_rdf[parent_gn_node:GN.name:].next()
    parent_type        = parent_gn_rdf[parent_gn_node:GN.featureCode:].next()
    parent_id, parent_uri, parent_node = get_emplaces_id_uri_node(
        parent_name, parent_type, parent_geonames_id, suffix="_geonames"
        )
    b_relation = add_place_relation(emplaces_rdf, 
        EM.P_PART_OF_A, parent_node,
        EMT.Current, 
        EM.DEFINITIVE,
        ems_node_geonames_source
        )
    emplaces_rdf.add((emp_node_geonames, EM.hasRelation, b_relation))

    # Define map resource for current
    b_body = add_resource_attributes(emplaces_rdf, 
        { RDFS.label:       Literal("Current map for %s"%(place_name,))
        , EM.link:          place_map
        })
    b_annotation = add_resource_attributes(emplaces_rdf, 
        { RDF.type:         OA.Annotation
        , OA.motivatedBy:   EM.MAP_RESOURCE
        , OA.hasTarget:     emp_node_geonames
        , OA.hasBody:       b_body
        , EM.when:          EMT.Current
        , EM.source:        ems_node_geonames_source
        })
    emplaces_rdf.add((emp_node_geonames, EM.hasAnnotation, b_annotation))
    return (emp_id_merged, emp_uri_merged, emplaces_rdf)

def get_geonames_id_data(gcdroot, geonames_id, emplaces_rdf=None):
    """
    Build EMPlaces place data for a specified GeoNames place id.
    """
    geonames_uri, geonames_url = get_geonames_uri(geonames_id)
    geonames_rdf = get_geonames_place_data(geonames_url)
    geo_ont_rdf  = get_geonames_ontology()
    emplaces_id, emplaces_uri, emplaces_rdf = get_emplaces_core_data(
        geonames_id, geonames_uri, geonames_url, geonames_rdf, geo_ont_rdf,
        emplaces_rdf=emplaces_rdf
        )
    return emplaces_rdf

def get_common_defs(options, emplaces_rdf):
    if options.emplaces_defs or options.common_defs:
        add_turtle_data(emplaces_rdf, COMMON_EMPLACES_DEFS)
    if options.geonames_defs or options.common_defs:
        add_turtle_data(emplaces_rdf, COMMON_GEONAMES_DEFS)
    if options.language_defs or options.common_defs:
        add_turtle_data(emplaces_rdf, COMMON_LANGUAGE_DEFS)
    return emplaces_rdf

def do_get_geonames_place_data(gcdroot, options):
    geonames_id  = getargvalue(getarg(options.args, 0), "GeoNames Id: ")
    emplaces_rdf = get_geonames_id_data(gcdroot, geonames_id)
    get_common_defs(options, emplaces_rdf)
    print(emplaces_rdf.serialize(format='turtle', indent=4), file=sys.stdout)
    return GCD_SUCCESS

def do_get_many_geonames_place_data(gcdroot, options):
    """
    Read multiple place Ids from standard input, and return a graph of
    EMPlaces data for all of the identified places.
    """
    emplaces_rdf = None     # Graph created on first loop below
    geonames_ids = get_many_place_ids()
    if not geonames_ids:
        return GCD_NO_PLACE_IDS
    for geonames_id in geonames_ids:
        try:
            emplaces_rdf = get_geonames_id_data(
                gcdroot, geonames_id, emplaces_rdf=emplaces_rdf
                )
        except Exception as e:
            log.error(
                "Error getting data for GeoNames Id %s"%(geonames_id), 
                exc_info=True
                )
    get_common_defs(options, emplaces_rdf)
    print(emplaces_rdf.serialize(format='turtle', indent=4), file=sys.stdout)
    return GCD_SUCCESS

def get_geonames_place_rdf(place_id):
    log.debug("get_geonames_place_rdf(%s)"%(place_id))
    place_uri, place_url = get_geonames_uri(place_id)
    place_node   = URIRef(place_uri)
    place_rdf    = get_geonames_place_data(place_url)
    return (place_node, place_rdf)

def get_geonames_place_name_type_parent(place_node, place_rdf):
    place_name = None
    place_type = None
    parent_id  = None
    for place_type in place_rdf[place_node:GN.featureCode:]:
        break
    for place_name in place_rdf[place_node:GN.name:]:
        break
    for parent_node in place_rdf[place_node:GN.parentFeature:]:
        parent_id = get_geonames_id(str(parent_node))
        break
    if place_type == GN["A.PCLI"]:
        parent_id = None     # No parent place for country
    return (place_name, place_type, parent_id)

def get_place_admin_hierarchy(place_ids, hier_ids):
    """
    Reads admin hierarchy places directly out of a place record

    This is an alternative to `get_places_hierarchy` which walks the parent featiure
    links up the tree.  We have found the parent links are not always consistent.
    """
    log.debug("get_places_hierarchy(%s, %s)"%(place_ids, hier_ids))
    admin_parent_properties = (
        [ GN.parentADM5
        , GN.parentADM4
        , GN.parentADM3
        , GN.parentADM2
        , GN.parentADM1
        , GN.parentCountry
        ])
    for place_id in place_ids:
        if place_id not in hier_ids:
            place_node, place_rdf = get_geonames_place_rdf(place_id)
            place_name, place_type, parent_id = (
                get_geonames_place_name_type_parent(place_node, place_rdf)
                )
            hier_ids[place_id] = (place_id, place_name, place_type)
            for prop in admin_parent_properties:
                for parent_obj in place_rdf[place_node:prop:]:
                    parent_id = get_geonames_id(parent_obj)
                    if parent_id not in hier_ids:
                        log.debug("get_places_hierarchy: parent_id %s"%(parent_id,))
                        parent_node, parent_rdf = get_geonames_place_rdf(parent_id)
                        parent_name, parent_type, grandparent_id = (
                            get_geonames_place_name_type_parent(parent_node, parent_rdf)
                            )
                        hier_ids[parent_id] = (parent_id, parent_name, parent_type)
    return hier_ids

def get_places_hierarchy(place_ids, hier_ids):
    log.debug("get_places_hierarchy(%s, %s)"%(place_ids, hier_ids))
    for place_id in place_ids:
        if place_id not in hier_ids:
            place_node, place_rdf = get_geonames_place_rdf(place_id)
            place_name, place_type, parent_id = (
                get_geonames_place_name_type_parent(place_node, place_rdf)
                )
            hier_ids[place_id] = (place_id, place_name, place_type)
            if parent_id:
                hier_ids   = get_places_hierarchy([parent_id], hier_ids)
    return hier_ids

def do_get_place_hierarchy(gcdroot, options):
    geo_ont_rdf = get_geonames_ontology()
    geonames_id = getargvalue(getarg(options.args, 0), "GeoNames Id: ")
    #@@ follow parentFeature links: results are inconsistent.
    # hier_id_name_types = get_places_hierarchy([geonames_id], {})
    #@@
    hier_id_name_types = get_place_admin_hierarchy([geonames_id], {})
    for p, n, t in hier_id_name_types.values():
        print(format_id_name(p, n, t, geo_ont_rdf), file=sys.stdout)
    return GCD_SUCCESS

def do_get_many_place_hierarchy(gcdroot, options):
    geo_ont_rdf = get_geonames_ontology()
    place_ids   = get_many_place_ids()
    if not place_ids:
        return GCD_NO_PLACE_IDS
    #@@ follow parentFeature links: results are inconsistent.
    # hier_id_name_types = get_places_hierarchy(place_ids, {})
    #@@
    hier_id_name_types = get_place_admin_hierarchy(place_ids, {})
    for p, n, t in hier_id_name_types.values():
        print(format_id_name(p, n, t, geo_ont_rdf), file=sys.stdout)
    return GCD_SUCCESS

def extract_geonames_id(url, rex):
    """
    Extract GeoNames Id from URL or string using suplied Regexp,
    if range of built-in defails regexps.
    Returns extracted Id or None.
    """
    default_rex = (
        [ r"https?://www\.geonames\.org/([0-9]+)/.+$"
        , r"https?://sws\.geonames\.org/([0-9]+)/about\.rdf$"
        ])

    def match_geonames_id(url, rex):
        """
        Local helper to match and process a specified regexp.
        Returns extracted Id or None.
        """
        log.debug("match_geonames_id: url %s, regexp /%s/"%(url, rex))
        geo_id = None
        try:
            matchobject = re.match(rex, url)
            if matchobject:
                geo_id = matchobject.group(1)
        except IndexError:
            geo_id = None
        except re.error as e:
            print("Invalid regular expression '%s' (%s)"%(rex, e), file=sys.stderr)
            raise
        return geo_id

    if rex:
        geo_id = match_geonames_id(url, rex)
    else:
        for rex in default_rex:
            geo_id = match_geonames_id(url, rex)
            if geo_id:
                break
    return geo_id

def do_extract_geonames_id(gcdroot, options):
    url    = getargvalue(getarg(options.args, 0), "GeoNames URL: ")
    # rex = getargvalue(getarg(options.args, 1), "Regexp:       ")
    rex    = getarg(options.args, 1) or ""
    geo_id = extract_geonames_id(url, rex)
    if not geo_id:
        print("No match: %s"%(url,), file=sys.stderr)
        return GCD_NO_GEONAMES_URL
    print(format_id_text(geo_id, url), file=sys.stdout)
    return GCD_SUCCESS

def do_extract_many_geonames_ids(gcdroot, options):
    # No prompt fpr mamy-value input
    rex    = getarg(options.args, 0) or ""
    urls   = get_many_geonames_urls()
    status = GCD_NO_GEONAMES_URL
    match_seen = False
    fail_seen  = False
    for url in urls:
        geo_id = extract_geonames_id(url, rex)
        if geo_id:
            print(format_id_text(geo_id, url), file=sys.stdout)
            match_seen = True
        else:
            print("No match: %s"%(url,), file=sys.stderr)
            fail_seen = True
    if match_seen:
        if fail_seen:
            status = GCD_SOME_GEONAMES_URLS
        else:
            status = GCD_SUCCESS
    return status

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

def wikidata_sparql_query(query, endpoint="https://query.wikidata.org/sparql"):
    query_url      = make_query_url(endpoint, query=query)
    # print("@@@ query URL:\n--\n%s\n--"%(query_url,), file=sys.stderr)
    query_response = http_get_json(query_url)
    # print("@@@ query_response:\n--\n%s\n--"%(query_response,), file=sys.stderr)
    return json.loads(query_response)

def do_extract_wikidata_id(gcdroot, options):
    geo_id = getargvalue(getarg(options.args, 0), "GeoNames ID: ")
    wikidata_query = ("""
        SELECT ?item ?itemLabel 
        WHERE 
        {
          ?item wdt:P1566 "%s" .
          SERVICE wikibase:label 
            { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
        }
        """)%(geo_id,)
    query_response_dict = wikidata_sparql_query(wikidata_query)
    # print("@@@ query_response_dict:\n--\n%s\n--"%
    #     (json.dumps(query_response_dict, sort_keys=True, indent=4),), 
    #     file=sys.stderr
    #     )
    # @@@@@ print(format_id_text(geo_id, url), file=sys.stdout)
    result_bindings = query_response_dict["results"]["bindings"]
    ids_uris_labels = (
        [ ( get_wikidata_id(b["item"]["value"])
          , b["item"]["value"]
          , b["itemLabel"]["value"]
          ) 
          for b in result_bindings 
        ])
    if len(ids_uris_labels) == 0:
        print("No Wikidata IDs found for %s"%(geo_id,), file=sys.stderr)
        return GCD_NO_WIKIDATA_IDS
    elif len(ids_uris_labels) != 1:
        print("Multiple Wikidata IDs found for %s:"%(geo_id,), file=sys.stderr)
        print("  %s"%([i for i,u,l in ids_uris_labels],), file=sys.stderr)
        return GCD_MANY_WIKIDATA_IDS
    print(ids_uris_labels[0][0], file=sys.stdout)
    return GCD_SUCCESS

#   ===================================================================

def do_zzzzzz(gcdroot, options):
    print("Un-implemented sub-command: %s"%(options.command), file=sys.stderr)
    return GCD_UNIMPLEMENTED

#   ===================================================================

def run(userhome, userconfig, options, progname):
    """
    Command dispatcher.
    """
    if options.command.startswith("@@@"):
        return do_zzzzzz(gcdroot, options)
    if options.command.startswith("get"):
        return do_get_geonames_place_data(gcdroot, options)
    if options.command.startswith("manyget"):
        return do_get_many_geonames_place_data(gcdroot, options)
    if options.command.startswith("placeh"):
        return do_get_place_hierarchy(gcdroot, options)
    if options.command.startswith("manyplaceh"):
        return do_get_many_place_hierarchy(gcdroot, options)
    if options.command.startswith("geo"):
        return do_extract_geonames_id(gcdroot, options)
    if options.command.startswith("manygeo"):
        return do_extract_many_geonames_ids(gcdroot, options)
    if options.command.startswith("wikidataid"):
        return do_extract_wikidata_id(gcdroot, options)
    if options.command.startswith("ver"):
        return show_version(gcdroot, userhome, options)
    if options.command.startswith("help"):
        return show_help(options, progname)
    print("Un-recognised sub-command: %s"%(options.command), file=sys.stderr)
    print("Use '%s --help' to see usage summary"%(progname), file=sys.stderr)
    return GCD_BADCMD

def runCommand(userhome, userconfig, argv):
    """
    Run program with supplied configuration base directory, 
    configuration directory and command arguments.

    This is called by main function (below), and also by test suite routines.

    Returns exit status.
    """
    options = parseCommandArgs(argv[1:])
    if options and options.debug:
        logging.basicConfig(level=logging.DEBUG, filename="get-geonames-data.log", filemode="w")
    else:
        logging.basicConfig(level=logging.INFO)
    log.debug("runCommand: userhome %s, userconfig %s, argv %s"%(userhome, userconfig, repr(argv)))
    log.debug("Options: %s"%(repr(options)))
    if options:
        progname = os.path.basename(argv[0])
        status   = run(userhome, userconfig, options, progname)
    else:
        status = GCD_BADCMD
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
    if status != GCD_SUCCESS:
        print("Exit status: %d"%(status,), file=sys.stderr)
    sys.exit(status)

# End.

