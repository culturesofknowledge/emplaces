# !/usr/bin/env python
#
# get_core_data.py - command line tool to create EMPlaces core from GeoNames data
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

from rdflib         import Graph, Namespace, URIRef, Literal, BNode, RDF, RDFS
from rdflib.paths   import Path

from getargvalue    import getargvalue, getarg

log = logging.getLogger(__name__)

dirhere = os.path.dirname(os.path.realpath(__file__))
gcdroot = os.path.dirname(os.path.join(dirhere))
sys.path.insert(0, gcdroot)

#   ===================================================================
#
#   Data constants
#
#   ===================================================================

#   Software version

GCD_VERSION = "0.1"

#   Status return codes

GCD_SUCCESS         = 0         # Success
GCD_BADCMD          = 2         # Command error
GCD_UNKNOWNCMD      = 3         # Unknown command
GCD_UNIMPLEMENTED   = 4         # Unimplemented command or feature
GCD_UNEXPECTEDARGS  = 5         # Unexpected arguments supplied
GCD_NO_PLACE_IDS    = 6         # No place ids given

#   Namespaces

SKOS      = Namespace("http://www.w3.org/2004/02/skos/core#")
XSD       = Namespace("http://www.w3.org/2001/XMLSchema#")

OA        = Namespace("http://www.w3.org/ns/oa#")
CC        = Namespace("http://creativecommons.org/ns#")
DCTERMS   = Namespace("http://purl.org/dc/terms/")
FOAF      = Namespace("http://xmlns.com/foaf/0.1/")
BIBO      = Namespace("http://purl.org/ontology/bibo/")

GN        = Namespace("http://www.geonames.org/ontology#")  # GeoNames ontology
GEONAMES  = Namespace("http://sws.geonames.org/")           # GeoNames place 
WGS84_POS = Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#")
EM        = Namespace("http://emplaces.namespace.example.org/")
EMP       = Namespace("http://emplaces.namespace.example.org/place/")
EMT       = Namespace("http://emplaces.namespace.example.org/timespan/")
EML       = Namespace("http://emplaces.namespace.example.org/language/")

