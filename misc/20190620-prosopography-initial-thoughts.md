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

The central question I see is:  which of two possible models should we adopt/recommend for recording contextual information about: (a) the role of an actor in some activity or event, and (b) relationships between people.  And, should we adopt the same approach for both?

To recap, the two models are:

- reificaton of relations (ala SNAP), or
- specilization of entities (ala CRM BIO)

I shall focus initially on the modeling of roles in activities.  I'll use a simple example of musical performance to explore each of the modeling approaches.  

On the 1970 Beatles album, Paul McCartney plays both bass guitar and piano, among other instruments.  Specifically, on the song "Across the Universe", he plays piano, and on "Get Back" he plays bass guitar.  How can we capture these distinct roles in two different performances?  We can't simply attach the information to a representation of Paul McCartney the person, as that would fail to capture his role in the different performances.

As a starting point, we have Paul McCartney participating in two performances, which we could represent in CIDOC CRM using Turtle syntax thus:

    :PaulMcCartney a crm:E21_Person, :Pianist, :BassGuitarist ;
        crm:P131_is_identified_by [ a crm:E82_Actor_Appellation; rdfs:label "Paul McCartney" ] ;
        .

    :AcrossTheUniversePerformance a crm:E7_Activity ;
        crm:P11_had_participant :PaulMcCartney ;
        .

    :GetBackPerformance a crm:E7_Activity ;
        crm:P11_had_participant :PaulMcCartney ;
        .

Although we've recorded that `:PaulMcCartney` is both a `:Pianist` and `:BassGuitarist`, we can't tell from this which of these capabilities he employes in the individual performances.  And, using RDF, there's not a direct way to attach this information to the individual `crm:P11_had_participant` relations.


## Reify the relationship

