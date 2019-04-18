@@@@TODO: edit for use with Annlist data exporter@@@@

@@@@ e.g, 
@@@@ python get_annalist_data.py getsourced Place_sourced/Opole_P_CofK

# This is a sample script for generating ...

DATE=$(date "+%Y%m%d")
SELECT=25
DATADIR=data-$DATE

# Write GeoNames URLs to new file

mkdir $DATADIR
echo "Extracting place data from Annalist" > $DATADIR/geonames-ids-from-EMLO.log
echo "Data extraction starts: $(date)" >> $DATADIR/geonames-ids-from-EMLO.log

python get_geonames_data.py manygeo \
    <20181008-geonames-urls-from-EMLO.txt \
    >$DATADIR/geonames-ids-from-EMLO.txt

# For testing: select first N (=10) ids:
head -n ${SELECT} $DATADIR/geonames-ids-from-EMLO.txt \
    >$DATADIR/geonames-ids-from-EMLO-${SELECT}.txt

# # Find all admin hierarchy ids in GeoNames
# python get_geonames_data.py manyplacehierarchy \
#     <$DATADIR/geonames-ids-from-EMLO-${SELECT}.txt \
#     >$DATADIR/geonames-ids-from-EMLO-with-hierarchy-${SELECT}.txt

# # Retrieve GeoNames data and reformat for EMPlaces
# python get_geonames_data.py manyget \
#     --include-common-defs --include-emplaces-defs \
#     --include-geonames-defs --include-language-defs \
#     <$DATADIR/geonames-ids-from-EMLO-with-hierarchy-${SELECT}.txt \
#     >$DATADIR/geonames-date-ref-by-EMLO-${SELECT}.ttl

# End
