DATE=$(date "+%Y%m%d")
FROM="0001"
TO="0002"
SELECT="$FROM-$TO"
DATADIR=data-$DATE
DATADIR=data-test
DATADIR=data-test-alternate-authorities

python get_geonames_data.py manygetwikidata  \
    <$DATADIR/wikidata-ids-from-EMLO-with-hierarchy-${SELECT}.txt \
    >$DATADIR/wikidata-ref-by-EMLO-${SELECT}.ttl

