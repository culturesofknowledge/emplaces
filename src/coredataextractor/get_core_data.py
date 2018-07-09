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

#   ===================================================================

def do_get_geonames_data(gcdroot, options):
    geonames_id = getargvalue(getarg(options.args, 0), "GoeNames Id: ")


    print("@@@ get %s"%())

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
    sys.exit(status)

# End.

