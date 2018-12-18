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
import requests

from rdflib         import Graph, Namespace, URIRef, Literal, BNode, RDF, RDFS
from rdflib.paths   import Path

from getargvalue    import getargvalue, getarg

log = logging.getLogger(__name__)

def load_rdf_text(entity_url, format="turtle"):
    rdf_formats = (
        { "turtle":     "text/turtle"
        , "xml":        "application/rdf+xml"
        })

    rdf_content_type = rdf_formats.get(format, rdf_formats["turtle"])
    req_headers = (
        { "accept":     rdf_content_type 
        })
    response = requests.get(entity_url, headers=req_headers)
    response.raise_for_status()  # raise an error on unsuccessful status codes
    return response.text

class RDFDataCache(object):

    def __init__(self):
        self._graph_cache = {}
        return

    def get_graph(self, entity_url, format="turtle"):
        if entity_url not in self._graph_cache:
            try:
                rdf_text = load_rdf_text(entity_url, format=format)
            except Exception as e:
                print("RDF load error '%s' (%s)"%(entity_url, e), file=sys.stderr)
            g = Graph()
            try:
                g.parse(data=rdf_text, format=format)
                self._graph_cache[entity_url] = g
            except Exception as e:
                print("RDF parse error '%s' (%s)"%(entity_url, e), file=sys.stderr)
            # result = g.parse(data=r.content, publicID=u, format="turtle")
            # result = g.parse(source=s, publicID=b, format="json-ld")
        return self._graph_cache[entity_url]

Rdf_graph_cache = RDFDataCache()

class EmptySelection(ValueError):
    pass

