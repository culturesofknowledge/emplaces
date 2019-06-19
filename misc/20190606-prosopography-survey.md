# Prosopography vocabulary survey

See also: https://docs.google.com/document/d/16a08sPWYb3qPEjAeD4CMn0Vpn3bH7c93_jbRCFtB9og/edit#heading=h.j58v4tqldiy7

NOTE: this should probably be moved to a different GitHub repo.  I'm parking it here foir now.


# Oxford Cultures of Knowledge prosopography model proposal

(No public instance, analysis based on privately provided spreadsheet)

(Could we put the spreadsheet and notes in GitHub?)

@@TODO: look at reviews too

## People

- id
- name (last, first, etc)
- aliases, other info (labels wrong?)
- birth year
- death year

## Life events

- category
- type
- @@rather like EM Places place typography?
- @@spreadsheet has lots of event types listed and organized
- @@See also Roles, Glossary tabs

## Activity

- label (id?), category, event type
- name/description

Primary participant:
- (EMLO Id, name)
- role in event

Secondary participant:
-  (as primary)
@@NOTE: I think CRM has some material in this area, but role-in-event representation is not well handled)

Time:

Date 1:
- date
- uncertainty

Date 2:
- (as date 1)
@@ what purpose 2 dates?

Location:

- id
- description
- ??
- uncertainty

Source:
- @@use EM Places structure?

Tech provenance and editorial notes

## Places:

- @@assume we’ll have EM Places ref?

## Sources:

- @@encode this data into EM Places source model?

## Roles:

- @@seems to be repeat of data from life events tab
- @@See also Glossary

## Glossary:

- descriptions of roles



# SNAP

http://snapdrgn.net/ontology

NOTE: based on Roman prosopography work

