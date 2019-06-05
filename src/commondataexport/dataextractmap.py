# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# RDF data extraction and mapping.
# See class DataExtractMap for details.
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
import urllib
import urlparse

from rdflib         import Graph, Namespace, URIRef, Literal, BNode, RDF, RDFS
from rdflib.paths   import Path

log = logging.getLogger(__name__)

def merge_two_dicts(x, y):
    # From: https://stackoverflow.com/a/26853961
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z

def copy_update_dict(x, **updates):
    return merge_two_dicts(x, updates)

def http_get_json(url, req_headers={}):
    """
    Issue an HTTP GET request to the supplied URL, and return the result data.
    """
    return http_get(url, copy_update_dict(req_headers, accept="application/json"))

def http_get(url, req_headers={}):
    """
    Issue an HTTP GET request to the supplied URL, and return the result data.
    """
    response = requests.get(url, headers=req_headers)
    response.raise_for_status()  # raise an error on unsuccessful status codes
    return response.text

def make_query_url(endpoint_url, **query_params):
    """
    Builds a query URL from the supplied endpoint URL and query params.
    """
    # encode_query = urllib.urlencode(query_params)
    query_string = "&".join([ key+"="+urllib.quote(query_params[key]) for key in query_params ])
    encode_query = "?" + query_string
    query_url    = urlparse.urljoin(endpoint_url, encode_query)
    return query_url

