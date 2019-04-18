python get_geonames_data.py get 3090048 >a1.tmp --debug
diff -s a1.tmp data-test/a1.ttl
  
python get_geonames_data.py placehierarchy 3090048 >a2.tmp
diff -s a2.tmp data-test/a2.txt
  
python get_geonames_data.py placehierarchy 3090048 |
  python get_geonames_data.py manyget >a3.tmp
# diff -s a3.tmp data-test/a3.ttl
# Ordering of output is not consistent
  
cat Opole_nearby_places.txt |
  python get_geonames_data.py manyplacehierarchy >a4.tmp
diff -s a4.tmp data-test/a4.txt

