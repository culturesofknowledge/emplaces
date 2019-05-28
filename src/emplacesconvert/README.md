# Annalist data exporter

This directory contains code for a command line tool to convert EMPlaces data to (and from?) other formats.

Initially, focusing on EMPlaces-to-LPIF [1] conversion.

[1] https://github.com/LinkedPasts/linked-places/blob/master/README.md

## Installation (under Linux/Unix/MacOS)

@@TODO: review this later@@

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

    python convert_emplaces_data.py to-lpif \
        ../../models/20180802-opole-example-multisourced.ttl \
        place:Opole_P


## Command line usage

    python convert_emplaces_data.py tolpif (data-url) (place-uri)

The converted data is written to stdout.

@@TODO: full usage
