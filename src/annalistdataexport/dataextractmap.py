# !/usr/bin/env python
#
# get_annalist_data.py - command line tool to create EMPlaces core from Annalist data
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

class EmptySelection(ValueError):
    pass

class DataExtractMap:
    """
    Class and supporting methods for extracting and mapping source data to 
    a target graph.

    Adds mapped data from node `base` in graph `src` to graph `tgt`

    To use this class:

    1. instantiate an instance object with a base node, source and target graphs.
    2. use methods of the instantiated instances to build a list of extract/transform functions
    3. call extract_map to perform the required transformation


    @@The design of the mapping is evolving. Curently:@@

    set_subj(<stmt_select>, <value>)
        sets value for `subj` (see <value>).  Defaults to `base`.

    emit(<stmt_select>, <subgraph>)
        adds a specified subgraph to the target graph.

    WHERE:

    <stmt_select> may be:
        prop_eq(<URI>)      matches statements whose property is <URI>
        prop_ne(<URI>)      matches statements whose property is different than <URI>

    <subgraph> may be:
        stmt(<value>, <value>, <value>)
                            a single statement with subject, object, pedicate

    <value> may be any of the following, which are evaluated by calling
    with a selected statement:
        tgt_subj            target subject: specified by set_subj, or source subject
        src_base            base node in source graph
        src_subj            subject from selected source statement.
        src_prop            property from selected source statement
        src_obj             object from selected source statement
    """

    def __init__(self, base, src):
        """
        base    is a node in the source graph
        src     source graph, from which data is extracted
        tgt     target graph, to which data is added
        """
        self._base     = base
        self._src      = src
        self._tgt      = None
        self._tgt_subj = None
        return

    # Helpers

    def _select(self, selector):
        """
        selector    is a function that is applied to the source graph and base
                    node URI, returning an iterator over selected triples from 
                    the source graph.

        returns an iterator of statements from source graph that match the selector.
        """
        return selector(self._src, self._base)

    def _select_single(self, selector):
        """
        selector    is a statement selector: see _select method.

        returns a single statement matching the selector, or raises an exception.
        """
        matches = self._select(selector)
        try:
            s, p, o        = matches.next()
            try:
                _ = matches.next()
            except StopIteration as e:
                pass    # expected response
            else:
                raise ValueError("map_def.set_subj: ambiguous selection")
        except StopIteration as e:
            raise EmptySelection("map_def.set_subj: empty selection")
        return (s, p, o)

    # Extract and map data using supplied mapping table

    def extract_map(self, data_mapping_table, target_graph):
        """
        This method invokes a supplied mapping table to extract data to a
        supplied target graph.
        """
        self._tgt = target_graph
        for emf in data_mapping_table:
            emf()
        return

    # Extract / transform methods

    def set_subj(self, selector, value):
        """
        Set subject based on matched statement

        selector    is a statement selector: see _select method.
        """
        def emf():
            try:
                s, p, o = self._select_single(selector)
                self._tgt_subj = value(s, p, o)
            except EmptySelection:
                pass # No subject to save
            return
        return emf

    def emit(self, selector, subgraph):
        """
        Emit statement(s) based on selected statements
        """
        def emf():
            matches = self._select(selector)
            for s, p, o in matches:
                for stmt in subgraph(s, p, o):
                    self._tgt.add(stmt)
        return emf

    # Statement selector methods

    def prop_eq(self, uri):
        """
        Returns selector for statements whose property is the supplied URI value.
        """
        def sel(src, base):
            print("@@@ prop_eq.sel %s, %r, %s"%(uri, src, base))
            return src.triples((base, URIRef(uri), None))
        return sel

    def prop_ne(self, uri):
        """
        Returns selector for statements whose property is the supplied URI value.
        """
        prop_ref = URIRef(uri)
        def sel(src, base):
            print("@@@ prop_ne.sel %s, %r, %s"%(uri, src, base))
            for s, p, o in src:
                if p != prop_ref:
                    yield (s, p, o)
            return
        return sel

    # Result subgraph generator methods

    def stmt(self, gen_s, gen_p, gen_o):
        """
        Returns a subgraph-generator function that emits a single statement.

        The subgraph-generator is called with subject, predicate and object 
        from a source statement, and returns an iterator of statements that 
        are to be added to the target graph.

        The arguments to this method are generators for subject, property and 
        object values respectvely, that are caled with the source statement
        components as arguments, and return corresponding values for the 
        target statement.
        """
        def gen(s, p, o):
            yield (gen_s(s, p, o), gen_p(s, p, o), gen_o(s, p, o))
            return
        return gen

    # Value generator methods

    def src_subj(self, s, p, o):
        """
        Return subject of matched statement
        """
        return s

    def src_prop(self, s, p, o):
        """
        Return property of matched statement
        """
        return p

    def src_obj(self, s, p, o):
        """
        Return object of matched statement
        """
        return o

    def src_base(self, s, p, o):
        """
        Returns the base node from the source graph that is being processed.
        """
        return self._base

    def tgt_subj(self, s, p, o):
        """
        Returns a subject for a target statement, either previously specified
        by `set_subj`, or from the currently matched statement.
        """
        return self._tgt_subj or s

    # @@@@ generate subgraph using recursive invocation


# End.
