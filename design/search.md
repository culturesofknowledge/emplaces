# Overview (Search)

TBA

## Concepts and Principles

TBA

### Basic Search

**Priority:** High 

**Source:** Core data, additional data

This will be a free keyword, place centric search (i.e. all results will be places, whether current or historical). A key design challenge will be offering a workflow capable of accommodating searching and browsing.

#### Discussion

Unlike, for example, in an OPAC setting, a gazetteer’s search results should not terminate with the list of matched items to a search term. For example, the search term “Oxford” will yield places with this string from a pre-defined set of fields in the gazetteer (preferred name, alternative names, name attestations etc.). But we also want to encourage the exploration (i.e. browsing) of places _related_ to a search result (typically, further places such as buildings ‘contained within’ the larger unit). 

For this, we will need some way to transition between display contexts: from a ranked (and optionally keyword filtered and/or ranked) list of results, to a (potentially hierarchical) linked list of further results. Roughly speaking, we can go about this one one of either two approaches: 1) all results, including 'contained within' results are shown in one list, and we provide some mechanism (filters, facets) to surface the deeper levels. Pros: Easy to implement. Cons: If you search for e.g. 'Germany' you are going to get many, many related places. 2) Show only the results matching against the preferred name of a place, and don't show its related results at all until you go to its detail view. Pros: Initial list is much shorter. Cons: You just push the problem to the detail view, which is less suited to cope with potentially hundreds of results. 

The [Getty TGN][5] follows a variant of approach #2. Here are the results of an initial keyword search for ["Opole"][1]. By clicking on the hierarchy icon you can select an item on the initial list of results for drilling down further (i.e. to see all known places ‘contained within’ it). Here, for example, for [Siena][2].

However, this doesn't include other types of associations with the place. These are shown in [a place record’s detail view][3]. Additional, e.g. historical administrative hierarchies and other type of place relations are not included in the search results for places and so must surfaced by inspection of individual place records.

The German genealogical [GOV gazetteer][6] addresses this differently by following a variant of approach #1. Here are the results of an initial keyword search for ["Opole""][4]. The search results are structured similarly to Getty (GOV also includes a very useful keyword filter widget to help pick out feature types). 

GOV doesn't offer a transition level analogous to the TGN's hierarchy-only view. After selecting a single place record from the initial list of results ([the town of Opole][4]), GOV divides the detail view listing into higher and lower nodes in the place hierarchy (what it calls superordinate and subordinate objects). _Superordinate_ objects can be of multiple types. Their hierarchies, in turn, are represented both in a graph and in traversable tree, with multiple, branching historical hierarchies. _Subordinate objects_ (e.g. buildings) are represented in a flat list (though with a feature type, and the option of including a date range).

The way search results are initially represented in the Getty TGN is more compact than GOV and puts the flattened, comma separated administrative hierarchy right underneath the primary name. It does not list alternative names, and does not allow one to sort or filter by feature type (e.g. inhabited place, building etc.) or other criteria. GOV does allow this, and also shows alternative names, but doesn't make it easy to compare a series of places in sequence by their administrative hierarchy. 

#### Recommendation

By and large, GOV (following approach #1) offers the better solution. If we provide a comprehensive, and intelligently ranked listing of all matching places (i.e. also including places from the appropriate sub-hierarchies) with an improved tabular layout, a keyword filter and facets, then we can avoid the cons associated with option #1. Crucially, a user can learn to avoid a long list of result but entering more specific search terms. It is not a solution that has to be engineered. 

We can also learn from GOV at the detail view. A simpler version of GOV's Subordinate Places listing in the detail view (i.e. very similar to the Name Attestation listing) could serve as a flexible means to show not just places 'contained within' but (in the future) potentially other relation types. This section could be called 'Related Places' (in distinction to the already planned 'Related Resources'). For more details, see the current [draft design notes][7].

### Facets

TBD. 

A potential concern are dates. If a facet limits results to a certain date or date range, to what will this apply? For current places accompanied by current hierarchies, perhaps not at all. But in the case of historical hierarchies a date can mean i) the temporal extent of the entity, ii) the temporal extent of the relationship between two entities, iii) the temporal extent of a a particular historical hierarchy, iv) different kinds of historical hierarchies (admin, ecclesiastical, judicial and/or military). A date can also apply to a Name Attestation, a Calendar, a historical map, and possibly (depending on implementation and data available) to Related Places. Looking further afield (i.e. advanced search), a date can also refer to a bibliographic item.


### Advanced Search (TBD)

**Priority:** Medium 

**Source:** Core data, additional data)

Multi-term search, and with the possibility of returning not just a sorted list of places, but also other types of data collected by the gazetteer, e.g. calendars, related resources, name attestations, places with historical maps etc. Initial ranked results can be sorted, keyword filtered, and facetted.


[1]:	http://www.getty.edu/vow/TGNServlet?english=Y&find=opole&place=&page=1&nation=poland
[2]:	http://www.getty.edu/vow/TGNHierarchy?find=siena&place=&nation=italy&prev_page=1&english=Y&subjectid=7011179
[3]:	http://www.getty.edu/vow/TGNFullDisplay?find=siena&place=&nation=italy&english=Y&subjectid=7011179
[4]:	http://gov.genealogy.net/item/show/OPPELNJO80XQ
[5]:	https://www.getty.edu/research/tools/vocabularies/tgn/
[6]:	http://gov.genealogy.net
[7]:	/design/display.md


