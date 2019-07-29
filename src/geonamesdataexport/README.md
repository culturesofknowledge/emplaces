# GeoNames data exporter

This directory contains code for a command line tool to extract EMPlaces data from GeoNamnes, and some related values, given a GeoNames ID.


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


## Example usage

Run the extractor for Opole ("3090048" is the GeoNames id for the City of Opole):

    python get_geonames_data.py get 3090048

Turtle data is sent to stdout, and may be redirected to a file, thus:

    python get_geonames_data.py get 3090048 >emplaces_opole.ttl

Get list of place Ids in administrative hierarchy:

    python get_geonames_data.py placehierarchy 3090048

Get Turtle data for all places in administrative hierarchy:

    python get_geonames_data.py placehierarchy 3090048 | \
    python get_geonames_data.py manyget >emplaces_opole_hierarchy.ttl

Get all members of the administrative hierarchy covering a supplied list of places:

    cat Opole_nearby_places.txt | python get_geonames_data.py manyplacehierarchy

Get RDF Turtle data for all members of the administrative hierarchy covering the list of places near Opole:

    cat Opole_nearby_places.txt | \
    python get_geonames_data.py manyplacehierarchy | \
    python get_geonames_data.py manyget > Opole_extracted_data.ttl


## Command line usage

    usage: get_geonames_data.py [-h] [--version] [--debug] [-e] [-g] [-l] [-c]
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

      get_geonames_data.py help [command]
      get_geonames_data.py getgeonamesdata GEONAMESID
      get_geonames_data.py manygetgeonamesdata
      get_geonames_data.py placehierarchy GEONAMESID
      get_geonames_data.py manyplacehierarchy
      get_geonames_data.py geonamesid URL [REGEXP]
      get_geonames_data.py manygeonamesids [REGEXP]
      get_geonames_data.py wikidataid GEONAMESID
      get_geonames_data.py many wikidataid
      get_geonames_data.py getwikidata WIKIDATAID
      get_geonames_data.py manygetwikidata
      get_geonames_data.py getwikitext WIKIDATAID
      get_geonames_data.py manygetwikitext WIKIDATAID
      get_geonames_data.py version
