See for more information: https://github.com/HuygensING/timbuctoo/blob/master/documentation/create_an_index_config.adoc
EMPlaces index
```json
{
  "dataSetId": "ue85b462c027ef2b282bf87b44e9670ebb085715d__emplaces20190710",
  "collectionUri": "http://id.emplaces.info/vocab/Place",
  "indexConfig": {
    "facet": [
      {
        "paths": ["[[\"em_Place\",\"em_placeType\"],[\"skos_Concept\",\"title\"],[\"Value\",\"value\"]]"],
        "type": "MultiSelect",
        "caption": "Place type"
      },
      {
        "caption": "Authorities",
        "paths": ["[[\"em_Place\",\"em_source\"],[\"em_Authority\",\"title\"],[\"Value\",\"value\"]]"],
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
