# Thoughts about interoperability for prosopographical data

These discussion notes have been prepared as part of an activity with 2 related goals:

1. proposals for a linked data format to be used by the EM People activity, which aims to present  data about People collected by the Cultures of Knowledge (CofK) Early Modern Letters Online (EMLO) project as separate linked data resource.
2. an action accepted at a Prosopography workshop in London held in May 2019 to compare and attempt to crosswalk various ontologies used by prosopographical research projects.

See also [Prosopography vocabulary survey](./20190606-prosopography-survey.md).


## Where to start?

The major ontologies that appear to have significant traction in the prosopography DH community are:

- CIDOC CRM
- SNAP (Standards for Networking Ancient Prosopographies)
- FPO (Factoid Prosopography Ontology)

It turns out there is less overlap between these than I first anticipated, so the idea of preparing a crosswalk between them is probably not so helpful.  I expand on this below.

There is also related work:

- Swiss Art Research Person Reference Data Model (based on CIDOC CRM)
- CRM-BIO (also based on CRM, focused on relationship and role modelling)
- W3C PROV: a W3C standard ontology for recording "provenance": structured information about the processes, actors and entities ivolved in the production of some entity.

I also looked at schema.org, but feel it doesn't really address the kinds of representational issues that are of concern to prosopographical researchers (that's not to say it's not relevant, but that its approach doesn't lend itself to being a basis model for exchange).


### CIDOC CRM

See: http://www.cidoc-crm.org/use_and_learn

This is a well-developed ISO-standard ontology that has widespread adoption in the cultural heritage community, and beyond, for many years.  Its roots are in museum catalog data, with highly developed capabilities in the area of describing historical artifacts and assessments of their provenance.  It provides a well-organized and rich (but not overwhelming) vocabulary for describing artifacts, entities, people, locations, activities and events.

A key feature of CRM (which it shares with W3C PROV) is that it is event- (or activity-) centric.  The provenance of an artifact is described in terms of the events/activites that led to its production and subsequent states.  The other entities, people, places, and more that provide related information are for the most part connected by these event descriptions.

This model is capable of describing a wide range of information, but there are some topics that are not captured so well.  Notably the details of relationships between people and events (e.g. role), particularly for CRM represented as linked data on the web using RDF.  This limitation is highlighted by the extensions to CRM that are introduced by the Swiss Art Research Person Reference Model, and the CRM-BIO work.  But these projects take quite different approaches to how they capture this information (more on this later).


### SNAP (Standards for Networking Ancient Prosopographies)

See: http://snapdrgn.net/ontology

The SNAP ontology focuses on relationships between people.

In particular, it defines and organizes a number of classes to represent different kinds relationship between people.  As such, it might be described as "relationship-centric".

The primary structure adopted by SNAP is a hierarchy of classes that reify relationships between people.  The top-level classes and relations are:

- `QuAC`
    - seems to be the class used to represent people
    - defined equivalent to `lawd:Agent`, `dcterms:Agent` and `foaf:Agent`
- `Link` - reifies a relkation between people (`QuAC`s)
    - `Quac` --`has-link`--> `Link` --`link-with`--> `Quac`
    - presumably, additional contextual information (e.g. duration?) can be applied to the link.
- `Bond` - a subclass of `Link`
    - `Quac` --`has-bond`--> `Bond` --`bond-with`--> `Quac`

There are a whole hierachy of subclasses of `Bond` that appear to denote different types of family and non-family relationships between people.

The ontology itself is mostly free-standing, in that it does not extend some other ontology, though it does make reference to a number of other ontologies (e.g. LAWD, PROV, FOAF, etc.).  As far as I can tell, these references are mainly for ontology alignment purposes, and are not central to SNAP.


### FPO (Factoid Prosopography Ontology)

See: https://factoid-dighum.kcl.ac.uk/

Rather than attempting to model domain information about people directly, FPO focuses on assertions about people that are found in primary sources (or other literature?).

The central structral idea is a `Factoid`, which is an assertion that appears in some source expression (a `frbroo:F2_Expression`), and may make reference to a person (`crm:E39_Actor`), a place (`crm:E53_Place`) and a date of occurrence.  There are a number of subclasses of `Factoid` for representing different kinds of assertion about a person.

