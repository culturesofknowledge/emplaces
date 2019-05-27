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
import urlparse
import logging
import errno
import json
import requests
import datetime

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
    DataExtractMap, find_entity_url, make_query_url, http_get_json
    )
from commondataexport.emplaces_defs  import (
    SKOS, XSD, SCHEMA, OA, CC, DCTERMS, FOAF, BIBO,
    ANNAL, GN, GEONAMES, WGS84_POS, 
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
#   RDF mapping data
#
#   ===================================================================

M = DataExtractMap

def get_geonames_source_reference_mapping(emp_id_sourced, geonames_url, place_label):
    geonames_link_node      = URIRef(geonames_url)
    geonames_source_node    = URIRef(EMS[emp_id_sourced])
    geonames_source_label   = Literal("GeoNames data for %s"%(place_label,))
    geonames_source_tag     = Literal("GeoNames")
    geonames_source_descr   = Literal("Data from GeoNames URL %s"%(geonames_url,))
    geonames_access_date    = Literal(datetime.date.today().isoformat())
    geonames_source_mapping = M.emit(
        M.stmt_gen(EM.source, geonames_source_node), M.loc_subgraph(
            M.tgt_subj, M.src_prop, M.src_obj,
            [ M.emit(M.stmt_gen(RDF.type, EM.Source_desc),                M.stmt_copy())
            , M.emit(M.stmt_gen(RDF.type, EM.Authority),                  M.stmt_copy())
            , M.emit(M.stmt_gen(EM.short_label, geonames_source_tag),     M.stmt_copy())
            , M.emit(M.stmt_gen(RDFS.label, geonames_source_label),       M.stmt_copy())
            , M.emit(M.stmt_gen(EM.editorialNote, geonames_source_descr), M.stmt_copy())
            , M.emit(M.stmt_gen(EM.link, geonames_link_node),             M.stmt_copy())
            , M.emit(M.stmt_gen(EM.licence, EMS.GeoNames_licence),        M.stmt_copy())
            , M.emit(M.stmt_gen(EM.accessed, geonames_access_date),       M.stmt_copy())
            ])
        )
    return geonames_source_mapping

def get_when_current_mapping(place_year):
    period_id        = "Current_%d"%place_year
    period_label     = Literal("Current, as of %d"%place_year)
    short_label      = Literal(str(place_year))
    year_node        = Literal(str(place_year))
    period_node      = URIRef(EMP[period_id])
    period_comment   = Literal("Time period including the year %d"%place_year)
    timespan_node    = URIRef(EMT[period_id])
    timespan_comment = Literal(
        ("Timespan starting no later than %d, "%place_year) +
        ("and ending no sooner than %d"%place_year)
        )
    when_current_mapping = M.emit(
        M.stmt_gen(EM.when, period_node), M.loc_subgraph(
            M.tgt_subj, M.src_prop, M.src_obj,
            [ M.emit(M.stmt_gen(RDF.type, EM.Time_period),     M.stmt_copy())
            , M.emit(M.stmt_gen(RDFS.label, period_label),     M.stmt_copy())
            , M.emit(M.stmt_gen(RDFS.comment, period_comment), M.stmt_copy())
            , M.emit(M.stmt_gen(EM.short_label, short_label),  M.stmt_copy())
            , M.emit(M.stmt_gen(EM.timespan, timespan_node),   M.loc_subgraph(
                M.tgt_subj, M.src_prop, M.src_obj,
                [ M.emit(M.stmt_gen(RDF.type, EM.Time_span),         M.stmt_copy())
                , M.emit(M.stmt_gen(RDFS.label, period_label),       M.stmt_copy())
                , M.emit(M.stmt_gen(RDFS.comment, timespan_comment), M.stmt_copy())
                , M.emit(M.stmt_gen(EM.short_label, short_label),    M.stmt_copy())
                , M.emit(M.stmt_gen(EM.latestStart, year_node),      M.stmt_copy())
                , M.emit(M.stmt_gen(EM.earliestEnd, year_node),      M.stmt_copy())
                ]))
            ])
        )
    return when_current_mapping

def get_geonames_merged_place_mapping(
    emp_id_merged, emp_id_sourced, source_uri, place_name
    ):
    emp_node_merged  = URIRef(PLACE[emp_id_merged])
    emp_node_sourced = URIRef(PLACE[emp_id_sourced])
    source_uri_node  = URIRef(source_uri)
    source_uri_label = Literal("GeoNames URI for %s"%(place_name,))
    merged_place_mapping = (
        [ M.set_subj(M.stmt_gen(EM.dummy_prop),                M.const(emp_node_merged))
        , M.emit(M.stmt_gen(RDF.type, EM.Place),               M.stmt_copy())
        , M.emit(M.stmt_gen(RDF.type, EM.Place_merged),        M.stmt_copy())
        , M.emit(M.stmt_gen(EM.canonicalURI, emp_node_merged), M.stmt_copy())
        , M.emit(M.stmt_gen(EM.alternateURI), M.loc_subgraph(
            M.tgt_subj, M.src_prop, M.src_obj, # M.src_obj -> BNode from M.stmt_gen  
            [ M.emit(M.stmt_gen(RDFS.label, source_uri_label), M.stmt_copy())
            , M.emit(M.stmt_gen(EM.link,    source_uri_node),  M.stmt_copy())
            ]
            ))
        , M.emit(M.stmt_gen(EM.place_data, emp_node_sourced),  M.stmt_copy())
        ])
    return merged_place_mapping

def get_geonames_sourced_place_mapping(
    emp_id_sourced, geonames_url, 
    place_category, place_type, place_name, place_label, place_country,
    place_altnames, place_displaynames, place_seeAlso
    ):
    geonames_link_node     = URIRef(geonames_url)
    geonames_source_node   = URIRef(PLACE[emp_id_sourced])
    geonames_source_label  = Literal("GeoNames data for %s"%(place_name,))
    geonames_source_tag    = Literal("GeoNames")
    geonames_place_mapping = (
        [ M.set_subj(M.stmt_gen(EM.dummy_prop), M.const(geonames_source_node))
        , M.emit(M.stmt_gen(RDF.type, EM.Place),                   M.stmt_copy())
        , M.emit(M.stmt_gen(RDF.type, EM.Place_sourced),           M.stmt_copy())
        , M.emit(M.stmt_gen(RDFS.label, place_label),              M.stmt_copy())
        , M.emit(M.stmt_gen(RDFS.isDefinedBy, geonames_link_node), M.stmt_copy())
        , M.emit(M.stmt_gen(EM.placeCategory, place_category),     M.stmt_copy())
        , M.emit(M.stmt_gen(EM.placeType, place_type),             M.stmt_copy())
        , M.emit(M.stmt_gen(EM.preferredName, place_name),         M.stmt_copy())
        , M.emit(M.stmt_gen(GN.countryCode, place_country),        M.stmt_copy())
        , get_geonames_source_reference_mapping(emp_id_sourced, geonames_url, place_label)
        ] +
        [ M.emit(M.stmt_gen(EM.alternateName, an), M.stmt_copy())
          for an in place_altnames
        ] +
        [ M.emit(M.stmt_gen(EM.displayName, dn), M.stmt_copy())
          for dn in place_displaynames
        ] +
        [ M.emit(M.stmt_gen(RDFS.seeAlso, sa), M.stmt_copy())
          for sa in place_seeAlso
        ])
    return geonames_place_mapping

def get_geonames_setting_mapping(
    emp_id_sourced, geonames_url, place_label,
    place_lat, place_long, place_year
    ):
    place_lat_node  = Literal(str(place_lat),  datatype=XSD.double)
    place_long_node = Literal(str(place_long), datatype=XSD.double)
    geonames_setting_mapping = (
        [ M.emit(M.stmt_gen(EM.setting), M.loc_subgraph(
            M.tgt_subj, M.src_prop, M.src_obj, # M.src_obj -> BNode from M.stmt_gen 
            [ M.emit(M.stmt_gen(RDF.type, EM.Setting),                 M.stmt_copy())
            , M.emit(M.stmt_gen(EM.location), M.loc_subgraph(
                M.tgt_subj, M.src_prop, M.src_obj, # M.src_obj -> BNode from M.stmt_gen 
                [ M.emit(M.stmt_gen(WGS84_POS.lat,  place_lat_node),   M.stmt_copy())
                , M.emit(M.stmt_gen(WGS84_POS.long, place_long_node),  M.stmt_copy())
                ]
                ))
            # Qualifications
            , get_when_current_mapping(place_year)
            , get_geonames_source_reference_mapping(emp_id_sourced, geonames_url, place_label)
            ]))
        ])
    return geonames_setting_mapping

def get_geonames_place_relation_mapping(
    emp_id_geonames, geonames_url, place_label,
    relation_type, parent_geonames_uri, 
    relation_year, relation_competence
    ):
    parent_geonames_id = get_geonames_id(str(parent_geonames_uri))
    parent_gn_node, parent_gn_rdf = get_geonames_place_rdf(parent_geonames_id)
    parent_type = parent_gn_rdf[parent_gn_node:GN.featureCode:].next()
    parent_name = parent_gn_rdf[parent_gn_node:GN.name:].next()
    emp_parent_id = get_emplaces_id(
        parent_name, parent_type, parent_geonames_id, suffix="_geonames"
        )
    emp_parent_node = URIRef(PLACE[emp_parent_id])
    place_relation_mapping = (
        [ M.emit(M.stmt_gen(EM.hasRelation), M.loc_subgraph(
            M.tgt_subj, M.src_prop, M.src_obj, # M.src_obj -> BNode from M.stmt_gen 
            [ M.emit(M.stmt_gen(RDF.type, EM.Qualified_relation),     M.stmt_copy())
            , M.emit(M.stmt_gen(EM.relationType, relation_type),      M.stmt_copy())
            , M.emit(M.stmt_gen(EM.relationTo, emp_parent_node),      M.stmt_copy())
            # Qualifications
            , M.emit(M.stmt_gen(EM.competence, relation_competence),  M.stmt_copy())
            , get_when_current_mapping(relation_year)
            , get_geonames_source_reference_mapping(emp_id_geonames, geonames_url, place_label)
            ]))
        ])
    return place_relation_mapping

def get_place_map_resource_mapping(
    emp_id_geonames, geonames_url, place_label,
    map_short_label, map_label, map_url, map_preview_url,
    map_year, map_competence
    ):
    emp_node_geonames = URIRef(PLACE[emp_id_geonames])
    place_map_resource_mapping = (
        [ M.emit(M.stmt_gen(EM.hasAnnotation), M.loc_subgraph(
            M.tgt_subj, M.src_prop, M.src_obj, # M.src_obj -> BNode from M.stmt_gen 
            [ M.emit(M.stmt_gen(RDF.type, OA.Annotation), M.stmt_copy())
            , M.emit(M.stmt_gen(OA.motivatedBy, EM.MAP_RESOURCE),  M.stmt_copy())
            , M.emit(M.stmt_gen(OA.hasTarget, emp_node_geonames),  M.stmt_copy())
            , M.emit(M.stmt_gen(OA.hasBody), M.loc_subgraph(
                M.tgt_subj, M.src_prop, M.src_obj, # M.src_obj -> BNode from M.stmt_gen 
                [ M.emit(M.stmt_gen(RDFS.label,     map_label),       M.stmt_copy())
                , M.emit(M.stmt_gen(RDFS.comment,   map_label),       M.stmt_copy())
                , M.emit(M.stmt_gen(EM.short_label, map_short_label), M.stmt_copy())
                , M.emit(M.stmt_gen(EM.preview,     map_url),         M.stmt_copy())
                , M.emit(M.stmt_gen(EM.link,        map_preview_url), M.stmt_copy())
                ]))
            # Qualifications
            , M.emit(M.stmt_gen(EM.competence, map_competence),  M.stmt_copy())
            , get_when_current_mapping(map_year)
            , get_geonames_source_reference_mapping(emp_id_geonames, geonames_url, place_label)
            ]))
        ])
    return place_map_resource_mapping

def get_wikidata_merged_place_mapping(
    emp_id_merged, emp_id_sourced, source_uri, place_name
    ):
    emp_node_merged  = URIRef(PLACE[emp_id_merged])
    emp_node_sourced = URIRef(PLACE[emp_id_sourced])
    source_uri_node  = URIRef(source_uri)
    source_uri_label = Literal("WikiData URI for %s"%(place_name,))
    merged_place_mapping = (
        [ M.set_subj(M.stmt_gen(EM.dummy_prop), M.const(emp_node_merged))
        , M.emit(M.stmt_gen(RDF.type, EM.Place),               M.stmt_copy())
        , M.emit(M.stmt_gen(RDF.type, EM.Place_merged),        M.stmt_copy())
        , M.emit(M.stmt_gen(EM.canonicalURI, emp_node_merged), M.stmt_copy())
        , M.emit(M.stmt_gen(EM.alternateURI), M.loc_subgraph(
            M.tgt_subj, M.src_prop, M.src_obj, # M.src_obj -> BNode from M.stmt_gen  
            [ M.emit(M.stmt_gen(RDFS.label, source_uri_label), M.stmt_copy())
            , M.emit(M.stmt_gen(EM.link,    source_uri_node),  M.stmt_copy())
            ]
            ))
        , M.emit(M.stmt_gen(EM.place_data, emp_node_sourced),  M.stmt_copy())
        ])
    return merged_place_mapping

def get_wikidata_sourced_place_mapping(emp_id_sourced, wikidata_url):
    def alt_authority(auth_uri_template, auth_tag, auth_label, auth_descr, auth_link=None):
        return M.loc_subgraph(
            M.tgt_subj, M.const_uri(EM.alternateAuthority), M.const_gen_uri(auth_uri_template),
            [ M.emit(M.stmt_gen(RDF.type,         EM.Source_desc),      M.stmt_copy())
            , M.emit(M.stmt_gen(RDF.type,         EM.Authority),        M.stmt_copy())
            , M.emit(M.stmt_gen(EM.short_label,   Literal(auth_tag)),   M.stmt_copy())
            , M.emit(M.stmt_gen(RDFS.label,       Literal(auth_label)), M.stmt_copy())
            , M.emit(M.stmt_gen(EM.editorialNote, Literal(auth_descr)), M.stmt_copy())
            , M.emit(M.stmt_gen_link(EM.link,     auth_link),           M.stmt_copy())
            ])
    emp_node_sourced = URIRef(PLACE[emp_id_sourced])
    wikidata_data_mapping = (
        [ M.set_subj(M.stmt_gen(EM.dummy_prop),            M.const(emp_node_sourced))
        , M.emit(M.stmt_gen(RDF.type,   EM.Place),         M.stmt_copy())
        , M.emit(M.stmt_gen(RDF.type,   EM.Place_sourced), M.stmt_copy())
        , M.emit(M.prop_eq(RDFS.label),                    M.stmt_copy())
        , M.emit(M.prop_eq(WDT.P268),   
            alt_authority(
                EMS["%(obj)s_bnf"], 
                "BnF", 
                "BnF identifier",
                "BNF (Bibliothèque nationale de France) identifier. See: https://www.wikidata.org/wiki/Property:P268.",
                auth_link=None
                )
            )
        , M.emit(M.prop_eq(WDT.P227),   
            alt_authority(
                EMS["%(obj)s_gnd"], 
                "GND", 
                "GND identifier",
                "Deutsche Nationalbibliothek Identifier. See: https://www.wikidata.org/wiki/Property:P227.",
                auth_link=None
                )
            )
        , M.emit(M.prop_eq(WDT.P1566),   
            alt_authority(
                EMS["%(obj)s_geonames"], 
                "GeoNames", 
                "GeoNames identifier",
                "GeoNames identifier. See: https://www.wikidata.org/wiki/Property:P1566.",
                auth_link=None
                )
            )
        , M.emit(M.prop_eq(WDT.P1667),   
            alt_authority(
                EMS["%(obj)s_tgn"], 
                "TGN", 
                "TGN identifier",
                "TGN (Getty Thesaurus of Geographic Names) identfier. See: https://www.wikidata.org/wiki/Property:P1667.",
                auth_link=None
                )
            )
        , M.emit(M.prop_eq(WDT.P1871),   
            alt_authority(
                EMS["%(obj)s_cerl"], 
                "CERL", 
                "CERL identifier",
                "CERL (Consortium of European Research Libraries thesaurus) identifier. See: https://www.wikidata.org/wiki/Property:P1871.",
                auth_link=None
                )
            )
        , M.emit(M.prop_eq(WDT.P2503),   
            alt_authority(
                EMS["%(obj)s_gov"], 
                "GOV", 
                "GOV identifier",
                "Historical Gazetteer (GOV) identifier. See: https://www.wikidata.org/wiki/Property:P2503.",
                auth_link=None
                )
            )
        , M.emit(M.prop_eq(WDT.P6060),   
            alt_authority(
                EMS["%(obj)s_moeml"], 
                "MoEML", 
                "MoEML identifier",
                "MoEML (Map of Early Modern London) identifier. See: https://www.wikidata.org/wiki/Property:P6060.",
                auth_link=None
                )
            )
        ])
    return wikidata_data_mapping

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
    "  %(prog)s manygetgeonames\n"+
    "  %(prog)s placehierarchy GEONAMESID\n"+
    "  %(prog)s manyplacehierarchy\n"+
    "  %(prog)s geonamesid URL [REGEXP]\n"
    "  %(prog)s manygeonamesids [REGEXP]\n"
    "  %(prog)s wikidataid GEONAMESID\n"+
    "  %(prog)s many wikidataid\n"+
    "  %(prog)s getwikidata WIKIDATAID\n"+
    "  %(prog)s manygetwikidata\n"+
    "  %(prog)s getwikitext WIKIDATAID\n"+
    "  %(prog)s manygetwikitext WIKIDATAID\n"+
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
    elif options.args[0].startswith("manygetg"):
        help_text = ("\n"+
            "  %(prog)s manygetgeonames\n"+
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
    elif options.args[0].startswith("getg"):
        help_text = ("\n"+
            "  %(prog)s getgeonamesdata GEONAMESID\n"+
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
            "The output can be used as input to a `manygetgeonames` command.\n"+
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
            "The output can be used as input to a `manygetgeonames` command.\n"+
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
            "The output can be used as input to a `manygetgeonames` or similar command.\n"+
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
            "The output can be used as input to a `manygetgeonames` or similar command.\n"+
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
    elif options.args[0].startswith("manywikidataid"):
        help_text = ("\n"+
            "  %(prog)s manywikidataids geonamesid\n"+
            "\n"+
            "Determines Wikidata Ids corresponding to Geonames Ids read from standard input,\n"+
            "and writes rhwm to stdout, or a diagnostic message is output to stderr.\n"+
            "\n"+
            "The output data may be used as input to 'manygetwikidata' or 'manygetwikitext'.\n"+
            "\n"+
            "@@@@ (more detail TBD)\n"+
            "\n"+
            "")
    elif options.args[0].startswith("getwikid"):
        help_text = ("\n"+
            "  %(prog)s getwikidata WIKIDATAID\n"+
            "\n"+
            "Gets data about a referenced place from Wikidata, and sends EMPlaces description\n"+
            "data in Turtle format to standard output.  It also generates statements that link\n"+
            "the generated wikidata information to the EMPLaces merged place description.\n"+
            "\n"+
            "\n"+
            "\n"+
            "")
    elif options.args[0].startswith("manygetwikid"):
        help_text = ("\n"+
            "  %(prog)s manygetwikidata\n"+
            "\n"+
            "Reads wikidata IDs from standard input, for each of these creates an EMPlaces\n"+
            "description (see 'getwikidata').  The resulting data is output in Turtle format\n"+
            "to standard output.\n"+
            "\n"+
            "")
    elif options.args[0].startswith("getwikit"):
        help_text = ("\n"+
            "  %(prog)s getwikitext WIKIDATAID\n"+
            "\n"+
            "Gets summary text about a referenced place from Wikipedia, and sends \n"+
            "data in Turtle format to standard output.  The generated data is intended\n"+
            "to be used with the output from 'getwikidata'.\n"+
            "\n"+
            "")
    elif options.args[0].startswith("manygetwikit"):
        help_text = ("\n"+
            "  %(prog)s manygetwikitext\n"+
            "\n"+
            "Reads wikidata IDs from standard input, for each of these locates a wikipedia text\n"+
            "description of the place, and generates an EMPlaces description (see 'getwikitext').\n"+
            "The resulting data is output in Turtle format to standard output.\n"+
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

def get_many_geonames_ids():
    geonames_ids = get_many_inputs()
    if not geonames_ids:
        print("No GeoNames place Ids found", file=sys.stderr)
    return geonames_ids    

def get_many_geonames_urls():
    geonames_urls = get_many_inputs()
    if not geonames_urls:
        print("No GeoNames URLs found", file=sys.stderr)
    return geonames_urls    

def get_many_wikidata_ids():
    wikidata_ids = get_many_inputs()
    if not wikidata_ids:
        print("No WikiData place Ids found", file=sys.stderr)
    return wikidata_ids    

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

def get_emplaces_geonames_data(
    geonames_id, geonames_uri, geonames_url, 
    geonames_rdf, geo_ont_rdf,
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
        geonames_node      = URIRef(geonames_uri)
        place_name         = geonames_rdf[geonames_node:GN.name:].next()
        place_altnames     = list(geonames_rdf[geonames_node:GN.alternateName:])
        place_displaynames = list(set([Literal(unicode(n)) for n in place_altnames]))
        place_category     = geonames_rdf[geonames_node:GN.featureClass:].next()
        place_type         = geonames_rdf[geonames_node:GN.featureCode:].next()
        place_map          = geonames_rdf[geonames_node:GN.locationMap:].next()
        place_parent       = geonames_rdf[geonames_node:GN.parentFeature:].next()
        place_country      = geonames_rdf[geonames_node:GN.countryCode:].next()
        place_seeAlso      = list(geonames_rdf[geonames_node:(RDFS.seeAlso|GN.wikipediaArticle):])
        place_lat          = geonames_rdf[geonames_node:WGS84_POS.lat:].next()
        place_long         = geonames_rdf[geonames_node:WGS84_POS.long:].next()
        place_type_label   = get_geonames_place_type_label(place_type, geo_ont_rdf)
        place_label        = Literal("%s (%s)"%(place_name, place_type_label))
    except Exception as e:
        log.error("Problem accessing data for %s"%(geonames_url,), exc_info=True)
        raise
    log.debug("get_emplaces_geonames_data: geonames_uri    %r"%(geonames_uri))
    log.debug("get_emplaces_geonames_data: place_name:     %r"%(place_name))
    log.debug("get_emplaces_geonames_data: place_altnames: %r"%(place_altnames))
    log.debug("get_emplaces_geonames_data: place_category: %r"%(place_category))
    log.debug("get_emplaces_geonames_data: place_type:     %r"%(place_type))
    log.debug("get_emplaces_geonames_data: place_map:      %r"%(place_map))
    log.debug("get_emplaces_geonames_data: place_parent:   %r"%(place_parent))
    log.debug("get_emplaces_geonames_data: place_seeAlso:  %r"%(place_seeAlso))
    log.debug("get_emplaces_geonames_data: lat, long:      %r, %r"%(place_lat, place_long))
    log.debug("get_emplaces_geonames_data: place_label:    %r"%(place_label))
    log.debug("get_emplaces_geonames_data: display_names:  %s"%(",".join(place_displaynames)))
    log.debug("get_emplaces_geonames_data: GeoNames graph:")
    log.debug(geonames_rdf.serialize(format='turtle', indent=4))

    # for gn_pre, gn_uri in geonames_rdf.namespaces():
    #     emplaces_rdf.bind(gn_pre, gn_uri)
    # lit_geonames_data = Literal("GeoNames data for %s"%(place_name,))
    # lit_geonames_uri  = Literal("GeoNames URI for %s"%(place_name,))
    # Allocate URIs and nodes for merged and geonames data
    emp_id_merged, emp_uri_merged, _ = get_emplaces_id_uri_node(
        None, None, geonames_id
        )
    emp_id_geonames = get_emplaces_id(
        place_name, place_type, geonames_id, suffix="_geonames"
        )
    log.debug("get_emplaces_geonames_data: emp_id_merged   %s"%emp_id_merged)
    log.debug("get_emplaces_geonames_data: emp_uri_merged  %s"%emp_uri_merged)
    log.debug("get_emplaces_geonames_data: emp_id_geonames %s"%emp_id_geonames)

    # Initial empty graph
    if emplaces_rdf is None:
        emplaces_rdf = Graph()
        add_emplaces_common_namespaces(emplaces_rdf, local_namespaces={})
    # Assemble mapping tables...
    merged_place_mapping = get_geonames_merged_place_mapping(
        emp_id_merged, emp_id_geonames, geonames_uri, place_name
        )
    sourced_place_mapping = get_geonames_sourced_place_mapping(
        emp_id_geonames, geonames_url,
        place_category, place_type, place_name, place_label, place_country,
        place_altnames, place_displaynames, place_seeAlso
        )
    place_setting_mapping = get_geonames_setting_mapping(
        emp_id_geonames, geonames_url, place_label,
        place_lat, place_long, 2018,
        )
    place_relation_mapping = get_geonames_place_relation_mapping(
        emp_id_geonames, geonames_url, place_label,
        EM.P_PART_OF_A, place_parent, 
        2018, EM.DEFINITIVE
        )
    place_map_resource_mapping = get_place_map_resource_mapping(
        emp_id_geonames, geonames_url, place_label,
        Literal("Current"), 
        Literal("Current map for %s"%(place_name)), 
        place_map, place_map,
        2018, EM.DEFINITIVE
        )

    # Apply mapping tables...
    log.debug("get_emplaces_geonames_data: geonames_uri   %s"%geonames_uri)
    m = DataExtractMap(geonames_node, geonames_rdf, emplaces_rdf)
    m.extract_map(merged_place_mapping)
    m.extract_map(sourced_place_mapping)
    m.extract_map(place_setting_mapping)
    m.extract_map(place_relation_mapping)
    m.extract_map(place_relation_mapping)
    m.extract_map(place_map_resource_mapping)

    return (emp_id_merged, emp_uri_merged, emplaces_rdf)

#@@TODO remove this when new code (above) is fully tested
# def get_emplaces_core_data(
#     geonames_id, geonames_uri, geonames_url, geonames_rdf, geo_ont_rdf,
#     emplaces_rdf=None
#     ):
#     """
#     Constructs EMPlaces RDF data from supplied GeoNames place data.

#     Returns tuple of:
#         0. EMPlaces Id for place
#         1. EMPlaces URI for place
#         2. Graph of EMPlaces data
#     """
#     if geonames_rdf is None:
#         msg = "No RDF data for %s"%(geonames_url,)
#         log.error(msg)
#         raise ValueError(msg)

#     try:
#         geonames_node     = URIRef(geonames_uri)
#         place_name        = geonames_rdf[geonames_node:GN.name:].next()
#         place_altnames    = list(geonames_rdf[geonames_node:GN.alternateName:])
#         place_def_by      = URIRef(geonames_url)
#         place_category    = geonames_rdf[geonames_node:GN.featureClass:].next()
#         place_type        = geonames_rdf[geonames_node:GN.featureCode:].next()
#         place_map         = geonames_rdf[geonames_node:GN.locationMap:].next()
#         place_parent      = geonames_rdf[geonames_node:GN.parentFeature:].next()
#         place_country     = geonames_rdf[geonames_node:GN.countryCode:].next()
#         place_seeAlso     = list(geonames_rdf[geonames_node:(RDFS.seeAlso|GN.wikipediaArticle):])
#         place_lat         = geonames_rdf[geonames_node:WGS84_POS.lat:].next()
#         place_long        = geonames_rdf[geonames_node:WGS84_POS.long:].next()
#         place_type_label  = get_geonames_place_type_label(place_type, geo_ont_rdf)
#         display_label     = Literal("%s (%s)"%(place_name, place_type_label)) 
#         display_names     = list(set([Literal(unicode(n)) for n in place_altnames]))
#     except Exception as e:
#         log.error("Problem accessing data for %s"%(geonames_url,), exc_info=True)
#         raise
#     log.debug("get_emplaces_core_data: geonames_node   %r"%(geonames_node))
#     log.debug("get_emplaces_core_data: place_name:     %r"%(place_name))
#     log.debug("get_emplaces_core_data: place_altnames: %r"%(place_altnames))
#     log.debug("get_emplaces_core_data: place_def_by:   %r"%(place_def_by))
#     log.debug("get_emplaces_core_data: place_category: %r"%(place_category))
#     log.debug("get_emplaces_core_data: place_type:     %r"%(place_type))
#     log.debug("get_emplaces_core_data: place_map:      %r"%(place_map))
#     log.debug("get_emplaces_core_data: place_parent:   %r"%(place_parent))
#     log.debug("get_emplaces_core_data: place_seeAlso:  %r"%(place_seeAlso))
#     log.debug("get_emplaces_core_data: lat, long:      %r, %r"%(place_lat, place_long))
#     log.debug("get_emplaces_core_data: display_label:  %r"%(display_label))
#     log.debug("get_emplaces_core_data: display_names:  %s"%(",".join(display_names)))
#     log.debug("get_emplaces_core_data: GeoNames graph:")
#     log.debug(geonames_rdf.serialize(format='turtle', indent=4))

#     # Initial empty graph
#     if emplaces_rdf is None:
#         emplaces_rdf = Graph()
#         add_emplaces_common_namespaces(emplaces_rdf, local_namespaces={})
#     # for gn_pre, gn_uri in geonames_rdf.namespaces():
#     #     emplaces_rdf.bind(gn_pre, gn_uri)
#     lit_geonames_data = Literal("GeoNames data for %s"%(place_name,))
#     lit_geonames_uri  = Literal("(GeoNames URI) for %s"%(place_name,))

#     # Allocate URIs and nodes for merged and geonames data
#     emp_id_merged, emp_uri_merged, emp_node_merged = get_emplaces_id_uri_node(
#         place_name, place_type, geonames_id
#         )
#     emp_id_geonames, emp_uri_geonames, emp_node_geonames = get_emplaces_id_uri_node(
#         place_name, place_type, geonames_id, suffix="_geonames"
#         )
#     ems_uri_geonames_source  = EMS[emp_id_geonames]
#     ems_node_geonames_source = URIRef(ems_uri_geonames_source)

#     # Add em:Place_merged description
#     emplaces_rdf.add((emp_node_merged, RDF.type, EM.Place))
#     emplaces_rdf.add((emp_node_merged, RDF.type, EM.Place_merged))
#     emplaces_rdf.add((emp_node_merged, EM.canonicalURI, emp_node_merged))
#     b_alturi = BNode()
#     emplaces_rdf.add((emp_node_merged,  EM.alternateURI,  b_alturi))
#     emplaces_rdf.add((b_alturi,  RDFS.label, lit_geonames_uri ))
#     emplaces_rdf.add((b_alturi,  EM.link,    geonames_node    ))
#     emplaces_rdf.add((emp_node_merged, EM.place_data, emp_node_geonames))

#     # Add description of GeoNames source
#     emplaces_rdf.add((ems_node_geonames_source, RDF.type,       EM.Authority       ))
#     emplaces_rdf.add((ems_node_geonames_source, RDFS.label,     lit_geonames_data  ))
#     emplaces_rdf.add((ems_node_geonames_source, EM.short_label, Literal("GeoNames")))
#     emplaces_rdf.add((ems_node_geonames_source, EM.link,        place_def_by       ))

#     # Add em:Place_sourced description for GeoNames
#     emplaces_rdf.add((emp_node_geonames,  RDF.type,         EM.Place                ))
#     emplaces_rdf.add((emp_node_geonames,  RDFS.label,       display_label           ))
#     emplaces_rdf.add((emp_node_geonames,  RDFS.isDefinedBy, place_def_by            ))
#     emplaces_rdf.add((emp_node_geonames,  EM.source,        ems_node_geonames_source))
#     emplaces_rdf.add((emp_node_geonames,  EM.placeCategory, place_category          ))
#     emplaces_rdf.add((emp_node_geonames,  EM.placeType,     place_type              ))
#     emplaces_rdf.add((emp_node_geonames,  EM.preferredName, place_name              ))
#     for an in place_altnames:
#         emplaces_rdf.add((emp_node_geonames, EM.alternateName, an))
#     for dn in display_names:
#         emplaces_rdf.add((emp_node_geonames, EM.displayName, dn))
#     for sa in place_seeAlso:
#         emplaces_rdf.add((emp_node_geonames, RDFS.seeAlso, sa))

#     # Define setting for current location
#     b_location = add_place_location(emplaces_rdf, place_lat, place_long)
#     b_setting  = add_place_setting(emplaces_rdf, 
#         b_location, 
#         EMP.Current, 
#         ems_node_geonames_source
#         )
#     emplaces_rdf.add((emp_node_geonames, EM.where, b_setting))

#     # Add country code
#     emplaces_rdf.add((emp_node_geonames, GN.countryCode, place_country))

#     # Define relation for current admin hierarchy (1 level up only)
#     parent_geonames_id = get_geonames_id(str(place_parent))
#     parent_gn_node, parent_gn_rdf = get_geonames_place_rdf(parent_geonames_id)
#     parent_name        = parent_gn_rdf[parent_gn_node:GN.name:].next()
#     parent_type        = parent_gn_rdf[parent_gn_node:GN.featureCode:].next()
#     parent_id, parent_uri, parent_node = get_emplaces_id_uri_node(
#         parent_name, parent_type, parent_geonames_id, suffix="_geonames"
#         )
#     b_relation = add_place_relation(emplaces_rdf, 
#         EM.P_PART_OF_A, parent_node,
#         EMP.Current, 
#         EM.DEFINITIVE,
#         ems_node_geonames_source
#         )
#     emplaces_rdf.add((emp_node_geonames, EM.hasRelation, b_relation))

#     # Define map resource for current
#     b_body = add_resource_attributes(emplaces_rdf, 
#         { RDFS.label:       Literal("Current map for %s"%(place_name,))
#         , EM.link:          place_map
#         })
#     b_annotation = add_resource_attributes(emplaces_rdf, 
#         { RDF.type:         OA.Annotation
#         , OA.motivatedBy:   EM.MAP_RESOURCE
#         , OA.hasTarget:     emp_node_geonames
#         , OA.hasBody:       b_body
#         , EM.when:          EMP.Current
#         , EM.source:        ems_node_geonames_source
#         })
#     emplaces_rdf.add((emp_node_geonames, EM.hasAnnotation, b_annotation))
#     return (emp_id_merged, emp_uri_merged, emplaces_rdf)
#@@

def get_geonames_id_data(gcdroot, geonames_id, emplaces_rdf=None):
    """
    Build EMPlaces place data for a specified GeoNames place id.
    """
    geonames_uri, geonames_url = get_geonames_uri(geonames_id)
    # print("geonames_url: %s"%(geonames_url,), file=sys.stderr)
    geonames_rdf = get_geonames_place_data(geonames_url)
    geo_ont_rdf  = get_geonames_ontology()
    # emplaces_id, emplaces_uri, emplaces_rdf = get_emplaces_core_data(
    #     geonames_id, geonames_uri, geonames_url, geonames_rdf, geo_ont_rdf,
    #     emplaces_rdf=emplaces_rdf
    #     )
    # @@@@ This version uses common shape shifting libraries
    emplaces_id, emplaces_uri, emplaces_rdf = get_emplaces_geonames_data(
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
    geonames_ids = get_many_geonames_ids()
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
    place_ids   = get_many_geonames_ids()
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
    # Get identifiers, URIs and other values from wikidata RDFD
    # (Geonames Id is needed to connect with EMPlaces merged data)
    emp_id_wikidata, emp_uri_wikidata, emp_node_wikidata = get_emplaces_uri_node(
        wikidata_id, suffix="_wikidata"
        )
    src_node_wikidata = WD[wikidata_id]
    geonames_id = wikidata_rdf[src_node_wikidata:URIRef(WDT.P1566):].next()
    place_name  = "(name unknown)"
    for l in wikidata_rdf[src_node_wikidata:URIRef(RDFS.label):]:
        if ( isinstance(l, Literal) and 
             ( (l.language is None) or (l.language.startswith("en")) ) ):
            place_name = l
    emp_id_merged, emp_uri_merged, _ = get_emplaces_id_uri_node(
        None, None, geonames_id
        )
    # ----- Copy prefixes -----
    for prefix, ns_uri in wikidata_rdf.namespaces():
        result_rdf.bind(prefix, ns_uri)
    result_rdf.bind("em",    EM.term(""))
    result_rdf.bind("place", PLACE.term(""))
    # ----- mapping tables -----
    merged_place_mapping = get_wikidata_merged_place_mapping(
        emp_id_merged, emp_id_wikidata, wikidata_url, place_name
        )
    wikidata_data_mapping = get_wikidata_sourced_place_mapping(
        emp_id_wikidata, wikidata_url
        )

    #@@@@
    # def alt_authority(auth_uri_template, auth_tag, auth_label, auth_descr, auth_link=None):
    #     return M.loc_subgraph(
    #         M.tgt_subj, M.const_uri(EM.alternateAuthority), M.const_gen_uri(auth_uri_template),
    #         [ M.emit(M.stmt_gen(RDF.type,         EM.Source_desc),      M.stmt_copy())
    #         , M.emit(M.stmt_gen(RDF.type,         EM.Authority),        M.stmt_copy())
    #         , M.emit(M.stmt_gen(EM.short_label,   Literal(auth_tag)),   M.stmt_copy())
    #         , M.emit(M.stmt_gen(RDFS.label,       Literal(auth_label)), M.stmt_copy())
    #         , M.emit(M.stmt_gen(EM.editorialNote, Literal(auth_descr)), M.stmt_copy())
    #         , M.emit(M.stmt_gen_link(EM.link,     auth_link),           M.stmt_copy())
    #         ])
    # wikidata_data_mapping = (
    #     [ M.set_subj(M.stmt_gen(EM.dummy_prop), M.const(emp_node_wikidata))
    #     , M.emit(M.stmt_gen(RDF.type,   EM.Place),         M.stmt_copy())
    #     , M.emit(M.stmt_gen(RDF.type,   EM.Place_sourced), M.stmt_copy())
    #     , M.emit(M.prop_eq(RDFS.label),                    M.stmt_copy())
    #     , M.emit(M.prop_eq(WDT.P268),   
    #         alt_authority(
    #             EMS["%(obj)s_bnf"], 
    #             "BnF", 
    #             "BnF identifier",
    #             "BNF (Bibliothèque nationale de France) identifier. See: https://www.wikidata.org/wiki/Property:P268.",
    #             auth_link=None
    #             )
    #         )
    #     , M.emit(M.prop_eq(WDT.P227),   
    #         alt_authority(
    #             EMS["%(obj)s_gnd"], 
    #             "GND", 
    #             "GND identifier",
    #             "Deutsche Nationalbibliothek Identifier. See: https://www.wikidata.org/wiki/Property:P227.",
    #             auth_link=None
    #             )
    #         )
    #     , M.emit(M.prop_eq(WDT.P1566),   
    #         alt_authority(
    #             EMS["%(obj)s_geonames"], 
    #             "GeoNames", 
    #             "GeoNames identifier",
    #             "GeoNames identifier. See: https://www.wikidata.org/wiki/Property:P1566.",
    #             auth_link=None
    #             )
    #         )
    #     , M.emit(M.prop_eq(WDT.P1667),   
    #         alt_authority(
    #             EMS["%(obj)s_tgn"], 
    #             "TGN", 
    #             "TGN identifier",
    #             "TGN (Getty Thesaurus of Geographic Names) identfier. See: https://www.wikidata.org/wiki/Property:P1667.",
    #             auth_link=None
    #             )
    #         )
    #     , M.emit(M.prop_eq(WDT.P1871),   
    #         alt_authority(
    #             EMS["%(obj)s_cerl"], 
    #             "CERL", 
    #             "CERL identifier",
    #             "CERL (Consortium of European Research Libraries thesaurus) identifier. See: https://www.wikidata.org/wiki/Property:P1871.",
    #             auth_link=None
    #             )
    #         )
    #     , M.emit(M.prop_eq(WDT.P2503),   
    #         alt_authority(
    #             EMS["%(obj)s_gov"], 
    #             "GOV", 
    #             "GOV identifier",
    #             "Historical Gazetteer (GOV) identifier. See: https://www.wikidata.org/wiki/Property:P2503.",
    #             auth_link=None
    #             )
    #         )
    #     , M.emit(M.prop_eq(WDT.P6060),   
    #         alt_authority(
    #             EMS["%(obj)s_moeml"], 
    #             "MoEML", 
    #             "MoEML identifier",
    #             "MoEML (Map of Early Modern London) identifier. See: https://www.wikidata.org/wiki/Property:P6060.",
    #             auth_link=None
    #             )
    #         )
    #     ])
    # wikidata_data_mapping = (
    #     [ M.emit(M.prop_eq(RDFS.label), M.stmt_copy())
    #     , M.emit(M.prop_eq(WDT.P227),  M.stmt_copy())   # GND ID
    #     , M.emit(M.prop_eq(WDT.P268),  M.stmt_copy())   # BnF ID
    #     , M.emit(M.prop_eq(WDT.P1566), M.stmt_copy())   # Geonames ID
    #     , M.emit(M.prop_eq(WDT.P1667), M.stmt_copy())   # Getty TGN ID
    #     , M.emit(M.prop_eq(WDT.P2503), M.stmt_copy())   # GOV ID
    #     , M.emit(M.prop_eq(WDT.P1871), M.stmt_copy())   # CERL ID
    #     , M.emit(M.prop_eq(WDT.P6060), M.stmt_copy())   # MoEML ID
    #     ])
    # -----
    #@@@@
    m = DataExtractMap(wikidata_uri, wikidata_rdf, result_rdf)
    m.extract_map(merged_place_mapping)
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
        emp_id_wikidata, emp_uri_wikidata, emp_node_wikidata = get_emplaces_uri_node(wikidata_id, suffix="_wikidata")
        if result_rdf is None:
            result_rdf = Graph()
            result_rdf.bind("em", EM.term(""))
            result_rdf.bind("place", PLACE.term(""))
        summary_text = summary_data["extract"]
        result_rdf.add((emp_node_wikidata, EM.description, Literal(summary_text)))
    return result_rdf

def wikidata_sparql_query(query, endpoint="https://query.wikidata.org/sparql"):
    query_url      = make_query_url(endpoint, query=query)
    # print("@@@ query URL:\n--\n%s\n--"%(query_url,), file=sys.stderr)
    query_response = http_get_json(query_url)
    # print("@@@ query_response:\n--\n%s\n--"%(query_response,), file=sys.stderr)
    return json.loads(query_response)

def extrtact_wikidata_id(geo_id):
    """
    Gor given GeoNames Id, return:

    (status, None)              if error detected
    (status, (id, uri, label))  if wikidata id found OK
    """
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
    result_bindings = query_response_dict["results"]["bindings"]
    ids_uris_labels = (
        [ ( get_wikidata_id(b["item"]["value"])
          , b["item"]["value"]
          , b["itemLabel"]["value"]
          ) 
          for b in result_bindings 
        ])
    if len(ids_uris_labels) == 0:
        print("No Wikidata IDs found for GeoNames Id %s"%(geo_id,), file=sys.stderr)
        return (GCD_NO_WIKIDATA_IDS, None)
    elif len(ids_uris_labels) != 1:
        print("Multiple Wikidata IDs found for GeoNames Id %s:"%(geo_id,), file=sys.stderr)
        print("  %s"%([i for i,u,l in ids_uris_labels],), file=sys.stderr)
        return (GCD_MANY_WIKIDATA_IDS, None)
    return (GCD_SUCCESS, ids_uris_labels[0])

def do_extract_wikidata_id(gcdroot, options):
    geo_id  = getargvalue(getarg(options.args, 0), "GeoNames Id: ")
    status, wiki_id_uri_label = extrtact_wikidata_id(geo_id)
    if status == GCD_SUCCESS:
        print("%-16s # %s"%(wiki_id_uri_label[0],wiki_id_uri_label[2]), file=sys.stdout)
    return status

def do_extract_many_wikidata_ids(gcdroot, options):
    # No prompt for mamy-value input
    gids   = get_many_geonames_ids()
    if not gids:
        return GCD_NO_GEONAMES_IDS
    return_status = GCD_SUCCESS
    for geo_id in gids:
        status, wiki_id_uri_label = extrtact_wikidata_id(geo_id)
        if status == GCD_SUCCESS:
            print("%-16s # %s"%(wiki_id_uri_label[0],wiki_id_uri_label[2]), file=sys.stdout)
        else:
            return_status = status
    return return_status

def do_get_wikidata_place_data(gcdroot, options):
    """
    Get Wikidata RDF for a place
    """
    wikidata_id  = getargvalue(getarg(options.args, 0), "Wikidata ID: ")
    wikidata_rdf = get_wikidata_id_data(wikidata_id)
    print(wikidata_rdf.serialize(format='turtle', indent=4), file=sys.stdout)
    return GCD_SUCCESS

def do_get_many_wikidata_place_data(gcdroot, options):
    """
    Get Wikidata RDF for multiple places
    """
    wids         = get_many_geonames_ids()
    wikidata_rdf = Graph()
    wikidata_rdf.bind("em",    EM.term(""))
    wikidata_rdf.bind("place", PLACE.term(""))
    for wikidata_id in wids:
        print("wikidata_id: %s"%(wikidata_id,), file=sys.stderr)
        wikidata_rdf = get_wikidata_id_data(wikidata_id, result_rdf=wikidata_rdf)
    print(wikidata_rdf.serialize(format='turtle', indent=4), file=sys.stdout)
    return GCD_SUCCESS

def do_get_wikidata_place_text(gcdroot, options):
    """
    Get Wikidata descrioption text for a place, as EMPlaces format RDF.
    """
    wikidata_id  = getargvalue(getarg(options.args, 0), "Wikidata ID: ")
    wikidata_rdf = get_wikidata_id_text(wikidata_id)
    print(wikidata_rdf.serialize(format='turtle', indent=4), file=sys.stdout)
    return GCD_SUCCESS

def do_get_many_wikidata_place_text(gcdroot, options):
    """
    Get Wikidata descrioption text for a place, as EMPlaces format RDF.
    """
    wids         = get_many_geonames_ids()
    wikidata_rdf = Graph()
    wikidata_rdf.bind("em",    EM.term(""))
    wikidata_rdf.bind("place", PLACE.term(""))
    for wikidata_id in wids:
        wikidata_rdf = get_wikidata_id_text(wikidata_id, result_rdf=wikidata_rdf)
    print(wikidata_rdf.serialize(format='turtle', indent=4), file=sys.stdout)
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
    if options.command.startswith("getg"):
        return do_get_geonames_place_data(gcdroot, options)
    if options.command.startswith("manygetg"):
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
    if options.command.startswith("manywikidataid"):
        return do_extract_many_wikidata_ids(gcdroot, options)
    if options.command.startswith("getwikid"):
        return do_get_wikidata_place_data(gcdroot, options)
    if options.command.startswith("manygetwikid"):
        return do_get_many_wikidata_place_data(gcdroot, options)
    if options.command.startswith("getwikit"):
        return do_get_wikidata_place_text(gcdroot, options)
    if options.command.startswith("manygetwikit"):
        return do_get_many_wikidata_place_text(gcdroot, options)
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

