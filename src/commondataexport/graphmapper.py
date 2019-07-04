# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# RDF graph mapping.
# See class GraphMapper for details.
#
# This is an alternative, more procedural, approach to providing functionality
# dataextractmap.py, which should be more flexible whemn it comes to dealing with 
# complex structure mapping (dataextractmap.py being better suited to simple
# change-of-name types of conversion.)
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

#   ===================================================================
#
#   Helpers
#
#   ===================================================================

def make_node(n):
    """
    Returns a node cor the supplied value
    """
    if isinstance(n, (str, unicode)):
        n = URIRef(n)
    return n

#   ===================================================================
#
#   Match pattern class
#
#   ===================================================================

class GraphMatchPattern(object):
    """
    Represents a pattern to be matched.
    """

    def __init__(self, pattern_list):
        """
        Initialize a graph match pattern.

        pattern_list
            is a list of graph path elements to be matched.  

        Each element of pattern_list may be any one of:

        URIRef or str
            coresponds to a graph path property to be matched.

        GraphMatchPattern object
            a pattern to be matched at the corresponding point in the match pattern.

        A match is initiated from a designated start node.  Each matched element advances 
        the node in the graph at which the next pattern element is matched.  Some elements
        (e.g. filter patterns) do not advance the graph next-match node.

        Each element can potentially have zero, on or multiple matches in the graph.
        If an element does not match (zero matches), or when all matches have been tried,
        the current element is abandoned and alternative matches for the previously matched
        element are attempted.

        Thus, the result of a match is zero, one or more sequences of connected graph nodes, 
        each starting with the initial start node.
        """
        self._pattern_elems = [self.make_pattern_elem(p) for p in pattern_list]
        return

    def __repr__(self):
        return "pattern[%s]"%(",".join(str(self._match_elems)))

    @classmethod
    def make_pattern_elem(cls, item):
        """
        Make pattern element object for a supplied pattern item
        """
        if isinstance(item, str):
            item = URIRef(item)
        if isinstance(item, URIRef):
            return GraphMatchProperty(item)
        if isinstance(item, GraphMatchPattern):
            return item
        raise ValueError("Unexpected pattern item %r"%(item,))
        return None

    def match(self, src_graph, start_node):
        return GraphMatchSequenceResult(src_graph, start_node, self._pattern_elems)

    @classmethod
    def filter(cls, pattern_list, node_match):
        """
        Constructs and returns a GraphMatchPattern object that fails unless the 
        specified pattern list can be matched yielding a leaf node that satisfies
        the node_match value.
        """
        return GraphMatchFilter(pattern_list, node_match)

    @classmethod
    def repeat(cls, pattern_list):
        """
        Constructs and returns a GraphMatchPattern object that successively matches 
        zero or more instances of the indicated pattern.
        """        
        return GraphMatchRepeat(pattern_list)

#   ===================================================================
#
#   Match results class
#
#   ===================================================================

class GraphMatchResult(object):
    """
    This class represents the results of a graph matching operation
    (GraphMapper.match)
    """

    def __init__(self):
        """
        Initialize a new graph pattern match result object.

        The match results are evaluated lazily, so if only the first
        result is accessed, not other results are actually computed.

        This also permits streamed processing of match results.
        """
        raise "@@ GraphMatchResult.__init__: not implemented"

    def leaves(self):
        return (seq[-1] for seq in self)

    def leaf(self):
        results = iter(self)
        result  = results.next()
        try:
            more = results.next()
            raise ValueError("GraphMatchResult.leaf: Single result expected")
        except StopIteration:
            pass
        return result[-1]

#   ===================================================================
#
#   Match result for a sequence of match elements
#
#   ===================================================================

class GraphMatchSequenceResult(GraphMatchResult):
    """
    Represents result from matching a sequence of match elements.
    """

    def __init__(self, src_graph, start_node, match_elems):
        self._src_graph   = src_graph
        self._start_node  = start_node
        self._match_elems = match_elems
        return

    def __iter__(self):
        next_elem  = self._match_elems[0]
        tail_elems = self._match_elems[1:]
        # log.debug("GraphMatchSequenceResult %r, %r, %r"%(self._start_node, next_elem, tail_elems))
        for next_match in next_elem.match(self._src_graph, self._start_node):
            # log.debug("GraphMatchSequenceResult next_match %r"%(next_match))
            if tail_elems:
                tail_matches = GraphMatchSequenceResult(self._src_graph, next_match[-1], tail_elems)
                for tail_match in tail_matches:
                    yield next_match + tail_match[1:]
            else:
                yield next_match
        return

