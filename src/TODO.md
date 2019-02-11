# Data extraction utility tasks

See also `src/annalistdataexport/TODO.md`

## Outstanding at 2019-01-29
 
From 2018-11-08 meeting (20181108-CofK-Arno-meeting-notes):

- [ ] Review Annalist definitions with Arno
    - this was intended to be a face-to-face session, but was previously stymied by an Annalist login bug.  This has been fixed.
    - See: https://demo.annalist.net/annalist/c/EMPlaces_defs/
- [ ] Push ahead on Wikidata cross-referencing for alternate authorities
    - [x] find wikidata Id for given Geonames Id
    - [x] Logic to extract selected place data from wikidata
    - [ ] Finalize data to be extracted from Wikidata
    - see: 
        - models/wikidata-opole.ttl
        - https://demo.annalist.net/annalist/c/EMPlaces_defs/d/Authority/Wikidata_Opole_source/
        - Have some basic logic working; see:
            - python get_geonames_data.py wikidataid 3090048
            - python get_annalist_data.py getwikidata Q92212
        - Needs refactoring, and an enumeration of external id properties to be pulled from wikidata.
- [ ] Create capability to import EMPLaces data into Annalist, based on existing data (e.g., a new option for "get_annalist_data").

From 2018-11-23 meeting (20181123-EMPlaces-meeting-Oxford)

- [ ] Arno send "related places" details;  ??
    - I think this was to be a small number of examples and associated details, but my notes don't say.
- [ ] GK to prototype one or two "related places" cases

Other:

- [ ] Update `src/commondataexport/README.md` (documentation)
- [ ] Test wrangled data with Timbuctoo
- [ ] Create capability to import EMPLaces data into Annalist, based on existing data (e.g., a new option for "get_annalist_data").
- [ ] Define minimal viable information model for historical place definitions (with no GeoNames data to seed)
- [ ] Test suite for data wrangling utilities


See also:

- https://www.wikidata.org/wiki/Wikidata:SPARQL_query_service

- https://query.wikidata.org/#SELECT%20%3Fs%20%3FsLabel%20WHERE%20%7B%0A%20%20%3Fs%20wikibase%3ApropertyType%20wikibase%3AExternalId.%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22%5BAUTO_LANGUAGE%5D%2Cen%22.%20%7D%0A%7D%0ALIMIT%201000%0A

- Query for wikidata properties for authority control of places (HT @Tagishsimon)
    SELECT ?property ?propertyLabel WHERE {
      ?property wdt:P31 wd:Q19829908.
      SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
    }

- https://query.wikidata.org/embed.html#SELECT%20%3Fproperty%20%3FpropertyLabel%20WHERE%20%7B%0A%20%20%3Fproperty%20wdt%3AP31%20wd%3AQ19829908.%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22%5BAUTO_LANGUAGE%5D%2Cen%22.%20%7D%0A%7D%0A



