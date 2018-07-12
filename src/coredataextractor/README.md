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

