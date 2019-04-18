# Wikidata access notes

- https://www.wikidata.org/wiki/Wikidata:SPARQL_query_service

- https://query.wikidata.org/#SELECT%20%3Fs%20%3FsLabel%20WHERE%20%7B%0A%20%20%3Fs%20wikibase%3ApropertyType%20wikibase%3AExternalId.%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22%5BAUTO_LANGUAGE%5D%2Cen%22.%20%7D%0A%7D%0ALIMIT%201000%0A

- Query for wikidata properties for authority control of places (HT @Tagishsimon)
    SELECT ?property ?propertyLabel WHERE {
      ?property wdt:P31 wd:Q19829908.
      SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
    }

- https://query.wikidata.org/embed.html#SELECT%20%3Fproperty%20%3FpropertyLabel%20WHERE%20%7B%0A%20%20%3Fproperty%20wdt%3AP31%20wd%3AQ19829908.%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22%5BAUTO_LANGUAGE%5D%2Cen%22.%20%7D%0A%7D%0A



