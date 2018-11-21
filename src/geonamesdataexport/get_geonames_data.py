# !/usr/bin/env python
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

GCD_SUCCESS             = 0         # Success
GCD_BADCMD              = 2         # Command error
GCD_UNKNOWNCMD          = 3         # Unknown command
GCD_UNIMPLEMENTED       = 4         # Unimplemented command or feature
GCD_UNEXPECTEDARGS      = 5         # Unexpected arguments supplied
GCD_NO_PLACE_IDS        = 6         # No place ids given
GCD_NO_GEONAMES_URL     = 7         # No GeoNames URL
GCD_SOME_GEONAMES_URLS  = 8         # Some but not all all URLs matched GeoNames IDs

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
EM        = Namespace("http://http://id.emplaces.info/vocab/")
EMP       = Namespace("http://id.emplaces.info/place/")
EMT       = Namespace("http://id.emplaces.info/timespan/")
EML       = Namespace("http://id.emplaces.info/language/")
EMS       = Namespace("http://id.emplaces.info/source/")
EMC       = Namespace("http://id.emplaces.info/calendar/")

PLACE     = Namespace("http://id.emplaces.info/place/")
AGENT     = Namespace("http://id.emplaces.info/agent/")
REF       = Namespace("http://id.emplaces.info/reference/")


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

def get_emplaces_id_uri_node(place_name, place_type, unique_id, suffix=""):
    """
    Given a place name, place type, GeoNames Id and optional suffix,
    returns a place Id, URI and Node for 
    """
    type_id       = get_geonames_place_type_id(place_type)
    name_slug     = place_name.replace(" ", "_")
    name_slug     = name_slug[:40]
    emplaces_id   = "%s_%s_%s%s"%(name_slug, type_id, unique_id, suffix)
    emplaces_uri  = EMP[emplaces_id]
    emplaces_node = URIRef(emplaces_uri)
    # emplaces_id   = "g_%s"%(geonames_id)
    # emplaces_uri  = EMP[emplaces_id]
    # emplaces_node = URIRef(emplaces_uri)
    return (emplaces_id, emplaces_uri, emplaces_node)

def get_many_inputs():
    inputs = []
    for line in sys.stdin:
        u_line = line.decode("utf8")
        bare_input = u_line.split("#", 1)[0].strip()
        if bare_input:
            inputs.append(bare_input)
    return inputs    

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
    emp_graph.bind("ems",       EMS.term(""))
    emp_graph.bind("emc",       EMC.term(""))
    emp_graph.bind("place",     PLACE.term(""))
    emp_graph.bind("agent",     AGENT.term(""))
    emp_graph.bind("ref",       REF.term(""))
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
    # emplaces_id, emplaces_uri, emplaces_rdf = get_emplaces_core_data(
    #     geonames_id, geonames_uri, geonames_url, geonames_rdf, geo_ont_rdf
    #     )
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
        #@@TODO: catch exception and return failure
        emplaces_rdf = get_geonames_id_data(gcdroot, geonames_id, emplaces_rdf=emplaces_rdf)
    get_common_defs(options, emplaces_rdf)
    print(emplaces_rdf.serialize(format='turtle', indent=4), file=sys.stdout)
    return GCD_SUCCESS

# def get_geonames_place_parent(place_id):
#     log.debug("get_geonames_place_parent(%s)"%(place_id))
#     place_uri, place_url = get_geonames_uri(place_id)
#     place_node   = URIRef(place_uri)
#     place_rdf    = get_geonames_place_data(place_url)
#     for place_type in place_rdf[place_node:GN.featureCode:]:
#         if place_type == GN["A.PCLI"]:
#             return None
#     for place_parent in place_rdf[place_node:GN.parentFeature:]:
#         parent_id    = get_geonames_id(str(place_parent))
#         return parent_id
#     return None     # No parent place here

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

