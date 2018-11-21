@@@@TODO: edit for use with Annlist data exporter@@@@


# This is a sample script for generating GeoNames IDs from
# data exported from EMLO.
#
# The starting point is file `20181008-geonames-urls-from-EMLO.txt`, which is
# a list of all GeoNames URLs extracted from EMLO. (This file was created by 
# hand from an EMLO spreadsheet dump, using simple row selection and export by 
# copy-and-paste to a text file.)

DATE=$(date "+%Y%m%d")
SELECT=25

# Write GeoNames IDs to nmew file

python get_geonames_data.py manygeo \
    <20181008-geonames-urls-from-EMLO.txt \
    >$DATE-geonames-ids-from-EMLO.txt

# For testing: select first N (=10) ids:
head -n ${SELECT} $DATE-geonames-ids-from-EMLO.txt \
    >$DATE-geonames-ids-from-EMLO-${SELECT}.txt

# Find all admin hierarchy ids in GeoNames
python get_geonames_data.py manyplacehierarchy \
    <$DATE-geonames-ids-from-EMLO-${SELECT}.txt \
    >$DATE-geonames-ids-from-EMLO-with-hierarchy-${SELECT}.txt

# Retrieve GeoMNamnes data and reformat for EMPlaces
python get_geonames_data.py manyget \
    --include-common-defs --include-emplaces-defs \
    --include-geonames-defs --include-language-defs \
    <$DATE-geonames-ids-from-EMLO-with-hierarchy-${SELECT}.txt \
    >$DATE-geonames-date-ref-by-EMLO-${SELECT}.ttl

# End
