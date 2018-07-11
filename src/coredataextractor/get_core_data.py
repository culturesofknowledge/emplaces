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

from rdflib         import Graph, Namespace, URIRef, Literal
from rdflib.paths   import Path

from getargvalue    import getargvalue, getarg

log = logging.getLogger(__name__)

dirhere = os.path.dirname(os.path.realpath(__file__))
gcdroot = os.path.dirname(os.path.join(dirhere))
sys.path.insert(0, gcdroot)

# Software version

GCD_VERSION = "0.1"

# Status return codes

GCD_SUCCESS          = 0         # Success
GCD_BADCMD           = 2         # Command error
GCD_UNKNOWNCMD       = 3         # Unknown command
GCD_UNIMPLEMENTED    = 4         # Unimplemented command or feature
GCD_UNEXPECTEDARGS   = 5         # Unexpected arguments supplied

#   ===================================================================

def progname(args):
    return os.path.basename(args[0])

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
                             "Also creates log file 'annalist-manager.log' in the working directory"
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

#   ===================================================================

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

command_summary_help = ("\n"+
    "Commands:\n"+
    "\n"+
    "  %(prog)s help [command]\n"+
    "  %(prog)s get GEONAMESID\n"+
    "  %(prog)s version\n"+
    "")

def gcd_help(options, progname):
    """
    Display annalist-manager command help

    options     contains options parsed from the command line.

    returns     0 if all is well, or a non-zero status code.
                This value is intended to be used as an exit status code
                for the calling program.
    """
    if len(options.args) > 1:
        print("Unexpected arguments for %s: (%s)"%(options.command, " ".join(options.args)), file=sys.stderr)
        return gcd_errors.AM_UNEXPECTEDARGS
    status = gcd_errors.AM_SUCCESS
    if len(options.args) == 0:
        help_text = (
            command_summary_help+
            "\n"+
            "For more information about command options, use:\n"+
            "\n"+
            "  %(prog)s --help\n"+
            "")
    elif options.args[0].startswith("get"):
        help_text = ("\n"+
            "  %(prog)s get GEONAMESID\n"+
            "\n"+
            "Gets data about a specified place from GeoNames, and sends corresponding\n"+
            "EMPlaces data to standard output.\n"+
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

def do_get_geonames_data(gcdroot, options):
    gn        = Namespace("http://www.geonames.org/ontology#")
    wgs84_pos = Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#")
    skos      = Namespace("http://www.w3.org/2004/02/skos/core#")


    geonames_id  = getargvalue(getarg(options.args, 0), "GeoNames Id: ")
    geonames_uri = "http://sws.geonames.org/%s/"%(geonames_id,)
    geonames_url = "http://sws.geonames.org/%s/about.rdf"%(geonames_id,)
    geonames_rdf = get_rdf_graph(geonames_url)

    geo_ont_url  = "http://www.geonames.org/ontology/ontology_v3.1.rdf"
    geo_ont_rdf  = get_rdf_graph(geo_ont_url)

    geonames_node   = URIRef(geonames_uri)
    place_name      = geonames_rdf[geonames_node:gn.name:].next()
    place_altnames  = list(geonames_rdf[geonames_node:gn.alternateName:])
    place_def_by    = URIRef(geonames_url)
    place_category  = geonames_rdf[geonames_node:gn.featureClass:].next()
    place_type      = geonames_rdf[geonames_node:gn.featureCode:].next()
    place_map       = geonames_rdf[geonames_node:gn.locationMap:].next()
    place_parent    = geonames_rdf[geonames_node:gn.parentFeature:].next()
    place_seeAlso   = list(geonames_rdf[geonames_node:gn.seeAlso|gn.wikipediaArticle:])
    place_lat       = geonames_rdf[geonames_node:wgs84_pos.lat:].next()
    place_long      = geonames_rdf[geonames_node:wgs84_pos.long:].next()

    place_type_labels = geo_ont_rdf[place_type:skos.prefLabel:]
    for l in place_type_labels:
        if l.language == "en":
            place_type_label  = Literal(" ".join(str(l).split()))
            # https://stackoverflow.com/a/46501496/324122
    display_label     = Literal("%s (%s)"%(place_name, place_type_label)) 
    display_names     = list(set([Literal(unicode(n)) for n in place_altnames]))

    print("@@@ get %s"%(geonames_id))
    print("@@@ geonames_node   %r"%(geonames_node))
    print("@@@ place_name:     %r"%(place_name))
    print("@@@ place_altnames: %r"%(place_altnames))
    print("@@@ place_def_by:   %r"%(place_def_by))
    print("@@@ place_category: %r"%(place_category))
    print("@@@ place_type:     %r"%(place_type))
    print("@@@ place_map:      %r"%(place_map))
    print("@@@ place_parent:   %r"%(place_parent))
    print("@@@ place_seeAlso:  %r"%(place_seeAlso))
    print("@@@ lat, long:      %r, %r"%(place_lat, place_long))
    print("@@@ display_label:  %r"%(display_label))
    print("@@@ display_names:  %s"%(",".join(display_names)))
    # print("@@@ graph:")
    # print(geonames_rdf.serialize(format='turtle', indent=4))
    print("@@@")

    emplaces_id  = "g_%s"%(geonames_id)
    emplaces_uri = "http://emplaces.namespace.example.org/places/%s"%(emplaces_id)
    emplaces_rdf = Graph()

    emplaces_rdf.bind("em",  "http://emplaces.namespace.example.org/")
    emplaces_rdf.bind("emp", "http://emplaces.namespace.example.org/places/")
    emplaces_rdf.bind("emt", "http://emplaces.namespace.example.org/timespan/")
    emplaces_rdf.bind("eml", "http://emplaces.namespace.example.org/language/")
    for gn_pre, gn_uri in geonames_rdf.namespaces():
        emplaces_rdf.bind(gn_pre, gn_uri)





    # ex:Opole_P a em:Place ;
    #     # Added label to distinguish from other places with same name
    #     # (initial default to preferred name?)
    #     rdfs:label       "City of Opole" ;                              # Label for place
    #     rdfs:isDefinedBy <http://sws.geonames.org/3090048/about.rdf> ;  # document
    #     em:coreDataRef
    #       [ rdfs:label "GeoNames data" ;
    #         em:link <http://sws.geonames.org/3090048/about.rdf>
    #       ] ;
    #     em:alternateURI
    #       [ rdfs:label "GeoNames URI" ;
    #         em:link <http://sws.geonames.org/3090048/>
    #       ] ;
    #     # Core data (derived from GeoNames /reference gazetteer)
    #     em:placeCategory gn:P ;             # from gn:featureClass
    #     em:corePlaceType gn:P.PPLA ;        # from gn:featureCode
    #     em:preferredName "Opole" ;          # from gn:name
    #     em:alternateName "Opole" ;          # from gn:alternateName
    #     em:displayName "Opole" ;


    return GCD_UNIMPLEMENTED

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
        return do_get_geonames_data(gcdroot, options)
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