Sample query to SNAP SPARQL endpoint (using [ASQC](https://github.com/gklyne/asqc):

    asq 'select * where {?s <http://xmlns.com/foaf/0.1/name> ?n} limit 100' \
      -e https://snap.dighum.kcl.ac.uk/sparql/ -f csv

(query tested 2019-05-17)

Ontology Imports:

- http://lawd.info/ontology/
- http://purl.org/saws/ontology
- http://www.w3.org/ns/oa#
- http://www.w3.org/ns/prov#
- http://xmlns.com/foaf/0.1/

Also seems to have some occasional CIDOC CRM references.

@@NOTE: Interesting structure: seems to use lots of classes to represent relationships, with relatively few properties.  So, effectively, a reified relationship structure?  Compare with our places work, uses OWL classes rather than SKOS concepts.

See ontology visualizations:

- http://snap.dighum.kcl.ac.uk/img/SNAPOntoGraf.png or
- http://snap.dighum.kcl.ac.uk/img/OwlVizImage.png

(I find the latter easier to read.)


## Classes:

- QuAC (equiv. “agent”) - seems to stand for a person
- Link 

@@Why so many synonyms for “Agent”?  Is one recommended?
@@Considered using SKOS categories instead of OWL classes?  (depends on required use: IR or inference?)

## Properties:

- disambiguatingFeature (associatedDate, associatedPlace, occupation)
- has-link (has-bond) - associates person with relation
- link-with (bond-with) - 
- certainty (no range specified)
- 

    QuAC —has-link—> Link —link-with—> QuAC
                                        ^
                                      Bond

@@What’s the difference between Link and Bond?  According to http://snap.dighum.kcl.ac.uk/img/SNAPOntoGraf.png, all sub relations are subclasses of Bond.

@@Lots of sub-relations: KinOf (etc), IntimateRelationshipWith (married or mistress?), Household (slaves, etc?), Qualified relationship (like extended family but not direct kin?), friends, enemies,

@@confused by apparent overlap between KinOf and QualifiedRelationship

@@Need to find more relationship instance documentation


# SwissArtResearch: Person Reference Data Model

https://docs.swissartresearch.net/et/person/

My initial impression is thgat this is a carefully thought out and comprehensive reference model for describing people, based primnarily on CIDOC CRM, with some selected extensions (including to handle the infamous "rtole-in-activity" problem when usiong CIDOC CRM with RDF).

My concern is that this may prove too complex for some applications to deal with directly.  But I think it could form a useful basis for mapping appliucation-specific person ontologies.

Aniother cobncern is that the "Qualified properties" problem doesn't seem to be fully worked out for family relations (cf. [Qualified properties](https://github.com/gklyne/notes/blob/master/20180307-qualified-property-links.md)).


## Names and classifications

Base class: [crm:E21_Person](http://www.cidoc-crm.org/Entity/e21-person/version-6.2)

See: 

- https://workspace.digitale-diathek.net/confluence/rest/gliffy/1.0/embeddedDiagrams/acf58953-c7f4-4356-80ed-ed4f7ddf97e4.png

Properties:

- Identifier: [P1 is identified by](http://www.cidoc-crm.org/node/4423) -> [E42 Identifier](http://www.cidoc-crm.org/entity/e42-identifier/version-6.2)
    - Identifier type: P2 has type -> E55 Type
    - Identifier provider
    - Identifier source
- Person name: P1 -> E41 -> P2 -> E55 ["full namne"]
    - Name language
    - Honorific
- Alternate name
    - Alternate name type
    - Alternate name earliest use
    - ALternate name latest use
- Gender: P2 -> E55 [gender id URI]


## Existence

- Birth: P98i was born -> E67 Birth (event)  ->
    - Place: P7 took place at - E53 Place
    - earliest date: P4 - E52 - P82a
    - latest date: P4 - E52 - P82b
    - @@ This seems a bit odd to me:  is described as earliest and latest *known* date, but surely range implies date not *known*?
    - See also: 
        - http://www.cidoc-crm.org/Issue/ID-417-beginofthebegin-endoftheend-is-excluded-from-time-range
        - http://new.cidoc-crm.org/guidelines-for-using-p82a-p82b-p81a-p81b
        - P82 is described as "P82 at some time within", which implies uncertainty
    - I note this structure aligns (semantically) with the proposed structure in EM Places
- Death: P100i died in -> E69 Death (event) ->
    - Place: P7 took place at - E53 Place
    - earliest date: P4 - E52 - P82a
    - latest date: P4 - E52 - P82b


## Social relations

- Father
- Mother
- Relative: SRP3 in family relation -> E21
- Relation type
    - SRP3_in_family_relation -> SRP3.1_had_family_relation_type -> E55 Family Relation Type
    - @@doesn't play well with RDF
    - @@Could use SNAP terms here?
- National affiliation
- Cultural afiliation
- Institutional afiliation
- Associate: P11i Participated in - E5 Event - P11i - E21 (@@Eh?)

SRP3_in_family_relation and SRP3.1_had_family_relation_type are CRM extensions.


## Knowledge

- Used language:  SRP1 used language -> E56 Language

SRP2 used language is a CRM extension.

This section is quite sketchy, but may be of particular future interest to CofK work? (e.g,. to capture topics like academic specialties or competencies?).


## Activities

- Floruit
    - "This field is used to indicate the period of greatest activity/flourishing of the documented individual."
    - @@ I guess is is particularly significant for art research?
- Occupation / general role
    - not linked to specific periods
- Related works
    - "This field is used to indicate related works that the documented person was primarily responsible for as creator."
    - @@why "related"?
- Field of activity
    E21 -> P14i Performed -> [F51 Pursuit](http://www.cidoc-crm.org/f51-pursuit) -> R59 had typical subject  -> E55
    - "This field is used to indicate different activities which the documented person pursued during their lifetime. Each individual field of activity should be documented separately so that it can be tracked individually."
    - Uses FRBRoo
    - F51 Pursuit is subclass of activity
    - Time period information can be associated with F51 pursuit (being a CRM event)
- Well known events: E21 -> P11i -> E5


# Factoid ontology (FPO)

(John Bradley, KCL)

see:
- https://factoid-dighum.kcl.ac.uk/
- http://factoid-dighum.kcl.ac.uk/fpo-factoid-prosopography-ontology/
- https://factoid-dighum.kcl.ac.uk/fpo-factoid-prosopography-ontology/fpo-overall-concepts/ (useful overview diagram)
    -- @@ I'm puzzled that :Institution appears to be a subclass of :Person - maybe that's just the terminology used?
- https://github.com/johnBradley501/FPO

Generally, the ontology appears to be quite general, and applicable to fields beyond prosopography.  The prosopographical aspects seem to be concentrated in a number of "reference" types that specifically refer to people (or agents).

The factoid model for prosoporaphy attempts to focus of claims made in sources, rather than (of itself) appealing to some higher notion of truth about people and their activities and relationships.  (e.g. similar to the way that PeriodO deals with time periods?)

Key ideas in the ontology seem to be:

- person/actor
- place/location
- sources (e.g., documents, etc.)
- assertions (factoids)
- references (a reification of a referring relation)
- date ranges

It appears (and is ackowldged) that the factoid ontology could be represented using CRM terms used to describe documentation, but this would require further investigation to verify.


# CIDOC-CRM BIO, etc

See:
- https://seco.cs.aalto.fi/publications/2018/tuominen-et-al-bio-crm-2018.pdf

"Bio CRM extends CIDOC CRM by introducing role-centric modeling."

The paper suggests the formal description is at http://ldf.fi/schema/bioc/, but I could not retrieve that URL (as of 2019-06-19).  "The namespace of the Bio CRM schema is [http://ldf.fi/schema/bioc/](http://ldf.fi/schema/bioc/), here used with the prefix `bioc`. The full specification of Bio CRM (class and property listing) is available in the namespace URI."

`bioc:bearer_of` seems to overlap with `crm:P2_has_type`.

There's also some overlap here wit the SNAP approach to handling roles/relations.

The class `bioc:Actore_role` appears to represent a "specialization" of a person in a particlar role, rather than reify the reklationship - this is implied by the use of `cidoc:P11_had_participant`, whose range is an actor, not some other thing.  See also `prov:specializationOf`.  It's not stated explcitly, but I think `bioc:Actore_role` is a subclass of `bioc:Actor`.

@@CHECK: Suggested use of `owl:AllValuesFrom` looks suspect to me.  Subsequent text implies this would be applied to an appropriate subclass of `bioc:Event`, which I think is fine.  But the sparql query in section 3 suggests the intended meaning of `bioc:Actor_role` is as a reification of a role relation, which I think is incompatible with the use of `cidoc:P11_had_participant`.


# Schema.org