def find_entity_url(entity_uri, content_type="text/turtle"):
    """
    Use content negotiuation to find URL for data with specified 
    content type.
    """
    req_headers = (
        { "accept":     content_type 
        })
    response = requests.head(entity_uri, headers=req_headers, allow_redirects=True)
    response.raise_for_status()  # raise an error on unsuccessful status codes
    return response.url    

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
    2. use methods of the instantiated instances to build a list of 
       extract/transform functions
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
        stmt_gen(<URI>,<obj>)
                            generate and return a single statement whose subject is the
                            current base URI, property is <URI> and object is <obj>.
                            Use this with 'stmt_copy' to synthesize new statements that 
                            don't appear in the source graph.

    <subgraph> may be:
        stmt(<value>, <value>, <value>)
                            a single statement with subject, object, pedicate
        stmt_copy()         a short form for 'stmt(tgt_subj, src_prop, src_obj)'
        ref_subgraph(<value>, <value>, <subgraph_ref>, <subgraph_map>)
                            a subgraph that is mapped and referenced by a statement for
                            which subject and property generators are supplied.  A new
                            node is created as subject for the subgraph statements, and 
                            the URI is dereferenced as RDF, and used as a new source graph 
                            from which statements are scanned.
        loc_subgraph(<value>, <value>, <subgraph_ref>, <subgraph_map>)
                            a subgraph that is mapped and referenced by a statement for
                            which subject and property generators are supplied.  A new
                            node is created as subject for the subgraph statements.  
                            Unlike 'ref_subgraph', statements about the new subject are
                            scanned from the current source graph.

    <value> may be any of the following, which are evaluated by calling
    with a selected statement:
        tgt_subj            target subject: specified by set_subj, or source subject
        src_base            base node in source graph
        src_subj            subject from selected source statement.
        src_prop            property from selected source statement
        src_obj             object from selected source statement
        srv_val             additional value from the source data
        const(val)          specified value
        src_obj_or_val(prop) property of referenced resource (obj), or just the 
                            referenced resource.  (Use this for resources that may
                            indicate alternate reference URIs, e.g. using owl:sameAs.)
    """

    def __init__(self, base, src, tgt, ref_src_subj=None, ref_tgt_subj=None, ref_src_obj=None):
        """
        base    is a node in the source graph
        src     source graph, from which data is extracted
        tgt     target graph, to which data is added
        ref_src_subj 
                if specified, is the subject of a source graph statement 
                that triggers this mapping.
        ref_tgt_subj 
                if specified, is a target graph subject for which the triggering
                statement is defining properties.
        ref_src_obj 
                if specified, is the object of a source graph statement 
                that triggers this mapping.
         """
        # print("@@@ DataExtractMap, base %s"%(base,))
        self._base      = base
        self._src       = src
        self._tgt       = tgt
        self._tgt_subj  = None
        self._ref_src_subj = ref_src_subj
        self._ref_tgt_subj = ref_tgt_subj
        self._ref_src_obj  = ref_src_obj
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
                    self._tgt_subj = subj #@@ value(self, s, p, o)
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
            for s, p, o in src.triples((URIRef(base), None, None)):
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
            for stmt in src.triples((URIRef(base), None, None)):
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
            for stmt in src.triples((URIRef(base), None, None)):
                if not str(stmt[1]).startswith(str(uri)):
                    yield stmt
            return
        return prop_nsne_sel

    @classmethod
    def stmt_gen(cls, prop_uri, obj=None):
        """
        Returns generator for a single statement with the supplied property and object.

        If no object value is supplied, a blank node is allocated and used.
        """
        obj_node = obj      # Assume already presented as RDF node
        if obj is None:
            obj_node = BNode()
        elif isinstance(obj, str):
            # Heuristic for kind of graph node
            if obj.startswith("http:") or obj.startswith("https:") or obj.startswith("file:"):
                obj_node = URIRef(obj)
            else:
                obj_node = Literal(obj)
        #@@@ obj_node = URIRef(obj) if obj else BNode()
        def stmt_gen_sel(src, base):
            yield (base, URIRef(prop_uri), obj_node)
            return
        return stmt_gen_sel

    @classmethod
    def stmt_gen_link(cls, prop_uri, obj_url):
        """
        Returns generator for a single statement with the supplied property and 
        URL object vaue.  If the supplied object value is None, no statement is generated.
        """
        def stmt_gen_sel(src, base):
            if isinstance(obj_url, str):
                yield (base, URIRef(prop_uri), URIRef(obj_url))
            return
        return stmt_gen_sel


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
    def stmt_copy(cls, s=None, p=None, o=None):
        """
        Returns a subgraph generator that emits a copy of the current statement,
        possibly with the subject replaced according to a previous "set_subj".

        The subject, property or object may be overridden by supplied 
        `s`, `p` or `o` parameters.
        """
        s = s or cls.tgt_subj
        p = p or cls.src_prop
        o = o or cls.src_obj
        return cls.stmt(s, p, o)
        # return cls.stmt(cls.tgt_subj, cls.src_prop, cls.src_obj)

    @classmethod
    def stmt_copy_val(cls, obj_val):
        """
        Returns a subgraph generator that emits a copy of the current statement,
        but with the object value replaced by the value returned by the supplied
        obj_val function.
        """
        #@@deprecate this: use `stmt_copy` instead
        return cls.stmt(cls.tgt_subj, cls.src_prop, obj_val)

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
    def loc_subgraph(cls, gen_s, gen_p, subgraph_ref, subgraph_map):
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
                to be scanned and emited.
        subgraph_map
                a mapping table that drived generation of the emited subgraph.
        """
        def loc_subgraph_gen(self, s, p, o):
            # Get copy of graph
            subgraph_node = subgraph_ref(self, s, p, o)
            # Map and emit subgraph
            sub_subgraph_map = DataExtractMap(
                subgraph_node, 
                self._src, 
                self._tgt,
                ref_src_subj=s, 
                ref_tgt_subj=self._tgt_subj, 
                ref_src_obj=o
                )
            subgraph_res = sub_subgraph_map.extract_map(subgraph_map)
            # Link to subgraph (if subject/property supplied)
            if gen_s and gen_p:
                yield (gen_s(self, s, p, o), gen_p(self, s, p, o), subgraph_res or subgraph_node)
            return
        return loc_subgraph_gen

    @classmethod
    def ref_subgraph(cls, gen_s, gen_p, subgraph_ref, subgraph_map):
        # @@TODO: refactor common logic in gen_subgraph and ref_subgraph
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
            subgraph_node = subgraph_ref(self, s, p, o)
            subgraph_url  = str(subgraph_node)
            print("@@@ subgraph_url %s, link from %s, %s"%(subgraph_url,gen_s(self, s, p, o), gen_p(self, s, p, o)))
            if subgraph_url.startswith("#"):
                assert false, "@@@@ URL error"
            subgraph_rdf = Rdf_graph_cache.get_graph(subgraph_url)
            # Map and emit subgraph
            sub_subgraph_map = DataExtractMap(
                subgraph_node, 
                subgraph_rdf, 
                self._tgt,
                ref_src_subj=s, 
                ref_tgt_subj=self._tgt_subj, 
                ref_src_obj=o
                )
            subgraph_res = sub_subgraph_map.extract_map(subgraph_map)
            # Link to subgraph
            yield (gen_s(self, s, p, o), gen_p(self, s, p, o), subgraph_res or subgraph_node)
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
                a function that returns a reference to the head of a list of subgraphs 
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
    # These are object methods, or class methods that return an unbound 
    # object method, which are invoked with a data extract map instance and 
    # the subject, predicate and object of a matched source statement.

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

    def ref_src_subj(self, s, p, o):
        """
        Returns the source subject of the referring statement that triggers the
        current mapping.
        """
        return self._ref_src_subj

    def ref_tgt_subj(self, s, p, o):
        """
        Returns the target subject of the referring statement that triggers the
        current mapping.  I.e. `tgt_subj` for the referring statement.

        This can be used in a set_subj in the subgraph to continue defining values
        for the same target, effectively flattening the graph by a level.
        """
        return self._ref_tgt_subj

    def ref_src_obj(self, s, p, o):
        """
        Returns the source object of the referring statement that triggers the
        current mapping.

        This can be used to carry a value down a level from the referring graph to
        a generated subgraph.
        """
        return self._ref_src_obj

    @classmethod
    def const(cls, value):
        """
        Value generator that returns a supplied node value.

        NOTE: unlike some other value generators, this is invoked as a function call.
        """
        def val(self, s, p, o):
            return value
        return val

    @classmethod
    def const_uri(cls, uri):
        """
        Value generator that returns a node named using the supplied URI.
        """
        return cls.const(URIRef(uri))

    @classmethod
    def const_gen_literal(cls, template):
        """
        Value generator that interpolates statement values in a template 
        to yield a new literal node.

        Template may contain '%(subj)s', '%(prop)s' and/or '%(obj)s' to refer to statement
        subject, property or object respectively
        """
        def val(self, s, p, o):
            return Literal(template%{'subj': str(s), 'prop': str(p), 'obj': str(o)})
        return val

    @classmethod
    def const_gen_uri(cls, template):
        """
        Value generator that interpolates statement values in a template 
        to yield a new URI node

        Template may contain '%(subj)s', '%(prop)s' and/or '%(obj)s' to refer to statement
        subject, property or object respectively
        """
        def val(self, s, p, o):
            return URIRef(template%{'subj': str(s), 'prop': str(p), 'obj': str(o)})
        return val

    @classmethod
    def src_obj_or_val(cls, prop):
        """
        If the object of matched statement is a resource with an indicated
        property, return the value of that property, otherwise return the 
        object of the current statement.

        (This allows resources to indicate alternate values or aliases
        with which they should be referenced.)

        NOTE: unlike some other value generators, this is invoked as a function.
        """
        def val(self, s, p, o):
            value = self._src.value(subject=o, predicate=prop, any=False)
            if value is None:
                value = o
            return value
        return val

# End.