class DataExtractMap(object):
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
        prop_nseq(<URI>)    matches statements whose property starts with <URI>
        prop_nsne(<URI>)    matches statements whose property does not start with <URI>

    <subgraph> may be:
        stmt(<value>, <value>, <value>)
                            a single statement with subject, object, pedicate
        ref_subgraph(<value>, <value>, <value>, <subgraph_ref>, <subgraph_map>)
                            a subgraph that is mapped and referenced.

    <value> may be any of the following, which are evaluated by calling
    with a selected statement:
        tgt_subj            target subject: specified by set_subj, or source subject
        src_base            base node in source graph
        src_subj            subject from selected source statement.
        src_prop            property from selected source statement
        src_obj             object from selected source statement
    """

    def __init__(self, base, src, tgt):
        """
        base    is a node in the source graph
        src     source graph, from which data is extracted
        tgt     target graph, to which data is added
        """
        # print("@@@ DataExtractMap, base %s"%(base,))
        self._base      = base
        self._src       = src
        self._tgt       = tgt
        self._tgt_subj  = None
        return

    # Helpers
    # -------

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
                raise ValueError("map_def._select_single: ambiguous selection")
        except StopIteration as e:
            raise EmptySelection("map_def._select_single: empty selection")
        return (s, p, o)


    # Extract and map data using supplied mapping table
    # -------------------------------------------------

    def extract_map(self, data_mapping_table):
        """
        This method invokes a supplied mapping table to extract data to the
        target graph specified in the object constructor.

        Returns the subject resource set by the generated subgraph.
        """
        for emf in data_mapping_table:
            emf(self)
        return self._tgt_subj


    # Extract / transform methods
    # ---------------------------

    @classmethod
    def set_subj(cls, selector, value):
        """
        Set subject based on matched statement

        selector    is a statement selector: see _select method.
        """
        def set_subj_emf(self):
            try:
                s, p, o = self._select_single(selector)
                subj = value(self, s, p, o)
                if subj:
                    self._tgt_subj = value(self, s, p, o)
                # print("@@@ tgt_subj %s"%(self._tgt_subj))
            except EmptySelection:
                pass # No subject to save
            return
        return set_subj_emf

    @classmethod
    def emit(cls, selector, subgraph):
        """
        Emit statement(s) based on selected statements
        """
        def emit_emf(self):
            matches = self._select(selector)
            for s, p, o in matches:
                for stmt in subgraph(self, s, p, o):
                    # print("@@@ emit stmt %s"%(stmt,))
                    self._tgt.add(stmt)
        return emit_emf

    # Statement selector methods
    # --------------------------

    @classmethod
    def prop_all(cls):
        """
        Returns selector that matches all statements.
        """
        def prop_all_sel(src, base):
            # print("@@@ prop_all_sel %r, %s"%(src, base))
            return src.triples((URIRef(base), None, None))
        return prop_all_sel

    @classmethod
    def prop_eq(cls, uri):
        """
        Returns selector for statements whose property is the supplied URI value.
        """
        def prop_eq_sel(src, base):
            # print("@@@ prop_eq_sel u: %s, b: %r"%(uri, base))
            # print("@@@ triples     %r"%(list( 
            #     src.triples((URIRef(base), URIRef(uri), None))
            #     )))
            return src.triples((URIRef(base), URIRef(uri), None))
        return prop_eq_sel

    @classmethod
    def prop_ne(cls, uri):
        """
        Returns selector for statements whose property is the supplied URI value.
        """
        prop_ref = URIRef(uri)
        def prop_ne_sel(src, base):
            # print("@@@ prop_ne_sel %s, %r, %s"%(uri, src, base))
            for s, p, o in src:
                if p != prop_ref:
                    yield (s, p, o)
            return
        return prop_ne_sel

    @classmethod
    def prop_nseq(cls, uri):
        """
        Returns selector for statements whose property starts with the supplied URI value.
        """
        def prop_nseq_sel(src, base):
            for stmt in src:
                if str(stmt[1]).startswith(str(uri)):
                    yield stmt
            return
        return prop_nseq_sel

    @classmethod
    def prop_nsne(cls, uri):
        """
        Returns selector for statements whose property starts with the supplied URI value.
        """
        def prop_nsne_sel(src, base):
            for stmt in src:
                if not str(stmt[1]).startswith(str(uri)):
                    yield stmt
            return
        return prop_nsne_sel


    # Result subgraph generator methods
    # ---------------------------------
    #
    # These are class methods that return an unbound object method which is
    # invoked with a data extract map instance and the subject, predicate and 
    # object of a matched source statement.

    @classmethod
    def stmt(cls, gen_s, gen_p, gen_o):
        """
        Returns a subgraph-generator function that emits a single statement.

        The subgraph-generator is called with subject, predicate and object 
        from a source statement, and returns an iterator of statements that 
        are to be added to the target graph.

        gen_s
        gen_p
        gen_o   are generators for subject, property and object values respectvely.
                These are called at the point of emiting data with the source 
                statement components as arguments, and return corresponding values 
                for the target statement.  They may also access local variables of
                the current `DataExtractMap` object.
        """
        def gen(self, s, p, o):
            yield (gen_s(self, s, p, o), gen_p(self, s, p, o), gen_o(self, s, p, o))
            return
        return gen

    @classmethod
    def stmt_copy(cls):
        """
        Returns a subgraph generator that emits a copy of the current statement,
        possibly with the subject replaced according to a previous "set_subj".
        """
        return cls.stmt(cls.tgt_subj, cls.src_prop, cls.src_obj)

    @classmethod
    def stmt_copy_not_blank(cls):
        """
        Returns a subgraph generator that emits a copy of the current statement,
        possibly with the subject replaced according to a previous "set_subj",
        provided that the object is not a blank literal or URI reference.
        """
        def gen(self, s, p, o):
            o_val = self.src_obj(s, p, o)
            # print("@@@ stmt_copy_not_blank o_val %s"%(o_val,))
            if o_val != "":
                yield (self.tgt_subj(s, p, o), self.src_prop(s, p, o), o_val)
            return
        return gen

    @classmethod
    def stmt_copy_obj_ne(cls, val):
        """
        Returns a subgraph generator that emits a copy of the current statement,
        possibly with the subject replaced according to a previous "set_subj",
        provided that the object is not equal to the supplied value
        """
        def gen(self, s, p, o):
            o_val = self.src_obj(s, p, o)
            # print("@@@ stmt_copy_val_ne o_val %s"%(o_val,))
            if str(o_val) != val:
                yield (self.tgt_subj(s, p, o), self.src_prop(s, p, o), o_val)
            # else:
            #     print("@@@ stmt_copy_val_ne skipped o_val %s"%(o_val,))
            return
        return gen

    @classmethod
    def ref_subgraph(cls, gen_s, gen_p, subgraph_ref, subgraph_map):
        """
        Returns a subgraph-generator function that emits a link to a subgraph, 
        then scans and maps the referenced subgraph and also emits that.

        The subgraph-generator is called with subject, predicate and object 
        from a source statement, and returns an iterator of statements that 
        are to be added to the target graph.

        gen_s
        gen_p   are generators for subject and property of a statement that references 
                the generated subgraph. These are called at the point of emiting data 
                with the source statement components as arguments, and return 
                corresponding values for the subgraph reference statement.
                (They may also access local variables of the current object.)
        subgraph_ref
                a function that returns a reference to the base of a subgraph
                to be extracted and emited.
        subgraph_map
                a mapping table that drived generation of the emited subgraph.
        """
        def ref_subgraph_gen(self, s, p, o):
            # Get copy of graph
            subgraph_url = str(subgraph_ref(self, s, p, o))
            # print("@@@ subgraph_url %s, link from %s, %s"%(subgraph_url,gen_s(self, s, p, o), gen_p(self, s, p, o)))
            # if subgraph_url.startswith("#"):
            #     assert false, "@@@@ URL error"
            subgraph_rdf = Rdf_graph_cache.get_graph(subgraph_url)
            # Map and emit subgraph
            sub_subgraph_map = DataExtractMap(
                subgraph_url, 
                subgraph_rdf, 
                self._tgt
                )
            subgraph_res = sub_subgraph_map.extract_map(subgraph_map)
            # Link to subgraph
            # print("@@@ link to subgraph; %s"%((gen_s(self, s, p, o), gen_p(self, s, p, o), subgraph_res or o),))
            yield (gen_s(self, s, p, o), gen_p(self, s, p, o), subgraph_res or o)
            return
        return ref_subgraph_gen

    @classmethod
    def ref_list(cls, gen_s, gen_p, list_head, subgraph_map):
        """
        Returns a subgraph-generator function that scans and maps a referenced 
        list of subgraphs, and also emits a link to that list.

        The subgraph-generator is called with subject, predicate and object 
        from a source statement, and returns an iterator of statements that 
        are to be added to the target graph.

        The arguments are very simlar to `ref_subgraph`, except that the provided
        reference is to the head of a list of subgruaf references

        gen_s
        gen_p   are generators for subject and property of a statement that references 
                the generated subgraph. These are called at the point of emiting data 
                with the source statement components as arguments, and return 
                corresponding values for the subgraph reference statement.
                (They may also access local variables of the current object.)
        list_head
                a functiomn that returns a reference to the head of a list of subgraphs 
                to be extracted and emited.
        subgraph_map
                a mapping table that drived generation of the emited subgraphs.
        """
        def ref_list_gen(self, s, p, o):
            # Initialse cursor to head of of list
            prev_s = gen_s(self, s, p, o)
            prev_p = gen_p(self, s, p, o)
            cursor = list_head(self, s, p, o)
            while cursor != RDF.nil:
                item     = self._src.value(subject=cursor, predicate=RDF.first, any=False)
                tail     = self._src.value(subject=cursor, predicate=RDF.rest,  any=False)
                new_cons = BNode()
                # Extract and map subgraph, linked from new list item
                ref_subg = self.ref_subgraph(self.const(new_cons), self.const(RDF.first), self.const(item), subgraph_map)
                for stmt in ref_subg(self, s, p, o):
                    yield stmt
                # Link to new list item from referrer
                yield (prev_s, prev_p, new_cons)
                # Advance values to next list item
                prev_s   = new_cons     # Referrer subject   to next cons in target list
                prev_p   = RDF.rest     # Referrer predicate to next cons in target list
                cursor   = tail         # Next cons in source list
            # Close off new list
            yield (prev_s, prev_p, RDF.nil)
            return
        return ref_list_gen

    @classmethod
    def alt_values(cls, test_stmt, alt_pass, alt_fail):
        """
        Emit alternative statement(s) based on selected statements,
        depending on result of test applied to each match.
        """
        def emit_alt_gen(self, s, p, o):
            # print("@@@ emit_alt_gen (%s, %s, %s)"%(s, p, o))
            alt_gen = alt_pass if test_stmt(self, s, p, o) else alt_fail
            for stmt in alt_gen(self, s, p, o):
                # print("@@@ emit_alt stmt %s"%(stmt,))
                yield stmt
        return emit_alt_gen

    # Statement test methods
    # ----------------------
    #
    # These are class methods that return an unbound object method which is
    # invoked with a data extract map instance and the subject, predicate and 
    # object of a matched source statement, and return True or False depending
    # on whether the corresponding test passes.

    @classmethod
    def test_prop_in(cls, prop_set):
        """
        Tests if property is one of a supplied set.
        """
        def tst(self, s, p, o):
            # print("@@@ test_prop_in %s {%r}"%(p, prop_set))
            return p in prop_set
        return tst


    # Value generator methods
    # -----------------------
    #
    # These are class methods that return an unbound object method which is
    # invoked with a data extract map instance and the subject, predicate and 
    # object of a matched source statement.

    @classmethod
    def const(cls, value):
        """
        Value generator that returns a supplied node value.

        NOTE: unlike some other value generators, this is invoked as a function.
        """
        def val(self, s, p, o):
            return value
        return val

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

    @classmethod
    def src_obj_or_val(cls, prop):
        """
        If the object of matched statement is a resource with an indicated
        property, return the value of that property, otherwise return the 
        object of the current statement.

        (This allows resources to indiocated alternate values or aliases
        with which they should be referenced.)

        NOTE: unlike some other value generators, this is invoked as a function.
        """
        def val(self, s, p, o):
            value = self._src.value(subject=o, predicate=prop, any=False)
            if value is None:
                value = o
            return value
        return val

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

# End.
