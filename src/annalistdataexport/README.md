# Annalist data exporter

This directory contains code for a command line tool to extract EMPlaces data and related values from Annalist, given an Annalist place reference.


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

    cd src/geonamesdataexport
    pip install rdflib==4.2.2
    pip install requests==2.21.0


## Example usage

Run the extractor for Opole data as defined in GeoNames:

    python get_annalist_data.py gets Place_sourced/Opole_P_GeoNames

Turtle data is sent to stdout, and may be redirected to a file, thus:

    python get_annalist_data.py getsourced Place_sourced/Opole_P_GeoNames \
      >opole_geonames.ttl

Run the extractor for Opole data from multiple sources:

    python get_annalist_data.py getmerged Place_merged/Opole_P


## Command line usage

    usage: get_annalist_data.py [-h] [--version] [--debug] [-e] [-g] [-l] [-c]
                                COMMAND [ARGS [ARGS ...]]

    EMPlaces Annalist data exporter

    positional arguments:
      COMMAND               sub-command, one of the options listed below.
      ARGS                  Additional arguments, depending on the command used.

    optional arguments:
      -h, --help            show this help message and exit
      --version             show program's version number and exit
      --debug               Run with full debug output enabled. Also creates log
                            file 'get-annalist-data.log' in the working directory
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

      get_annalist_data.py help [command]
      get_annalist_data.py getmerged ANNALISTREF
      get_annalist_data.py getsourced ANNALISTREF
      get_annalist_data.py resource ANNALISTREF
      get_annalist_data.py version


