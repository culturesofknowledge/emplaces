@@@@TODO: edit for use with Annlist data exporter@@@@

@@@@ e.g, 
@@@@ python get_annalist_data.py get Place_sourced/Opole_P_CofK

# This is a sample script for generating ...

DATE=$(date "+%Y%m%d")
SELECT=25

# Write GeoNames URLs to new file

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
