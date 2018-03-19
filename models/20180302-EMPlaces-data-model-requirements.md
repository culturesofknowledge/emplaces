# EMPlaces (structural) requirements

- Preferred name (label)
- Alternative representations of the preferred name (transliterations, translations)
- Editorial note (Textual description)
- Temporal (duration of place as entity)
- Reference citations (mentions in scholarly sources not covered by. e.g., citations for alternative names) (@@Not for place)
- Gazetteer/authority references
- Uncertain and contested information?
- Related resources

- Types (with temporality) (Getty AAT?)
- Current hierarchy (from reference gazetteer)
- Multiple hierarchies/relations (with temporality)
    - NOTE: use types for read-across in hierarchies
    - => each relation (type) should be associated with a set of types?  (e.g. a "contained within" relation might be associated with place types "town", "country", "country", "region", etc.)
    - This is really an implementation detail to help ensure that hieratchies can be aligned and read across; cf. discussion at workshop.
- Alternative names (with temporality?  Pleiades model includes this)
    - There are two things here: alternative names from the reference gazetteer, which are not temporal, and attestations of other names which may have associatecd temporality, attestation source, etc.)
- Location, with temporality.  (Pleiades model includes this)
- Calendars in use, with temporality.
    - Generalize this to other more specialized descriptions?
    - Use web annotations for framework?
- Multiple map-view URIs with labels for tabs

- Provenance
    - Creator (of the record)
    - Contributors (to the record)
    - (Arno: I don't think Initial Provenance, ala Pleiades works for us. We need a term to reference a provenance for saying that these and these fields came from our reference gazetteer, e.g. GeoNames, and are updated regularly.)
- Attestation - what's this exactly?   "attestations of name variants"   E.g,. claims of alternte name use for a place; cf mockup "attestations of name variants"

I propose the starting point for a conceptual model is the Pleides model with reified "connections".  Initially, I suggest minting new vocabulary terms, with a intent to replace or map these with existing terms later when we have a clearer view of the level of ontological commitments involved.

(Arno: Note: please take a look at the attached PDFs for more context. These are the draft list of features and draft mock-ups from last week in Amsterdam.)


# Existing work

Expect to have a proposal for interworking with these?

- Pleiades
    - use notion of place, and initial conceptual model
- LP-network (Linked pasts network/topotime/CommonPlace)
    - use for timespan representations
- PeriodO
    - use period references (as used by LP-network)
    - (Arno: Not sure about 'not before/not after' model used by PeriodO. We might need to come back to this as a follow-up to Karl's response.)
- Pelagios (interconnection format)
- World Historical Gazetteer (WHG)
- GOV (Geneology.net)
    - use concept of temporally qualified relationships to build hiererchies
- Getty (TGN, AAT)
    - use for place type vocabularies, and other terms
- CIDOC CRM
- LAWD (?)
- CommonPlace
    - Hub/node architecture for sharing with "multivocality"

(Arno: We just need to be compatible with Pelagios Gazetteer Interconnection Format - though this is being reworked now by Karl, and Peripleo API - which is also being reworked, no doubt, because of the former changes)



## Notes on data model

- Note that current hierarchy is intended to be handled by the relation structure (?)  Be clearer about colour coding)
- Ditto "Setting" (also, be clear how to distinguish as coredata may be updated automatically)
- (Note: assuming no alternative structures for "core" data that isn't temporally qualified - we just agreed this (2018-03-19))
- Do separate diagram for just core data??
- Need to add "provenance": distinbguish between creator and subsequent contributions (provided by Timbuctoo core system; not adeed to data model).  But also label for initial original provenance: attach to reference gazetteer entry reesource.
- Initial provenance: source of core data; plus label for display (attach label to reference gazetteer entry resource)
- Copy changes from original image to annotation version

- Annotations: label as type of annotation (e.g. name annotation, map annotation, etc.)
- Annotations: also have editorial note (for maps, attestations, calendars)
- Editorial note for hierarchies (attach to categories)
- Editorial note bibliography resources
- "Link-back" (usage)

- Name attestations: add language of name

- Maintain distinction between bibliographic entry and a web citation - simplest is link+label, but biblio may need to be more comprehensive (e.g. subclassing)

- Bibliography; which bits specific to location, which to larger units?  Distinguish bibliography and source

(In addition to data model diagram, also need a crossswalk explaining how information for UI elements would be accessed.)

- "Editorial notes" -> "Description"

- Calendars - multiple calendars in use in region ?  

- Related resources: link+label

- See search results under "layout tests" in Google drive

- Read-across not for now (or only partial?)

(search: Intermine?)