WiP example...


    (gcdenv) spare-94:src graham$ python geonamesdataexport/get_geonames_data.py wikidataid 3090048
    Q92212
    (gcdenv) spare-94:src graham$ python annalistdataexport/get_annalist_data.py getwikidata Q92212
    wikidata_uri: http://www.wikidata.org/entity/Q92212
    wikidata_url: https://www.wikidata.org/wiki/Special:EntityData/Q92212.ttl
    @prefix cc: <http://creativecommons.org/ns#> .
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix geo: <http://www.opengis.net/ont/geosparql#> .
    @prefix ontolex: <http://www.w3.org/ns/lemon/ontolex#> .
    @prefix owl: <http://www.w3.org/2002/07/owl#> .
    @prefix p: <http://www.wikidata.org/prop/> .
    @prefix pq: <http://www.wikidata.org/prop/qualifier/> .
    @prefix pqn: <http://www.wikidata.org/prop/qualifier/value-normalized/> .
    @prefix pqv: <http://www.wikidata.org/prop/qualifier/value/> .
    @prefix pr: <http://www.wikidata.org/prop/reference/> .
    @prefix prn: <http://www.wikidata.org/prop/reference/value-normalized/> .
    @prefix prov: <http://www.w3.org/ns/prov#> .
    @prefix prv: <http://www.wikidata.org/prop/reference/value/> .
    @prefix ps: <http://www.wikidata.org/prop/statement/> .
    @prefix psn: <http://www.wikidata.org/prop/statement/value-normalized/> .
    @prefix psv: <http://www.wikidata.org/prop/statement/value/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix schema: <http://schema.org/> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
    @prefix wd: <http://www.wikidata.org/entity/> .
    @prefix wdata: <https://www.wikidata.org/wiki/Special:EntityData/> .
    @prefix wdno: <http://www.wikidata.org/prop/novalue/> .
    @prefix wdref: <http://www.wikidata.org/reference/> .
    @prefix wds: <http://www.wikidata.org/entity/statement/> .
    @prefix wdt: <http://www.wikidata.org/prop/direct/> .
    @prefix wdtn: <http://www.wikidata.org/prop/direct-normalized/> .
    @prefix wdv: <http://www.wikidata.org/value/> .
    @prefix wikibase: <http://wikiba.se/ontology#> .
    @prefix xml: <http://www.w3.org/XML/1998/namespace> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    wd:Q92212 rdfs:label "Opole"@af,
            "أوبولي"@ar,
            "Opole"@ast,
            "Ополе"@ba,
            "Аполе"@be,
            "Аполе"@be-tarask,
            "Ополе"@bg,
            "ওপলে"@bn,
            "Opole"@br,
            "Opole"@bs,
            "Opole"@ca,
            "Opole (kapital sa gingsakopan)"@ceb,
            "Opolí"@cs,
            "Òpòle"@csb,
            "Opole"@cy,
            "Opole"@da,
            "Oppeln"@de,
            "Opole"@dsb,
            "Όπολε"@el,
            "Opole"@en,
            "Opole"@en-ca,
            "Opole"@en-gb,
            "Opole"@eo,
            "Opole"@es,
            "Opole"@et,
            "Opole"@eu,
            "اوپوله"@fa,
            "Opole"@fi,
            "Opole"@fr,
            "Oppeln"@gsw,
            "ઓપોલે"@gu,
            "Opole"@gv,
            "O-pô-lòi"@hak,
            "אופולה"@he,
            "ओपोले"@hi,
            "Opole"@hr,
            "Opole"@hsb,
            "Opole"@hu,
            "Օպոլե"@hy,
            "Opole"@id,
            "Opole"@is,
            "Opole"@it,
            "オポーレ"@ja,
            "Opole"@jv,
            "ოპოლე"@ka,
            "ಓಪೋಲ್"@kn,
            "오폴레"@ko,
            "Oppeln"@ksh,
            "Opole"@li,
            "Opole"@lmo,
            "Opolė"@lt,
            "Opole"@lv,
            "Ополе"@mk,
            "ऑपॉली"@mr,
            "Opole"@ms,
            "Opole"@na,
            "Opole"@nan,
            "Opole"@nb,
            "Oppeln"@nds,
            "Oppeln"@nds-NL,
            "ओपोल"@ne,
            "Opole"@nl,
            "Opole"@nn,
            "Opole"@oc,
            "Opole"@pl,
            "اوپول"@pnb,
            "Opole"@pt,
            "Opole"@pt-br,
            "Opole"@qu,
            "Opole"@ro,
            "Ополе"@ru,
            "Opole"@sco,
            "ඕපෝල්"@si,
            "Opole"@sk,
            "Opole"@sl,
            "Opole"@sq,
            "Ополе"@sr,
            "Opole"@sv,
            "Uopole"@szl,
            "ஆபோலி"@ta,
            "ఒపోల్"@te,
            "Opole"@tet,
            "ออปอแล"@th,
            "Opole"@tr,
            "Ополе"@tt,
            "Ополе"@udm,
            "Ополе"@uk,
            "اوپولے"@ur,
            "Opole"@vep,
            "Opole"@vi,
            "Opole"@war,
            "奧波萊"@yue,
            "奥波莱"@zh,
            "奧波萊"@zh-hant ;
        wdt:P1566 "3090048" .

