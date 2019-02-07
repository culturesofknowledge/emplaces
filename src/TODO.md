# Data extraction utility tasks

See also `src/annalistdataexport/TODO.md`

## Outstanding at 2019-01-29
 
From 2018-11-08 meeting (20181108-CofK-Arno-meeting-notes):

- [ ] Review Annalist definitions with Arno
    - this was intended to be a face-to-face session, but was previously stymied by an Annalist login bug.  This has been fixed.
    - See: https://demo.annalist.net/annalist/c/EMPlaces_defs/
- [ ] Push ahead on Wikidata cross-referencing for alternate authorities
    - see: 
        - models/wikidata-opole.ttl
        - https://demo.annalist.net/annalist/c/EMPlaces_defs/d/Authority/Wikidata_Opole_source/
        - Have some basic logic working; see:
            - python get_geonames_data.py wikidataid 3090048
            - python get_annalist_data.py getwikidata Q92212
        - Needs refactoring, and an enumeration of external id properties to be pulled from wikidata.

From 2018-11-23 meeting (20181123-EMPlaces-meeting-Oxford)

- [ ] Arno send "related places" details;  ??
    - I think this was to be a small number of examples and associated details, but my notes don't say.
- [ ] GK to prototype one or two "related places" cases

Other:

- [ ] Update `src/commondataexport/README.md` (documentation)
- [ ] Test wrangled data with Timbuctoo

