# This is a sample script for generating GeoNames IDs from
# data exported from EMLO.
#
# The starting point is file `20181008-geonames-urls-from-EMLO.txt`, which is
# a list of all GeoNames URLs extracted from EMLO. (This file was created by 
# hand from an EMLO spreadsheet dump, using simple row selection and export by 
# copy-and-paste to a text file.)
#
# NOTE: sed (on MacOS) fails silently if the first line number is zero.

DATE=$(date "+%Y%m%d")
FROM="0001"
TO="0002"
SELECT="$FROM-$TO"
DATADIR=data-$DATE
DATADIR=data-test
DATADIR=data-test-alternate-authorities

# Write GeoNames IDs to new file

mkdir $DATADIR
echo "Extracting data for EMLO place references $FROM-$TO from geonames" > $DATADIR/geonames-ids-from-EMLO.log
echo "Data extraction starts: $(date)" >> $DATADIR/geonames-ids-from-EMLO.log

python get_geonames_data.py manygeonamesids \
    <20181008-geonames-urls-from-EMLO.txt \
    >$DATADIR/geonames-ids-from-EMLO.txt

echo "Created $DATADIR/geonames-ids-from-EMLO.txt: $(date)"
echo "Created $DATADIR/geonames-ids-from-EMLO.txt: $(date)" >> $DATADIR/geonames-ids-from-EMLO.log

# Extract selected range of ids:

sed -n "${FROM},${TO}p" $DATADIR/geonames-ids-from-EMLO.txt \
    >$DATADIR/geonames-ids-from-EMLO-${SELECT}.txt

echo "Created $DATADIR/geonames-ids-from-EMLO-${SELECT}.txt: $(date)"
echo "Created $DATADIR/geonames-ids-from-EMLO-${SELECT}.txt: $(date)" >> $DATADIR/geonames-ids-from-EMLO.log

# Find all admin hierarchy ids in GeoNames

python get_geonames_data.py manyplacehierarchy \
    <$DATADIR/geonames-ids-from-EMLO-${SELECT}.txt \
    >$DATADIR/geonames-ids-from-EMLO-with-hierarchy-${SELECT}.txt

echo "Created $DATADIR/geonames-ids-from-EMLO-with-hierarchy-${SELECT}.txt: $(date)"
echo "Created $DATADIR/geonames-ids-from-EMLO-with-hierarchy-${SELECT}.txt: $(date)" >> $DATADIR/geonames-ids-from-EMLO.log

# Retrieve GeoNames data and reformat for EMPlaces

python get_geonames_data.py manygetgeo \
    --include-common-defs --include-emplaces-defs \
    --include-geonames-defs --include-language-defs \
    <$DATADIR/geonames-ids-from-EMLO-with-hierarchy-${SELECT}.txt \
    >$DATADIR/geonames-data-ref-by-EMLO-${SELECT}.ttl

echo "Created $DATADIR/geonames-data-ref-by-EMLO-${SELECT}.ttl: $(date)"
echo "Created $DATADIR/geonames-data-ref-by-EMLO-${SELECT}.ttl: $(date)" >> $DATADIR/geonames-ids-from-EMLO.log

# Retrieve Wikidata ids, data, wikipedia text summary, and reformat for EMPlaces

python get_geonames_data.py manywikidataids \
    <$DATADIR/geonames-ids-from-EMLO-with-hierarchy-${SELECT}.txt \
    >$DATADIR/wikidata-ids-from-EMLO-with-hierarchy-${SELECT}.txt

echo "Created $DATADIR/wikidata-ids-from-EMLO-with-hierarchy-${SELECT}.txt: $(date)"
echo "Created $DATADIR/wikidata-ids-from-EMLO-with-hierarchy-${SELECT}.txt: $(date)" >> $DATADIR/geonames-ids-from-EMLO.log

python get_geonames_data.py manygetwikidata  \
    <$DATADIR/wikidata-ids-from-EMLO-with-hierarchy-${SELECT}.txt \
    >$DATADIR/wikidata-ref-by-EMLO-${SELECT}.ttl

echo "Created $DATADIR/wikidata-ref-by-EMLO-${SELECT}.ttl: $(date)"
echo "Created $DATADIR/wikidata-ref-by-EMLO-${SELECT}.ttl: $(date)" >> $DATADIR/geonames-ids-from-EMLO.log

python get_geonames_data.py manygetwikitext \
    <$DATADIR/wikidata-ids-from-EMLO-with-hierarchy-${SELECT}.txt \
    >$DATADIR/wikitext-ref-by-EMLO-${SELECT}.ttl

echo "Created $DATADIR/wikitext-ref-by-EMLO-${SELECT}.ttl: $(date)"
echo "Created $DATADIR/wikitext-ref-by-EMLO-${SELECT}.ttl: $(date)" >> $DATADIR/geonames-ids-from-EMLO.log

# ----

echo "Data extraction ends: $(date)" >> $DATADIR/geonames-ids-from-EMLO.log

# End