#   ===================================================================
#
#   Common definitions for EMPlaces / GeoNames data
#
#   ===================================================================

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
    
    @prefix em:         <http://emplaces.namespace.example.org/> .   #@@@@ TBD
    @prefix emp:        <http://emplaces.namespace.example.org/place/> .
    @prefix emt:        <http://emplaces.namespace.example.org/timespan/> .
    @prefix eml:        <http://emplaces.namespace.example.org/language/> .
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

    # Place types
    gn:P.PPL a skos:Concept ;
        skos:narrower gn:P ;
        rdfs:label    "Populated place" ;
        rdfs:comment  "A populated place (town, city, village, etc.).  From GeoNames (feature code)." 
        .
    gn:P.PPLA a skos:Concept ;
        skos:narrower gn:P ;
        rdfs:label    "Seat of 1st-order admin div" ;
        rdfs:comment  "Populated place that is a seat of a first-order administrative division.  From GeoNames (feature code)." 
        .
    gn:P.PPLH a skos:Concept ;
        skos:narrower gn:P ;
        rdfs:label    "Former populated place" ;
        rdfs:comment  "A former populated place that no longer exists.  From GeoNames (feature code)." 
        .
    gn:A.PCLI a skos:Concept ;
        skos:narrower gn:A ;
        rdfs:label    "Independent political entity" ;
        rdfs:comment  "An independent political entity, typically a country.  From GeoNames (feature code)."
        .
    gn:A.ADM1 a skos:Concept ;
        skos:narrower gn:A ;
        rdfs:label    "First-order admin division" ;
        rdfs:comment  "A primary administrative division of a country, such as a state in the United States.  From GeoNames (feature code)."
        .
    gn:A.ADM2 a skos:Concept ;
        skos:narrower gn:A ;
        rdfs:label    "Second-order admin division" ;
        rdfs:comment  "A subdivision of a first-order administrative division.  From GeoNames (feature code)."
        .
    gn:A.ADM3 a skos:Concept ;
        skos:narrower gn:A ;
        rdfs:label    "Third-order admin division" ;
        rdfs:comment  "A subdivision of a second-order administrative division.  From GeoNames (feature code)."
        .
    gn:A.PCLH a skos:Concept ;
        skos:narrower gn:A ;
        rdfs:label    "Former independent political entity" ;
        rdfs:comment  "A former independent political entity, typically a country.  From GeoNames (feature code)."
        .
    gn:A.ADM1H a skos:Concept ;
        skos:narrower gn:A ;
        rdfs:label    "Former first-order admin division" ;
        rdfs:comment  "A former first-order administrative division.  From GeoNames (feature code)."
        .
    gn:A.ADM2H a skos:Concept ;
        skos:narrower gn:A ;
        rdfs:label    "Former second-order admin division" ;
        rdfs:comment  "A former first-order administrative division.  From GeoNames (feature code)."
        .
    gn:A.ADM3H a skos:Concept ;
        skos:narrower gn:A ;
        rdfs:label    "Former Third-order admin division" ;
        rdfs:comment  "A former third-order administrative division.  From GeoNames (feature code)."
        .
    """)

COMMON_EMPLACES_DEFS = (
    """
    # Timespan for "current" data
    emt:Current a em:Time_period ;
        rdfs:label   "Current, as of 2018" ;
        rdfs:comment "For ease of retrieval, use this specific resource to label any current information (e.g. core data extracted from GeoNames).  Additional Timespan values could be indicated if required to convey more specific information." ;
        em:timespan
          [ a em:Time_span ;
            em:latestStart: "2018" ;
            em:earliestEnd: "2018" ;
          ]
        .

    #   This avoids having to create extra historical places 
    #   corresponding to a current P.  See em:AH_PART_OF_AH below.
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

    # Information competence (certainty)
    #
    # Information in a qualified relation or annotation may be uncertain.  These properties and values
    # are used to qualify these claims.  Information that is directly attached to an em:Place 
    # (i.e. not as a qualified relation or annotation) is considered to be definitive.
    #
    # Specifically, annotations for calendar-in-use and alternate name attestations should have 
    # associated competence values.
    #
    # Approximate date ranges are represented by range values in the corresponding Timespan value.
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

    # Core vs non-core data
    em:Place a rdfs:Class ;
        em:coreProperty em:preferredName, em:alternateName, em:placeCategory, em:corePlaceType ;
        .

    # Use em:corePlaceType for place type info that is obtained, and 
    # may be refreshed,from the reference gazetteer(s)
    em:corePlaceType rdfs:subPropertyOf em:placeType .

    # em:coreDataRef indicates source (reference gazetteer) for core data
    # Use em:source for other gazetteer references
    em:coreDataRef rdfs:subPropertyOf em:source .
    """)

COMMON_LANGUAGE_DEFS = (
    """
    # Language resources @@TODO: generate as-needed@@
    eml:de a em:Language_value ;
        em:tag "de" ; 
        rdfs:label "German"
        .
    eml:pl a em:Language_value ;
        em:tag "pl" ; 
        rdfs:label "Polish"
        .
    eml:la a em:Language_value ;
        em:tag "la" ; 
        rdfs:label "Latin"
        .
    """)


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
    "  %(prog)s getmultiple\n"+
    "  %(prog)s placehierarchy GEONAMESID\n"+
    "  %(prog)s version\n"+
    "")

def progname(args):
    return os.path.basename(args[0])

def gcd_version(gcdroot, userhome, options):
    """
    Print software version string to standard output.

    gcdroot     is the root directory for the Annalist software installation.
    userhome    is the home directory for the host system user issuing the command.
    options     contains options parsed from the command line.

    returns     0 if all is well, or a non-zero status code.
                This value is intended to be used as an exit status code
                for the calling program.
    """
    status = GCD_SUCCESS
    print(sitesettings.GCD_VERSION)
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
                description="EMPlaces GeoNames data extractor",
                formatter_class=argparse.RawDescriptionHelpFormatter,
                epilog=command_summary_help
                )
    parser.add_argument('--version', action='version', version='%(prog)s '+GCD_VERSION)
    parser.add_argument("--debug",
                        action="store_true", 
                        dest="debug", 
                        default=False,
                        help="Run with full debug output enabled.  "+
                             "Also creates log file 'get-core-data.log' in the working directory"
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
    elif options.args[0].startswith("getm"):
        help_text = ("\n"+
            "  %(prog)s getmultiple\n"+
            "\n"+
            "\n"+
            "Reads GeoNames place Ids from stdin, one per line, retrieves data\n"+
            "for these from GeoNames, and sends corresponding EMPlaces data in\n"+
            "Turtle format to standard output.\n"+
            "\n"+
            "To include come common non-place-specific supporting definitions, see options\n"+
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
            "To include come common non-place-specific supporting definitions, see options\n"+
            "'--include-common-defs', '--include-emplaces-defs', '--include-geonames-defs', \n"+
            "and '--include-language-defs'.\n"+
            "\n"+
            "")
    elif options.args[0].startswith("placehierarchy"):
        help_text = ("\n"+
            "  %(prog)s placehierarchy GEONAMESID\n"+
            "\n"+
            "Gets current administrative hierarchy about a place from GeoNames, \n"+
            "and outputs a list of place Ids, oine poer line,m to standard output.\n"+
            "\n"+
            "The output can be used as input to a `getmultiple` command.\n"+
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

    gcdroot     is the root directory for the getcoredata software installation.
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

def show_error(msg, status):
    print(msg, file=sys.stderr)
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

def get_emlaces_id_uri_node(geonames_id):
    """
    Given a GeoNames Id, returns Id, URI and Node for EMPlaces
    """
    emplaces_id   = "g_%s"%(geonames_id)
    emplaces_uri  = EMP[emplaces_id]
    emplaces_node = URIRef(emplaces_uri)
    return (emplaces_id, emplaces_uri, emplaces_node)

#   ===================================================================
#
#   RDF data wrangling
#
#   ===================================================================

def get_rdf_graph(url, format="xml"):
    """
    Return RDF graph at given location.
    """
    # e.g. http://sws.geonames.org/3090048/about.rdf
    g = Graph()
    g.parse(location=url, format=format)
    # result = g.parse(data=r.content, publicID=u, format="turtle")
    # result = g.parse(source=s, publicID=b, format="json-ld")
    return g

def get_geonames_ontology():
    """
    Return Graph of GeoNames ontology data
    """
    geo_ont_url  = "http://www.geonames.org/ontology/ontology_v3.1.rdf"
    geo_ont_rdf  = get_rdf_graph(geo_ont_url)
    return geo_ont_rdf

def get_geonames_place_data(geonames_url):
    """
    Returns graph of GeoNames place data
    """
    geonames_rdf = get_rdf_graph(geonames_url)
    return geonames_rdf

def get_geonames_place_type_label(place_type, geo_ont_rdf):
    """
    Returns label for supplied GeoNames place type
    """
    # Alternatives to ontology labels
    place_type_labels = (
        { GN["P.PPL"]:   "Populated place"
        , GN["P.PPLA"]:  "Populated place (city?)"
        , GN["A.ADM3"]:  "City"
        , GN["A.ADM2"]:  "County"
        , GN["A.ADM1"]:  "Region"
        , GN["A.PCLI"]:  "Country"
        })
    type_labels = geo_ont_rdf[place_type:SKOS.prefLabel:]
    for l in type_labels:
        if l.language == "en":
            type_label  = Literal(" ".join(str(l).split()))
            # https://stackoverflow.com/a/46501496/324122
    return type_label

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
    emp_rdf.parse(data=COMMON_PREFIX_DEFS+turtle_str, format="turtle")
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

def add_place_location(emp_rdf, place_lat, place_long):
    """
    Create BNode for location - supplied lat, long are string literals
    """
    b_location = BNode()
    emp_rdf.add((b_location, RDF.type,       EM.Location_value))
    emp_rdf.add((b_location, WGS84_POS.lat,  Literal(str(place_lat),  datatype=XSD.double)))
    emp_rdf.add((b_location, WGS84_POS.long, Literal(str(place_long), datatype=XSD.double)))
    return b_location

def add_source(emp_rdf, label, link):
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
    geonames_node     = URIRef(geonames_uri)
    place_name        = geonames_rdf[geonames_node:GN.name:].next()
    place_altnames    = list(geonames_rdf[geonames_node:GN.alternateName:])
    place_def_by      = URIRef(geonames_url)
    place_category    = geonames_rdf[geonames_node:GN.featureClass:].next()
    place_type        = geonames_rdf[geonames_node:GN.featureCode:].next()
    place_map         = geonames_rdf[geonames_node:GN.locationMap:].next()
    place_parent      = geonames_rdf[geonames_node:GN.parentFeature:].next()
    place_seeAlso     = list(geonames_rdf[geonames_node:(RDFS.seeAlso|GN.wikipediaArticle):])
    place_lat         = geonames_rdf[geonames_node:WGS84_POS.lat:].next()
    place_long        = geonames_rdf[geonames_node:WGS84_POS.long:].next()
    place_type_label  = get_geonames_place_type_label(place_type, geo_ont_rdf)
    display_label     = Literal("%s (%s)"%(place_name, place_type_label)) 
    display_names     = list(set([Literal(unicode(n)) for n in place_altnames]))

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
        add_emplaces_common_namespaces(emplaces_rdf)
    # for gn_pre, gn_uri in geonames_rdf.namespaces():
    #     emplaces_rdf.bind(gn_pre, gn_uri)
    lit_geonames_data = Literal("GeoNames data")
    lit_geonames_uri  = Literal("GeoNames URI")

    # Add em:Place description
    emp_id   = "g_%s"%(geonames_id)
    emp_uri  = EMP[emp_id]
    emp_node = URIRef(emp_uri)
    emplaces_rdf.add((emp_node,  RDF.type,         EM.Place         ))
    emplaces_rdf.add((emp_node,  RDFS.label,       display_label    ))
    emplaces_rdf.add((emp_node,  RDFS.isDefinedBy, place_def_by     ))
    emplaces_rdf.add((emp_node,  EM.canonicalURI,  emp_node         ))
    b_coreref = BNode()
    emplaces_rdf.add((emp_node,  EM.coreDataRef,   b_coreref        ))
    emplaces_rdf.add((b_coreref, RDFS.label,       lit_geonames_data))
    emplaces_rdf.add((b_coreref, EM.link,          place_def_by     ))
    b_alturi = BNode()
    emplaces_rdf.add((emp_node,  EM.alternateURI,  b_alturi         ))
    emplaces_rdf.add((b_alturi,  RDFS.label,       lit_geonames_uri ))
    emplaces_rdf.add((b_alturi,  EM.link,          geonames_node    ))

    emplaces_rdf.add((emp_node,  EM.placeCategory, place_category   ))
    emplaces_rdf.add((emp_node,  EM.corePlaceType, place_type       ))
    emplaces_rdf.add((emp_node,  EM.preferredName, place_name       ))
    for an in place_altnames:
        emplaces_rdf.add((emp_node, EM.alternateName, an))
    for dn in display_names:
        emplaces_rdf.add((emp_node, EM.displayName, dn))
    for sa in place_seeAlso:
        emplaces_rdf.add((emp_node, RDFS.seeAlso, sa))

    # Define setting for current location
    b_location = add_place_location(emplaces_rdf, place_lat, place_long)
    b_source   = add_source(emplaces_rdf, lit_geonames_data, place_def_by)
    b_setting  = add_place_setting(emplaces_rdf, b_location, EMT.Current, b_source)
    emplaces_rdf.add((emp_node, EM.where, b_setting))

    # Define relation for current admin hierarchy (1 level up only)
    parent_geonames_id  = get_geonames_id(str(place_parent))
    parent_id, parent_uri, parent_node = get_emlaces_id_uri_node(parent_geonames_id)
    b_source   = add_source(emplaces_rdf, lit_geonames_data, place_def_by)
    b_relation = add_place_relation(emplaces_rdf, 
        EM.P_PART_OF_A, parent_node,
        EMT.Current, 
        EM.DEFINITIVE,
        b_source
        )
    emplaces_rdf.add((emp_node, EM.hasRelation, b_relation))

    # Define map resource for current
    b_body = add_resource_attributes(emplaces_rdf, 
        { RDFS.label:       Literal("Current map for %s"%(place_name,))
        , EM.link:          place_map
        })
    b_source = add_source(emplaces_rdf, lit_geonames_data, place_def_by)
    b_annotation = add_resource_attributes(emplaces_rdf, 
        { RDF.type:         OA.Annotation
        , OA.motivatedBy:   EM.MAP_RESOURCE
        , OA.hasTarget:     emp_node
        , OA.hasBody:       b_body
        , EM.when:          EMT.Current
        , EM.source:        b_source
        })
    emplaces_rdf.add((emp_node, EM.hasAnnotation, b_annotation))
    return (emp_id, emp_uri, emplaces_rdf)

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
    # emplaces_id, emplaces_uri, emplaces_rdf = get_emplaces_core_data(
    #     geonames_id, geonames_uri, geonames_url, geonames_rdf, geo_ont_rdf
    #     )
    get_common_defs(options, emplaces_rdf)
    print(emplaces_rdf.serialize(format='turtle', indent=4), file=sys.stdout)
    return GCD_SUCCESS

def do_get_geonames_multiple_data(gcdroot, options):
    """
    Read multiple place Ids from standard input, and return a graph of
    EMPlaces data for all of the identified places.
    """
    emplaces_rdf = None     # Graph created on first loop below
    geonames_ids = []
    for line in sys.stdin:
        bare_id = line.split("#", 1)[0].strip()
        if bare_id:
            geonames_ids.append(bare_id)
    if not geonames_ids:
        print("No place Ids found", file=sys.stderr)
        return GCD_NO_PLACE_IDS
    for geonames_id in geonames_ids:
        #@@TODO: catch exception and return failure
        emplaces_rdf = get_geonames_id_data(gcdroot, geonames_id, emplaces_rdf=emplaces_rdf)
    get_common_defs(options, emplaces_rdf)
    print(emplaces_rdf.serialize(format='turtle', indent=4), file=sys.stdout)
    return GCD_SUCCESS

def get_geonames_place_parent(place_id):
    log.debug("get_geonames_place_parent(%s)"%(place_id))
    place_uri, place_url = get_geonames_uri(place_id)
    place_node   = URIRef(place_uri)
    place_rdf    = get_geonames_place_data(place_url)
    for place_type in place_rdf[place_node:GN.featureCode:]:
        if place_type == GN["A.PCLI"]:
            return None
    for place_parent in place_rdf[place_node:GN.parentFeature:]:
        parent_id    = get_geonames_id(str(place_parent))
        return parent_id
    return None     # No parent place here

    # if ... in place_rdf:
    #     place_parent = place_rdf[place_node:GN.parentFeature:].next()
    #     parent_id    = get_geonames_id(str(place_parent))
    # else:
    #     place_id = None
    # return parent_id

def get_places_hierarchy(place_ids, parent_ids):
    log.debug("get_places_hierarchy(%s, %s)"%(place_ids, parent_ids))
    for place_id in place_ids:
        if place_id not in parent_ids:
            parent_ids.append(place_id)
            parent_id    = get_geonames_place_parent(place_id)
            if parent_id:
                parent_ids   = get_places_hierarchy([parent_id], parent_ids)
    return parent_ids

def do_get_place_hierarchy(gcdroot, options):
    geonames_id   = getargvalue(getarg(options.args, 0), "GeoNames Id: ")
    parent_ids    = get_places_hierarchy([geonames_id], [])
    for p in parent_ids:
        print(p, file=sys.stdout)
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
    if options.command.startswith("getm"):
        return do_get_geonames_multiple_data(gcdroot, options)
    if options.command.startswith("get"):
        return do_get_geonames_place_data(gcdroot, options)
    if options.command.startswith("placeh"):
        return do_get_place_hierarchy(gcdroot, options)
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
        logging.basicConfig(level=logging.DEBUG, filename="get-core-data.log", filemode="w")
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

