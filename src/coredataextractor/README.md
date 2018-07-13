# Core data extractor

This directory contains code for a command line tool to extract EMPlaces core data, and other useful values, given a GeoNames ID.


## Installation (under Linux/Unix/MacOS)

Prerequisites: Python, git

Tested under Python 2.7.15.

Check out github repository:

    EMPLACES_ROOT=(working dir)
    cd $EMPLACES_ROOT
    git clone https://github.com/culturesofknowledge/emplaces.git
    cd emplaces
    git checkout develop   # For now: won't be needed when stable version released

Recommended to create and activate a new Python "virtualenv", thus:

    virtualenv gcdenv
    source gcdenv/bin/activate

Install `rdflib` dependency

    cd src/coredataextractor
    pip install rdflib==4.2.2

Run the extractor for Opole ("3090048" is the GeoNames id for the City of Opole):

    python get_core_data.py get 3090048

Turtle data is sent to stdout; may be redirected to a file, thus:

    python get_core_data.py get 3090048 >emplaces_opole.ttl


## Command line usage

    usage: get_core_data.py [-h] [--version] [--debug] [-e] [-g] [-l] [-c]
                            COMMAND [ARGS [ARGS ...]]

    EMPlaces GeoNames data extractor

    positional arguments:
      COMMAND               sub-command, one of the options listed below.
      ARGS                  Additional arguments, depending on the command used.

    optional arguments:
      -h, --help            show this help message and exit
      --version             show program's version number and exit
      --debug               Run with full debug output enabled. Also creates log
                            file 'get-core-data.log' in the working directory
      -e, --include-emplaces-defs
                            Include common EMPlaces defintions (e.g. for relation
                            types, periods, competencies, etc.) in the output
                            graph.
      -g, --include-geonames-defs
                            Include common GeoNames defintions (e.g. for feature
                            codes, categories, etc.) in the output graph.
      -l, --include-language-defs
                            Include common language resource defintions (as
                            referenced by name attestations, etc.) in the output
                            graph.
      -c, --include-common-defs
                            Include common EMPlaces, GeoNames and language
                            resource defintions in the output graph.

    Commands:

      get_core_data.py help [command]
      get_core_data.py get GEONAMESID
      get_core_data.py version