Following (loosely) a [proposal in the CIDOC CRM community](http://www.ics.forth.gr/isl/CRMext/Roles.pdf), one approach would be to use a new entity to represent the performance, and attach the role information to that new node.  This process of representing the relation as a new node to which we can attach further information is called "reificaton".  Add the following to the initial example:

    :AcrossTheUniversePaulMcCartneyParticipation a crm:PC11_had_participant ;
        crm:P01_has_domain :AcrossTheUniversePerformance ;
        crm:P02_has_range  :PaulMcCartney ;
        crm:P11.1_in_the_role_of :Pianist ;
        .

    :GetBackPerformancePaulMcCartneyParticipation a crm:PC11_had_participant ;
        crm:P01_has_domain :GetBackPerformance ;
        crm:P02_has_range  :PaulMcCartney ;
        crm:P11.1_in_the_role_of :BassGuitarist ;
        .

The class `crm:PC11_had_participant` is used to represent (abstract) entities that reify the relation `crm:P11_had_participant` (the "PC" in the name might be read as "property class").

NOTE: the value of the `crm:P11.1_in_the_role_of` used here is a somewhat arbitrary choice, and does impose some additional constraints.  The original CRM proposal uses a `crm:E55_type` value here, but I felt that using the original type makes the connection clearer.  It does imply that the value of the `crm:P11.1_in_the_role_of` property must be a subclass of the range type of the property that is reified (in this case: `crm:P11_had_participant`, whose range is `crm:E39_Actor`).  This may be incompatible with the CRM proposal upon which it is based if that is eventually adopted into the CRM standard.  @@REVIEW THIS, NOT SURE IF IT'S COHERENT@@

NOTE: this pattern could in principle be applied to any of the properties that relate an activity to a person, or indeed to any property.  One would expect that values of `crm:P01_has_domain` correspond to instances of the domain type of the reified property, and similarly for values of `crm:P01_has_range` being instances of its range type.


## Specialize the person

Use a specialized instance of the person tha corresponds to them performing a particular role.  A notion of specialization is introduced in the [W3C PROV-O specification](https://www.w3.org/TR/prov-o/#specializationOf), and also in CRM-BIO.  For the purposes of this example, I'll follow the CRM-BIO examples as they are more closely aligned with CIDOC CRM.  Add the following to the initial example:

    :PaulMcCartneyAsPianist a crm:E21_Person, :Pianist ;
        bioc:inheres_in :PaulMcCartney ;
        .

    :PaulMcCartneyAsBassGuitarist a crm:E21_Person, :BassGuitarist ;
        bioc:inheres_in :PaulMcCartney ;
        .

Now we can say:

    :AcrossTheUniversePerformance a crm:E7_Activity ;
        crm:P11_had_participant :PaulMcCartneyAsPianist ;
        .

    :GetBackPerformance a crm:E7_Activity ;
        crm:P11_had_participant :PaulMcCartneyAsBassGuitarist ;
        .

## Discussion

Putting the pieces together, wer have the following alternative representations:

1. Using reified relation:

        :PaulMcCartney a crm:E21_Person, :Pianist, :BassGuitarist ;
            crm:P131_is_identified_by 
                [ a crm:E82_Actor_Appellation; rdfs:label "Paul McCartney" ] ;
            .

        :AcrossTheUniversePerformance a crm:E7_Activity ;
            crm:P11_had_participant :PaulMcCartney ;
            .

        :GetBackPerformance a crm:E7_Activity ;
            crm:P11_had_participant :PaulMcCartney ;
            .

        :AcrossTheUniversePaulMcCartneyParticipation a crm:PC11_had_participant ;
            crm:P01_has_domain :AcrossTheUniversePerformance ;
            crm:P02_has_range  :PaulMcCartney ;
            crm:P11.1_in_the_role_of :Pianist ;
            .

        :GetBackPerformancePaulMcCartneyParticipation a crm:PC11_had_participant ;
            crm:P01_has_domain :GetBackPerformance ;
            crm:P02_has_range  :PaulMcCartney ;
            crm:P11.1_in_the_role_of :BassGuitarist ;
            .

2. Using specialized person:

        :PaulMcCartney a crm:E21_Person, :Pianist, :BassGuitarist ;
            crm:P131_is_identified_by [ a crm:E82_Actor_Appellation; rdfs:label "Paul McCartney" ] ;
            .

        :PaulMcCartneyAsPianist a crm:E21_Person, :Pianist ;
            bioc:inheres_in :PaulMcCartney ;
            .

        :PaulMcCartneyAsBassGuitarist a crm:E21_Person, :BassGuitarist ;
            bioc:inheres_in :PaulMcCartney ;
            .

        :AcrossTheUniversePerformance a crm:E7_Activity ;
            crm:P11_had_participant :PaulMcCartney ;
            crm:P11_had_participant :PaulMcCartneyAsPianist ;
            .

        :GetBackPerformance a crm:E7_Activity ;
            crm:P11_had_participant :PaulMcCartney ;
            crm:P11_had_participant :PaulMcCartneyAsBassGuitarist ;
            .

In both cases, I've retained the original (unqualified) participation information, so that it remains accessible to applications that don't understand the extension vocabularies used.

In terms of complexity of representation, there's not much to choose between them: they use the same number lof RDF triples.

I feel the use of the original types (`:Pianist`, `:BassGuitarist`) sits more comfortably with the second approach (specialized person), but this is very much a value judgement.

The second approach (specialized person) requires only one new vocabulary term that is not present in the original (`bioc:inheres_in`).

Both approaches require the creation of two new instance nodes to represent the additional information.  For (1) it is the reified relation nodes, which must be generated for each act of participation.  For (2), it is the specialized person nodes, which might be re-used over  participation in mutiple activities - which suggests an advantage for this approach.

Possibly set across the previous advantages in favour of (2) are:  the reification pattern is one that seems to be more widely understood and used, and I suspect it might be slightly easier to add additional contextual information to any act of particpation because each such act is reified separately.  (E.g. adding the track times during which musician played a partocular instrument:  this could be done using the person specialization, but would require creation of a different specialization for each act of participation.)

I feel the choice is finely balanced.  I lean toward the person specialization:

- it introduces fewer new vocabulary terms (and might simply use the existing `prov:specializationOf` term).
- it provides greater opportunity for sharing role information between activities.
- new role information can be introducedincrementally through new specializations and participation.
- it feels in some sense "closer" to the original CRM structures that it aims to refine; e.g. it uses the same `crm:P11_had_participant` property.

But none of these are overwhelming, or even unarguable reasons.


## Application to relationships

Next, I consider how the above patterns apply to relationships.  I note that SNAP uses an approach following the "reified relation" pattern, which clearly works there.

CRM-BIO explores using the "specialized person" approach for relations; this is a Turtle representationfor one of the diagrams in [one of the CRM-BIO papers](https://seco.cs.aalto.fi/publications/2018/tuominen-et-al-bio-crm-2018.pdf):

    :john_kennedy a bioc:Person ;
        bioc:has_family_relation
          [ a :Spouse ;
            bioc:inheres_in :jaqueline_kennedy_onassis ] ;
        .

This seems rather unsatisfactory to me:

1. Why is only one membership of a (nominally symmetric) partnership specialized.
2. Where would we add information about, e.g., the duration of the marriage?
    - it might be attached to the "Spouse" node, but as that node is a specialization of one of the partner it is not logically obvious that is applicable to both of the partners.  Suppose the relation was "has_friend_relation"?

I think my root objection here is that it introduces an asymmetric structure, attached to just one of the related people, to represent what is inherently a relationship that applies equally to both of them.  This suggests to me that there could be a different representation of the same information that is centred on the other partner.

There's a further example of John F Kennedy as President of US that models the relationship as an activity in which there are multiple particpants.  This looks fine to me, but would be covered by the previous discussion.

So, I'm not seeing a convincing case that the person-specialization approach is working well for relationships between people and/or organizations, except to the extent that they are modeled as an activity.

(See also what https://linked.art/model/profile/class_analysis.html has to say about "relationship".)


### Relationships in CIDOC CRM

If a prosopographical ontology is to be based on CIDOC CRM (as is the Swiss Art Research Peson Reference Model), then what are the options provided by CIDOC CRM?

Looking through the CIDOC CRM core documenation, there are no properties that correspond directly to relationships between people.  Where a relationship is expressed, it by way of some event (e.g. [crm:P97_from_father](http://www.cidoc-crm.org/sites/default/files/Documents/cidoc_crm_version_5.0.4.html#_Toc310250884)).

However, in separate discussions (e.g., [here](http://www.cidoc-crm.org/Issue/ID-256-groups-and-relations-between-persons), it is noted that the "CRM way" to describe relationships is via [crm:E74_Group](http://www.cidoc-crm.org/sites/default/files/Documents/cidoc_crm_version_5.0.4.html#_Toc310250783), together witj a membership property [P107 has current or former member](http://www.cidoc-crm.org/sites/default/files/Documents/cidoc_crm_version_5.0.4.html#P107).  But subsequent discussion exposes that there are relationships that don't fit neatly into this idea of a group.  Work is under way to define a CRM extension class that an capture a wider range of relationships, such as those that appear in prosopographical data.

Also: "The question of social relations that are explored in the question of prosopography were argued to go beyond the scope of CRMBase." - [here](http://www.cidoc-crm.org/Issue/ID-256-groups-and-relations-between-persons) (towards end of page).

I would observe that a group might be conceived as a reification of a relationship, though the CRM structures don't distingush directly between the different roles (this is handled by role assignments on the membership property, which cannot be directly encoded in RDF).  This notion sits well with SNAP, which defines a fair number of relationships.

Using (for now) the `crm:E74_Group` class to reify a group, and `crm:P107_has_current_or_former_member` to describe membershp, it seems to me that the person-specialization model of CRM-BIO could also be used to capture role information.

Thus, returning to the previous example of John Kennedy from CRM-BIO, we might get:

    :john_kennedy_marriage_jaqueline_kennedy_onassis a crm:E74_Group, :Marriage ;
        crm:P107_has_current_or_former_member :john_Kennedy_as_husband ;
        crm:P107_has_current_or_former_member :jaqueline_kennedy_onassis_as_wife ;
        .

    :john_kennedy_as_husband a crm:E21_Person, :Spouse, :Husband ;
        bioc:inheres_in :john_kennedy ;
        .

    :jaqueline_kennedy_onassis_as_wife a crm:E21_Person, :Spouse, :Wife ;
        bioc:inheres_in :jaqueline_kennedy_onassis ;
        .

This introduces a Group entity to represent the union, and specializations of the participants to represent their roles.

Compared with the SNAP approach, which effectively reifies a relationship property applied between two people, this approach can generalize to any number of members in a relationship.  Or even a role like President that is filled by just one person at a time.


# Tentative proposal for ongoing work

@@@@review reviews

Nothing much there at the level of modeling.  But there are criticisms of the presentation of the model.  I think we should separate the modelmused for exchange/interoperability from the model used for presentation (i.e. streamline the latter for user convenience - I'm noticing something similar in my work with Annalist).


@@@@

(((swissartresearch, minus CRM extensions)))

(((CRM BIO role modeling)))

(((Something based on SNAP for relationship types)))

(((Something based on FPO for separating recorded assertions from interpretations/claims?  Or map to CRM documentation/assignment terms?)))

@@@@