#   ===================================================================
#
#   Match pattern and result for a single property in a graph
#
#   ===================================================================

class GraphMatchProperty(GraphMatchPattern):
    """
    Represents a single property to be matched.
    """

    def __init__(self, property_uriref):
        self._uriref = property_uriref
        return

    def __repr__(self):
        return "%s"%(self._uriref)

    def match(self, src_graph, start_node):
        return GraphMatchPropertyResult(src_graph, start_node, self._uriref)

class GraphMatchPropertyResult(GraphMatchResult):
    """
    Represents result from matching a single property.
    """

    def __init__(self, src_graph, start_node, property_uriref):
        self._src_graph  = src_graph
        self._start_node = start_node
        self._uriref     = property_uriref
        return

    def __iter__(self):
        log.debug("GraphMatchPropertyResult %r, %r"%(self._start_node, self._uriref))
        for obj in self._src_graph.objects(subject=self._start_node, predicate=self._uriref):
            log.debug("GraphMatchPropertyResult yield %r"%(obj))
            yield [self._start_node, obj]
        return

#   ===================================================================
#
#   Match pattern and result for a filter element
#
#   ===================================================================

class GraphMatchFilter(GraphMatchPattern):
    """
    Constructs and returns a GraphMatchPattern object that fails unless the 
    specified pattern list can be matched yielding a leaf node that satisfies
    the node_match value.

    node_match may be any one of:

    URIRef or str
        satisfied by a node labelled with the indicated URI.

    Literal
        satisfied by a node that is the indicated literal.
    """

    def __init__(self, pattern_list, node_match):
        self._match_elems = [self.make_pattern_elem(p) for p in pattern_list]
        if isinstance(node_match, str):
            node_match = IRIRef(node_match)
        if isinstance(node_match, (URIRef,Literal)):
            self._node_match = node_match
        else:
            raise ValueError("Unexpected node_match value %r"%(node_match,))
        return

    def __repr__(self):
        return "filter(%r, %s)"%(self._match_elems, self._node_match)

    def match(self, src_graph, start_node):
        return GraphMatchFilterResult(src_graph, start_node, self._match_elems, self._node_match)

class GraphMatchFilterResult(GraphMatchResult):
    """
    Represents result from matching a result filter.

    If the filter matches, a single result sequence containing just the start
    node is returned; otherwise no results are returned.
    """

    def __init__(self, src_graph, start_node, match_elems, node_match):
        self._src_graph   = src_graph
        self._start_node  = start_node
        self._match_elems = match_elems
        self._node_match  = node_match
        return

    def __iter__(self):
        for match in GraphMatchSequenceResult(
            self._src_graph, self._start_node, self._match_elems):
            if match[-1] == self._node_match:
                log.debug("GraphMatchFilterResult match %r"%(self._start_node))
                yield [self._start_node]
        return

#   ===================================================================
#
#   Match pattern and result for a repeat element
#
#   ===================================================================

class GraphMatchRepeat(GraphMatchPattern):
    """
    Constructs and returns a GraphMatchPattern object that matches a graph path that
    contains the specified pattern sequentially zero, one or more times.
    """

    def __init__(self, pattern_list):
        self._match_elems = [self.make_pattern_elem(p) for p in pattern_list]
        return

    def __repr__(self):
        return "repeat(%r)"%(self._match_elems,)

    def match(self, src_graph, start_node):
        return GraphMatchRepeatResult(src_graph, start_node, self._match_elems)

class GraphMatchRepeatResult(GraphMatchResult):
    """
    Represents result from matching a result filter.

    If the filter matches, a single result sequence containing just the start
    node is returned; otherwise no results are returned.
    """

    def __init__(self, src_graph, start_node, match_elems):
        self._src_graph   = src_graph
        self._start_node  = start_node
        self._match_elems = match_elems
        return

    #@@TODO: figure how to prevent chasing round a graph loop
    def __iter__(self):
        yield [self._start_node]    # zero repeats case
        for next_match in GraphMatchSequenceResult(
            self._src_graph, self._start_node, self._match_elems):
            if len(next_match) > 1:     # Don't recurse on zero repeats match
                more_matches = GraphMatchRepeatResult(
                    self._src_graph, next_match[-1], self._match_elems
                    )
                for more_match in more_matches:
                    yield next_match + more_match[1:]
        return