There apears to be some overlap between FPO and some of the CIDOC CRM vocabulary that is used to describe documentation of artifacts.  It is conceivable that FPO could be cast in terms of these CIDOV CRM terms.

FPO also reifies the references from `Factoid` to people and places, using a structure that might be extended to include references to other kinds of thing (e.g. CRM events?).  This refied structure, which might be used to associate additional information about the reference, might captured directly in CRM using referencing events.  This will need investigation, and might result in a more complex data model.

FPO also defines subclasses of CIDOC CRM people and places (e.g., female, male, group) which might also be extended.


### Swiss Art Research Person Reference Data Model

See: https://docs.swissartresearch.net/et/person/

This is a "profile" of CIDOC CRM for describing people, using some extension terms to capture roles in activities.  It appears to be quite comprehensive and well thought through, using CIDOC CRM terms wherever possible.

One known area of weaknes of CIDOC CRM is in the representation of a person's role in an activity, particularly when the desired representation is RDF linked data on the Web.  The problem is that CRM uses a direct property (`crm:P12_occurred_in_the_presence_of`, `crm:P11_had_participant` and subproperties) to relate people to an event, a use of which cannot be further qualified using RDF.

For relationship modeling, the Swiss Art Research profile uses a CRM extension (`SRP3_in_family_relation` and `SRP3.1_had_family_relation_type`), but the data pattern described isn't making any sense to me.  I am not seeing any structures for describing role-in-activity.

Apart from the issue of modelling relationships and roles in activities, this work looks like a good starting point for representing exchangeable Prosopographical data.  I return to this topic later.


### CRM BIO

See: https://seco.cs.aalto.fi/publications/2018/tuominen-et-al-bio-crm-2018.pdf

This work describes a CRM extension that explicitly attempts to tackle the person relationship and role-in-activity challenges in using CRM with RDF that have been noted.

Most proposals I have seen for addressing this problem involve introducing a new class to represent a relationship between entities, to which additional qualifying information about the relation can be attached.  For example, the W3C PROV ontology uses this pattern in a form known as [Qualified terms](https://www.w3.org/TR/prov-o/#description-qualified-terms).  This pattern can be described as "reifying a relationship".

(It may be worth noting that "property graph" implementations generally do not have this limitation, and allow qualifying information to be added to any relationship between entities.  There are experiments under way to address this issue generically in RDF.)

CRM BIO, however, takes a philosophically quite different approach (though the effect in practice is quite similar).  Rather than reifying the relationshiop between (say) an activity and a person, it takes the approach of defining a "specialization" of the person
that quite specifically denotes them as a participant in the event.  This pattern can be described as "specializing an entity".   The W3C PROV ontology defines a general term [prov:specializationOf](https://www.w3.org/TR/prov-o/#specializationOf) that can be used for this.  This approach allows all existing properties of an ontology to be used with unchanged semantics; it is the entities to which they refer that are changed to reflect the context of an activity or a relationship.


### W3C PROV

See: https://www.w3.org/TR/prov-o/

The W3C PROV ontology is used sporadically in existing prosopography ontology work.  There is a good deal of overlap between PROV and the CRM event model.  But PROV also defines patterns for refiying relations between activities and agents, and for defining specialized (of contextualized) instances of a perspon (or any entity).

Given the degree of overlap with CRM, and the extent of existing prosopographical work that already uses CRM, I don't propose to explore PROV further in this context.  I also note that its descriptopn as a "provenance" ontology may be jarring for some in the academic historical and cultural heritage communities, since it only partially aligns with other uses of that term.


# Dealing with relationships and roles

@@@@

The central question:

- reificaton of relations (ala SNAP)

OR

- specilization of entities (ala CRM BIO)

@@@@


# Tentative proposal for ongoing work

@@@@

(((swissartresearch, minus CRM extensions)))

(((CRM BIO role modeling)))

(((Something based on SNAP for relationship types)))

(((Something based on FPO for separating recorded assertions from interpretations/claims?  Or map to CRM documentation/assignment terms?)))

@@@@

