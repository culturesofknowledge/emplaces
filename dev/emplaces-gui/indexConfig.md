See for more information: https://github.com/HuygensING/timbuctoo/blob/master/documentation/create_an_index_config.adoc
EMPlaces index
```json
{
  "dataSetId": "ue85b462c027ef2b282bf87b44e9670ebb085715d__emdates_places",
  "collectionUri": "http://id.emplaces.info/vocab/Place",
  "indexConfig": {
    "facet": [
      {
        "paths": ["[[\"em_Place\",\"em_placeType\"],[\"skos_Concept\",\"title\"],[\"Value\",\"value\"]]"],
        "type": "MultiSelect",
        "caption": "Place type"
      },
      {
        "caption": "Calendars",
        "paths": ["[[\"em_Place\",\"em_hasAnnotationList\"],[\"items\",\"items\"],[\"oa_Annotation\",\"oa_hasBody\"],[\"em_Calendar\",\"title\"],[\"Value\",\"value\"]]"],
        "type": "MultiSelect"
      },
      {
        "caption": "Authorities",
        "paths": ["[[\"em_Place\",\"em_alternateAuthorityList\"],[\"items\",\"items\"],[\"em_Authority\",\"title\"],[\"Value\",\"value\"]]"],
        "type": "MultiSelect"
      }
    ],
    "fullText": {
      "caption": "Fulltext",
      "fields": [
        {
          "path": "[[\"em_Place\", \"em_preferredName\"], [\"Value\", \"value\"]]"
        },
        {
          "path": "[[\"em_Place\", \"em_alternateNameList\"],[\"items\", \"items\"],[\"Value\", \"value\"]]"
        }
      ]
    }
  }
}
```
