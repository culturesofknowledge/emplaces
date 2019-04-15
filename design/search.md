# Overview

## Concepts and Principles

### Basic Search

The first version of EM Places will be limited to a free keyword, place centric search (i.e. all results will be places, whether current or historical). A key design challenge will be offering a workflow capable of accommodating searching and browsing of both matching and related/connected places.

#### Discussion

Unlike, for example, in an OPAC setting, a gazetteer’s search results should not terminate with the list of matched items to a search term. For example, the search term “Oxford” will yield places with this string from a pre-defined set of fields in the gazetteer (preferred name, alternative names, name attestations etc.). But we also want to encourage the exploration (i.e. browsing) of places relatedto a search result (typically, further places ‘contained within’ the larger unit). For example, a town that is part of a province or a building that is part of a town. For this, we will need some way to either integrate or else transition between different display contexts: from a ranked (and optionally keyword filtered) list of results, to a (potentially hierarchical) linked list also including further related results. Other gazetteers address this problem using basically one of two general approaches: 

**Method 1)** all results, including ‘related' results are shown in one long list, and we provide some additional mechanism (filters, facets) to surface the deeper levels. Pros: Easy to implement as this is the default behavior for most search environments. Cons: If you search for e.g. 'Germany' you are going to get many places that are related to it (e.g. all towns in Germany etc.). 

**Method 2)** Show only the results matching against the preferred name of a place, and don't show its related results at all until you go to its detail view. Pros: Initial list is much shorter. Search is easier to use for users who don’t need to browse. Cons: This only displaces the problem, as we now need to show related results somewhere else.

The [Getty TGN gazetteer](https://www.getty.edu/research/tools/vocabularies/tgn/) follows a variant of Method #2. Here are the results of an [initial keyword search](http://www.getty.edu/vow/TGNServlet?english=Y&find=siena&place=&page=1&nation=italy) for Siena in Italy. The search matches all places which match or include ‘Siena’ in the preferred name field. In this case, Siena is both the name of a town and a province (as well as a set of hills, and a second town which includes Siena as part of its name). However, we can’t immediately tell from this list whether the TGN gazetteer knows of other places relatedto, for example, the province called Siena or the town called Siena (for example, towns within the province or buildings contained within the town). If we look at the [detail record view](http://www.getty.edu/vow/TGNFullDisplay?find=siena&place=&nation=italy&english=Y&subjectid=7011179) for the town of Siena, we don’t see this either. Instead, this is discovered by clicking on the traingular hierarchy/network icon next to the place name. This reveals that the TGN also knows about the Ognissanti Monastery and the Piazzao del Campo in the town of Siena. Similarly, to find out what other places are included within the province of Siena, we’d have to click on the hierarchy icon next to its name (revealing over two hundred inhabited places). Other types of places occasionally recorded in the Getty TGN, e.g. historical administrative hierarchies and other type of place relations (e.g. Siena as a historical ‘ally of’ Florence) are also not included in the initial search results and must surfaced manually by inspection of the hierarchy tree and/or individual place record details.

The German genealogical [GOV gazetteer](http://gov.genealogy.net/search/index) addresses the problem by following a variant of Option #1. The search results are structured similarly to Getty (GOV also includes a very useful keyword filter widget to help pick out feature types). But GOV doesn't offer a transition level analogous to the TGN's hierarchy-only view. After selecting a single place record from the initial list of results (e.g. the [town of Opole](http://gov.genealogy.net/item/show/OPPELNJO80XQ) in Poland), GOV divides the detail view listing into higher and lower nodes in the place hierarchy (what it calls superordinate and subordinate objects). Superordinate objects can be of multiple types. Their hierarchies, in turn, are represented both in a graph and in traversable tree, with multiple, branching historical hierarchies. Subordinate objects (e.g. buildings) are represented in a flat list (though with a feature type, and the option of including a date range).

#### Initial Preference

By and large, GOV (following approach #2) offers the better solution. If we provide a comprehensive, and intelligently ranked listing of all matching places (i.e. also including places from the appropriate sub-hierarchies) together with an improved tabular layout, a keyword filter and facets (all present already in Timbuctoo), then we can avoid most of the disadvantages associated with this option. 

### Facets

A potential concern are dates. If a facet limits results to a certain date or date range, to what will this apply? For current places accompanied by current hierarchies, perhaps not at all. But in the case of historical hierarchies a date can mean i) the temporal extent of the entity, ii) the temporal extent of the relationship between two entities, iii) the temporal extent of a a particular historical hierarchy, iv) different kinds of historical hierarchies (admin, ecclesiastical, judicial and/or military). A date can also apply to a Name Attestation, a Calendar, a historical map, and possibly (depending on implementation and data available) to Related/Connected Places. Looking further afield (i.e. advanced search), a date can also refer to a bibliographic item or in fact to any temporally bound object in the database. 

### Advanced Search

Multi-term search, and with the possibility of returning not just a sorted list of places, but also other types of data collected by the gazetteer, e.g. calendars, related resources, name attestations, places with historical maps etc. Initial ranked results can be sorted, keyword filtered, and facetted.