#   ===================================================================
#
#   GraphMapper class
#
#   ===================================================================

class GraphMapper(object):
    """
    This class provides methods to match patterns in a source graph and add statements
    to a result graph.  The Pattern matching uses a form of path expression, and acts
    as a generator yielding a number of "matches".  In internal structiure of a match 
    is considered private, and methods are provided to extract @@@
    """

    def __init__(self, src_graph, tgt_graph):
        """
        Initialize a graph mapper object with specified source and target graphs.
        """
        self._src_graph = src_graph
        self._tgt_graph = tgt_graph
        return

    def match(self, start_node, pattern_list):
        """
        Initiate a pattern match starting at a specified node.
        """
        pattern = GraphMatchPattern(pattern_list)
        result  = pattern.match(self._src_graph, start_node)
        return result

    @classmethod
    def filter(cls, pattern_list, node_match):
        """
        Constructs and returns a GraphMatchPattern object that fails unless the 
        specified pattern list can be matched yielding a leaf node that satisfies
        the node_match value.

        node_match may be any one of:

        URIRef or str
            satisfied by a node labelled with the indicated URI.

        Literal
            satisfied by a node that is the indicated literal.
        """
        return GraphMatchPattern.filter(pattern_list, node_match)

    @classmethod
    def repeat(cls, pattern_list):
        """
        Constructs and returns a GraphMatchPattern object that successively matches 
        zero or more instances of the indicated pattern.
        """        
        return GraphMatchPattern.repeat(pattern_list)

    def emit(self, s, p, o):
        """
        Adds a triple to the target graph

        s, p and o may be RDFLib node values, or 
        URI strings that are treated as URIRef nodes.
        """
        log.debug("GraphMapper.emit: %r %r %r"%(s, p, o))
        self._tgt_graph.add((s, p, o))
        return


#   ===================================================================
#
#   Test patterns
#
#   ===================================================================

EX = Namespace("http://example.org/test/")

test_data = (
    """
    @prefix ex: <http://example.org/test/> .

    ex:base
        ex:prop  ex:val1, ex:val2 ;
        ex:prop1 
            [ ex:prop2 ex:val1211, ex:val1212 ],
            [ ex:prop2 ex:val1221, ex:val1222 ],
            [ ex:prop2 ex:val1231, ex:val1232 ] ;
        ex:prop1
            [ ex:prop4 ex:val141, ex:val142 ],
            [ ex:prop6 ex:val161 ] ;
        .

    ex:val1222 ex:prop3 ex:val2 .
    ex:val1232 ex:prop3 ex:val3 .

    ex:val141 
        ex:prop5 [ ex:prop6  ex:val162 ] .

    ex:val142 
        ex:prop5 
            [ ex:prop4 [ ex:prop5  [ ex:prop6 ex:val163 ] ] ]
        .

    """)

test_patterns_leaves = (
    [ ( [ EX.prop ]
      , [ EX.val1, EX.val2 ]
      )
    , ( [ EX.prop1, EX.prop2 ]
      , [ EX.val1211, EX.val1212, EX.val1221, EX.val1222, EX.val1231, EX.val1232 ]
      )
    , ( [ EX.prop1, EX.prop2, GraphMapper.filter([EX.prop3],  EX.val3) ]
      , [ EX.val1232 ]
      )
    , ( [ EX.prop1, GraphMapper.repeat([EX.prop4, EX.prop5]), EX.prop6 ]
      , [ EX.val161, EX.val162, EX.val163 ] 
      )
    ])

def test_mapper():
    src_graph = Graph()
    tgt_graph = Graph()
    src_graph.parse(data=test_data, format="turtle")
    m = GraphMapper(src_graph, tgt_graph)
    for pattern, expect_leaves in test_patterns_leaves:
        log.debug("test pattern %r, expect %r"%(pattern, expect_leaves))
        leaves = set(m.match(EX.base, pattern).leaves())
        log.debug("actual %r"%(leaves,))
        if leaves != set(expect_leaves):
            print("test pattern %r"%(pattern,))
            print("expect %r"%(expect_leaves,))
            print("actual %r"%(leaves,))
            assert leaves == set(expect_leaves)
        print("Match OK: %r"%(pattern,))
    return

#   ===================================================================
#
#   ....
#
#   ===================================================================


if __name__ == "__main__":
    test_mapper()
